from fastapi import APIRouter
from pydantic import BaseModel
from app.services.evaluator import evaluate_answer

router = APIRouter()


class EvaluationRequest(BaseModel):
    skill: str
    answer: str


@router.post("/evaluate")
def evaluate(data: EvaluationRequest):
    result = evaluate_answer(data.skill, data.answer)
    return result