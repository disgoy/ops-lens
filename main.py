from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Team
from schemas import TeamRead

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
