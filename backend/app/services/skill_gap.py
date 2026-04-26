"""
skill_gap.py
Single source of truth for skill comparison logic.
Replaces the duplicate skill_matcher.py — delete skill_matcher.py.
"""
 
 
def compare_skills(jd_skills: list, resume_skills: list) -> dict:
    """
    Compare JD-required skills vs candidate's resume skills.
 
    Returns:
    - core_skills:    in both JD and resume (assess these for depth)
    - jd_only_skills: in JD but NOT resume (true gaps)
    - resume_only:    in resume but NOT JD (irrelevant to this role)
    """
 
    jd_set     = set(s.lower().strip() for s in jd_skills)
    resume_set = set(s.lower().strip() for s in resume_skills)
 
    core_skills    = sorted(jd_set & resume_set)      # ✅ claimed + required
    jd_only_skills = sorted(jd_set - resume_set)      # ❌ required but missing
    resume_only    = sorted(resume_set - jd_set)       # ignored for this role
 
    return {
        "core_skills":    core_skills,
        "jd_only_skills": jd_only_skills,
        "resume_only":    resume_only,
 
        # Legacy keys kept for backward compatibility with any existing route code
        "matched_skills": core_skills,
        "missing_skills": jd_only_skills,
        "extra_skills":   resume_only,
    }