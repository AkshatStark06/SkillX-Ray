from app.services.llm_router import call_with_fallback
import json
import re
 
 
def evaluate_answer(skill: str, answer: str) -> dict:
    """
    Evaluate candidate's answer for a given skill.
    Returns score (1-5), level, and feedback.
    """
 
    prompt = f"""
    You are an expert technical interviewer.
 
    Evaluate the candidate's answer for the skill: {skill}
 
    Candidate's Answer:
    {answer}
 
    Return ONLY valid JSON in this exact format, nothing else:
    {{
        "score": <integer from 1 to 5>,
        "level": "<one of: Weak, Moderate, Strong>",
        "feedback": "<short 1-2 sentence explanation>"
    }}
    """
 
    raw_text = call_with_fallback(prompt)
    print("\n--- EVALUATION RESPONSE ---\n", raw_text)
 
    
    if not raw_text:
        print("Evaluator: LLM returned None, using fallback score.")
        return {
            "score": 3,
            "level": "Moderate",
            "feedback": "Could not evaluate — all LLMs unavailable. Defaulting to Moderate."
        }
 
    try:
        match = re.search(r"\{.*?\}", raw_text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
 
            
            score = int(data.get("score", 3))
            score = max(1, min(5, score))  # clamp to 1-5
 
            return {
                "score": score,
                "level": data.get("level", "Moderate"),
                "feedback": data.get("feedback", "No feedback provided.")
            }
        else:
            print("Evaluator: No JSON found in response.")
            return {
                "score": 3,
                "level": "Moderate",
                "feedback": "Could not parse LLM response."
            }
 
    except Exception as e:
        print("Evaluator parse error:", e)
        return {
            "score": 3,
            "level": "Moderate",
            "feedback": "Fallback evaluation due to parse error."
        }
 