"""
scraper.py
-----------
Responsible for fetching recent jobs from LinkedIn and Indeed
using python-jobspy. It filters results based on 
keywords, location, and the post date (hours old).
"""

import streamlit as st
from jobspy import scrape_jobs
import pandas as pd
import time

def fetch_jobs(search_term, location, hours_old):
    """
    Focused scraper for LinkedIn and Indeed.
    Uses batching to reach ~100 results while avoiding Cloud blocks.
    """
    is_remote = "remote" in location.lower() if location else False
    loc = location.lower().replace("remote", "").strip() if location else "USA"

    # Restricted to the two most reliable sources for Cloud deployment
    sites = ["linkedin", "indeed"]
    all_jobs = []
    
    # Batching logic: 4 batches of 25 = 100 results
    results_per_batch = 25
    total_batches = 4

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(total_batches):
        status_text.text(f"🚀 Fetching batch {i+1} of {total_batches}...")
        
        try:
            # We scrape both sites together in this version for speed
            batch_df = scrape_jobs(
                site_name=sites,
                search_term=search_term,
                location=loc,
                results_wanted=results_per_batch,
                offset=i * results_per_batch,
                hours_to_look_back=hours_old,
                is_remote=is_remote,
                enforce_desktop_browser=True, # Critical for LinkedIn on Cloud
                timeout=30
            )

            if batch_df is not None and not batch_df.empty:
                all_jobs.append(batch_df)
            
            # Anti-bot delay: Prevents the server from being flagged as a scraper
            time.sleep(2.5) 
            progress_bar.progress((i + 1) / total_batches)

        except Exception as e:
            # Log the error to the console but don't crash the app
            print(f"Batch {i+1} skip: {e}")
            continue

    status_text.empty()

    if all_jobs:
        # Combine batches and remove duplicates based on the URL
        final_df = pd.concat(all_jobs, ignore_index=True)
        final_df = final_df.drop_duplicates(subset=['job_url'])
        st.sidebar.success(f"✅ Found {len(final_df)} unique jobs!")
        return final_df
    
    return None