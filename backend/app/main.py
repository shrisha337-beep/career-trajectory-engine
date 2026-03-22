from fastapi import FastAPI # type: ignore
from app.routes import recommend

app = FastAPI()

app.include_router(recommend.router) # type: ignore

@app.get("/")
def home():
    return {"message": "Career Trajectory Engine Running"}