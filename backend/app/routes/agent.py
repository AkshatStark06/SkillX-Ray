from fastapi import APIRouter
from pydantic import BaseModel
from app.services.agent import agent_step
from typing import Optional

router = APIRouter()


class AgentRequest(BaseModel):
    skill: str
    answer: Optional[str] = None
    level: str = "medium"


@router.post("/agent")
def run_agent(data: AgentRequest):
    result = agent_step(
        skill=data.skill,
        answer=data.answer,
        level=data.level
    )
    return result