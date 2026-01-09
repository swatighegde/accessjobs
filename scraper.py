import streamlit as st
from jobspy import scrape_jobs
import pandas as pd

def fetch_jobs(search_term, location, hours_old):
    is_remote = "remote" in location.lower() if location else False
    loc = location.lower().replace("remote", "").strip() if location else "USA"

    # Step 1: Start with ONLY the most basic, universal arguments
    search_args = {
        "site_name": ["indeed", "zip_recruiter", "linkedin"],
        "search_term": search_term,
        "location": loc,
        "results_wanted": 10,
        "is_remote": is_remote
    }

    try:
        # Step 2: Try to run with the time filter (hours_to_look_back)
        return scrape_jobs(**search_args, hours_to_look_back=hours_old)
    except TypeError:
        try:
            # Step 3: Try the older time filter (hours_old)
            return scrape_jobs(**search_args, hours_old=hours_old)
        except TypeError:
            # Step 4: Final Fallback - No time filter, No extra flags
            # This is the "Safe Mode" that should never throw a TypeError
            st.info("🔍 Running in compatibility mode...")
            return scrape_jobs(**search_args)
    except Exception as e:
        st.error(f"Scraper error: {str(e)}")
        return None