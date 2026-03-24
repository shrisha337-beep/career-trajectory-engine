def generate_roadmap(role, missing_skills):
    roadmap_links = {
        "Backend Developer": "https://roadmap.sh/backend",
        "Frontend Developer": "https://roadmap.sh/frontend",
        "Data Scientist": "https://roadmap.sh/data-science"
    }

    roadmap = []

    for skill in missing_skills:
        roadmap.append(f"Learn {skill}")

    # 🔥 Add external roadmap reference
    if role in roadmap_links:
        roadmap.append(f"Follow complete roadmap: {roadmap_links[role]}")

    return roadmap