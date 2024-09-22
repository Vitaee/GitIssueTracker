from sqlalchemy.orm import Session
from app import crud, models
from app.schemas import RepoCreate
from app.tests.util import random_lower_string
from app.tests.user import create_random_user

def create_random_repo(db: Session) -> models.Repo:
    user = create_random_user(db)
    name = random_lower_string()
    owner = random_lower_string()
    repo_in = RepoCreate(name=name, owner=owner)
    return crud.create_repo(db=db, repo=repo_in, user=user)


def create_random_repo_for_user(db: Session, user) -> models.Repo:
    name = random_lower_string()
    owner = random_lower_string()
    repo_in = RepoCreate(name=name, owner=owner)
    return crud.create_repo(db=db, repo=repo_in, user=user)