"""
scraper.py
-----------
Responsible for fetching recent jobs from LinkedIn, Indeed, Glassdoor
and ZipRecruiter using python-jobspy. It filters results based on 
keywords, location, and the post date (hours old).
"""

from jobspy import scrape_jobs
from config import JOB_SOURCES, MAX_JOBS

def fetch_jobs(search_term, location, hours_old):
    """
    Fetch recent jobs using JobSpy.
    """
    # 1. Check if user typed 'remote' in the location box
    is_remote_search = False
    search_location = location
    
    if location and "remote" in location.lower():
        is_remote_search = True
        # If the input was ONLY 'remote', set location to empty for a global/USA search
        search_location = location.lower().replace("remote", "").strip()
        
    # 2. Call scrape_jobs with the is_remote parameter
    try:
        jobs_df = scrape_jobs(
            site_name=JOB_SOURCES,
            search_term=search_term,
            location=location,
            results_wanted=MAX_JOBS,
            hours_old=hours_old,
            country_indeed="USA",
            is_remote=is_remote_search
        )
    except Exception as e:
        print(f"Scraping error encountered: {e}")
        return None

    if jobs_df is None or jobs_df.empty:
        return None

    return jobs_df
