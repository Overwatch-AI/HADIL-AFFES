import numpy as np
import io
from PIL import Image
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from src.generator import generate_answer
import faiss
from rank_bm25 import BM25Okapi

def hybrid_search(query: str, index: faiss.IndexFlatIP, bm25: BM25Okapi, all_chunks: List[Dict[str, Any]], top_k: int = 5, alpha: float = 0.5) -> List[Dict[str, Any]]:
    """Performs a hybrid search combining semantic (FAISS) and keyword (BM25)."""
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')
    distances, indices = index.search(query_embedding, top_k * 3)

    semantic_scores = 1 / (1 + distances[0])
    semantic_scores = semantic_scores / (semantic_scores.max() + 1e-6)

    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)
    bm25_scores = bm25_scores / (bm25_scores.max() + 1e-6)

    combined_scores = {}
    for idx, score in zip(indices[0], semantic_scores):
        combined_scores[idx] = alpha * score
    for idx, score in enumerate(bm25_scores):
        if idx in combined_scores:
            combined_scores[idx] += (1 - alpha) * score
        else:
            combined_scores[idx] = (1 - alpha) * score

    sorted_indices = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    # Group by page to ensure page diversity
    page_groups = {}
    for idx, score in sorted_indices:
        chunk = all_chunks[idx]
        page_num = chunk["page_number"]
        if page_num not in page_groups:
            page_groups[page_num] = {"chunks": [], "max_score": score, "page_num": page_num}
        page_groups[page_num]["chunks"].append({"chunk_idx": idx, "score": score, "chunk": chunk})
        if score > page_groups[page_num]["max_score"]:
            page_groups[page_num]["max_score"] = score

    sorted_pages = sorted(page_groups.values(), key=lambda x: x["max_score"], reverse=True)

    results = []
    for page_group in sorted_pages[:top_k]:
        best_chunk = max(page_group["chunks"], key=lambda x: x["score"])
        chunk = best_chunk["chunk"]
        results.append({
            "content": chunk["content"], "page_number": page_group["page_num"], "type": chunk.get("type", "text"),
            "score": float(best_chunk["score"]), "has_image": chunk.get("page_image") is not None,
            "page_image": chunk.get("page_image"), "metadata": chunk.get("metadata", {})
        })
    return results

def simple_rerank(query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Simple re-ranking based on query type."""
    query_lower = query.lower()
    is_performance_query = any(term in query_lower for term in ["weight", "limit", "altitude", "runway", "performance", "field", "climb"])
    is_procedural_query = any(term in query_lower for term in ["procedure", "step", "checklist", "how to", "perform"])

    for result in results:
        metadata = result.get("metadata", {})
        rerank_score = result["score"]
        if is_performance_query and metadata.get("table_type"):
            rerank_score *= 1.5
        if is_procedural_query and "procedure" in result["content"].lower():
            rerank_score *= 1.3
        result["rerank_score"] = rerank_score

    results.sort(key=lambda x: x["rerank_score"], reverse=True)
    return results

def query_boeing_manual(question: str, index: faiss.IndexFlatIP, bm25: BM25Okapi, all_chunks: List[Dict[str, Any]], top_k: int = 5) -> Dict[str, Any]:
    """
    Complete RAG query pipeline: retrieval, re-ranking, and answer generation.

    Args:
        question: The user's question.
        index: The FAISS index.
        bm25: The BM25 index.
        all_chunks: The list of all document chunks.
        top_k: The number of top results to consider.

    Returns:
        A dictionary containing the answer and a list of source page numbers.
    """
    # Step 1: Initial retrieval
    results = hybrid_search(question, index, bm25, all_chunks, top_k=top_k * 2)

    # Step 2: Re-ranking
    results = simple_rerank(question, results)
    results = results[:top_k]

    # Step 3: Prepare context for generation
    seen_pages = set()
    page_numbers = []
    text_parts = []
    visual_parts = []

    for r in results:
        if r["page_number"] not in seen_pages:
            page_numbers.append(r["page_number"])
            seen_pages.add(r["page_number"])

        if r["type"] == "visual" and r["has_image"]:
            visual_parts.append(r)
        else:
            text_parts.append(f"[Page {r['page_number']}]\n{r['content']}")

    context = "\n\n---\n\n".join(text_parts)

    # Step 4: Generate answer
    answer = generate_answer(question, context, visual_parts)

    return {"answer": answer, "pages": sorted(list(set(page_numbers)))}