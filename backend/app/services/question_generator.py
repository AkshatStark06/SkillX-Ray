import json
import re
from app.services.llm_router import call_with_fallback
 
 
def generate_question(skill: str, level: str = "medium") -> dict:
    """
    Generate one interview question for a given skill and difficulty level.
    Returns {"question": "..."}
    """
 
    prompt = f"""
    You are an expert technical interviewer for data and AI roles.
 
    Generate ONE interview question for the skill: {skill}
 
    Rules:
    - Prefer conceptual or scenario-based questions
    - Focus on explanation and real understanding
    - Avoid long coding tasks — at most 1-2 lines if code is needed
 
    Difficulty guidance:
    - easy   → basic concept or definition
    - medium → scenario-based, how/why questions
    - hard   → deep explanation, edge cases, trade-offs
 
    Difficulty level: {level}
 
    Return ONLY valid JSON, nothing else:
    {{
        "question": "<your question here>"
    }}
    """
 
    raw_text = call_with_fallback(prompt)
    print("\n--- QUESTION RESPONSE ---\n", raw_text)
 
    # ✅ CRITICAL FIX: Guard against None before regex
    if not raw_text:
        print("QuestionGenerator: LLM returned None, using fallback question.")
        return {
            "question": f"Can you explain how you have used {skill} in a real project or scenario?"
        }
 
    try:
        match = re.search(r"\{.*?\}", raw_text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            question = data.get("question", "").strip()
 
            if not question:
                raise ValueError("Empty question in response")
 
            return {"question": question}
        else:
            print("QuestionGenerator: No JSON found in response.")
            return {
                "question": f"Explain the core concept of {skill} and give a practical example."
            }
 
    except Exception as e:
        print("QuestionGenerator parse error:", e)
        return {
            "question": f"Describe how {skill} works and when you would use it."
        }
 