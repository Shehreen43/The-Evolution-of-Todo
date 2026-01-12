#!/usr/bin/env python3
"""
Test script to verify SQLModel models work with Neon database.
This script tests:
- Database connection
- Table creation
- Data insertion
- Data retrieval
"""

import asyncio
import os
from sqlmodel import SQLModel, select
from sqlalchemy.exc import IntegrityError

# Import models
from app.models.user import User
from app.models.task import Task
from app.database.connection import async_engine, async_session
from app.database.init_db import create_db_and_tables


async def test_database_connection():
    """Test basic database connection."""
    print("Testing database connection...")

    try:
        # Create tables using sync method
        create_db_and_tables()
        print("✓ Tables created successfully")
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False

    return True


async def test_user_operations():
    """Test user creation and retrieval."""
    print("\nTesting user operations...")

    async with async_session() as session:
        # Create a test user
        user = User(
            id="test_user_123",
            email="test@example.com",
            name="Test User",
            password_hash="$2b$12$example_hashed_password",  # Valid bcrypt hash format
        )

        try:
            session.add(user)
            await session.commit()
            print("✓ User created successfully")

            # Retrieve the user
            statement = select(User).where(User.email == "test@example.com")
            result = await session.execute(statement)
            retrieved_user = result.first()

            if retrieved_user:
                print(f"✓ User retrieved: {retrieved_user.name} ({retrieved_user.email})")
                return retrieved_user.id
            else:
                print("✗ Failed to retrieve user")
                return None

        except IntegrityError as e:
            print(f"✗ Integrity error (likely duplicate): {e}")
            await session.rollback()
            # Try to retrieve existing user
            statement = select(User).where(User.email == "test@example.com")
            result = await session.execute(statement)
            retrieved_user = result.first()
            if retrieved_user:
                print(f"✓ Existing user found: {retrieved_user.name} ({retrieved_user.email})")
                return retrieved_user.id
            return None
        except Exception as e:
            print(f"✗ Error creating/retrieving user: {e}")
            await session.rollback()
            return None


async def test_task_operations(user_id: str):
    """Test task creation and retrieval."""
    print("\nTesting task operations...")

    if not user_id:
        print("✗ Cannot test tasks without a valid user_id")
        return False

    async with async_session() as session:
        # Create a test task
        task = Task(
            user_id=user_id,
            title="Test Task",
            description="This is a test task description",
            priority="high",
            completed=False
        )

        try:
            session.add(task)
            await session.commit()
            print("✓ Task created successfully")

            # Retrieve the task
            statement = select(Task).where(Task.user_id == user_id)
            result = await session.execute(statement)
            retrieved_task = result.first()

            if retrieved_task:
                print(f"✓ Task retrieved: {retrieved_task.title} (completed: {retrieved_task.completed})")

                # Test updating the task
                retrieved_task.completed = True
                retrieved_task.title = "Updated Test Task"
                await session.commit()
                print("✓ Task updated successfully")

                # Retrieve updated task
                statement = select(Task).where(Task.id == retrieved_task.id)
                result = await session.execute(statement)
                updated_task = result.first()

                if updated_task and updated_task.completed:
                    print(f"✓ Task update verified: {updated_task.title} (completed: {updated_task.completed})")
                    return True
                else:
                    print("✗ Task update not reflected in database")
                    return False
            else:
                print("✗ Failed to retrieve task")
                return False

        except Exception as e:
            print(f"✗ Error creating/retrieving/updating task: {e}")
            await session.rollback()
            return False


async def main():
    """Main test function."""
    print("Starting SQLModel database tests with Neon database...")

    # Check if database URL is configured
    db_url = os.environ.get("DATABASE_URL", "")
    if not db_url:
        # Use the database URL from settings
        from app.config import settings
        db_url = settings.database_url
        if not db_url:
            print("✗ DATABASE_URL environment variable not set!")
            return

    print(f"Using database: {db_url.split('@')[1].split('/')[0] if '@' in db_url else 'Unknown'}")

    # Test database connection and table creation
    if not await test_database_connection():
        print("✗ Database connection test failed")
        return

    # Test user operations
    user_id = await test_user_operations()

    # Test task operations
    task_success = await test_task_operations(user_id)

    if task_success:
        print("\n✓ All tests passed! Database models are working correctly with Neon database.")
    else:
        print("\n✗ Some tests failed.")

    # Close the engine
    await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())