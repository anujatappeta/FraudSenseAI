from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.core.scoring import calculate_realness_score
from app.core.graph_analysis import generate_trust_graph  # NEW

router = APIRouter()

class Experience(BaseModel):
    role: str
    company: str
    years: int

class Education(BaseModel):
    degree: str
    university: str
    year: int

class ProfileData(BaseModel):
    name: str
    experience: List[Experience]
    education: List[Education]
    skills: List[str]

@router.post("/score")
async def score_profile(profile: ProfileData):
    result = calculate_realness_score(profile_data=profile.dict())
    return result

# ✅ NEW: Trust Graph Endpoint
@router.post("/trust-graph")
async def get_trust_graph(profile: ProfileData):
    # For now, use placeholder verifications (replace with real checks later)
    verified_profile = {
        **profile.dict(),
        "linkedin_verified": True,              # Placeholder
        "github_verified": False,               # Placeholder
        "company_verified": True,               # Placeholder
        "certificate_verified": False           # Placeholder
    }

    graph_data = generate_trust_graph(verified_profile)
    return graph_data
