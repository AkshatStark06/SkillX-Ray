from app.services.llm_router import call_with_fallback
import json
import re
 
 
# Hardcoded fallback resources per skill category (0-cost, always works)
FALLBACK_RESOURCES = {
    "python":           ["https://docs.python.org/3/tutorial/", "https://www.youtube.com/watch?v=rfscVS0vtbw"],
    "sql":              ["https://sqlzoo.net/", "https://www.youtube.com/watch?v=HXV3zeQKqGY"],
    "machine learning": ["https://www.coursera.org/learn/machine-learning (audit free)", "https://youtube.com/watch?v=GwIo3gDZCVQ"],
    "deep learning":    ["https://www.deeplearning.ai/courses/ (audit free)", "https://youtube.com/watch?v=aircAruvnKk"],
    "data analysis":    ["https://www.kaggle.com/learn/pandas", "https://youtube.com/watch?v=vmEHCJofslg"],
    "nlp":              ["https://huggingface.co/learn/nlp-course/", "https://youtube.com/watch?v=8rXD5-xhemo"],
    "statistics":       ["https://www.khanacademy.org/math/statistics-probability", "https://youtube.com/watch?v=xxpc-HPKN28"],
}
 
DEFAULT_RESOURCES = ["https://www.youtube.com/results?search_query={skill}+tutorial", "https://www.freecodecamp.org/"]
DEFAULT_TIME      = "2-3 weeks"
 
 
def _get_fallback_plan(weak_skills: list) -> dict:
    """Generate a basic learning plan without LLM."""
    plan = []
    for skill in weak_skills:
        key = skill.lower()
        resources = FALLBACK_RESOURCES.get(key, [r.format(skill=skill) for r in DEFAULT_RESOURCES])
        plan.append({
            "skill":         skill,
            "topics":        f"Core concepts and practical application of {skill}",
            "resources":     resources,
            "time_estimate": DEFAULT_TIME
        })
    return {"plan": plan}
 
 
def generate_learning_plan(results: list) -> dict:
    """
    Generate personalized learning plan from assessment results.
    Skills scoring < 4 are treated as weak and included in the plan.
    """
 
    if not results:
        return {
            "strong_skills": [],
            "weak_skills":   [],
            "plan":          [],
            "message":       "No assessment results provided."
        }
 
    weak_skills   = []
    strong_skills = []
 
    for item in results:
        skill = item.get("skill", "unknown")
        # ✅ Safe access — evaluation might be a fallback dict
        score = item.get("evaluation", {}).get("score", 3)
 
        if score < 4:
            weak_skills.append(skill)
        else:
            strong_skills.append(skill)
 
    # No weak skills → candidate is strong across the board
    if not weak_skills:
        return {
            "strong_skills": strong_skills,
            "weak_skills":   [],
            "plan":          [],
            "message":       "No major gaps found. You are strong in all assessed skills."
        }
 
    prompt = f"""
    You are a career mentor helping a candidate improve their skills.
 
    The candidate is weak in these skills: {weak_skills}
 
    Create a structured personalized learning plan.
    For each skill provide:
    - Key topics to study
    - 2-3 free online resources (YouTube, official docs, free courses)
    - Realistic time estimate to reach competency
 
    Return ONLY valid JSON, nothing else:
    {{
      "plan": [
        {{
          "skill": "<skill name>",
          "topics": "<what exactly to learn>",
          "resources": ["<url or resource name>", "<url or resource name>"],
          "time_estimate": "<e.g. 2-3 weeks>"
        }}
      ]
    }}
    """
 
    try:
        raw_text = call_with_fallback(prompt)
 
        # ✅ CRITICAL FIX: Guard against None before regex
        if not raw_text:
            print("LearningPlan: LLM returned None, using hardcoded fallback.")
            result = _get_fallback_plan(weak_skills)
        else:
            match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if match:
                result = json.loads(match.group(0))
            else:
                print("LearningPlan: No JSON found, using hardcoded fallback.")
                result = _get_fallback_plan(weak_skills)
 
    except Exception as e:
        print("LearningPlan failed:", e)
        result = _get_fallback_plan(weak_skills)
 
    # ✅ Always attach strong/weak summary alongside the plan
    result["strong_skills"] = strong_skills
    result["weak_skills"]   = weak_skills
 
    return result
 