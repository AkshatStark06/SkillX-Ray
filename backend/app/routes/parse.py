from fastapi import APIRouter, UploadFile, File
from app.services.resume_parser import extract_text_from_pdf
 
router = APIRouter()
 
 
@router.post("/parse/resume")
async def parse_resume_text(file: UploadFile = File(...)):
    file_bytes = await file.read()
    try:
        text = extract_text_from_pdf(file_bytes)
        return {"text": text[:2000]}
    except Exception as e:
        return {"error": str(e), "text": ""}
 