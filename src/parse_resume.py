from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Reads a PDF file and returns all its text as a single string.
    """
    reader = PdfReader(pdf_path)
    text = ""

    # A PDF is made of pages; we loop through each and grab its text
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:  # some pages might be empty/None
            text += page_text + "\n"

    return text.strip()

def extract_text_from_upload(uploaded_file):
    """
    Reads an uploaded PDF (in-memory file object from Streamlit)
    and returns its text. Reuses the same logic as the path version.
    """
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

import re

def redact_pii(text):
    """
    Basic PII redaction for blind screening.
    Removes email addresses and phone numbers from resume text.
    NOTE: This is a lightweight mitigation, not a complete anonymizer.
    """
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '[EMAIL REDACTED]', text)
    # Remove phone-number-like sequences
    text = re.sub(r'\+?\d[\d\s\-()]{7,}\d', '[PHONE REDACTED]', text)
    return text


# This block only runs when we execute THIS file directly (for testing)
if __name__ == "__main__":
    sample = "resumes/my_resume.pdf"
    result = extract_text_from_pdf(sample)
    print("----- EXTRACTED TEXT -----")
    print(result)
    print("--------------------------")
    print(f"\nTotal characters extracted: {len(result)}")