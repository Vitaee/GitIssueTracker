from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.api import deps
from app.core.email_sender import send_email
from app.core.security import get_password_hash


router = APIRouter()

@router.post("/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)

@router.get("/me", response_model=schemas.User)
def read_user_me(current_user: schemas.User = Depends(deps.get_current_user)):
    return current_user

@router.get("/me/repos", response_model=List[schemas.Repo])
def read_my_tracked_repos(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user)
):
    repos = crud.get_user_repos(db, user=current_user)
    return repos