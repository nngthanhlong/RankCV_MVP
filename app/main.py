# app/main.py
import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.gemini_client import evaluate_match
from app.schemas import MatchRequest

app = FastAPI(title="CV-JD Match API")


@app.post("/evaluate")
def evaluate(req: MatchRequest):
    try:
        validated = evaluate_match(req)
        return JSONResponse(content=json.loads(validated.model_dump_json()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
