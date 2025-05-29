from pydantic import BaseModel
from typing import List, Optional, Dict

class Experience(BaseModel):
    role: str
    company: str
    years: int

class Education(BaseModel):
    degree: str
    university: str
    year: int

class Profile(BaseModel):
    name: str
    experience: List[Experience]
    education: List[Education]
    skills: List[str]

class ResumeAnalysisResult(BaseModel):
    ai_likelihood_score: int
    flags: List[str]

class RealnessScoreResult(BaseModel):
    realness_score: int
    details: Optional[Dict]
