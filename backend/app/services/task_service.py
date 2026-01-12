from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import List, Optional

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_tasks(self, user_id: str) -> List[Task]:
        """List all tasks for a user."""
        result = await self.db.execute(
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
        )
        return result.scalars().all()

    async def create_task(self, user_id: str, task_data: TaskCreate) -> Task:
        """Create a new task."""
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_task(self, user_id: str, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        result = await self.db.execute(
            select(Task)
            .where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def update_task(
        self, user_id: str, task_id: int, task_data: TaskUpdate
    ) -> Task:
        """Update a task."""
        task = await self.get_task(user_id, task_id)
        if not task:
            raise ValueError("Task not found")

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(task, field, value)

        task.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, user_id: str, task_id: int) -> bool:
        """Delete a task."""
        task = await self.get_task(user_id, task_id)
        if task:
            await self.db.delete(task)
            await self.db.commit()
            return True
        return False

    async def toggle_complete(self, user_id: str, task_id: int) -> Task:
        """Toggle task completion status."""
        task = await self.get_task(user_id, task_id)
        if not task:
            raise ValueError("Task not found")

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(task)
        return task