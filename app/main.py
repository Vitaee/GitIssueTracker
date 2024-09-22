from fastapi import FastAPI
from app.api.endpoints import users, repos
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter
import os, secure


env = os.getenv('ENV', 'development')

root_path="/"
redis_url = settings.REDIS_URL

if env == 'production': 
    root_path = "/issue-tracker"

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title=settings.PROJECT_NAME,  
    description="An API for tracking GitHub issues",
    version="1.0.0", root_path=root_path, lifespan=lifespan)

from app.api.endpoints import users, repos, auth

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://canilgu.dev"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
secure_headers = secure.Secure()

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response

app.include_router(auth.router,  prefix="/token", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(repos.router, prefix="/repos", tags=["repos"])



@app.get("/")
async def root():
    return {"message": "Welcome to Github Issue Tracker"}
