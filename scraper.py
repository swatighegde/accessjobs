import streamlit as st
from jobspy import scrape_jobs
import pandas as pd
import time

def fetch_jobs(search_term, location, hours_old):
    is_remote = "remote" in location.lower() if location else False
    loc = location.lower().replace("remote", "").strip() if location else "USA"

    # 1. ADD LINKEDIN BACK TO THE LIST
    sites = [ "glassdoor", "linkedin", "indeed"]
    all_jobs = []

    # 2. INCREASE COUNT TO 100 (Handled in batches to avoid 403/Timeout)
    # Most job boards serve 25 jobs per page. We do 4 "pages".
    results_per_batch = 25
    total_batches = 4 

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(total_batches):
        status_text.text(f"Fetching batch {i+1} of {total_batches}...")
        try:
            # We use 'offset' to get the next set of 25 jobs
            jobs = scrape_jobs(
                site_name=sites,
                search_term=search_term,
                location=loc,
                results_wanted=results_per_batch,
                offset=i * results_per_batch, 
                hours_to_look_back=hours_old,
                is_remote=is_remote,
                enforce_desktop_browser=True, # Essential for Cloud
                verbose=0
                # PRO TIP: If you have a proxy, add: proxies=["user:pass@host:port"]
            )

            if jobs is not None and not jobs.empty:
                all_jobs.append(jobs)
            
            # 3. ANTI-BOT DELAY: Wait 2-3 seconds between batches
            time.sleep(2.5) 
            progress_bar.progress((i + 1) / total_batches)

        except Exception as e:
            st.warning(f"Batch {i+1} encountered an issue: {e}")
            continue

    if all_jobs:
        final_df = pd.concat(all_jobs, ignore_index=True).drop_duplicates(subset=['job_url'])
        status_text.text(f"✅ Found {len(final_df)} unique jobs!")
        return final_df
    
    return None