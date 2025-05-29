from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.core.scoring import calculate_realness_score
from app.core.mistral_prompt import ask_mistral
import json

router = APIRouter()

@router.get("/")
async def get_realness_score(resume_text: str = Query(None), profile_data: str = Query(None)):
    if not resume_text and not profile_data:
        return JSONResponse(content={"error": "Provide resume_text or profile_data"}, status_code=400)
    
    profile_data_dict = None
    if profile_data:
        try:
            # Parse the JSON string into dictionary
            profile_data_dict = json.loads(profile_data)
        except json.JSONDecodeError as e:
            return JSONResponse(content={"error": f"Invalid JSON: {str(e)}"}, status_code=400)

    # Calculate realness score using your existing logic
    score_data = calculate_realness_score(resume_text, profile_data_dict)

    # Prepare input text for Mistral reasoning
    mistral_input = "Analyze the following candidate details for authenticity:\n"
    if resume_text:
        mistral_input += f"Resume Text:\n{resume_text}\n"
    if profile_data_dict:
        mistral_input += f"Profile Data:\n{json.dumps(profile_data_dict, indent=2)}\n"

    # Get reasoning/feedback from Mistral model
    mistral_response = ask_mistral(mistral_input)

    # Return combined response
    return JSONResponse(
        content={
            "realness_score": score_data.get("score", None),
            "details": score_data,
            "mistral_reasoning": mistral_response
        }
    )
