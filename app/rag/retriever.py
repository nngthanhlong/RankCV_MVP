# app/rag/retriever.py
import json
import math
import re
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "fpt_companies.json"


def tokenize(text: str) -> set[str]:
    text = text.lower()
    return set(re.findall(r"[a-zA-Z0-9À-ỹ+#.]+", text))


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


def score_text(query: str, document: str) -> float:
    q_tokens = tokenize(query)
    d_tokens = tokenize(document)

    if not q_tokens or not d_tokens:
        return 0.0

    overlap = len(q_tokens & d_tokens)
    return overlap / math.sqrt(len(d_tokens))


def retrieve_fpt_context(query: str, top_k: int = 5) -> str:
    companies = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    scored = []
    for company in companies:
        doc = company_to_text(company)
        scored.append((score_text(query, doc), company, doc))

    scored.sort(key=lambda x: x[0], reverse=True)

    context_parts = []
    for i, (score, company, doc) in enumerate(scored[:top_k]):
        context_parts.append(f"""
[Retrieved FPT Context {i + 1}]
Company: {company.get("name", "Unknown")}
Slug: {company.get("slug", "unknown")}
Score: {score}

{doc}
""")

    return "\n\n".join(context_parts)