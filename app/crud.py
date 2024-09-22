from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_repos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Repo).offset(skip).limit(limit).all()

def create_repo(db: Session, repo: schemas.RepoCreate, user: models.User) -> models.Repo:
    db_repo = models.Repo(name=repo.name, owner=repo.owner)
    db_repo.users.append(user) 
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)
    return db_repo

def get_repo(db: Session, repo_id: int):
    return db.query(models.Repo).filter(models.Repo.id == repo_id).first()

def delete_repo(db: Session, repo_id: int):
    db_repo = db.query(models.Repo).filter(models.Repo.id == repo_id).first()
    if db_repo:
        db.delete(db_repo)
        db.commit()
    return db_repo

def get_user_repos(db: Session, user: models.User):
    return db.query(models.Repo).filter(models.Repo.users.contains(user)).all()

def update_last_checked_repo(db: Session, repo_id: int, last_checked: datetime):
    repo = db.query(models.Repo).filter(models.Repo.id == repo_id).update({"last_checked": last_checked})
    db.commit()
    return repo

def is_user_tracking_repo(db: Session, user: models.User, repo_id: int):
    return db.query(models.Repo).filter(models.Repo.id == repo_id, models.Repo.users.contains(user)).first() is not None


def remove_user_repo(db: Session, user: models.User, repo: models.Repo):
    user.repos.remove(repo)
    db.commit()


def get_repo_by_owner_and_name(db: Session, owner: str, name: str):
    return db.query(models.Repo).filter(models.Repo.owner == owner, models.Repo.name == name).first()
