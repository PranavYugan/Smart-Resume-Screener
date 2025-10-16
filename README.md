Demo Video: https://drive.google.com/file/d/1pHBy65ra9rifJUnErDkSdtGxb__AAxNF/view?usp=sharing

project_name: Smart Resume Screener

description: >
  An AI-powered application that compares a candidate's resume with a job description
  and generates a compatibility score with explanation, strengths, and weaknesses.

tech_stack:
  backend: FastAPI (Python)
  frontend: Streamlit
  parsing: pdfplumber, spaCy
  scoring: Rule-based (optional OpenAI GPT integration)

architecture:
  flow:
    - Resume (PDF or Text)
    - parser.py: extracts name, skills, experience, and education
    - scorer.py: compares candidate data with JD and calculates score
    - backend/app.py: FastAPI server exposing /upload_resume and /score endpoints
    - frontend/app.py: Streamlit web interface for uploading resume and displaying results

example_llm_prompt: |
  You are an assistant that evaluates how well a candidate fits a job description.
  Given the candidate JSON and JD JSON, return JSON with:
    score: 0–10
    breakdown: {skills, experience, education, semantic}
    justification: 2–3 sentences
    strengths: []
    weaknesses: []

run_locally: |
  - Clone repository:
      git clone https://github.com/PranavYugan/Smart-Resume-Screener.git
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

notes:
  - Do not commit the venv folder or any secrets. Add .env to .gitignore if present.
  - If you want OpenAI-based semantic scoring, add OPENAI_API_KEY to a .env file.

author:
  name: Pranav Yugan R
  email: pranavyugan.r2022@vitstudent.ac.in
  linkedin: https://www.linkedin.com/in/pranav-yugan/
  github: https://github.com/PranavYugan
