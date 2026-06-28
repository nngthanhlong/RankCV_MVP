from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.schemas import MatchRequest
from app.services.matching_service import evaluate_cv_match

router = APIRouter(tags=["matching"])


@router.post("/evaluate")
def evaluate(req: MatchRequest):
    try:
        response = evaluate_cv_match(req)
        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))