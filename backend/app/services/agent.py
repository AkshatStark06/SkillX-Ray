from app.services.question_generator import generate_question
from app.services.evaluator import evaluate_answer
 
 
def agent_step(skill: str, answer: str = None) -> dict:
    """
    One step of the assessment agent.
    - answer is None  → generate and return a question
    - answer provided → evaluate and decide next action
    """
 
    # ── Step 1: No answer yet → ask first question ──
    if answer is None:
        question_data = generate_question(skill, level="medium")
        return {
            "action":   "ask",
            "skill":    skill,
            "question": question_data.get("question", f"Tell me about your experience with {skill}.")
        }
 
    # ── Step 2: Evaluate the candidate's answer ──
    evaluation = evaluate_answer(skill, answer)
    score      = evaluation.get("score", 3)
 
    # ── Step 3: Decide next action based on score ──
    if score <= 2:
        # Weak answer → easy follow-up to give candidate a chance
        followup = generate_question(skill, level="easy")
        return {
            "action":       "follow_up",
            "message":      "Let's revisit the basics.",
            "question":     followup.get("question", f"Can you explain {skill} in simple terms?"),
            "evaluation":   evaluation
        }
 
    elif score == 3:
        # Moderate answer → push slightly deeper
        followup = generate_question(skill, level="medium")
        return {
            "action":       "follow_up",
            "message":      "Good start — let's go a bit deeper.",
            "question":     followup.get("question", f"Give a real-world scenario where you applied {skill}."),
            "evaluation":   evaluation
        }
 
    else:
        # Score 4 or 5 → strong answer, move on
        return {
            "action":     "next_skill",
            "message":    "Great answer! Moving to the next skill.",
            "evaluation": evaluation
        }
 