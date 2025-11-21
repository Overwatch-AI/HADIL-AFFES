import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#PDF_PATH = os.getenv("PDF_PATH")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH")
BM25_INDEX_PATH = os.getenv("BM25_INDEX_PATH")
CHUNKS_PATH = os.getenv("CHUNKS_PATH")

# Validate that all required environment variables are set
if not all([GEMINI_API_KEY, FAISS_INDEX_PATH, BM25_INDEX_PATH, CHUNKS_PATH]):
    raise ValueError("Missing one or more required environment variables. Please check your .env file.")

