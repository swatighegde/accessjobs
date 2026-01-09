"""
scraper.py
-----------
Enhanced version for Cloud Debugging.
"""
import streamlit as st
from jobspy import scrape_jobs
import pandas as pd

def fetch_jobs(search_term, location, hours_old):
    # Debug message visible on the app screen
    st.toast(f"🔍 Searching {search_term} in {location}...")
    
    is_remote = "remote" in location.lower() if location else False
    loc = location.lower().replace("remote", "").strip() if location else "USA"

    try:
        # We start with a very small request to see if it passes
        jobs_df = scrape_jobs(
            site_name=["indeed", "zip_recruiter"], # Temporarily removed LinkedIn for testing
            search_term=search_term,
            location=loc,
            results_wanted=5, 
            hours_old=hours_old,
            country_indeed="USA",
            is_remote=is_remote,
            enforce_desktop_browser=True,
            verbose=2 
        )
        
        if jobs_df is not None and not jobs_df.empty:
            st.sidebar.success(f"Fetched {len(jobs_df)} jobs!")
            return jobs_df
        else:
            # This will show up in your 'Manage App' logs
            print(f"DEBUG LOG: Scraper returned 0 results for {search_term}")
            
    except Exception as e:
        st.error(f"Scraper encountered a technical error: {str(e)}")
        print(f"CRITICAL ERROR: {e}")
        
    return None