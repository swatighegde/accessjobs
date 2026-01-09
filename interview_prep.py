"""
interview_prep.py
-----------
Generates a comprehensive interview preparation guide based on the 
job description. It provides 6 theory questions, 2 conceptual 
design questions, and 2 coding challenges with detailed answers.
"""

import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

client = Groq(api_key=api_key) if api_key else None

def get_interview_questions(job_description):
    if not client:
        return {"error": "GROQ_API_KEY not found."}

    try:
        # 1.  PROMPT: Specific instructions for escaping code
        prompt = f"""
        You are an expert technical interviewer. Analyze the Job Description and generate interview preparation content.
        
        STRICT RULES:
        - Output MUST be valid JSON.
        - For 'coding' answers, use plain text or escaped characters. 
        - DO NOT use actual newlines (\n) inside JSON strings; use the literal string "\\n" instead.
        
        REQUIREMENTS:
        1. 6 Theory Questions (Fundamentals, definitions, comparisons)
        2. 2 Conceptual/System Design Questions (Architecture, implementation strategies)
        3. 2 Coding/Practical Questions (Short snippets or logic problems)
        

        JSON STRUCTURE:
        {{
            "theory": [ {{"q": "...", "a": "..."}} ],
            "conceptual": [ {{"q": "...", "a": "..."}} ],
            "coding": [ {{"q": "...", "a": "..."}} ]
        }}

        JOB DESCRIPTION:
        {job_description[:3000]}
        """

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": "You are a technical interviewer that only communicates via valid JSON. Ensure all code snippets in values are properly escaped for JSON compliance."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1, # Lower temperature = more stable JSON
            response_format={"type": "json_object"}
        )

        response_text = completion.choices[0].message.content.strip()

        # 2. SANITIZATION LAYER: Fixes common LLM-to-JSON formatting blunders
        response_text = re.sub(r'^```json\s*|```$', '', response_text, flags=re.MULTILINE)

        return json.loads(response_text)

    except json.JSONDecodeError as e:

        return {"error": "The AI produced complex code that broke the format. Please refresh to try again."}
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}
