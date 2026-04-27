from fastapi import APIRouter
from pydantic import BaseModel
from app.services.skill_gap import compare_skills
 
router = APIRouter()
 
 
class SkillGapRequest(BaseModel):
    jd_skills:     list
    resume_skills: list
 
 

@router.post("/skill-gap/compare")
def skill_gap_compare(data: SkillGapRequest):
    result = compare_skills(data.jd_skills, data.resume_skills)
    return result