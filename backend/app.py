# backend/app.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from .parser import extract_text_from_pdf, extract_basic_fields
from .scorer import compute_score
import shutil
from pathlib import Path

app = FastAPI(title="Smart Resume Screener")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    text = extract_text_from_pdf(str(file_path))
    parsed = extract_basic_fields(text)
    return parsed


@app.post("/score")
async def score_resume(candidate_text: str = Form(...), jd_text: str = Form(...)):
    cand = extract_basic_fields(candidate_text)
    required, preferred, min_exp = [], [], 0

    for line in jd_text.splitlines():
        l = line.lower()
        if "required:" in l:
            required = [x.strip() for x in l.split(":", 1)[1].split(",")]
        elif "preferred:" in l:
            preferred = [x.strip() for x in l.split(":", 1)[1].split(",")]
        elif "experience" in l:
            import re
            m = re.search(r"(\d+)", l)
            if m:
                min_exp = int(m.group(1))

    jd = {
        "title": jd_text.splitlines()[0] if jd_text.splitlines() else None,
        "required_skills": required,
        "preferred_skills": preferred,
        "min_experience_years": min_exp,
        "raw_text": jd_text
    }

    return compute_score(cand, jd)
