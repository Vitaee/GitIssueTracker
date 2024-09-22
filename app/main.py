from fastapi import FastAPI
from app.api.endpoints import users, repos
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

from app.api.endpoints import users, repos, auth

app.include_router(auth.router,  prefix="/token", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(repos.router, prefix="/repos", tags=["repos"])


@app.get("/")
async def root():
    return {"message": "Welcome to Github Issue Tracker"}