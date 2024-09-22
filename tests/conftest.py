from datetime import timedelta
import pytest,sys,os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.db.base import Base
from app.tests.user import create_random_user
from app.api.deps import create_access_token, get_db
from typing import Generator
from dotenv import load_dotenv


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(dotenv_path='.env')
    assert os.getenv("DATABASE_URL"), "DATABASE_URL not loaded from .env"


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def db() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def user_token_headers(db: Session) -> tuple:
    user = create_random_user(db)
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=timedelta(minutes=15)
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    return user, headers
