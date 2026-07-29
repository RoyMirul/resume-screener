import sys
import os
import time
import pandas as pd
import streamlit as st

# Let app.py import our modules from the src/ folder
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from parse_resume import extract_text_from_upload
from scorer import score_resume

MAX_RESUMES = 10  # our free-tier batch cap

# ---------- Page setup ----------
st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")
st.title("📄 AI Resume Screener")
st.caption("Upload a job description and candidate resumes to get an AI-ranked shortlist.")

# Near the top, after the caption:
blind_mode = st.checkbox(
    "🕶️ Blind screening (ignore names & personal identifiers to reduce bias)",
    value=False,
)

# ---------- Inputs ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Job Description")
    jd_text = st.text_area(
        "Paste the job description here",
        height=250,
        placeholder="Paste the full job description...",
    )

with col2:
    st.subheader("2. Candidate Resumes")
    uploaded_resumes = st.file_uploader(
        f"Upload up to {MAX_RESUMES} resume PDFs",
        type="pdf",
        accept_multiple_files=True,
    )

# ---------- Screen button ----------
if st.button("🚀 Screen Candidates", type="primary"):

    # --- Validation ---
    if not jd_text.strip():
        st.error("Please paste a job description first.")
        st.stop()
    if not uploaded_resumes:
        st.error("Please upload at least one resume.")
        st.stop()
    if len(uploaded_resumes) > MAX_RESUMES:
        st.error(f"Please upload at most {MAX_RESUMES} resumes "
                 f"(free-tier limit). You uploaded {len(uploaded_resumes)}.")
        st.stop()

    # --- Scoring with progress feedback ---
    results = []
    progress = st.progress(0, text="Starting...")

    for i, file in enumerate(uploaded_resumes):
        progress.progress(
            (i) / len(uploaded_resumes),
            text=f"Scoring {file.name} ({i+1}/{len(uploaded_resumes)})...",
        )
        try:
            text = extract_text_from_upload(file)
            if blind_mode:
                from parse_resume import redact_pii   # (or import at top)
                text = redact_pii(text)
            result = score_resume(jd_text, text, blind=blind_mode)
            result["file"] = file.name
            results.append(result)
        except Exception as e:
            st.warning(f"Could not score {file.name}: {e}")

        if i < len(uploaded_resumes) - 1:
            time.sleep(12)  # stay under free-tier rate limit

    progress.progress(1.0, text="Done!")

    if not results:
        st.error("No resumes could be scored. Please try again.")
        st.stop()

    # --- Rank ---
    results.sort(key=lambda r: r["score"], reverse=True)

    # --- Summary table ---
    st.subheader("🏆 Ranked Shortlist")
    table = pd.DataFrame([
        {
            "Rank": i + 1,
            "Candidate": r["candidate_name"],
            "Score": r["score"],
            "Fit": r["recommendation"],
        }
        for i, r in enumerate(results)
    ])
    st.dataframe(table, use_container_width=True, hide_index=True)

    # --- Detailed per-candidate breakdown ---
    st.subheader("🔍 Candidate Details")
    for i, r in enumerate(results):
        with st.expander(f"#{i+1}  {r['candidate_name']}  —  {r['score']}/100  ({r['recommendation']})"):
            st.markdown(f"**Years of experience:** {r['years_experience']}")
            st.markdown(f"**✅ Matched skills:** {', '.join(r['matched_skills']) or '—'}")
            st.markdown(f"**❌ Missing skills:** {', '.join(r['missing_skills']) or '—'}")
            st.markdown(f"**Justification:** {r['justification']}")

            # ---------- Footer ----------
st.markdown("---")  # a horizontal divider line
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.85em; padding: 10px;'>
        Built by <a href='https://github.com/RoyMirul' target='_blank'>Amirul Azham</a>
        · AI Resume Screener · Powered by Google Gemini
    </div>
    """,
    unsafe_allow_html=True,
    
)