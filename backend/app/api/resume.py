from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.core.nlp_analysis import analyze_resume_text
from io import BytesIO
import pdfplumber

router = APIRouter()

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith((".txt", ".pdf")):
        raise HTTPException(status_code=400, detail="Only .txt or .pdf files supported")

    content = await file.read()
    text = ""

    # Extract text depending on file type
    if file.filename.lower().endswith(".txt"):
        try:
            text = content.decode("utf-8", errors="ignore")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error decoding text file: {str(e)}")
    elif file.filename.lower().endswith(".pdf"):
        try:
            with pdfplumber.open(BytesIO(content)) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading PDF file: {str(e)}")

    # Check if text extracted successfully
    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty or unreadable file")

    # Call NLP analysis function
    result = analyze_resume_text(text)

    return JSONResponse(content=result)
