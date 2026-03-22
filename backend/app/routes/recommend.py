from fastapi import APIRouter # type: ignore
from app.services.matcher import match_roles # type: ignore

router = APIRouter()

@router.post("/recommend")
def recommend(data: dict):
    skills = data.get("skills", [])
    result = match_roles(skills)
    return {"recommendations": result}