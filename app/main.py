from fastapi import FastAPI
from app.api.endpoints import users, repos
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
import os


env = os.getenv('ENV', 'development')

root_path="/"

if env == 'production': root_path = "/issue-tracker"

app = FastAPI(title=settings.PROJECT_NAME,  
    description="An API for tracking GitHub issues",
    version="1.0.0", root_path=root_path)

from app.api.endpoints import users, repos, auth

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://canilgu.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,  prefix="/token", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(repos.router, prefix="/repos", tags=["repos"])


@app.get("/")
async def root():
    return {"message": "Welcome to Github Issue Tracker"}
