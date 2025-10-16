# backend/scorer.py

import os
from typing import Dict, Any
from .schemas import Candidate, JDProfile

OPENAI_ENABLED = False
try:
    import openai
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key:
        OPENAI_ENABLED = True
except Exception:
    OPENAI_ENABLED = False


def simple_skill_match(candidate_skills, jd_required, jd_preferred):
    candidate_set = set(s.lower() for s in candidate_skills)
    required = set(s.lower() for s in jd_required)
    preferred = set(s.lower() for s in jd_preferred)

    required_matches = len(candidate_set & required)
    required_total = max(1, len(required))
    required_score = required_matches / required_total

    preferred_matches = len(candidate_set & preferred)
    preferred_total = max(1, len(preferred))
    preferred_score = preferred_matches / preferred_total

    return required_score, preferred_score


def experience_score(candidate, min_years):
    total_years = 0
    for e in candidate.get("experiences", []):
        if e and isinstance(e.get("years"), (int, float)):
            total_years += e.get("years", 0)
    if not total_years:
        total_years = 0
    if not min_years:
        return 1.0
    return min(1.0, total_years / float(min_years))


def compute_score(candidate: Dict[str, Any], jd: Dict[str, Any]):
    w_skills = 0.5
    w_experience = 0.2
    w_education = 0.1
    w_semantic = 0.2

    req_score, pref_score = simple_skill_match(
        candidate.get("skills", []),
        jd.get("required_skills", []),
        jd.get("preferred_skills", [])
    )
    skill_component = (req_score * 0.8 + pref_score * 0.2)
    exp_component = experience_score(candidate, jd.get("min_experience_years", 0))
    edu_component = 1.0 if candidate.get("education") else 0.5
    semantic_component = 0.5
    justification = "Rule-based scoring used."
    strengths, weaknesses = [], []

    if OPENAI_ENABLED:
        try:
            prompt = (
                "Given a candidate and job description, return JSON with keys: "
                "semantic_score(0-1), justification(short), strengths[], weaknesses[]."
                f"\nCandidate:\n{candidate}\nJD:\n{jd}"
            )
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=300
            )
            import json
            data = json.loads(response.choices[0].message.content)
            semantic_component = float(data.get("semantic_score", 0.5))
            justification = data.get("justification", justification)
            strengths = data.get("strengths", [])
            weaknesses = data.get("weaknesses", [])
        except Exception as e:
            justification = f"LLM scoring unavailable: {e}"

    total = (
        w_skills * skill_component +
        w_experience * exp_component +
        w_education * edu_component +
        w_semantic * semantic_component
    )

    score_0_10 = round(total * 10, 1)
    breakdown = {
        "skills": round(skill_component * 10, 2),
        "experience": round(exp_component * 10, 2),
        "education": round(edu_component * 10, 2),
        "semantic": round(semantic_component * 10, 2)
    }

    if not strengths:
        if skill_component > 0.7:
            strengths.append("Good skill match")
        if exp_component >= 1.0:
            strengths.append("Meets experience")
    if not weaknesses:
        if skill_component < 0.6:
            weaknesses.append("Missing key required skills")
        if exp_component < 1.0:
            weaknesses.append("Less experience than required")

    return {
        "score": score_0_10,
        "breakdown": breakdown,
        "justification": justification,
        "strengths": strengths,
        "weaknesses": weaknesses
    }
