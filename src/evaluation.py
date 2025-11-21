import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import FAISS_INDEX_PATH, BM25_INDEX_PATH, CHUNKS_PATH
from src.indexer import load_indexes
from src.retriever import query_boeing_manual

#  Test Questions and Evaluation Code ---

test_questions = [
    ("I'm calculating our takeoff weight for a dry runway. We're at 2,000 feet pressure altitude, and the OAT is 50°C. What's the climb limit weight ?", [83]),
    ("We're doing a Flaps 15 takeoff. Remind me, what is the first flap selection we make during retraction, and at what speed?", [41]),
    
]

def evaluate_rag_system(test_questions, index, bm25, all_chunks, top_k=15, alpha=0.5, use_reranking=True):
    """
    Evaluates the RAG system with a focus on user-centric metrics, all computed @5.
    Note: This version is stateless and requires indexes to be passed in.
    """
    evaluation_results = []
    recall_at_5_list = []
    precision_at_5_list = []
    f1_score_list = []
    mrr_list = []
    map_score_list = []

    print(f"Evaluating {len(test_questions)} questions (retrieving top {top_k} results)...")

    for i, (question, expected_pages) in enumerate(test_questions, 1):
        print(f"\n--- Evaluating Question {i}/{len(test_questions)} ---")

        response = query_boeing_manual(
            question,
            index=index,
            bm25=bm25,
            all_chunks=all_chunks,
            top_k=top_k,
            alpha=alpha,
            use_reranking=use_reranking
        )

        retrieved_pages = response['pages']
        correct_ranks = [rank for rank, page_num in enumerate(retrieved_pages, 1) if page_num in expected_pages]
        num_total_relevant = len(expected_pages)
        num_relevant_in_top_5 = len([p for p in retrieved_pages[:5] if p in expected_pages])

        recall_at_5 = num_relevant_in_top_5 / num_total_relevant if num_total_relevant > 0 else 0
        recall_at_5_list.append(recall_at_5)
        precision_at_5 = num_relevant_in_top_5 / 5
        precision_at_5_list.append(precision_at_5)

        if (precision_at_5 + recall_at_5) > 0:
            f1_score = 2 * (precision_at_5 * recall_at_5) / (precision_at_5 + recall_at_5)
        else:
            f1_score = 0
        f1_score_list.append(f1_score)

        first_correct_rank = correct_ranks[0] if correct_ranks else None
        mrr_list.append(1 / first_correct_rank if first_correct_rank else 0)

        precisions_at_correct_docs = []
        for rank in correct_ranks:
            num_correct_up_to_this_rank = len([r for r in correct_ranks if r <= rank])
            precisions_at_correct_docs.append(num_correct_up_to_this_rank / rank)

        avg_precision = sum(precisions_at_correct_docs) / len(precisions_at_correct_docs) if precisions_at_correct_docs else 0
        map_score_list.append(avg_precision)

        evaluation_results.append({
            "question": question,
            "expected_pages": expected_pages,
            "retrieved_pages": retrieved_pages,
            "correct_ranks": correct_ranks,
            "recall_at_5": recall_at_5,
            "precision_at_5": precision_at_5,
            "f1_score": f1_score,
            "mrr": 1 / first_correct_rank if first_correct_rank else 0,
            "map_score": avg_precision
        })
        print(f"Expected: {expected_pages} | Retrieved Top 5: {retrieved_pages[:5]}")
        print(f"Recall@5: {recall_at_5:.2f} | Precision@5: {precision_at_5:.2f} | F1@5: {f1_score:.2f}")

    num_questions = len(test_questions)
    summary_metrics = {
        "total_questions": num_questions,
        "mean_recall_at_5": sum(recall_at_5_list) / num_questions,
        "mean_precision_at_5": sum(precision_at_5_list) / num_questions,
        "mean_f1_score": sum(f1_score_list) / num_questions,
        "mean_reciprocal_rank": sum(mrr_list) / num_questions,
        "map_score": sum(map_score_list) / num_questions
    }

    f1_weight = 0.4
    mrr_weight = 0.4
    map_weight = 0.2
    final_retrieval_score = (
        f1_weight * summary_metrics['mean_f1_score'] +
        mrr_weight * summary_metrics['mean_reciprocal_rank'] +
        map_weight * summary_metrics['map_score']
    )
    summary_metrics['final_retrieval_score'] = final_retrieval_score
    summary_metrics['score_weights'] = {'f1': f1_weight, 'mrr': mrr_weight, 'map': map_weight}
    return {"detailed_results": evaluation_results, "summary_metrics": summary_metrics}

def print_evaluation_report(evaluation_results):
    """Prints a formatted report with the new user-centric metrics."""
    print("\n" + "="*80)
    print("COMPREHENSIVE EVALUATION REPORT (FOCUSED ON RECALL@5 & PRECISION@5)")
    print("="*80)
    metrics = evaluation_results['summary_metrics']
    weights = metrics['score_weights']
    print(f"Total Questions Evaluated: {metrics['total_questions']}")
    print("\n--- Key User-Centric Performance Metrics ---")
    print(f"Mean Recall@5 (Correct page in top 5):      {metrics['mean_recall_at_5']:.2%}")
    print(f"Mean Precision@5 (Correctness of top 5):    {metrics['mean_precision_at_5']:.2%}")
    print("\n--- Core Performance Metrics ---")
    print(f"Mean F1-Score@5:                             {metrics['mean_f1_score']:.4f}")
    print(f"Mean Reciprocal Rank (MRR):                 {metrics['mean_reciprocal_rank']:.4f}")
    print(f"Mean Average Precision (MAP):               {metrics['map_score']:.4f}")
    print("\n--- Final Composite Retrieval Score ---")
    print(f"Formula: {weights['f1']}*F1 + {weights['mrr']}*MRR + {weights['map']}*MAP")
    print(f"Final Score: {metrics['final_retrieval_score']:.4f}")
    print("\n--- Detailed Question-by-Question Analysis ---")
    for result in evaluation_results['detailed_results']:
        print(f"\nQuestion: {result['question'][:80]}...")
        print(f"  Expected: {result['expected_pages']} | Retrieved Top 5: {result['retrieved_pages'][:5]}")
        print(f"  Recall@5: {result['recall_at_5']:.2f} | Precision@5: {result['precision_at_5']:.2f}")


# --- Main execution block to run the evaluation ---
if __name__ == "__main__":
    print("="*80)
    print("STARTING RAG SYSTEM EVALUATION")
    print("="*80)

    # Load the necessary indexes from disk
    index, bm25, all_chunks = load_indexes()

    if index is None:
        print("FATAL: Could not load indexes. Make sure they exist in the 'data/' directory.")
        sys.exit(1) # Exit with an error code

    print("✅ Indexes loaded successfully. Starting evaluation...")

    # Run the evaluation
    evaluation_results = evaluate_rag_system(
        test_questions,
        index=index,
        bm25=bm25,
        all_chunks=all_chunks,
        top_k=10,
        alpha=0.5,
        use_reranking=True
    )

    # Print the comprehensive report
    print_evaluation_report(evaluation_results)