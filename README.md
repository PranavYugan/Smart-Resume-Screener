# 🧠 Smart Resume Screener

An AI powered application that compares a candidate’s resume with a job description and generates a compatibility score with explanations.

Tech Stack:
  Backend: FastAPI (Python)
  Frontend: Streamlit
  Parsing: pdfplumber, spaCy
  Scoring: Rule based (optional OpenAI GPT integration)

Architecture:
  Flow:
    - Resume (PDF or Text)
    - parser.py: extracts name, skills, experience, and education
    - scorer.py: compares candidate data with JD and calculates score
    - backend/app.py: FastAPI server exposing /upload_resume and /score endpoints
    - frontend/app.py: Streamlit web interface for uploading resume and displaying results

Example LLM Prompt: |
  You are an assistant that evaluates how well a candidate fits a job description.
  Given the candidate JSON and JD JSON, return JSON with:
    score: 0–10
    breakdown: {skills, experience, education, semantic}
    justification: 2–3 sentences
    strengths: []
    weaknesses: []

Run Locally:
  - Clone repository:
      git clone https://github.com/<your-username>/Smart-Resume-Screener.git
      cd Smart-Resume-Screener
  - Setup environment:
      python -m venv venv
      .\venv\Scripts\activate
      pip install -r requirements.txt
      python -m spacy download en_core_web_sm
  - Start backend:
      uvicorn backend.app:app --reload
  - Start frontend:
      streamlit run frontend/app.py

Demo Video:
  Paste your Google Drive video link here.

Author:
  Name: Pranav Yugan R
  Email: pranavyugan.r2022@vitstudent.ac.in
  LinkedIn: https://www.linkedin.com/in/pranav-yugan/
  GitHub: https://github.com/PranavYugan
