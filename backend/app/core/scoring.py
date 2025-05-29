from typing import Optional, Dict, Any, List
from difflib import get_close_matches

# Constants for score weighting
MAX_AI_SCORE = 50
MAX_EXPERIENCE_SCORE = 30
MAX_EDUCATION_SCORE = 15
MAX_SKILL_SCORE = 20

# Trusted universities for education scoring (can be extended)
TRUSTED_UNIVERSITIES = ["IIT", "NIT", "BITS", "IIIT", "VRSEC"]

# Required skills for skill scoring (can be extended or loaded dynamically)
REQUIRED_SKILLS = {
    "python", "fastapi", "machine learning", "ml", "docker", "cloud",
    "sql", "git", "javascript", "react", "node.js", "java", "c++",
    "kubernetes", "aws", "azure", "tensorflow", "pytorch"
}

def fuzzy_skill_match(user_skills: List[str], required_skills: List[str], cutoff=0.8) -> List[str]:
    """
    Returns list of matched skills using fuzzy matching to handle typos and variants.
    """
    matched = set()
    for skill in user_skills:
        close = get_close_matches(skill, required_skills, n=1, cutoff=cutoff)
        if close:
            matched.add(close[0])
    return list(matched)

def calculate_realness_score(
    resume_text: Optional[str] = None,
    profile_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Calculate a realistic and balanced Realness Score based on:
    - AI-generated content likelihood from resume text (max 50)
    - Professional experience (max 30)
    - Education quality (max 15)
    - Skills match with fuzzy matching (max 20)

    Args:
        resume_text (str): Text extracted from resume for NLP analysis.
        profile_data (dict): Structured profile data including experience, education, skills.

    Returns:
        dict: Contains 'realness_score' (0-100) and 'details' explaining sub-scores.
    """
    score = 0
    details = {}

    # ----- Resume NLP Analysis -----
    if resume_text:
        from app.core.nlp_analysis import analyze_resume_text
        ai_result = analyze_resume_text(resume_text)

        ai_score_raw = ai_result.get("ai_likelihood_score", 0)
        # Higher AI likelihood means less real, invert it
        ai_score = (100 - ai_score_raw) * (MAX_AI_SCORE / 100)
        score += ai_score

        details["resume_ai_likelihood"] = round(ai_score_raw, 2)
        details["resume_ai_score"] = round(ai_score, 2)
        details["resume_flags"] = ai_result.get("flags", [])

    # ----- Profile Analysis -----
    if profile_data:
        # Experience scoring: smooth scaling rather than steps
        experience_years = sum(exp.get("years", 0) for exp in profile_data.get("experience", []))
        # Scale experience: 0 years -> 10% of max, 10+ years -> max score linearly
        experience_score = min(MAX_EXPERIENCE_SCORE, max(MAX_EXPERIENCE_SCORE * 0.1, (experience_years / 10) * MAX_EXPERIENCE_SCORE))
        score += experience_score

        details["experience_years"] = experience_years
        details["experience_score"] = round(experience_score, 2)

        # Education scoring: weight universities and degree levels
        education_score = 0
        for edu in profile_data.get("education", []):
            university = edu.get("university", "").upper()
            degree = edu.get("degree", "").lower()

            # University score
            uni_score = 10 if any(trusted in university for trusted in TRUSTED_UNIVERSITIES) else 5

            # Degree bonus: PhD > Masters > Bachelors > Diploma/Other
            if "phd" in degree or "doctor" in degree:
                degree_score = 5
            elif "master" in degree or "msc" in degree or "m.tech" in degree:
                degree_score = 3
            elif "bachelor" in degree or "bsc" in degree or "b.tech" in degree:
                degree_score = 2
            else:
                degree_score = 1

            education_score += (uni_score + degree_score)

        education_score = min(education_score, MAX_EDUCATION_SCORE)
        score += education_score
        details["education_score"] = round(education_score, 2)

        # Skills matching with fuzzy matching
        user_skills = [s.lower() for s in profile_data.get("skills", [])]
        matched_skills = fuzzy_skill_match(user_skills, list(REQUIRED_SKILLS))
        skill_score = min(len(matched_skills) * 4, MAX_SKILL_SCORE)  # 4 points per matched skill

        score += skill_score
        details["matched_skills"] = matched_skills
        details["skill_score"] = round(skill_score, 2)

    # ----- Final Score capped at 100 -----
    final_score = min(round(score, 2), 100)

    return {
        "realness_score": final_score,
        "details": details
    }
