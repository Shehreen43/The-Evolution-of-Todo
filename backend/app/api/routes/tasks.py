from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.connection import get_db
from app.api.deps import get_current_user, verify_user_access
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List all tasks for the authenticated user."""
    await verify_user_access(user_id, current_user)
    service = TaskService(db)
    tasks = await service.list_tasks(user_id)
    return [TaskResponse.model_validate(task) for task in tasks]

@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new task for the authenticated user."""
    await verify_user_access(user_id, current_user)
    service = TaskService(db)
    task = await service.create_task(user_id, task_data)
    return TaskResponse.model_validate(task)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific task by ID."""
    await verify_user_access(user_id, current_user)
    service = TaskService(db)
    task = await service.get_task(user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.model_validate(task)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update an existing task."""
    await verify_user_access(user_id, current_user)
    service = TaskService(db)
    try:
        task = await service.update_task(user_id, task_id, task_data)
        return TaskResponse.model_validate(task)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    user_id: str,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a task."""
    await verify_user_access(user_id, current_user)
    service = TaskService(db)
    success = await service.delete_task(user_id, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None

@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Toggle task completion status."""
    await verify_user_access(user_id, current_user)
    service = TaskService(db)
    try:
        task = await service.toggle_complete(user_id, task_id)
        return TaskResponse.model_validate(task)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")