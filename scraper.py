import streamlit as st
from jobspy import scrape_jobs
import pandas as pd

def fetch_jobs(search_term, location, hours_old):
    """
    Fetches jobs with 'Safe Mode' defaults for Cloud Deployment.
    Excludes Indeed/LinkedIn by default to prevent IP blocking crashes.
    """
    is_remote = "remote" in location.lower() if location else False
    loc = location.lower().replace("remote", "").strip() if location else "USA"

    # 1. USE ONLY CLOUD-FRIENDLY SOURCES
    # Indeed and LinkedIn almost always block Streamlit Cloud IPs.
    # ZipRecruiter and Glassdoor are much more reliable without proxies.
    safe_sources = ["zip_recruiter", "glassdoor"]
    
    # 2. Base Arguments
    search_args = {
        "site_name": safe_sources,
        "search_term": search_term,
        "location": loc,
        "results_wanted": 15,
        "is_remote": is_remote,
        # 'country_indeed' is removed since we aren't scraping Indeed
    }

    st.toast(f"Searching {', '.join(safe_sources)}...")

    try:
        # 3. Attempt to scrape
        # We try the new parameter first, then fallback
        try:
            return scrape_jobs(**search_args, hours_to_look_back=hours_old)
        except TypeError:
            return scrape_jobs(**search_args, hours_old=hours_old)
            
    except Exception as e:
        # 4. Graceful Error Handling (Prevents the "Red Screen of Death")
        error_msg = str(e).lower()
        if "indeed" in error_msg:
            st.error("Indeed blocked the connection. Switched to other sources.")
        elif "linkedin" in error_msg:
            st.error("LinkedIn blocked the connection. Switched to other sources.")
        else:
            st.error(f"Could not fetch jobs: {e}")
        
        return None