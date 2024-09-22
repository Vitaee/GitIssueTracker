from sqlalchemy.orm import Session
from app import crud, models
from app.schemas import UserCreate
from app.tests.util import random_email, random_lower_string
from app.core.security import get_password_hash


def create_random_user(db: Session, email: str = None, password: str = None) -> models.User:
    email = email or random_email()
    password = password or random_lower_string()
    user_in = UserCreate(email=email, password=password)
    hashed_password = get_password_hash(user_in.password)
    return crud.create_user(db=db, user=user_in, hashed_password=hashed_password)