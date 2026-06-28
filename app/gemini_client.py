# app/gemini_client.py
from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY
from app.rag.retriever import retrieve_fpt_context
from app.schemas import (
    MatchRequest,
    MatchResponse,
    InterviewQuestionsRequest,
    InterviewQuestionsResponse,
)

MODEL = "gemini-2.5-flash-lite"

client = genai.Client(api_key=GEMINI_API_KEY)


def build_prompt(req: MatchRequest) -> str:
    query = f"""
CV:
{req.cv_text}

Job Description:
{req.job_text}

Target Role:
{req.target_role}

Career Goal:
{req.career_goal}
"""

    fpt_context = retrieve_fpt_context(query, top_k=5)

    return f"""
You are an AI CV mentor specialized in FPT recruitment.

Use ONLY the FPT context below.
Do not invent extra FPT information.

FPT CONTEXT:
{fpt_context}

Analyze the candidate CV and job description.
Explain how the candidate fits FPT culture and how they should improve their CV for FPT.

Return ONLY valid JSON.
No markdown.
No code blocks.
No extra text.

Return JSON matching this schema:
{{
  "current_cv_summary": "",
  "fpt_culture_intro": "",
  "fpt_strengths": [],
  "candidate_fpt_fit": {{
    "fit_level": "",
    "matched_culture_points": [],
    "missing_culture_points": [],
    "fit_explanation": ""
  }},
  "cv_improvement_advice": {{
    "strengths_to_highlight": [],
    "weaknesses_to_fix": [],
    "keywords_to_add": [],
    "rewrite_suggestions": []
  }},
  "career_advice": {{
    "readiness_level": "",
    "recommended_next_steps": [],
    "estimated_timeline": ""
  }},
  "mentor_note": ""
}}

Rules:
- Use Vietnamese for all user-facing text.
- fit_level must be one of: "Cao", "Trung bình", "Thấp".
- fpt_culture_intro must be based only on FPT CONTEXT.
- fpt_strengths must be based only on FPT CONTEXT.
- matched_culture_points must connect evidence from the CV with FPT CONTEXT.
- missing_culture_points can be [] if the CV fits well.
- strengths_to_highlight must have at least 1 item.
- weaknesses_to_fix can be [] if the CV is already strong.
- keywords_to_add should come from the JD and FPT CONTEXT only.
- rewrite_suggestions should be practical and specific for CV improvement.
- Do not mention any FPT fact that is not included in FPT CONTEXT.

CV:
{req.cv_text}

JOB DESCRIPTION:
{req.job_text}

TARGET ROLE:
{req.target_role}

CAREER GOAL:
{req.career_goal}

RESPONSE JSON ONLY:
"""


def evaluate_match(req: MatchRequest) -> MatchResponse:
    response = client.models.generate_content(
        model=MODEL,
        contents=build_prompt(req),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MatchResponse,
        ),
    )

    return MatchResponse.model_validate_json(response.text)


def build_interview_prompt(req: InterviewQuestionsRequest) -> str:
    query = f"""
CV:
{req.cv_text}

Job Description:
{req.job_text}
"""

    fpt_context = retrieve_fpt_context(query, top_k=3)

    return f"""
You are a senior technical interviewer at FPT.

Use ONLY the FPT context below for company-related information.
Do not invent extra FPT information.

FPT CONTEXT:
{fpt_context}

Your task is to generate exactly 5 technical interview questions for a candidate based on their CV and the Job Description.

Guidelines:
1. Questions must be strictly technical and based on the intersection of skills found in the candidate's CV and the Job Description.
2. The style should match the retrieved FPT context: practical application, real-world project experience, problem-solving, and willingness to learn.
3. Do NOT hallucinate skills that the candidate does not have or the job does not require.
4. Provide a suggested answer for each question.
5. Return ONLY valid JSON. No markdown. No code blocks. No extra text.

Return JSON matching this schema:
{{
  "questions": [
    {{
      "skill_tag": "",
      "question": "",
      "suggested_answer": ""
    }}
  ]
}}

CV:
{req.cv_text}

JOB DESCRIPTION:
{req.job_text}

RESPONSE JSON ONLY:
"""


def generate_interview_questions(req: InterviewQuestionsRequest) -> InterviewQuestionsResponse:
    response = client.models.generate_content(
        model=MODEL,
        contents=build_interview_prompt(req),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=InterviewQuestionsResponse,
        ),
    )

    return InterviewQuestionsResponse.model_validate_json(response.text)