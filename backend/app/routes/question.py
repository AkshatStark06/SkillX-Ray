from fastapi import APIRouter
from pydantic import BaseModel
from app.services.question_generator import generate_question

router = APIRouter()


class QuestionRequest(BaseModel):
    skill: str
    level: str = "medium"


@router.post("/question")
def get_question(data: QuestionRequest):
    result = generate_question(data.skill, data.level)
    return result