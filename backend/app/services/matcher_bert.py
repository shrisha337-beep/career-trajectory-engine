import json
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.embeddings import get_embedding
import numpy as np

def match_roles_bert(user_skills):
    with open("data/roles.json") as f:
        roles = json.load(f)

    user_text = " ".join(user_skills)
    user_vec = get_embedding(user_text)

    results = []

    for role in roles:
        role_text = " ".join(role["skills"])
        role_vec = get_embedding(role_text)

        score = cosine_similarity(
    np.array(user_vec).reshape(1, -1),
    np.array(role_vec).reshape(1, -1)
)[0][0]
        
        results.append({
            "role": role["role"],
            "score": float(score),
            "skills": role["skills"]
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)