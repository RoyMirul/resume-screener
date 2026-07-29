# AI Resume Screener

An AI-powered tool that ranks candidate resumes against a job description using
Google's Gemini API. Built as a 3-day prototype challenge.

## What it does
- Upload a job description and up to 10 candidate resumes (PDF)
- Each resume is scored 0–100 against the JD using a defined rubric
  (skills 40 / experience 35 / evidence 20 / education 5)
- Returns a ranked shortlist with matched/missing skills and a justification
- Optional "blind screening" mode to reduce bias by ignoring personal identifiers

## Tech stack
- Python, Streamlit (UI)
- Google Gemini API (`google-genai` SDK) for scoring
- pypdf for PDF text extraction, pandas for ranking

## Run locally
1. Clone the repo and create a virtual environment:
python -m venv venv
source venv/Scripts/activate # Windows Git Bash
pip install -r requirements.txt

2. Add your Gemini API key. Create a `.env` file:
GEMINI_API_KEY=your_key_here

3. Run the app:
python -m streamlit run app.py


## Notes & limitations
- Uses the Gemini free tier, which has per-minute and per-day rate limits.
  Batch size is capped at 10 and requests are spaced 12s apart.
- Text-based (ATS-friendly) PDFs parse best; image/scanned resumes would need OCR.
- Blind screening reduces but does not fully eliminate bias.