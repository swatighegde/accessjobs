import streamlit as st
from jobspy import scrape_jobs
import pandas as pd
import time

def fetch_jobs(search_term, location, hours_old):
    is_remote = "remote" in location.lower() if location else False
    # Glassdoor often prefers 'City, State' format over just 'City'
    loc = location if location else "USA"

    sites = ["linkedin", "indeed", "glassdoor"]
    all_jobs = []
    
    # We'll stick to a slightly smaller batch for Cloud stability
    results_per_batch = 25
    total_batches = 3 # Aiming for ~75-100 results

    progress_bar = st.progress(0)

    for i in range(total_batches):
        for site in sites:
            try:
                # We scrape one site at a time to prevent one site's 403 
                # from killing the entire batch
                batch_df = scrape_jobs(
                    site_name=[site],
                    search_term=search_term,
                    location=loc,
                    results_wanted=results_per_batch,
                    offset=i * results_per_batch,
                    hours_to_look_back=hours_old,
                    is_remote=is_remote,
                    enforce_desktop_browser=True,
                    # Glassdoor is sensitive; we increase timeout specifically for it
                    timeout=40 if site == "glassdoor" else 25
                )

                if batch_df is not None and not batch_df.empty:
                    all_jobs.append(batch_df)
                
                # Small sleep between SITES to avoid triggering Cloudflare
                time.sleep(1.5)

            except Exception as e:
                # If Glassdoor fails, we don't want to stop LinkedIn/Indeed
                if "glassdoor" in site.lower():
                    print(f"Glassdoor still blocking: {e}")
                continue

        # Progress update after each full batch cycle
        progress_bar.progress((i + 1) / total_batches)
        # Larger delay between BATCHES
        time.sleep(2)

    if all_jobs:
        final_df = pd.concat(all_jobs, ignore_index=True)
        return final_df.drop_duplicates(subset=['job_url'])
    
    return None