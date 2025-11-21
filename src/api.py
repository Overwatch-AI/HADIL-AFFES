# src/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import faiss
from rank_bm25 import BM25Okapi

from src.config import FAISS_INDEX_PATH, BM25_INDEX_PATH, CHUNKS_PATH
from src.indexer import load_indexes  # We only need the load function now
from src.retriever import query_boeing_manual

# --- Pydantic Models for Request and Response ---
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    pages: List[int]

# --- FastAPI Application Initialization ---
app = FastAPI(
    title="Boeing 737 Manual RAG API",
    description="An API to ask questions about the Boeing 737 Operations Manual using a Retrieval-Augmented Generation (RAG) system.",
    version="1.0.0",
)

# --- Global Variables for Indexes and Chunks ---
index: faiss.IndexFlatIP = None
bm25: BM25Okapi = None
all_chunks: List[Dict[str, Any]] = None

@app.on_event("startup")
def startup_event():
    """
    On application startup, load the pre-built indexes from the data/ directory.
    The API is designed to run with pre-generated indexes and will not
    attempt to create them if they are missing.
    """
    global index, bm25, all_chunks

    print("Starting up the RAG system...")
    print(f"Attempting to load indexes from: {FAISS_INDEX_PATH}")

    loaded_index, loaded_bm25, loaded_chunks = load_indexes()

    if loaded_index is None or loaded_bm25 is None or loaded_chunks is None:
        # Provide a very clear error message to the user.
        error_message = (
            "FATAL: Could not load indexes. "
            "Please ensure the following files exist in the 'data/' directory:\n"
            f"- {FAISS_INDEX_PATH}\n"
            f"- {BM25_INDEX_PATH}\n"
            f"- {CHUNKS_PATH}\n"
            "If you do not have these files, you must first run the document processing "
            "and indexing script to generate them."
        )
        print(error_message)
        # Raising an exception will prevent the API from starting.
        raise RuntimeError(error_message)

    print("✅ Indexes loaded successfully.")
    index = loaded_index
    bm25 = loaded_bm25
    all_chunks = loaded_chunks

    print("RAG system is ready to accept queries.")


@app.get("/", tags=["General"])
def read_root():
    """A simple root endpoint to check if the API is running."""
    return {"message": "Boeing 737 Manual RAG API is running. Access /docs for the API documentation."}


@app.post("/ask", response_model=AnswerResponse, tags=["Query"])
def ask_question(request: QuestionRequest):
    """
    Accepts a question about the Boeing 737 manual and returns an answer
    along with the page numbers used as references.
    """
    if not all([index, bm25, all_chunks]):
        # This is a fallback check, should be caught by startup_event
        raise HTTPException(status_code=503, detail="RAG system is not initialized. Please check server logs.")

    try:
        response = query_boeing_manual(request.question, index, bm25, all_chunks)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")