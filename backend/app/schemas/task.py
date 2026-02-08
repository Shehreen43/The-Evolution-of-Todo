from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: str = Field(default="medium", max_length=20)
    
    # Advanced features
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    category: Optional[str] = Field(None, max_length=50)
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = Field(None, max_length=20)
    end_recurrence: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": "high",
                "due_date": "2024-12-31T12:00:00",
                "category": "personal"
            }
        }

class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[str] = Field(None, max_length=20)
    completed: Optional[bool] = None
    
    # Advanced features
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    category: Optional[str] = Field(None, max_length=50)
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = Field(None, max_length=20)
    end_recurrence: Optional[datetime] = None

class TaskResponse(BaseModel):
    """Schema for task API responses."""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    priority: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    # Advanced features
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    category: Optional[str] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    end_recurrence: Optional[datetime] = None
    next_occurrence: Optional[datetime] = None

    class Config:
        from_attributes = True