# 💼 AccessJobs: AI-Powered Career Assistant

**AccessJobs** is an intelligent job search and career preparation platform designed to empower tech professionals and emerging scholars. The application fetches **recent job postings based on user-provided criteria** and leverages **Large Language Models (LLMs) via the Groq API** to deliver personalized fit scores, deep semantic gap analysis, and tailored interview preparation based on a user's unique resume and specific job descriptions.

---

## ✨ Key Features

* **Live Job Aggregator:** Scrape multiple job boards simultaneously with filters for title, location, and post date using `python-jobspy`.
* **Instant Fit Scoring:** Get a **1-10 Profile Fit Score** immediately based on a semantic comparison between your resume and the job description.
* **Semantic Gap Analysis:** A deep-dive analysis that categorizes findings into:
    * **✅ Relevant Skills:** Requirements met with specific evidence extracted from your resume.
    * **❌ Missing:** Critical gaps or skills not clearly mentioned in your profile.
* **AI Interview Coach:** Generates a custom, job-specific study guide using **Llama 3.3** via Groq, featuring:
    * **6 Theory Questions:** Focused on core fundamentals and definitions.
    * **2 Conceptual Design Questions:** Focused on architecture and implementation strategies.
    * **2 Coding Challenges:** Practical logic or programming problems with solutions.
* **Smart State Management:** Results are preserved within the session
* **ATS Tailoring Tips:** Receive a specific, actionable tip for every job to help your resume pass through automated filters.

---

## 🎯 Objectives
* **Bridge the Information Gap:** Help professionals understand how their international or specialized experience aligns with job requirements.
* **Optimize Applications:** Provide actionable "Semantic Gap Analysis" to help users tailor their resumes for ATS (Applicant Tracking Systems).
* **Accelerate Interview Readiness:** Generate relevant technical and theoretical questions based on specific job postings to build user confidence.

---

## 🏗️ Project Structure

accessjobs/
├── app.py              # Main UI and application orchestration
├── scraper.py          # Job board scraping logic (LinkedIn, Indeed, etc.)
├── resume_parser.py    # PDF text extraction and cleaning
├── fit_score.py        # AI logic for 1-10 profile matching
├── match_details.py    # Semantic Gap Analysis & Evidence extraction
├── interview_prep.py   # Interview Q&A generation (Llama 3.3)
├── .env                # Environment variables (API Keys)
└── requirements.txt    # Python dependencies
├── README.md           # Project Details

---

## 💻 Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/)
* **LLM Provider:** [Groq Cloud](https://console.groq.com/)
* **Models:** Llama 3.3 70B (Match Analysis & Fit Score)
* **Scraping:** [JobSpy](https://github.com/Bunsly/JobSpy)
* **Parsing:** pdfplumber

---

## 🚀 Setup Instructions

### 1. Prerequisites
Ensure you have **Python 3.10+** installed and a **Groq API Key**.

### 2. Clone and Install
```bash
git clone https://github.com/swatighegde/accessjobs.git

```

### 3. Create & Activate Virtual Environment**

```bash
python3 -m venv accessjobs
source accessjobs/bin/activate   # macOS/Linux
accessjobs\Scripts\activate      # Windows
```

### 4. Install Requirements**

```bash
pip install -r requirements.txt
```

### 5. Create `.env` File**

Add your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

### 6. Run the Application (Local)**

```bash
python -m streamlit run app.py
```

---

## 🔗 Live Application

You can explore the deployed application here:  
👉 https://accessjobs.streamlit.app/

---