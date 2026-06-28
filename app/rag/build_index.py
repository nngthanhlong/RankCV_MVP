# app/rag/build_index.py
import json
from pathlib import Path

import chromadb
from google import genai

from app.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

DATA_PATH = Path("app/data/fpt_companies.json")
DB_PATH = "app/chroma_db"
COLLECTION_NAME = "fpt_knowledge"


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


def build_index():
    companies = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    chroma_client = chromadb.PersistentClient(path=DB_PATH)

    try:
        chroma_client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    for company in companies:
        text = company_to_text(company)

        collection.add(
            ids=[company["slug"]],
            documents=[text],
            embeddings=[embed_text(text)],
            metadatas=[{
                "slug": company["slug"],
                "name": company.get("name", ""),
                "group": company.get("group", "")
            }]
        )

    print(f"Indexed {len(companies)} FPT companies into ChromaDB.")


if __name__ == "__main__":
    build_index()