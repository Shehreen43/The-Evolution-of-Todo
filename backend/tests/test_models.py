import pytest
from sqlmodel import select
from app.models.user import User
from app.models.task import Task

@pytest.mark.asyncio
async def test_user_crud(db_session, sample_user_data):
    """Test creating and retrieving a user."""
    user = User(**sample_user_data)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    assert user.id is not None
    assert user.email == sample_user_data["email"]

    # Retrieve
    statement = select(User).where(User.email == sample_user_data["email"])
    result = await db_session.execute(statement)
    retrieved_user = result.scalar_one_or_none()
    
    assert retrieved_user is not None
    assert retrieved_user.id == user.id

@pytest.mark.asyncio
async def test_task_crud(db_session, sample_user_data, sample_task_data):
    """Test creating and retrieving a task."""
    # Create user first
    user = User(**sample_user_data)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Create task
    task = Task(user_id=user.id, **sample_task_data)
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    assert task.id is not None
    assert task.user_id == user.id
    
    # Retrieve
    statement = select(Task).where(Task.id == task.id)
    result = await db_session.execute(statement)
    retrieved_task = result.scalar_one_or_none()

    assert retrieved_task is not None
    assert retrieved_task.title == sample_task_data["title"]
