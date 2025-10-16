# frontend/app.py

import streamlit as st
import requests

st.set_page_config(page_title="Smart Resume Screener", layout="centered")

st.title("Smart Resume Screener 🧠")
st.markdown("Upload a resume and job description to get a compatibility score!")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
resume_text = st.text_area("Or paste resume text below")
jd_text = st.text_area("Paste Job Description")

if st.button("Score Candidate"):
    if not jd_text.strip():
        st.error("Please paste a job description.")
    else:
        if resume_text.strip():
            candidate_text = resume_text
        elif uploaded_file:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            resp = requests.post("http://127.0.0.1:8000/upload_resume", files=files)
            candidate_text = resp.json().get("raw_text", "")
        else:
            st.error("Upload a resume or paste text.")
            st.stop()

        data = {"candidate_text": candidate_text, "jd_text": jd_text}
        r = requests.post("http://127.0.0.1:8000/score", data=data)

        if r.status_code == 200:
            res = r.json()
            st.success(f"Match Score: {res['score']}/10")
            st.json(res["breakdown"])
            st.write("### Justification")
            st.write(res["justification"])
            st.write("### Strengths")
            for s in res["strengths"]:
                st.write(f"- {s}")
            st.write("### Weaknesses")
            for w in res["weaknesses"]:
                st.write(f"- {w}")
        else:
            st.error("Error: Could not connect to backend.")
