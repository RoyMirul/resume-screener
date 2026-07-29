import os
import glob
import time
import pandas as pd

from parse_resume import extract_text_from_pdf
from scorer import score_resume

RESUME_FOLDER = "resumes"
JOB_DESC_PATH = "resumes/job_description.txt"


def load_job_description(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_resume_files(folder):
    """Find all PDF files in the folder (ignores the .txt job description)."""
    return sorted(glob.glob(os.path.join(folder, "*.pdf")))


def run_pipeline():
    jd = load_job_description(JOB_DESC_PATH)
    resume_files = get_resume_files(RESUME_FOLDER)

    print(f"Found {len(resume_files)} resumes. Scoring against the job description...\n")

    results = []
    for path in resume_files:
        filename = os.path.basename(path)
        print(f"  Scoring: {filename} ...")
        try:
            text = extract_text_from_pdf(path)
            result = score_resume(jd, text)
            result["file"] = filename          # track which file it came from
            results.append(result)
        except Exception as e:
            print(f"    !! Failed on {filename}: {e}")
        time.sleep(12)  # stay under 5 requests/minute (60s / 5 = 12s spacing)

    # Sort by score, highest first
    results.sort(key=lambda r: r["score"], reverse=True)

    # Build a clean summary table
    table = pd.DataFrame([
        {
            "Rank": i + 1,
            "Candidate": r["candidate_name"],
            "Score": r["score"],
            "Fit": r["recommendation"],
            "File": r["file"],
        }
        for i, r in enumerate(results)
    ])

    print("\n" + "=" * 60)
    print("RANKED SHORTLIST")
    print("=" * 60)
    print(table.to_string(index=False))

    return results


if __name__ == "__main__":
    run_pipeline()