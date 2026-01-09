import streamlit as st
from jobspy import scrape_jobs
import pandas as pd
import time

def fetch_jobs(search_term, location, hours_old):
    is_remote = "remote" in location.lower() if location else False
    loc = location.lower().replace("remote", "").strip() if location else "USA"

    # LinkedIn and Glassdoor REQUIRE proxies on Streamlit Cloud.
    # Without a proxy, they will almost always return 0 results or 403 error.
    sites = ["indeed", "linkedin", "glassdoor"]
    all_jobs = []
    
    # We will fetch in 4 batches of 25 to reach 100 jobs total
    results_per_batch = 25
    total_batches = 4

    # --- PROXY CONFIGURATION ---
    # You can get a free/cheap residential proxy from sites like Webshare or ProxyScrape.
    # Format: "http://username:password@ip:port"
    # my_proxies = ["http://your_proxy_here"] 
    # ---------------------------

    progress_bar = st.progress(0)

    for i in range(total_batches):
        try:
            # Use 'offset' to get the next page of results
            batch_df = scrape_jobs(
                site_name=sites,
                search_term=search_term,
                location=loc,
                results_wanted=results_per_batch,
                offset=i * results_per_batch, # Page 1: 0, Page 2: 25...
                hours_to_look_back=hours_old,
                is_remote=is_remote,
                enforce_desktop_browser=True, # Helps with LinkedIn
                # proxies=my_proxies, # Uncomment this if you get a proxy
                timeout=30
            )

            if batch_df is not None and not batch_df.empty:
                all_jobs.append(batch_df)
            
            # ANTI-BOT DELAY: Very important for Cloud!
            time.sleep(3) 
            progress_bar.progress((i + 1) / total_batches)

        except Exception as e:
            st.warning(f"Batch {i+1} failed: {e}")
            continue

    if all_jobs:
        final_df = pd.concat(all_jobs, ignore_index=True)
        # Remove any duplicates that might have been fetched in different batches
        final_df = final_df.drop_duplicates(subset=['job_url'])
        return final_df
    
    return None