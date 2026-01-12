"""
match_details.py
-----------
Performs a deep semantic gap analysis using the Groq Llama 3.3 model.
It identifies specific qualifications found in the resume and 
highlights missing requirements, providing evidence for each.
"""

import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def get_match_details(resume_text, job_description):
    try:
        # Using Llama 3.3 70B for the highest quality reasoning
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert ATS (Applicant Tracking System) analyzer."
                },
                {
                    "role": "user", 
                    "content": f"""
                        Perform a detailed Semantic Gap Analysis. 
                        
                        For MATCHES: Find requirements met and provide evidence from the resume.
                        Format: ✅ [Requirement]: [Evidence from resume]

                        For GAPS: Identify missing requirements or those not explicitly stated.
                        Format: ❌ [Requirement]: (No explicit mention)

                        LIMIT: 5 detailed items for each category.
                        TIP: Provide one specific ATS tailoring tip at the end starting with 'TIP:'.

                        RESUME: {resume_text[:3000]}
                        JOB DESCRIPTION: {job_description[:3000]}
                    """
                }
            ],
            temperature=0.3, # Lower temperature for more consistent formatting
        )

        full_text = completion.choices[0].message.content

        matched = []
        missing = []
        tip = "Tailor your professional summary to include keywords from the JD."

        # IMPROVED PARSING: Handles bolding, whitespace, and case sensitivity
        lines = full_text.split('\n')
        for line in lines:
            clean_line = line.strip().replace("*", "") # Remove markdown bolding
            
            if "✅" in clean_line:
                # Extracts everything after the emoji
                parts = clean_line.split("✅", 1)
                matched.append(parts[1].strip())
            elif "❌" in clean_line:
                parts = clean_line.split("❌", 1)
                missing.append(parts[1].strip())
            elif "TIP:" in clean_line.upper():
                tip = clean_line.split(":", 1)[1].strip()

        # Final check: If the lists are empty, the AI might have skipped emojis
        if not matched:
            matched = ["AI could not find explicit evidence. Review your skills section."]
        if not missing:
            missing = ["No major gaps identified based on the provided text."]

        return matched, missing, tip

    except Exception as e:
        return [f"Error: {str(e)}"], ["Analysis failed"], "Check API connection."