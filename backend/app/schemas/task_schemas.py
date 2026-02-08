from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = "medium"
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    category: Optional[str] = None
    # Recurring task fields
    is_recurring: Optional[bool] = False
    recurrence_pattern: Optional[str] = None  # daily, weekly, monthly, yearly
    end_recurrence: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    category: Optional[str] = None
    completed: Optional[bool] = None
    # Recurring task fields
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None
    end_recurrence: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime
    priority: str
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    category: Optional[str] = None
    # Recurring task fields
    is_recurring: bool
    recurrence_pattern: Optional[str] = None
    next_occurrence: Optional[datetime] = None
    end_recurrence: Optional[datetime] = None
    parent_task_id: Optional[int] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        """Convert SQLAlchemy object to Pydantic model"""
        return cls(
            id=obj.id,
            user_id=obj.user_id,
            title=obj.title,
            description=obj.description,
            completed=obj.completed,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            priority=obj.priority,
            due_date=obj.due_date,
            reminder_time=obj.reminder_time,
            category=obj.category,
            is_recurring=obj.is_recurring,
            recurrence_pattern=obj.recurrence_pattern,
            next_occurrence=obj.next_occurrence,
            end_recurrence=obj.end_recurrence,
            parent_task_id=obj.parent_task_id
        )