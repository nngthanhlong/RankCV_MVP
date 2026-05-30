# app/gemini_client.py
import os

from google import genai
from google.genai import types

from app.schemas import MatchRequest, MatchResponse

MODEL = "gemini-3.1-flash-lite"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def build_prompt(req: MatchRequest) -> str:
    return f"""You are a resume-job matching engine. Analyze the CV and job description below and return ONLY valid JSON (no markdown, no code blocks, no extra text).

Return JSON with these fields:
- overall_score: integer 0-100
- skill_match: integer 0-100
- experience_match: integer 0-100
- education_match: integer 0-100
- missing_skills: list of skill names as strings
- strengths: list of strength descriptions as strings
- recommendation: one sentence recommendation as string

CV:
{req.cv_text}

JOB DESCRIPTION:
{req.job_text}

RESPONSE (JSON ONLY):"""


def evaluate_match(req: MatchRequest) -> MatchResponse:
    """Call Gemini and return a validated MatchResponse."""
    response = client.models.generate_content(
        model=MODEL,
        contents=build_prompt(req),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MatchResponse,
        ),
    )
    return MatchResponse.model_validate_json(response.text)
