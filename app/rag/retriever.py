# app/rag/retriever.py
import json
from pathlib import Path
from typing import List

import chromadb
from google import genai

from app.config import GEMINI_API_KEY

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "fpt_companies.json"
COLLECTION_NAME = "fpt_knowledge"
EMBEDDING_MODEL = "gemini-embedding-001"

client = genai.Client(api_key=GEMINI_API_KEY)

_chroma_client = None
_collection = None


def embed_text(text: str) -> List[float]:
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
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


def company_to_text(company: dict) -> str:
    hiring = company.get("hiring", {})

    return f"""
Company: {company.get("name", "")}
Short name: {company.get("shortName", "")}
Group: {company.get("group", "")}
Tagline: {company.get("tagline", "")}

Business:
{chr(10).join(company.get("business", []))}

Business model:
{company.get("businessModel", "")}

Culture:
{chr(10).join(company.get("culture", []))}

Hiring roles:
{chr(10).join(hiring.get("roles", []))}

Fit for:
{hiring.get("fitFor", "")}

Tech stack:
{", ".join(company.get("techStack", []))}
"""


def get_collection():
    global _chroma_client, _collection

    if _collection is not None:
        return _collection

    _chroma_client = chromadb.EphemeralClient()
    _collection = _chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    companies = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    for company in companies:
        text = company_to_text(company)

        _collection.add(
            ids=[company["slug"]],
            documents=[text],
            embeddings=[embed_text(text)],
            metadatas=[{
                "slug": company["slug"],
                "name": company.get("name", ""),
                "group": company.get("group", "")
            }]
        )

    return _collection


def retrieve_fpt_context(query: str, top_k: int = 5) -> str:
    if not query or not query.strip():
        raise ValueError("Query is empty.")

    collection = get_collection()
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    context_parts = []

    for i, doc in enumerate(documents):
        metadata = metadatas[i] if i < len(metadatas) else {}
        distance = distances[i] if i < len(distances) else None

        context_parts.append(f"""
[Retrieved FPT Context {i + 1}]
Company: {metadata.get("name", "Unknown")}
Slug: {metadata.get("slug", "unknown")}
Distance: {distance}

{doc}
""")

    return "\n\n".join(context_parts)