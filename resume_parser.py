"""
resume_parser.py
-----------
Handles the extraction of raw text from uploaded PDF resume files.
It ensures that the AI has a clean text version of the user's 
profile to use for matching and analysis.
"""

import pdfplumber

def extract_resume_text(uploaded_file):
    """
    Extract text from uploaded PDF resume.
    """

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"

    return text.strip()
