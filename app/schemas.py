from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(UserBase):
    id: int
    repos: List['Repo'] = []

    # Updated to use ConfigDict
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class User(UserBase):
    id: int

    # Updated to use ConfigDict
    model_config = ConfigDict(from_attributes=True)

class RepoBase(BaseModel):
    name: str
    owner: str

class RepoCreate(RepoBase):
    pass

class Repo(RepoBase):
    id: int
    users: List[User] = []

    # Updated to use ConfigDict
    model_config = ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    email: Optional[str] = None

class IssueUser(BaseModel):
    login: str
    id: int
    avatar_url: str

class IssueBase(BaseModel):
    number: int
    title: str
    state: str
    created_at: datetime
    updated_at: datetime
    body: Optional[str] = None
    user: IssueUser
    html_url: str
    comments: int

class IssueCreate(IssueBase):
    github_issue_id: int

class Issue(IssueBase):
    id: int
    github_issue_id: int
    repo_id: int

    # Updated to use ConfigDict
    model_config = ConfigDict(from_attributes=True)
