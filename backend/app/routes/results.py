from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.learning_plan import generate_learning_plan
 
router = APIRouter()
 
 
class ResultsRequest(BaseModel):
    # ✅ FIX: generate_learning_plan expects a list of
    # {"skill": "...", "evaluation": {"score": X, ...}} dicts
    # not just a list of missing skill strings
    results: List[dict]
 
 
@router.post("/results")
def get_results(data: ResultsRequest):
    plan = generate_learning_plan(data.results)
    return plan