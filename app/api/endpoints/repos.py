from app.core.github_client import GitHubClient
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from typing import List

from app import crud, schemas
from app.api import deps
from app.core.limiter import limiter


router = APIRouter()
github_client = GitHubClient()


@router.post("/track", response_model=schemas.Repo)
def track_repo(
    repo: schemas.RepoCreate,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user)
):
    try:
        github_repo = github_client.get_repo(repo.owner, repo.name)
    except:
        raise HTTPException(status_code=404, detail="Repository not found on GitHub")

    db_repo = crud.get_repo_by_owner_and_name(db, owner=repo.owner, name=repo.name)
    if not db_repo:
        db_repo = crud.create_repo(db=db, repo=repo, user=current_user)

    if current_user not in db_repo.users:
        db_repo.users.append(current_user)
        db.commit()
        db.refresh(db_repo)

    return db_repo


@router.delete("/untrack/{repo_id}", response_model=schemas.Repo)
def untrack_repo(
    repo_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user)
):
    db_repo = crud.get_repo(db, repo_id=repo_id)
    if db_repo is None:
        raise HTTPException(status_code=404, detail="Repo not found")
    if current_user in db_repo.users:
        db_repo.users.remove(current_user)
        db.commit()
        return db_repo
    else:
        raise HTTPException(status_code=403, detail="Not authorized to untrack this repo")


@router.get("/tracked", response_model=schemas.PaginatedRepoResponse)
@cache(expire=60)  #  60 seconds
@limiter.limit("15/minute") # 15 req per minute per ip
def read_tracked_repos(
    request: Request,
    db: Session = Depends(deps.get_db),
    limit: int = Query(10, description="Limit the number of results"),
    offset: int = Query(0, description="Offset for pagination"),
    current_user: schemas.User = Depends(deps.get_current_user)
):
    repos = crud.get_user_repos(db, user=current_user, limit=limit, offset=offset)
    return {
        "total_count": len(repos),
        "limit": limit,
        "offset": offset,
        "data": repos
    }
    


@router.get("/{repo_id}/issues", response_model=schemas.PaginatedIssueResponse)
@cache(expire=60)  #  60 seconds
def get_repo_issues(
    repo_id: int,
    db: Session = Depends(deps.get_db),
    limit: int = Query(10, description="Limit the number of results"),
    offset: int = Query(0, description="Offset for pagination"),
    current_user: schemas.User = Depends(deps.get_current_user)
):
    db_repo = crud.get_repo(db, repo_id=repo_id)
    if db_repo is None or current_user not in db_repo.users:
        raise HTTPException(status_code=404, detail="Repo not found or not authorized")
    
    try:
        github_issues = github_client.get_issues(owner=db_repo.owner, repo=db_repo.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching issues from GitHub")
    
    return {
        "total_count": len(github_issues),
        "limit": limit,
        "offset": offset,
        "data": github_issues
    }