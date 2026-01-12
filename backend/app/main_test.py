from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import tasks
import os

# Create a version of the app that uses SQLite for testing
app = FastAPI(
    title="The Evolution of Todo - Phase II API (Test Mode)",
    description="RESTful API for multi-user todo application - Test Mode",
    version="2.0.0"
)

# Temporarily set environment to use SQLite for testing
if not os.getenv("TESTING"):
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_todo_for_validation.db"

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "https://your-app.vercel.app",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "phase": "2", "db_mode": "test"}

@app.get("/")
async def root():
    return {
        "name": "The Evolution of Todo - Phase II (Test Mode)",
        "status": "running",
        "db_mode": "test using SQLite",
        "endpoints": {
            "tasks": "/api/{user_id}/tasks"
        }
    }