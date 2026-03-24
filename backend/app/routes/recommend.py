from fastapi import APIRouter
from app.services.matcher import match_roles
from app.services.skill_gap import find_skill_gap
from app.services.roadmap import generate_roadmap

router = APIRouter()

def extract_skills_from_text(text):
    if isinstance(text, list):
        text = " ".join(text)
    return text.lower().split()

def interpret_score(score):
    if score > 0.75:
        return "Strong match"
    elif score > 0.5:
        return "Moderate match"
    else:
        return "Low match"

def confidence_level(score):
    if score > 0.75:
        return "High"
    elif score > 0.5:
        return "Medium"
    else:
        return "Low"
    
def get_job_links(role, user_skills):
    stopwords = {"and", "or", "the", "a", "an", "with", "in", "on", "for", "to", "of", "by", "as", "at", "from", "is", "are", "was", "were", "be", "been", "being", "want", "need", "looking", "seeking", "experience", "skills", "knowledge", "proficient", "familiar", "expertise"}
    clean_skills = [s for s in user_skills if len(s) > 2][:3]
    
    role_query = f"{role} {' '.join(user_skills[:3])}"  # add top 3 skills to query
    role_query = role.replace(" ", "20%")
    
    return {
        "linkedin": f"https://www.linkedin.com/jobs/search/?keywords={role_query}",
        "indeed": f"https://www.indeed.com/jobs?q={role_query}",
        "glassdoor": f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={role_query}"
    } 
    
def get_progression(role):
    progression_map = {
        "Backend Developer": ["Senior Backend Developer", "System Architect"],
        "Frontend Developer": ["Senior Frontend Developer", "UI Architect"],
        "Data Scientist": ["Senior Data Scientist", "ML Engineer"],
        "Product Manager": ["Senior Product Manager", "Head of Product"],
        "UX Designer": ["Senior UX Designer", "Design Lead"],
        "DevOps Engineer": ["Senior DevOps Engineer", "Cloud Architect"],
        "Mobile Developer": ["Senior Mobile Developer", "Mobile Architect"],
        "QA Engineer": ["Senior QA Engineer", "Test Architect"],
        "Data Engineer": ["Senior Data Engineer", "Data Architect"],
        "Cybersecurity Analyst": ["Senior Cybersecurity Analyst", "Security Architect"]
    }       
    return progression_map.get(role, [])

def estimate_time(missing_skills):
    return f"{len(missing_skills) * 2}-{len(missing_skills) * 4} weeks"

def get_role_description(role):
    descriptions = {
        "Backend Developer": "Builds and maintains the server-side logic, databases, and APIs for web applications.",
        "Frontend Developer": "Creates the user interface and user experience of web applications using HTML, CSS, and JavaScript.",
        "Data Scientist": "Analyzes complex data to extract insights and build predictive models using machine learning.",
        "Product Manager": "Oversees the development and success of a product by coordinating between teams and stakeholders.",
        "UX Designer": "Designs intuitive and engaging user experiences for digital products through research and prototyping.",
        "DevOps Engineer": "Manages infrastructure, deployment pipelines, and ensures reliability of applications in production.",
        "Mobile Developer": "Develops applications for mobile devices using platforms like iOS and Android.",
        "QA Engineer": "Tests software to identify bugs and ensure quality before release.",
        "Data Engineer": "Builds and maintains data pipelines to support analytics and machine learning workloads.",
        "Cybersecurity Analyst": "Protects an organization's systems and data from cyber threats through monitoring and response."
    }
    return descriptions.get(role, "No description available")

@router.post("/recommend")
def recommend(data: dict):
    user_text = data.get("text", "")
    user_skills = data.get("skills", [])

    # 🔥 Option B logic
    if user_text:
        extracted = extract_skills_from_text(user_text)
        user_skills.extend(extracted)
        
    user_skills = list(set([skill.lower() for skill in user_skills]))    

    if not user_skills:
        return {"error": "No skills provided"}

    matched_roles = match_roles(user_skills)
    THRESHOLD = 0.5
    filtered_roles = [r for r in matched_roles if r["score"] >= THRESHOLD]
    
    if not filtered_roles:
        filtered_roles = matched_roles[:1] # at least give the best match

    final_results = []

    for role in filtered_roles[:3]:  # top 3 only
        missing = find_skill_gap(user_skills, role["skills"])
        roadmap = generate_roadmap(role["role"], missing) # type: ignore
        common_skills = list(set(user_skills) & set(role["skills"]))
        common_skills = [s for s in common_skills if len(s) > 2]
        final_results.append({
            "role": role["role"],
            "match_score": role["score"],
            "match_level": interpret_score(role["score"]),
            "confidence": confidence_level(role["score"]),
            "reason": f"based on overlap of {len(common_skills)} skills: {common_skills}",
            "missing_skills": missing,
            "roadmap": roadmap,
            "job_links": get_job_links(role["role"], user_skills[:3]),
            "career_path": get_progression(role["role"]),
            "estimated_time": estimate_time(missing),
            "description": get_role_description(role["role"])
        })

    return {"results": final_results}