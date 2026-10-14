import os

# Dummy database settings, set BEFORE importing the app. database.py reads
# these at import time, and load_dotenv() never overrides variables that
# already exist, so the real .env credentials are never loaded here. If any
# test accidentally bypassed the override below, the production engine
# would point at a non-existent database and fail loudly.
os.environ.update(
    {
        "DB_USER": "opslens_test",
        "DB_PASSWORD": "opslens_test",
        "DB_NAME": "opslens_test_does_not_exist",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
    }
)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import Session, sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from database import Base, get_db  # noqa: E402
from main import app  # noqa: E402


@pytest.fixture
def db_session():
    """A fresh, empty in-memory SQLite database for each test."""
    engine = create_engine(
        "sqlite://",
        # TestClient runs the app in a separate thread.
        connect_args={"check_same_thread": False},
        # Keep a single connection so the in-memory database survives
        # between the test's inserts and the app's queries.
        poolclass=StaticPool,
    )
    try:
        Base.metadata.create_all(engine)
        TestSessionLocal = sessionmaker(bind=engine, autoflush=False)
        with TestSessionLocal() as session:
            yield session
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def client(db_session: Session):
    """A TestClient whose get_db dependency is routed to the test session."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
