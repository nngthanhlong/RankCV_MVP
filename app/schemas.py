# app/schemas.py
from typing import List

from pydantic import BaseModel, Field, conint


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
