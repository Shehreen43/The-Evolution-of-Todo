import os
import sys
import tempfile
from unittest.mock import patch
import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session
from app.database.connection import get_db
from app.main import app
from fastapi.testclient import TestClient
from datetime import datetime


@pytest.fixture(scope="function")
async def db_session():
    """Create a test database session with SQLite in-memory."""
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Session factory
    TestingSessionLocal = sessionmaker(
        class_=AsyncSession, autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
    )

    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()
        
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_client(db_session):
    """Create a test client with dependency overrides."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    # Mock auth dependency
    from app.api.deps import get_current_user
    from app.utils.jwt import TokenPayload
        
    def override_get_current_user():
        return TokenPayload(
            sub="test-user-123", 
            email="test@example.com",
            exp=9999999999
        )
        
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "id": "test-user-123",
        "email": "test@example.com",
        "password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # hashed 'secret'
        "name": "Test User"
    }


@pytest.fixture
def sample_task_data():
    """Sample basic task data for testing."""
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "medium"
    }


@pytest.fixture(autouse=True)
def mock_openai_client():
    """Mock OpenAI client to avoid hitting API limits during tests."""
    with patch('app.services.chat_service.get_openai_client') as mock_get_client:
        mock_client = mock_get_client.return_value
        
        # Mock chat completion response
        mock_client.chat.completions.create.return_value.choices = [
            type('obj', (object,), {
                'message': type('obj', (object,), {
                    'content': 'Mocked AI response',
                    'tool_calls': None
                })
            })
        ]
        yield mock_client
        
    # No cleanup needed as patch context manager handles it


@pytest.fixture
def sample_advanced_task_data():
    """Sample advanced task data for testing."""
    return {
        "title": "Advanced Task",
        "description": "Task with advanced features",
        "priority": "high",
        "due_date": "2024-12-31T10:00:00",
        "reminder_time": "2024-12-31T09:00:00",
        "category": "work",
        "is_recurring": True,
        "recurrence_pattern": "weekly",
        "end_recurrence": "2025-12-31T10:00:00"
    }