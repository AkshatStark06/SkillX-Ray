from app.services.agent import agent_step
from app.services.session_manager import get_session, update_session
from app.services.learning_plan import generate_learning_plan
 
 
MAX_FOLLOWUPS = 2
 
 
def run_agent_flow(session_id: str, answer: str = None) -> dict:
    """
    Main agent loop.
    - If answer is None  → return first question for current skill
    - If answer provided → evaluate, decide follow-up or move to next skill
    - If all skills done → generate final learning plan
    """
 
    session = get_session(session_id)
 
    if not session:
        return {"error": "Invalid session ID"}
 
    skills = session["skills"]
    index  = session["current_index"]
 
    
    if index >= len(skills):
        final_analysis = generate_learning_plan(session["results"])
        return {
            "action":   "complete",
            "message":  "Assessment complete.",
            "results":  session["results"],
            "analysis": final_analysis
        }
 
    current_skill = skills[index]
 
    # Run one agent step
    result = agent_step(current_skill, answer)
 
    # ========================
    # FOLLOW-UP CONTROL LOGIC
    # ========================
 
    if result["action"] == "follow_up":
        session["followup_count"] = session.get("followup_count", 0) + 1
    else:
        session["followup_count"] = 0
 
    # Cap follow-ups at MAX_FOLLOWUPS
    if session["followup_count"] >= MAX_FOLLOWUPS:
        result["action"]  = "next_skill"
        result["message"] = "Moving to next skill (follow-up limit reached)."
 
        
        if "evaluation" not in result:
            result["evaluation"] = {
                "score":    3,
                "level":    "Moderate",
                "feedback": "Follow-up limit reached — defaulting to Moderate."
            }
 
    
 
    if result["action"] == "next_skill":
        evaluation = result.get("evaluation", {
            "score":    3,
            "level":    "Moderate",
            "feedback": "No evaluation available."
        })
 
        session["results"].append({
            "skill":      current_skill,
            "evaluation": evaluation
        })
 
        session["current_index"]  += 1
        session["followup_count"]  = 0
        update_session(session_id, session)
 
        
        return run_agent_flow(session_id, answer=None)
 
   
    
 
    update_session(session_id, session)
    return result