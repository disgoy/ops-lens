
from fastapi import FastAPI

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
