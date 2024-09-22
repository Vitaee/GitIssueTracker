from sqlalchemy import Table, Column, Integer, DateTime, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


# M2M
user_repo_association = Table(
    'user_repo_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('repo_id', Integer, ForeignKey('repos.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    repos = relationship("Repo", secondary=user_repo_association, back_populates="users")


class Repo(Base):
    __tablename__ = "repos"
    __table_args__ = (UniqueConstraint('owner', 'name', name='_owner_name_uc'),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner = Column(String, index=True)
    last_checked = Column(DateTime, nullable=True)
    
    users = relationship("User", secondary=user_repo_association, back_populates="repos")
    
    issues = relationship("Issue", back_populates="repo")


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    github_issue_id = Column(Integer, index=True)
    title = Column(String)
    body = Column(String)
    state = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    repo_id = Column(Integer, ForeignKey("repos.id"))

    repo = relationship("Repo", back_populates="issues")