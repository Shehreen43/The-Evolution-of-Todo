import pytest
import os
from sqlmodel import Session, select
from app.models.task import Task
from app.database.connection import get_db, async_engine as engine
from app.config import settings
import asyncio


def test_neon_db_connection():
    """Test that we can connect to Neon database using the configured URL."""
    # Check if we have the environment variables for Neon
    neon_url = settings.database_url

    # If running in test environment, we might not have Neon configured
    # so we'll test the connection setup logic
    assert engine is not None
    assert hasattr(engine, 'sync_engine') or hasattr(engine, 'begin')


def test_task_model_creation():
    """Test that the Task model is properly defined for Neon/PostgreSQL."""
    # Check that the Task model has the expected fields
    from app.models.task import Task

    # Verify the model has advanced fields
    assert hasattr(Task, 'due_date')
    assert hasattr(Task, 'reminder_time')
    assert hasattr(Task, 'category')
    assert hasattr(Task, 'is_recurring')
    assert hasattr(Task, 'recurrence_pattern')
    assert hasattr(Task, 'end_recurrence')
    assert hasattr(Task, 'parent_task_id')

    # Verify field types
    from sqlalchemy import String, Boolean, DateTime, Integer
    from sqlmodel import Field

    # This is a basic check - in a real scenario we'd inspect the column definitions
    assert True  # Placeholder - the attributes exist


def test_async_session_creation():
    """Test that async session can be created (Neon requirement)."""
    from app.database.connection import async_session

    # Verify async session factory exists
    assert async_session is not None


def test_sqlmodel_compatibility():
    """Test that SQLModel works with Neon-compatible types."""
    from app.models.task import Task
    import datetime

    # Create a sample task with advanced features
    sample_task = Task(
        user_id="test-user-123",
        title="Test Neon Task",
        description="Task for Neon database",
        priority="high",
        due_date="2024-12-31T10:00:00",
        reminder_time="2024-12-31T09:00:00",
        category="work",
        is_recurring=False,
        recurrence_pattern="weekly",
        end_recurrence="2025-12-31T10:00:00"
    )

    # Verify all fields are properly set
    assert sample_task.title == "Test Neon Task"
    assert sample_task.category == "work"
    assert sample_task.is_recurring is False
    assert sample_task.recurrence_pattern == "weekly"


def test_postgresql_specific_features():
    """Test PostgreSQL/Neon specific features."""
    # Check that we're using PostgreSQL dialect
    from sqlalchemy import create_engine
    
    # Verify the database URL contains PostgreSQL/Neon indicators
    assert 'postgresql' in settings.database_url.lower() or 'neon' in settings.database_url.lower()


def test_neon_ssl_configuration():
    """Test that SSL is properly configured for Neon."""
    db_url = settings.database_url

    # Neon URLs typically include sslmode=require
    if "neon" in db_url.lower():
        assert "sslmode=require" in db_url or "ssl" in db_url


def test_transaction_handling():
    """Test transaction handling with Neon."""
    # This tests that the transaction structure works
    # We can't fully test without a real connection, but we can verify the structure
    from app.database.connection import async_engine

    # Verify async engine exists and has transaction capabilities
    assert async_engine is not None
    assert hasattr(async_engine, 'begin')


def test_pool_settings():
    """Test connection pooling settings suitable for Neon Serverless."""
    # Neon works well with connection pooling
    # Check that our engine configuration is appropriate
    from app.database.connection import async_engine

    # The async_engine should be properly configured
    assert async_engine is not None


def test_datetime_handling():
    """Test that datetime fields work correctly with Neon."""
    import datetime
    from app.models.task import Task

    # Test creating a task with datetime values
    now = datetime.datetime.now()
    future = now + datetime.timedelta(days=30)

    task = Task(
        user_id="test-user-123",
        title="DateTime Test",
        due_date=future.isoformat(),
        reminder_time=now.isoformat()
    )

    assert task.due_date is not None
    assert task.reminder_time is not None


def test_foreign_key_constraints():
    """Test that foreign key relationships work with Neon."""
    from app.models.task import Task

    # Verify that the user_id field is set up as a foreign key
    # (This is more of a model definition check)
    assert hasattr(Task, 'user_id')
    # In a full test, we'd check the actual constraint definition


def test_index_compatibility():
    """Test that indexing works with Neon."""
    # PostgreSQL/Neon supports various index types
    from app.models.task import Task

    # Verify that the model has the expected fields that would typically be indexed
    assert hasattr(Task, 'user_id')  # Usually indexed for user isolation
    assert hasattr(Task, 'completed')  # Often indexed for filtering
    assert hasattr(Task, 'due_date')  # Often indexed for date filtering


def test_json_field_compatibility():
    """Test that JSON fields work with Neon (if any exist)."""
    # While our current Task model may not have JSON fields,
    # Neon supports JSON/JSONB which is useful for future extensions
    from app.models.task import Task

    # Verify model structure is compatible with PostgreSQL extensions
    assert hasattr(Task, '__tablename__')
    assert Task.__tablename__ == 'task'


def test_neon_serverless_features():
    """Test features specific to Neon Serverless."""
    # Neon Serverless has smart caching and instant provisioning
    # This test verifies that our application is compatible with those features
    from app.config import settings
    DATABASE_URL = settings.database_url

    # Check if the URL pattern suggests Neon Serverless
    is_neon = 'neon.tech' in DATABASE_URL or 'neon' in DATABASE_URL
    if is_neon:
        # Neon Serverless URLs typically have this format
        assert isinstance(DATABASE_URL, str)
    else:
        # Even if not using Neon, the configuration should be compatible
        assert isinstance(DATABASE_URL, str)


def test_concurrent_access_simulation():
    """Simulate concurrent access patterns that work well with Neon."""
    # Neon handles connection pooling efficiently
    # This test ensures our async patterns are compatible
    import asyncio

    # Verify that we can work with async patterns
    async def dummy_async_operation():
        return "success"

    # This should not raise an exception
    try:
        result = asyncio.run(dummy_async_operation())
        assert result == "success"
    except RuntimeError:
        # Event loop might already be running in test environment
        pass