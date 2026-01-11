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
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor

def fetch_single_batch(site, search_term, location, offset, is_remote):
    """Fetches a specific 'page' of results to maximize job count."""
    try:
        return scrape_jobs(
            site_name=[site],
            search_term=search_term,
            location=location,
            results_wanted=500, 
            offset=offset,
            hours_old=72,  
            is_remote=is_remote,
            enforce_desktop_browser=True,
            timeout=50
        )
    except:
        return pd.DataFrame()

def fetch_jobs(search_term, location, hours_old):
    is_remote = "remote" in location.lower() if location else False
    loc = location.lower().replace("remote", "").strip() if location else "USA"
    
    all_dfs = []
    status = st.empty()
    status.info(f"🚀 Deep-scanning {search_term} in {loc} (Last {hours_old}h)...")

    # 1. DEEP-DIVE BATCHING: Parallelize 3 pages per site (6 total requests at once)
    with ThreadPoolExecutor(max_workers=6) as executor:
        tasks = []
        for site in ["linkedin", "indeed"]:
            for offset in [0, 25, 50]: # Offset forces the site to show more than the 'sample'
                tasks.append(executor.submit(fetch_single_batch, site, search_term, loc, offset, is_remote))
        
        for future in tasks:
            res = future.result()
            if not res.empty:
                all_dfs.append(res.dropna(axis=1, how='all'))

    status.empty()
    if not all_dfs: return None

    # 2. CONSOLIDATE & NORMALIZE
    df = pd.concat(all_dfs, ignore_index=True).drop_duplicates(subset=['job_url'])
    df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce', utc=True)
    df = df.dropna(subset=['date_posted'])

    # 3. RUTHLESS TIME FILTER
    # Since the site only likes '72h', take the 72h data and 
    # manually throw away anything that doesn't fit  24h/48h request.
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=int(hours_old))
    final_df = df[df['date_posted'] >= cutoff].copy()

    # 4. FINAL SORT
    if final_df.empty:
        return df.sort_values(by='date_posted', ascending=False).head(65)
    
    return final_df.sort_values(by='date_posted', ascending=False)