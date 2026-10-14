from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Issue, Project, Team
from schemas import IssueRead, ProjectRead, TeamRead

app = FastAPI(
    title="OpsLens",
    description="An enterprise investigation agent",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to OpsLens!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.get("/teams", response_model=list[TeamRead])
def list_teams(db: Annotated[Session, Depends(get_db)]):
    return db.scalars(select(Team).order_by(Team.id)).all()


@app.get("/projects", response_model=list[ProjectRead])
def list_projects(db: Annotated[Session, Depends(get_db)]):
    return db.scalars(select(Project).order_by(Project.id)).all()


@app.get("/issues", response_model=list[IssueRead])
def list_issues(db: Annotated[Session, Depends(get_db)]):
    return db.scalars(select(Issue).order_by(Issue.id)).all()


@app.get("/issues/{issue_id}", response_model=IssueRead)
def get_issue(issue_id: int, db: Annotated[Session, Depends(get_db)]):
    issue = db.get(Issue, issue_id)
    if issue is None:
        raise HTTPException(
            status_code=404, detail=f"Issue {issue_id} not found"
        )
    return issue
