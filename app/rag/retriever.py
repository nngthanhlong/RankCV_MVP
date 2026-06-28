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


def embed_text(text: str) -> List[float]:
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )
    return result.embeddings[0].values


def retrieve_fpt_context(query: str, top_k: int = 5) -> str:
    if not query or not query.strip():
        raise ValueError("Query is empty. Cannot retrieve FPT context.")

    chroma_client = chromadb.PersistentClient(path=DB_PATH)

    try:
        collection = chroma_client.get_collection(name=COLLECTION_NAME)
    except Exception:
        raise RuntimeError(
            f"Chroma collection '{COLLECTION_NAME}' not found. "
            "Please run: python -m app.rag.build_index"
        )

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not documents:
        return ""

    context_parts = []

    for index, doc in enumerate(documents):
        metadata = metadatas[index] if index < len(metadatas) else {}
        distance = distances[index] if index < len(distances) else None

        company_name = metadata.get("name", "Unknown company")
        company_slug = metadata.get("slug", "unknown")

        context_parts.append(
            f"""[Retrieved FPT Context {index + 1}]
Company: {company_name}
Slug: {company_slug}
Distance: {distance}

{doc}
"""
        )

    return "\n\n".join(context_parts)