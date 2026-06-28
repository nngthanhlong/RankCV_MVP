# # app/schemas.py
# from typing import List

# from pydantic import BaseModel, Field, conint


# class MatchRequest(BaseModel):
#     cv_text: str = Field(..., min_length=50)
#     job_text: str = Field(..., min_length=50)


# class MatchResponse(BaseModel):
#     overall_score: conint(ge=0, le=100)
#     skill_match: conint(ge=0, le=100)
#     experience_match: conint(ge=0, le=100)
#     education_match: conint(ge=0, le=100)
#     missing_skills: List[str]
#     strengths: List[str]
#     recommendation: str


# class InterviewQuestionsRequest(BaseModel):
#     cv_text: str = Field(..., min_length=50)
#     job_text: str = Field(..., min_length=50)


# class InterviewQuestion(BaseModel):
#     skill_tag: str
#     question: str
#     suggested_answer: str


# class InterviewQuestionsResponse(BaseModel):
#     questions: List[InterviewQuestion]

# app/schemas.py
from typing import List, Optional, Literal

from pydantic import BaseModel, Field


class MatchRequest(BaseModel):
    cv_text: str = Field(..., min_length=50)
    job_text: str = Field(..., min_length=50)
    target_role: Optional[str] = ""
    career_goal: Optional[str] = ""
    tier: Optional[str] = "basic"


class CandidateFPTFit(BaseModel):
    fit_level: Literal["Cao", "Trung bình", "Thấp"]
    matched_culture_points: List[str]
    missing_culture_points: List[str]
    fit_explanation: str


class CVImprovementAdvice(BaseModel):
    strengths_to_highlight: List[str]
    weaknesses_to_fix: List[str]
    keywords_to_add: List[str]
    rewrite_suggestions: List[str]


class CareerAdvice(BaseModel):
    readiness_level: str
    recommended_next_steps: List[str]
    estimated_timeline: str


class MatchResponse(BaseModel):
    current_cv_summary: str
    fpt_culture_intro: str
    fpt_strengths: List[str]
    candidate_fpt_fit: CandidateFPTFit
    cv_improvement_advice: CVImprovementAdvice
    career_advice: CareerAdvice
    mentor_note: str


class InterviewQuestionsRequest(BaseModel):
    cv_text: str = Field(..., min_length=50)
    job_text: str = Field(..., min_length=50)


class InterviewQuestion(BaseModel):
    skill_tag: str
    question: str
    suggested_answer: str


class InterviewQuestionsResponse(BaseModel):
    questions: List[InterviewQuestion]