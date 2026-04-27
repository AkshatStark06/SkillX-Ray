from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.session_manager import create_session
from app.services.agent_flow import run_agent_flow
 
router = APIRouter()
 
 
class SessionCreateRequest(BaseModel):
    skills: list
 
 
class SessionRunRequest(BaseModel):
    session_id: str
    
    answer: Optional[str] = None
 
 
@router.post("/session/start")
def start_session(data: SessionCreateRequest):
    if not data.skills:
        return {"error": "No skills provided"}
    session_id = create_session(data.skills)
    return {"session_id": session_id}
 
 
@router.post("/session/run")
def run_session(data: SessionRunRequest):
    result = run_agent_flow(
        session_id=data.session_id,
        answer=data.answer      # None on first call → generates question
    )
    return result
 