# config.py
# This file stores project-wide settings

# Job sources supported by python-jobspy
JOB_SITES = ["linkedin", "indeed", "zip_recruiter"]

# Maximum number of jobs to fetch per search
MAX_JOBS = 100

# Default job age filter (in hours)
DEFAULT_HOURS_OLD = 24

# Gemini AI model (free tier)
GEMINI_MODEL = "models/gemini-1.5-flash"
