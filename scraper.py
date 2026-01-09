"""
scraper.py
-----------
Robust version with increased timeout and retry logic.
"""
import streamlit as st
from jobspy import scrape_jobs
import pandas as pd

def fetch_jobs(search_term, location, hours_old):
    is_remote = "remote" in location.lower() if location else False
    loc = location.lower().replace("remote", "").strip() if location else "USA"

    # Try up to 2 times if there's a timeout
    for attempt in range(2):
        try:
            jobs_df = scrape_jobs(
                site_name=["indeed", "zip_recruiter", "linkedin"], 
                search_term=search_term,
                location=loc,
                results_wanted=15,
                hours_to_look_back=hours_old,
                country_indeed="USA",
                is_remote=is_remote,
                enforce_desktop_browser=True,
                timeout=30, # Increased from default 10s to 30s
                verbose=2 
            )
            
            if jobs_df is not None and not jobs_df.empty:
                return jobs_df
            break # Exit loop if request finishes but is empty

        except Exception as e:
            # Check specifically for timeout in the error message
            if "timeout" in str(e).lower() and attempt == 0:
                st.toast("⚠️ Connection slow, retrying...")
                continue # Try one more time
            else:
                st.error(f"Scraper technical error: {str(e)}")
                break
                
    return None