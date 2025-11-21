import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from rank_bm25 import BM25Okapi
from typing import List, Dict, Any, Tuple, Optional
from src.config import FAISS_INDEX_PATH, BM25_INDEX_PATH, CHUNKS_PATH

def create_indexes(chunks_to_index: List[Dict[str, Any]]) -> Tuple[faiss.IndexFlatIP, BM25Okapi, List[Dict[str, Any]]]:
    """
    Creates and saves FAISS and BM25 indexes from a list of chunks.

    Args:
        chunks_to_index: A list of chunk dictionaries.

    Returns:
        A tuple containing the FAISS index, BM25 index, and the original chunks.
    """
    if not chunks_to_index:
        raise ValueError("No chunks provided for indexing!")

    print("Creating embeddings...")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    chunk_texts = [chunk["content"] for chunk in chunks_to_index]
    chunk_embeddings = embedding_model.encode(chunk_texts, show_progress_bar=True)

    print("Creating FAISS index...")
    embedding_dim = chunk_embeddings.shape[1]
    index = faiss.IndexFlatIP(embedding_dim)
    faiss.normalize_L2(chunk_embeddings)
    index.add(chunk_embeddings)

    print("Creating BM25 index...")
    tokenized_chunks = [chunk.lower().split() for chunk in chunk_texts]
    bm25 = BM25Okapi(tokenized_chunks)

    print(f" Created FAISS index with {index.ntotal} embeddings")
    print(f"Created BM25 index with {len(tokenized_chunks)} documents")

    print("Saving indexes and chunks to disk...")
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(BM25_INDEX_PATH, "wb") as f:
        pickle.dump(bm25, f)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks_to_index, f)
    print("✅ Saved indexes and chunks")

    return index, bm25, chunks_to_index

def load_indexes() -> Tuple[Optional[faiss.IndexFlatIP], Optional[BM25Okapi], Optional[List[Dict[str, Any]]]]:
    """
    Loads pre-built indexes from disk.

    Returns:
        A tuple containing the FAISS index, BM25 index, and the list of chunks,
        or (None, None, None) if the files are not found.
    """
    try:
        print("Loading existing indexes from disk...")
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(BM25_INDEX_PATH, "rb") as f:
            bm25 = pickle.load(f)
        with open(CHUNKS_PATH, "rb") as f:
            chunks = pickle.load(f)
        print(" Loaded existing indexes")
        return index, bm25, chunks
    except FileNotFoundError:
        print(" No existing indexes found. Will need to create new ones.")
        return None, None, None
    except Exception as e:
        print(f" Error loading indexes: {e}")
        return None, None, None