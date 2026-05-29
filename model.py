# app.py
import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, conint
from google import genai
from google.genai import types

app = FastAPI(title="CV-JD Match API")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  # or rely on env var

class MatchRequest(BaseModel):
    cv_text: str = Field(..., min_length=50)
    job_text: str = Field(..., min_length=50)

class MatchResponse(BaseModel):
    overall_score: conint(ge=0, le=100)
    skill_match: conint(ge=0, le=100)
    experience_match: conint(ge=0, le=100)
    education_match: conint(ge=0, le=100)
    missing_skills: List[str]
    strengths: List[str]
    recommendation: str

@app.post("/evaluate", response_model=MatchResponse)
def evaluate(req: MatchRequest):
    prompt = f"""
You are a resume-job matching engine.

Compare the CV and the job description.
Return only JSON matching this schema:
- overall_score: 0-100
- skill_match: 0-100
- experience_match: 0-100
- education_match: 0-100
- missing_skills: list of strings
- strengths: list of strings
- recommendation: short sentence

CV:
{req.cv_text}

JOB:
{req.job_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MatchResponse,
            ),
        )

        # The SDK should return JSON text that matches the schema.
        return MatchResponse.model_validate_json(response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))