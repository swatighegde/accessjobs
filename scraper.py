import streamlit as st
from jobspy import scrape_jobs
import pandas as pd

def fetch_jobs(search_term, location, hours_old):
    is_remote = "remote" in location.lower() if location else False
    loc = location.lower().replace("remote", "").strip() if location else "USA"

    # Define the base arguments
    search_args = {
        "site_name": ["indeed", "zip_recruiter", "linkedin"],
        "search_term": search_term,
        "location": loc,
        "results_wanted": 15,
        "country_indeed": "USA",
        "is_remote": is_remote,
        "enforce_desktop_browser": True,
        "timeout": 30
    }

    # Try different versions of the time-filter argument
    try:
        # Attempt 1: The newest version (hours_to_look_back)
        return scrape_jobs(**search_args, hours_to_look_back=hours_old)
    except TypeError:
        try:
            # Attempt 2: The older version (hours_old)
            return scrape_jobs(**search_args, hours_old=hours_old)
        except TypeError:
            # Attempt 3: If both fail, run without the time filter to at least get results
            st.warning("Running search without time filter due to version compatibility...")
            return scrape_jobs(**search_args)
    except Exception as e:
        st.error(f"Scraper technical error: {str(e)}")
        return None