import streamlit as st
from jobspy import scrape_jobs
import pandas as pd

def fetch_jobs(search_term, location, hours_old):
    """
    Individually scrapes sites so that if one (like Glassdoor) fails, 
    the others still return results.
    """
    is_remote = "remote" in location.lower() if location else False
    loc = location.lower().replace("remote", "").strip() if location else "USA"

    all_results = []
    # We try these one by one to isolate errors
    sites_to_try = ["zip_recruiter", "glassdoor", "indeed"]

    for site in sites_to_try:
        try:
            # Attempt scraping for a single site
            res = scrape_jobs(
                site_name=[site],
                search_term=search_term,
                location=loc,
                results_wanted=10,
                is_remote=is_remote,
                # We use a very high timeout for cloud stability
                timeout=20 
            )
            if res is not None and not res.empty:
                all_results.append(res)
        except Exception as e:
            # We log the error but CONTINUE to the next site
            print(f"Log: {site} failed with error {e}")
            continue 

    # Combine all successful results
    if all_results:
        final_df = pd.concat(all_results, ignore_index=True)
        return final_df
    
    return None