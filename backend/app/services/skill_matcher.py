def match_skills(jd_skills, resume_skills):
    matched = list(set(jd_skills) & set(resume_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    return {
        "matched": matched,
        "missing": missing
    }