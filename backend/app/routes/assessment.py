from fastapi import APIRouter
from pydantic import BaseModel
from app.services.question_generator import generate_question
from app.services.evaluator import evaluate_answer
 
router = APIRouter()
 
 
class QuestionRequest(BaseModel):
    skill: str
    level: str = "medium"
 
 
class EvaluateRequest(BaseModel):
    skill:  str
    answer: str
 
 
# ✅ FIX: was passing a list to generate_question — function expects a single string
@router.post("/questions")
def get_question(data: QuestionRequest):
    result = generate_question(data.skill, data.level)
    return result
 
 
# ✅ FIX: was evaluate_answer(answer, skill) — wrong order
# correct signature is evaluate_answer(skill, answer)
@router.post("/evaluate")
def eval_answer(data: EvaluateRequest):
    result = evaluate_answer(data.skill, data.answer)
    return result
 