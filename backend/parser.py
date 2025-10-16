# backend/parser.py

import re
import pdfplumber
import spacy
from pathlib import Path

# Load the small English NLP model from spaCy
nlp = spacy.load("en_core_web_sm")

# A small database of skills to look for
SKILLS_DB = {
    "python", "fastapi", "flask", "docker", "postgresql", "postgres", "sql", "nlp",
    "git", "linux", "ci/cd", "aws", "gcp", "kubernetes", "react", "javascript", "nodejs"
}


def extract_text_from_pdf(path: str) -> str:
    """Extract plain text from a PDF file."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")
    text = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            p = page.extract_text()
            if p:
                text.append(p)
    return "\n".join(text)


def extract_basic_fields(text: str) -> dict:
    """Extract simple information from resume text."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    name = lines[0] if lines else None

    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phones = re.findall(r"(?:\+?\d[\d\-\s]{7,}\d)", text)

    # Look for date ranges like 2019 - 2024 or 2018 to 2022
    years = re.findall(r"([12]\d{3})\s*[-to]{1,3}\s*([12]\d{3}|present|now|Present|Now)", text)
    experiences = []
    if years:
        try:
            start = int(years[0][0])
            end_raw = years[0][1]
            end = 2025 if end_raw.lower() in ["present", "now"] else int(re.sub(r"\D", "", end_raw))
            experiences.append({"start": start, "end": end, "years": end - start})
        except Exception:
            pass

    # Skill detection
    text_low = text.lower()
    found_skills = sorted([s for s in SKILLS_DB if s in text_low])

    # Education extraction (simple rule-based)
    doc = nlp(text)
    educations = []
    for sent in doc.sents:
        s = sent.text.strip()
        if any(keyword in s.lower() for keyword in ["b.tech", "bachelor", "master", "ms", "b.sc", "degree", "university", "college"]):
            educations.append(s)

    return {
        "name": name,
        "emails": emails,
        "phones": phones,
        "skills": found_skills,
        "experiences": experiences,
        "education": educations,
        "raw_text": text
    }
