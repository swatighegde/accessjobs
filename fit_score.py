"""
fit_score.py
-----------
Perform a high-level comparison between the resume text and a job description. 
It returns a numerical score from 1-10 representing the profile fit.
"""

import re
import pandas as pd

def clean_text(text):
    """
    Safely normalize text input.
    """

    if text is None or pd.isna(text):
        return set()

    if not isinstance(text, str):
        text = str(text)

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    return set(text.split())


def calculate_fit_score(resume_text, job_description):
    """
    Calculate keyword overlap fit score (1–10).
    """

    resume_words = clean_text(resume_text)
    job_words = clean_text(job_description)

    if not resume_words or not job_words:
        return 1

    overlap = resume_words.intersection(job_words)
    score = int((len(overlap) / len(job_words)) * 10)

    return max(1, min(score, 10))
