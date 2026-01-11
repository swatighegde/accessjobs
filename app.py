"""
app.py
-----------
The main entry point for the Streamlit application. It manages the 
UI layout, sidebar filters, session state for data persistence, 
and coordinates the logic between scraping, parsing, and AI analysis.
"""

import streamlit as st
import pandas as pd
from scraper import fetch_jobs
from resume_parser import extract_resume_text
from fit_score import calculate_fit_score
from match_details import get_match_details
from interview_prep import get_interview_questions

# --- Page Configuration ---
st.set_page_config(
    page_title="AccessJobs – AI Career Assistant",
    page_icon="💼",
    layout="wide"
)

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; }
    .job-card { border: 1px solid #e6e9ef; padding: 20px; border-radius: 10px; background-color: white; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- Initialize Session State ---
# This prevents data from disappearing when clicking 'Match Details'
if "jobs_list" not in st.session_state:
    st.session_state.jobs_list = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# --- Header ---
st.title("💼 AccessJobs")
st.caption("AI-Powered Career Assistant for Professionals")

# --- Sidebar Filters ---
with st.sidebar:
    st.header("🔍 Search Listings")
    
    search_term = st.text_input("Job Title / Keywords", placeholder="e.g. Data Scientist, Ml Engineer")
    location = st.text_input("Location", placeholder="e.g. Plano, Chicago or Remote")
    hours_old = st.selectbox("Posted Within", [ 24, 48, 72], index=1)
    
    st.divider()
    st.header("📄 Your Profile")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    
    search_button = st.button("🚀 Find Jobs")

# --- Logic: Fetch and Process Jobs ---
if search_button:
    if not search_term.strip():
        st.warning("Please enter a job title or keyword.")
        st.stop()
    if not resume_file:
        st.warning("Please upload a resume for AI matching.")
        st.stop()

    with st.spinner("Step 1: Parsing Resume..."):
        st.session_state.resume_text = extract_resume_text(resume_file)

    with st.spinner("Step 2: Searching Jobs "):
        jobs_df = fetch_jobs(search_term, location, int(hours_old))

    if jobs_df is not None and not jobs_df.empty:
        with st.spinner("Step 3: Calculating Fit Scores..."):
            processed_jobs = []
            for _, row in jobs_df.iterrows():
                desc = row.get("description") or ""
                # Calculate the 1-10 Fit Score
                score = calculate_fit_score(st.session_state.resume_text, desc)
                
                processed_jobs.append({
                    "id": str(row.get("job_url")),
                    "title": row.get("title", "N/A"),
                    "company": row.get("company", "Unknown"),
                    "location": row.get("location", "N/A"),
                    "source": str(row.get("site", "N/A")).title(),
                    "url": row.get("job_url"),
                    "description": desc,
                    "fit_score": score
                })
            
            # Sort by highest Fit Score
            processed_jobs.sort(key=lambda x: x["fit_score"], reverse=True)
            st.session_state.jobs_list = processed_jobs
    else:
        st.session_state.jobs_list = []
        st.error("No jobs found. Try expanding your search criteria.")
        
# --- Logic: Display Job Listings ---
if st.session_state.jobs_list:
    st.success(f"Found {len(st.session_state.jobs_list)} jobs matching your profile.")
    
    for idx, job in enumerate(st.session_state.jobs_list):
        with st.container(border=True):
            # 1. Title
            st.subheader(f"💼 {job['title']}")
            
            # 2. Other Details
            st.markdown(f"🏢 **Company:** {job['company']}")
            st.markdown(f"📍 **Location:** {job['location']}")
            st.markdown(f"🌐 **Source:** {job['source']}")
            
            # 3. Fit Score
            score_color = "#2ecc71" if job["fit_score"] >= 7 else "#e74c3c"
            st.markdown(
                f"<p style='font-size:16px; margin-top:5px; margin-bottom:15px;'>"
                f"📊 <b>Fit Score:</b> <span style='color:{score_color};'>{job['fit_score']}/10</span>"
                f"</p>", 
                unsafe_allow_html=True
            )

            # 4. Action Buttons (Row of 3)
            col_apply, col_match, col_interview = st.columns(3)
            
            # Button 1: Apply          
            with col_apply:
                st.link_button("🔗 Apply Now", job["url"], use_container_width=True)
            
            # Button 2: Match Analysis    
            with col_match:
                # FIX 2: Create a unique button key using the index
                btn_key = f"btn_match_{idx}_{job['id']}"
                if st.button("✨ Job Match Analysis", key=btn_key, use_container_width=True):
                    with st.spinner("Analyzing Job ..."):
                   
                        job_desc = str(job.get("description", ""))
                        
                        matched, missing, tip = get_match_details(
                            st.session_state.resume_text, 
                            job_desc
                        )
                        # Store in session state using a unique key
                        st.session_state[f"details_{idx}_{job['id']}"] = {
                            "matched": matched, 
                            "missing": missing,
                            "tip": tip
                        }
                        
            # Button 3: Interview Prep
            with col_interview:
      
                btn_key_int = f"btn_int_{idx}_{job['id']}"
                if st.button("🎤 Interview Q&A", key=btn_key_int, use_container_width=True):
                    with st.spinner("Generating Interview Question and Answer..."):
                        job_desc = str(job.get("description", ""))
                        qna_data = get_interview_questions(job_desc)
                        st.session_state[f"interview_{idx}_{job['id']}"] = qna_data
                    
                    # Clear match state if interview is clicked (using unique key)
                    match_key = f"details_{idx}_{job['id']}"
                    if match_key in st.session_state:
                        del st.session_state[match_key]

            # --- DISPLAY: Match Analysis ---
            data_key = f"details_{idx}_{job['id']}"
            if data_key in st.session_state:
                details = st.session_state[data_key]
                st.markdown("---")
                st.markdown("### 🔍 Semantic Gap Analysis")
                
                st.markdown("#### ✅ Relevant Skills")
                # Ensure details list exists and is not empty
                matched_list = details.get("matched", [])
                if matched_list:
                    for m in matched_list:
                        st.write(m if "✅" in m else f"✅ {m}")
                else:
                    st.write("No specific matches found.")
                
                st.write("") 

                st.markdown("#### ❌ Missing")
                missing_list = details.get("missing", [])
                if missing_list:
                    for g in missing_list:
                        st.write(g if "❌" in g else f"❌ {g}")
                else:
                    st.write("No missing skills identified.")
                
                st.info(f"💡 **Tailoring Tip:** {details['tip']}")


            # --- DISPLAY: Interview Q&A ---
            int_key = f"interview_{idx}_{job['id']}"
            if int_key in st.session_state:
                qna = st.session_state[int_key]
                
                if isinstance(qna, dict) and "error" in qna:
                    st.error(f"⚠️ Error: {qna['error']}")
                else:
                    st.markdown("---")
                    st.markdown("### 🎤 Interview Preparation Q&A")
                    
                    with st.expander("📘 Theory Questions (6)", expanded=True):
                        for i, item in enumerate(qna.get("theory", []), 1):
                            st.markdown(f"**Q{i}: {item['q']}**")
                            st.caption(f"💡 Answer: {item['a']}")
                            st.divider()

                    with st.expander("🛠️ Conceptual & Design (2)", expanded=False):
                        for i, item in enumerate(qna.get("conceptual", []), 1):
                            st.markdown(f"**Q{i}: {item['q']}**")
                            st.info(f"📝 Approach: {item['a']}")

                    with st.expander("💻 Coding Challenges (2)", expanded=False):
                        for i, item in enumerate(qna.get("coding", []), 1):
                            st.markdown(f"**Q{i}: {item['q']}**")
                            st.code(item['a'], language='python')
                            
else:
    if not search_button:
        st.info("👋 Welcome! Upload your resume and search for a job title to get started.")

st.markdown("""
<hr style="margin-top: 2rem;">
<div style="text-align: center; font-size: 0.85rem; color: #6B7280;">
    © 2026 <strong>Swati Hegde</strong> · 
    <a href="https://chieac.org" target="_blank" style="color: inherit; text-decoration: none;">
        Chicago Education Advocacy Cooperative (ChiEAC)
    </a><br>
""", unsafe_allow_html=True)
