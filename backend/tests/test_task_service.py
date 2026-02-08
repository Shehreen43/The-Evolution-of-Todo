import pytest
from datetime import datetime, timedelta
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.user import User

@pytest.mark.asyncio
async def test_task_service_advanced_features(db_session, sample_user_data):
    """Test advanced task service features."""
    # Setup user
    user = User(**sample_user_data)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    service = TaskService(db_session)
    
    # Test 1: Create task with advanced features
    task_data = TaskCreate(
        title="Test Advanced Task",
        description="Task with advanced features",
        priority="high",
        due_date=(datetime.now() + timedelta(days=2)).isoformat(),
        category="test-category",
        is_recurring=True,
        recurrence_pattern="weekly",
        end_recurrence=(datetime.now() + timedelta(weeks=4)).isoformat()
    )
    
    created_task = await service.create_task(user.id, task_data)
    assert created_task.id is not None
    assert created_task.priority == "high"
    assert created_task.category == "test-category"
    assert created_task.is_recurring is True

    # Test 2: Update task
    update_data = TaskUpdate(
        priority="medium",
        category="updated-category",
        is_recurring=False
    )
    
    updated_task = await service.update_task(user.id, created_task.id, update_data)
    assert updated_task.priority == "medium"
    assert updated_task.category == "updated-category"
    assert updated_task.is_recurring is False

    # Test 3: Filter tasks
    filtered_tasks = await service.filter_tasks(
        user_id=user.id,
        category="updated-category",
        priority="medium"
    )
    assert len(filtered_tasks) > 0
    assert filtered_tasks[0].id == created_task.id

    # Test 4: Toggle complete
    toggled_task = await service.toggle_complete(user.id, created_task.id)
    assert toggled_task.completed is True
