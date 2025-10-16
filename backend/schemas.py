# backend/schemas.py

from pydantic import BaseModel
from typing import List, Optional, Dict


class Experience(BaseModel):
    start: Optional[int]
    end: Optional[int]
    years: Optional[int]


class Candidate(BaseModel):
    name: Optional[str]
    emails: List[str] = []
    phones: List[str] = []
    skills: List[str] = []
    experiences: List[Experience] = []
    education: List[str] = []
    raw_text: Optional[str] = None


class JDProfile(BaseModel):
    title: Optional[str]
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    min_experience_years: Optional[int] = None
    raw_text: Optional[str] = None


class ScoreResponse(BaseModel):
    score: float
    breakdown: Dict[str, float]
    justification: str
    strengths: List[str]
    weaknesses: List[str]
