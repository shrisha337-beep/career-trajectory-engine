import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def match_roles(user_skills):
    with open("data/roles.json") as f:
        roles = json.load(f)

    role_texts = [" ".join(role["skills"]) for role in roles]
    user_text = " ".join(user_skills)

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(role_texts + [user_text])

    similarity = cosine_similarity(vectors[-1], vectors[:-1])[0] # type: ignore

    results = []
    for i, score in enumerate(similarity):
        results.append({
            "role": roles[i]["role"],
            "score": float(score),
            "skills": roles[i]["skills"]
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)