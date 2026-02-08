# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.api.routes import tasks
# from app.api.routes.auth import router as auth_router
# from app.api.routes.chat import router as chat_router
# from app.api.routes.agent_planning import router as agent_planning_router

# from app.database.init_db import create_db_and_tables
# from app.database.connection import init_db

# app = FastAPI(
#     title="The Evolution of Todo - Phase II API",
#     description="RESTful API for multi-user todo application",
#     version="2.0.0"
# )

# # CORS configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#         "https://your-app.vercel.app",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -----------------------
# # Router Registration
# # -----------------------
# app.include_router(tasks.router)
# app.include_router(auth_router)
# app.include_router(chat_router)
# app.include_router(agent_planning_router)

# # -----------------------
# # Startup Events
# # -----------------------
# @app.on_event("startup")
# async def on_startup():
#     # Initialize database tables
#     create_db_and_tables()
#     await init_db()

#     # Safety log: show all registered routes
#     for route in app.routes:
#         methods = ",".join(route.methods or [])
#         print(f"[ROUTE] {methods:<10} {route.path}")

# # -----------------------
# # Health Check
# # -----------------------
# @app.get("/health")
# async def health_check():
#     return {
#         "status": "healthy",
#         "phase": "3"
#     }

# # -----------------------
# # Root Info
# # -----------------------
# @app.get("/")
# async def root():
#     return {
#         "name": "The Evolution of Todo - Phase III",
#         "status": "running",
#         "architecture": {
#             "chat": "single unified endpoint",
#             "streaming": "request.stream flag",
#             "auth": "dependency-based",
#             "db": "initialized on startup"
#         },
#         "endpoints": {
#             "tasks": "/api/{user_id}/tasks",
#             "auth": "/api/auth/{signup|signin|logout}",
#             "chat": "/api/{user_id}/chat",
#             "conversations": "/api/{user_id}/conversations",
#             "messages": "/api/{user_id}/conversations/{conversation_id}/messages",
#             "audio": "/api/{user_id}/audio/{transcribe|speak}",
#             "agent_planning": "/api/{user_id}/chat/plan"
#         }
#     }
# # ------------------------------------------------

"""
Phase 4 - Production Ready FastAPI Main
Includes:
- Advanced features (tasks, chat, agent planning)
- Streaming + non-streaming chat
- Kafka producer/consumer
- Dapr service
- Background task scheduler
- Fully dev-ready CORS for frontend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import asyncio

from app.config import settings
from app.database.init_db import create_db_and_tables
from app.database.connection import init_db

# Routers
from app.api.routes import auth, tasks, agent_planning
from app.api.routes import streaming_chat  # Must be FIRST
from app.api.routes import chat           # Must be SECOND
from app.api.routes.task_advanced import router as advanced_tasks_router

# Services
from app.services.task_scheduler import scheduler
from app.services.kafka_consumer import get_kafka_consumer
from app.services.kafka_producer import get_kafka_producer
from app.services.dapr_service import get_dapr_service

# -----------------------
# Logging Setup
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------
# FastAPI App Setup
# -----------------------
app = FastAPI(
    title="Evolution of Todo API - Production Ready",
    description="AI-powered task manager with Kafka, Dapr, and advanced chat",
    version="2.0.0"
)

# CORS Middleware (DEV-FRIENDLY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Startup Event
# -----------------------
@app.on_event("startup")
async def on_startup():
    """Initialize DB, services, scheduler"""
    logger.info("Starting up FastAPI app...")

    # Database
    create_db_and_tables()
    await init_db()
    logger.info("Database initialized successfully.")

    # Kafka Producer
    try:
        kafka_bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        get_kafka_producer(kafka_bootstrap)
        logger.info("Kafka producer initialized.")
    except Exception as e:
        logger.warning(f"Kafka producer failed: {e}")

    # Kafka Consumer
    try:
        global kafka_consumer
        kafka_consumer = get_kafka_consumer(kafka_bootstrap)
        if kafka_consumer:
            asyncio.create_task(kafka_consumer.start_consuming())
            logger.info("Kafka consumer started.")
    except Exception as e:
        logger.warning(f"Kafka consumer failed: {e}")

    # Dapr Service
    try:
        dapr_port = int(os.getenv("DAPR_HTTP_PORT", "3500"))
        get_dapr_service(dapr_port)
        logger.info("Dapr service initialized.")
    except Exception as e:
        logger.warning(f"Dapr service failed: {e}")

    # Background Scheduler
    try:
        asyncio.create_task(scheduler.start_scheduler())
        logger.info("Background task scheduler started.")
    except Exception as e:
        logger.error(f"Scheduler failed to start: {e}")

    # Log all registered routes
    for route in app.routes:
        methods = ",".join(route.methods or [])
        logger.info(f"[ROUTE] {methods:<10} {route.path}")


# -----------------------
# Shutdown Event
# -----------------------
@app.on_event("shutdown")
async def on_shutdown():
    """Cleanup services safely"""
    logger.info("Shutting down services...")

    # Stop scheduler
    try:
        scheduler.stop_scheduler()
        logger.info("Background scheduler stopped.")
    except Exception as e:
        logger.warning(f"Scheduler stop failed: {e}")

    # Stop Kafka consumer
    try:
        if kafka_consumer:
            kafka_consumer.stop_consuming()
            logger.info("Kafka consumer stopped.")
    except Exception as e:
        logger.warning(f"Kafka consumer stop failed: {e}")


# -----------------------
# Root & Health Endpoints
# -----------------------
@app.get("/")
async def root():
    return {
        "message": "Evolution of Todo API - Production Ready",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "Advanced task management",
            "Recurring tasks",
            "Due dates and reminders",
            "Event-driven architecture with Kafka",
            "Dapr integration",
            "AI-powered chatbot"
        ]
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai_service": "configured" if settings.openrouter_api_key else "not configured",
        "kafka": "connected" if os.getenv("KAFKA_BOOTSTRAP_SERVERS") else "not configured",
        "dapr": "configured" if os.getenv("DAPR_HTTP_PORT") else "not configured",
    }


# -----------------------
# Routers Registration
# -----------------------
# Streaming chat first, then non-streaming
app.include_router(streaming_chat.router)
app.include_router(chat.router)
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(advanced_tasks_router)
app.include_router(agent_planning.router)

logger.info("All routers registered successfully.")


# -----------------------
# Uvicorn entrypoint
# -----------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
