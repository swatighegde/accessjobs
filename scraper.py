import streamlit as st
from jobspy import scrape_jobs
import pandas as pd

def fetch_jobs(search_term, location, hours_old):
    """
    Updated for JobSpy v1.1.60+ compatibility.
    """
    st.toast(f"Searching for {search_term}...")
    
    # Handle Remote Logic
    is_remote = False
    loc = location
    if location and "remote" in location.lower():
        is_remote = True
        loc = location.lower().replace("remote", "").strip()

    # Use cloud-friendly sources
    safe_sources = ["zip_recruiter", "glassdoor"]

    try:
        # CRITICAL UPDATE: Using 'hours_to_look_back' instead of 'hours_old'
        jobs_df = scrape_jobs(
            site_name=safe_sources,
            search_term=search_term,
            location=loc,
            results_wanted=15,
            hours_to_look_back=hours_old, # <--- THIS IS THE FIX
            is_remote=is_remote,
            enforce_desktop_browser=True
        )
        
        if jobs_df is not None and not jobs_df.empty:
            return jobs_df
            
    except TypeError as e:
        # If even 'hours_to_look_back' fails, we run without the time filter
        # This guarantees the app won't crash, even if the filter is ignored
        st.warning("⚠️ Version conflict detected. Running search without time filter.")
        try:
            return scrape_jobs(
                site_name=safe_sources,
                search_term=search_term,
                location=loc,
                results_wanted=15,
                is_remote=is_remote
            )
        except Exception as e2:
             st.error(f"Critical Scraper Error: {e2}")

    except Exception as e:
        st.error(f"Scraper Error: {e}")
        
    return None