"""
scraper.py
-----------
Responsible for fetching recent jobs from LinkedIn, Indeed, Glassdoor
and ZipRecruiter using python-jobspy. It filters results based on 
keywords, location, and the post date (hours old).
"""

import random
from jobspy import scrape_jobs
try:
    from config import JOB_SOURCES, MAX_JOBS
except ImportError:
    JOB_SOURCES = ["linkedin", "indeed", "zip_recruiter", "glassdoor"]
    MAX_JOBS = 15

def fetch_jobs(search_term, location, hours_old):
    """
    Enhanced scraper with bot-detection bypass for Streamlit Cloud.
    """
    # 1. Handle Remote logic
    is_remote = False
    loc = location
    if location and "remote" in location.lower():
        is_remote = True
        loc = location.lower().replace("remote", "").strip()

    # 2. Add a fallback location to prevent empty searches
    if not loc and not is_remote:
        loc = "USA"

    try:
        # 3. Rotating User Agents (Optional but helps)
        # JobSpy handles most of this, but enforce_desktop_browser is key
        jobs_df = scrape_jobs(
            site_name=JOB_SOURCES,
            search_term=search_term,
            location=loc,
            results_wanted=MAX_JOBS,
            hours_old=hours_old,
            country_indeed="USA",
            is_remote=is_remote,
            enforce_desktop_browser=True, # Crucial for Cloud deployment
            proxies=[] # If you ever get a proxy service, add it here
        )

        if jobs_df is not None and not jobs_df.empty:
            # Clean up the dataframe to ensure it's compatible with Streamlit
            return jobs_df.fillna("") 
            
    except Exception as e:
        # This will show up in your 'Manage App' logs
        print(f"DEBUG: Scraper failed with error: {e}")
        
    return None