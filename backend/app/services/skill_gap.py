def find_skill_gap(user_skills, role_skills):
    return list(set(role_skills) - set(user_skills))