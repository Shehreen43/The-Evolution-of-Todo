from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: str = Field(default="medium", max_length=20)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": "high"
            }
        }

class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[str] = Field(None, max_length=20)

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

    class Config:
        from_attributes = True