from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import tasks
from app.api.routes.auth import router as auth_router
from app.database.init_db import create_db_and_tables
from app.database.connection import init_db
import asyncio

app = FastAPI(
    title="The Evolution of Todo - Phase II API",
    description="RESTful API for multi-user todo application",
    version="2.0.0"
)

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
app.include_router(auth_router)

@app.on_event("startup")
async def on_startup():
    """Initialize database tables when the application starts."""
    # Create database tables synchronously
    create_db_and_tables()
    # Optionally, also initialize async tables
    await init_db()

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "phase": "2"}

@app.get("/")
async def root():
    return {
        "name": "The Evolution of Todo - Phase II",
        "status": "running",
        "endpoints": {
            "tasks": "/api/{user_id}/tasks",
            "auth": "/api/auth/{signup|signin|logout}"
        }
    }
