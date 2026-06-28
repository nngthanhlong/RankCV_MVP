import hashlib
import json
from datetime import datetime, timezone

from app.gemini_client import evaluate_match
from app.schemas import MatchRequest


def create_content_hash(req: MatchRequest) -> str:
    raw = json.dumps(req.model_dump(), ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def evaluate_cv_match(req: MatchRequest) -> dict:
    content_hash = create_content_hash(req)

    result = evaluate_match(req)

    return {
        "status": "success",
        "source": "ai",
        "content_hash": content_hash,
        "cached_at": None,
        "data": result.model_dump()
    }