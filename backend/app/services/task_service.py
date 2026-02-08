from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import List, Optional

from app.models.task_advanced import Task  # Using advanced task model with all features
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
        """Create a new task with advanced features."""
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            priority=getattr(task_data, 'priority', 'medium'),
            # Advanced task features
            due_date=getattr(task_data, 'due_date', None),
            reminder_time=getattr(task_data, 'reminder_time', None),
            category=getattr(task_data, 'category', None),
            is_recurring=getattr(task_data, 'is_recurring', False),
            recurrence_pattern=getattr(task_data, 'recurrence_pattern', None),
            end_recurrence=getattr(task_data, 'end_recurrence', None),
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
        """Update a task with advanced features."""
        task = await self.get_task(user_id, task_id)
        if not task:
            raise ValueError("Task not found")

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(task, field, value)

        # Update advanced fields if they exist in the update data
        for field, value in update_data.items():
            if hasattr(task, field) and value is not None:
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

    async def get_recurring_tasks(self, user_id: str, status: str = "all") -> List[Task]:
        """Get recurring tasks for a user."""
        query = select(Task).where(
            Task.user_id == user_id,
            Task.is_recurring == True
        )

        if status == "active":
            # Active recurring tasks are those that are still scheduled
            query = query.where(Task.end_recurrence.is_(None) | (Task.end_recurrence > datetime.utcnow()))
        elif status == "inactive":
            # Inactive recurring tasks are those that have ended
            query = query.where(Task.end_recurrence.isnot(None)).where(Task.end_recurrence <= datetime.utcnow())

        result = await self.db.execute(query.order_by(Task.created_at.desc()))
        return result.scalars().all()

    async def filter_tasks(
        self,
        user_id: str,
        status: str = "all",
        category: str = None,
        due_date_filter: str = "all",
        is_recurring: bool = None,
        priority: str = "all"
    ) -> List[Task]:
        """Filter tasks with advanced options."""
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        # Apply category filter
        if category:
            query = query.where(Task.category.ilike(f"%{category}%"))

        # Apply priority filter
        if priority != "all":
            query = query.where(Task.priority == priority)

        # Apply recurring filter
        if is_recurring is not None:
            query = query.where(Task.is_recurring == is_recurring)

        # Apply due date filter
        if due_date_filter != "all":
            now = datetime.utcnow()
            today = datetime(now.year, now.month, now.day)
            end_of_week = today.replace(day=today.day + 7)
            end_of_month = today.replace(day=1).replace(month=today.month + 1) if today.month < 12 else today.replace(year=today.year + 1, month=1)

            if due_date_filter == "today":
                query = query.where(Task.due_date.between(today, today.replace(hour=23, minute=59, second=59)))
            elif due_date_filter == "overdue":
                query = query.where(Task.due_date < now).where(Task.completed == False)
            elif due_date_filter == "week":
                query = query.where(Task.due_date.between(today, end_of_week))
            elif due_date_filter == "month":
                query = query.where(Task.due_date.between(today, end_of_month))

        result = await self.db.execute(query.order_by(Task.created_at.desc()))
        return result.scalars().all()