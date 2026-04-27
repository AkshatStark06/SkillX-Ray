from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.learning_plan import generate_learning_plan
 
router = APIRouter()
 
 
class ResultsRequest(BaseModel):
    
    results: List[dict]
 
 
@router.post("/results")
def get_results(data: ResultsRequest):
    plan = generate_learning_plan(data.results)
    return plan