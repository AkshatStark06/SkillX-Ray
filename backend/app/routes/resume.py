from fastapi import APIRouter, UploadFile, File
from app.services.resume_parser import extract_text_from_pdf
from app.services.gemini_service import extract_skills_with_llm
 
router = APIRouter()
 
 
@router.post("/resume/parse")
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported"}
 
    file_bytes = await file.read()
 
    # Extract raw text from PDF
    try:
        text = extract_text_from_pdf(file_bytes)
    except Exception as e:
        return {"error": f"Could not read PDF: {str(e)}", "skills": []}
 
    # Extract skills using LLM (falls back to rule-based if LLM fails)
    
    skills = extract_skills_with_llm(text, source="resume")
 
    return {
        "text_preview": text[:500],
        "skills": skills
    }