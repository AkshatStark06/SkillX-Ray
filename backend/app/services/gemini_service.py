"""
gemini_service.py
LLM-based skill extractor.
Primary extraction method — uses LLM to get skills from raw text.
Falls back to rule-based extractor if LLM fails.
"""
 
import json
import re
 
from app.services.llm_router import call_with_fallback
from app.services.skill_extractor import extract_skills as rule_based_extract
 
 
def extract_skills_with_llm(text: str, source: str = "document") -> list:
    """
    Extract professional skills from raw text using LLM.
    Falls back to rule-based extraction if LLM fails.
 
    Args:
        text:   Raw text from resume or JD
        source: Label for logging ("resume" or "jd")
 
    Returns:
        List of lowercase skill strings
    """
 
    if not text or not text.strip():
        return []
 
    # Truncate to avoid token limits (first 4000 chars is plenty)
    text_chunk = text[:4000]
 
    prompt = f"""
    Extract all professional and technical skills from this {source} text.
 
    Include:
    - Programming languages
    - Frameworks and libraries
    - Tools and platforms
    - Databases
    - ML/AI techniques and concepts
    - Soft skills only if explicitly mentioned
 
    Do NOT include:
    - Company names
    - Job titles
    - Dates or years
    - Generic words like "experience" or "knowledge"
 
    Return ONLY valid JSON, nothing else:
    {{
        "skills": ["skill1", "skill2", "skill3"]
    }}
 
    Text:
    {text_chunk}
    """
 
    raw_text = call_with_fallback(prompt)
    print(f"\n--- LLM SKILL EXTRACTION ({source}) ---\n", raw_text)
 
    # ✅ Guard against None
    if not raw_text:
        print(f"LLM skill extraction failed for {source}. Using rule-based fallback.")
        return rule_based_extract(text)
 
    try:
        match = re.search(r"\{.*?\}", raw_text, re.DOTALL)
        if match:
            data   = json.loads(match.group(0))
            skills = data.get("skills", [])
 
            if not skills:
                raise ValueError("Empty skills list in LLM response")
 
            return [s.lower().strip() for s in skills if s.strip()]
 
        else:
            print(f"No JSON found in LLM response for {source}. Using rule-based fallback.")
            return rule_based_extract(text)
 
    except Exception as e:
        print(f"Skill extraction parse error ({source}):", e)
        return rule_based_extract(text)
extract_skills_with_gemini = extract_skills_with_llm