"""
interview_prep.py
-----------
Generates a comprehensive interview preparation guide based on the 
job description. It provides 6 theory questions, 2 conceptual 
design questions, and 2 coding challenges with detailed answers.
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

# Initialize client safely
client = Groq(api_key=api_key) if api_key else None

def get_interview_questions(job_description):
    """
    Generates interview questions based on the JD using Groq (Llama 3.3).
    Returns a dictionary with 3 categories: Theory, Conceptual, Coding.
    """
    if not client:
        return {"error": "GROQ_API_KEY not found. Please add it to your .env file."}

    try:
        # We ask for JSON output for easier parsing
        prompt = f"""
        You are an expert technical interviewer. Analyze the following Job Description and generate interview questions with answers.
        
        REQUIREMENTS:
        1. 6 Theory Questions (Fundamentals, definitions, comparisons)
        2. 2 Conceptual/System Design Questions (Architecture, implementation strategies)
        3. 2 Coding/Practical Questions (Short snippets or logic problems)
        
        OUTPUT FORMAT (Strict JSON):
        {{
            "theory": [
                {{"q": "Question 1", "a": "Answer 1"}},
                ...
            ],
            "conceptual": [
                {{"q": "Question 1", "a": "Answer 1"}},
                ...
            ],
            "coding": [
                {{"q": "Question 1", "a": "Answer 1"}},
                ...
            ]
        }}

        JOB DESCRIPTION:
        {job_description[:3000]}
        """

        completion = client.chat.completions.create(
  
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs strictly valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"} # Forces JSON mode
        )

        response_text = completion.choices[0].message.content.strip()

        # Clean Markdown if the model adds it (e.g., ```json ... ```)
        if "```" in response_text:
            response_text = response_text.replace("```json", "").replace("```", "").strip()

        return json.loads(response_text)

    except json.JSONDecodeError:
        return {"error": "AI returned invalid JSON. Try again."}
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}