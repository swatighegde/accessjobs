import streamlit as st
from jobspy import scrape_jobs
import pandas as pd

def fetch_jobs(search_term, location, hours_old):
    """
    Stable scraper linked to jobspy==1.1.35
    """
    st.toast(f"Searching for {search_term}...")
    
    # Handle Remote Logic
    is_remote = False
    loc = location
    if location and "remote" in location.lower():
        is_remote = True
        loc = location.lower().replace("remote", "").strip()

    # Define safe sources (Indeed blocks cloud IPs, so we skip it)
    safe_sources = ["zip_recruiter", "glassdoor"]

    try:
        # We use 'hours_old' because we pinned jobspy==1.1.35 in requirements.txt
        jobs_df = scrape_jobs(
            site_name=safe_sources,
            search_term=search_term,
            location=loc,
            results_wanted=15,
            hours_old=hours_old, 
            is_remote=is_remote,
            country_indeed="USA"
        )
        
        if jobs_df is not None and not jobs_df.empty:
            return jobs_df
            
    except Exception as e:
        st.error(f"Scraper Error: {e}")
        
    return None