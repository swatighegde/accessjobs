"""
scraper.py
-----------
Responsible for fetching recent jobs from LinkedIn, Indeed, Glassdoor
and ZipRecruiter using python-jobspy. It filters results based on 
keywords, location, and the post date (hours old).
"""

from jobspy import scrape_jobs

def fetch_jobs(search_term, location, hours_old):
    # (Remote logic stays the same...)
    is_remote = "remote" in location.lower() if location else False
    loc = location.lower().replace("remote", "").strip() if location else ""

    try:
        # We add verbose=2 to see the "Under the hood" logs
        jobs_df = scrape_jobs(
            site_name=["linkedin", "indeed", "zip_recruiter"],
            search_term=search_term,
            location=loc or "USA",
            results_wanted=15,
            hours_old=hours_old,
            country_indeed="USA",
            is_remote=is_remote,
            enforce_desktop_browser=True,
            verbose=2  # <--- CRITICAL DEBUG LINE
        )
        
        # Check if the dataframe is truly empty or just None
        if jobs_df is not None:
            print(f"DEBUG: Scraper returned {len(jobs_df)} rows.")
            if not jobs_df.empty:
                return jobs_df
        else:
            print("DEBUG: Scraper returned None Type.")

    except Exception as e:
        print(f"CRITICAL ERROR in Scraper: {e}")
        
    return None