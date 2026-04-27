from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini_service import extract_skills_with_llm
 
router = APIRouter()
 
 
class TextInput(BaseModel):
    text: str
 
 

@router.post("/skills/extract")
def extract_skills(body: TextInput):
    if not body.text or not body.text.strip():
        return {"skills": []}
    skills = extract_skills_with_llm(body.text, source="jd")
    return {"skills": skills}