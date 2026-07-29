import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.0-flash"  # more generous free daily quota than 3.6-flash

def get_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None

client = genai.Client(api_key=get_api_key())

# ---- The response schema: forces Gemini to return exactly this shape ----
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "candidate_name": {"type": "string"},
        "years_experience": {"type": "number"},
        "matched_skills": {"type": "array", "items": {"type": "string"}},
        "missing_skills": {"type": "array", "items": {"type": "string"}},
        "score": {"type": "integer"},
        "recommendation": {
            "type": "string",
            "enum": ["Strong Fit", "Possible Fit", "Weak Fit"],
        },
        "justification": {"type": "string"},
    },
    "required": [
        "candidate_name", "years_experience", "matched_skills",
        "missing_skills", "score", "recommendation", "justification",
    ],
}

# ---- The prompt: role + rubric + grounding rules ----
def build_prompt(job_description, resume_text, blind=False):
    blind_instruction = ""
    if blind:
        blind_instruction = """
BLIND SCREENING MODE IS ON:
- Ignore the candidate's name, gender, ethnicity, nationality, age, and any personal identifiers.
- Base your evaluation ONLY on skills, experience, projects, and education.
- For "candidate_name", return "Candidate (anonymized)".
"""

    return f"""You are an experienced technical recruiter screening candidates for a job.
{blind_instruction}
Evaluate the CANDIDATE RESUME against the JOB DESCRIPTION using this rubric (total 100 points):
- Skills match: 40 points (how well the candidate's skills align with the required skills)
- Experience relevance: 35 points (relevant experience and appropriate level for the role)
- Evidence quality: 20 points (are claims backed by real projects/jobs, not just keywords?)
- Education/other: 5 points

GROUNDING RULES (must follow):
- Base your evaluation ONLY on information explicitly present in the resume text.
- Do NOT invent, assume, or infer skills, experience, or qualifications that are not clearly stated.
- If a required skill is only listed as a keyword with no supporting evidence (no project, job, or context), treat it with low confidence and reflect that in the score.
- If the resume lacks information for a criterion, score that criterion low rather than guessing generously.
- Keep the justification factual and concise (2-3 sentences). Do not add praise or speculation.
- You must ALWAYS return a complete evaluation in the required format. Never refuse or ask questions. If information is missing, reflect that in a lower score.

Recommendation guide: score >= 70 -> "Strong Fit"; 45-69 -> "Possible Fit"; below 45 -> "Weak Fit".

--- JOB DESCRIPTION ---
{job_description}

--- CANDIDATE RESUME ---
{resume_text}
"""


def score_resume(job_description, resume_text, blind=False, max_retries=3):
    prompt = build_prompt(job_description, resume_text, blind=blind)

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0,
                    response_mime_type="application/json",
                    response_schema=RESPONSE_SCHEMA,
                ),
            )
            return json.loads(response.text)

        except Exception as e:
            err = str(e)
            is_rate_limit = "429" in err or "RESOURCE_EXHAUSTED" in err
            is_network = "10053" in err or "aborted" in err or "connection" in err.lower()
            if (is_rate_limit or is_network) and attempt < max_retries - 1:
                wait = 15 * (attempt + 1)
                print(f"    Transient error. Waiting {wait}s before retry "
                      f"({attempt + 1}/{max_retries})...")
                time.sleep(wait)
            else:
                raise

    raise RuntimeError("Failed after retries due to rate limiting.")


# ---- Test block: score ONE resume ----
if __name__ == "__main__":
    from parse_resume import extract_text_from_pdf

    # Read the job description
    with open("resumes/job_description.txt", "r", encoding="utf-8") as f:
        jd = f.read()

    # Read one resume
    resume = extract_text_from_pdf("resumes/01_strong_match.pdf")

    # Score it
    result = score_resume(jd, resume)

    # Pretty-print the result
    print(json.dumps(result, indent=2))