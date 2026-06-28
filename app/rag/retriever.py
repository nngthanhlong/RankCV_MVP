# app/rag/retriever.py
from pathlib import Path
from typing import List

import chromadb
from google import genai

from app.config import GEMINI_API_KEY

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "fpt_knowledge"

EMBEDDING_MODEL = "gemini-embedding-001"

client = genai.Client(api_key=GEMINI_API_KEY)


def embed_text(text: str):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    if hasattr(result, "embeddings") and result.embeddings:
        emb = result.embeddings[0]
        if hasattr(emb, "values"):
            return emb.values
        if hasattr(emb, "embedding"):
            return emb.embedding

    if hasattr(result, "embedding"):
        emb = result.embedding
        if hasattr(emb, "values"):
            return emb.values
        if hasattr(emb, "embedding"):
            return emb.embedding

    raise ValueError(f"Unsupported embedding response format: {type(result)}")


def retrieve_fpt_context(query: str, top_k: int = 5) -> str:
    chroma_client = chromadb.PersistentClient(path=DB_PATH)

    collection = chroma_client.get_collection(name=COLLECTION_NAME)

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]

    return "\n\n".join(documents)