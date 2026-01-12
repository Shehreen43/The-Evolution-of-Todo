from sqlmodel import SQLModel, Field, Column, String, Boolean, Integer, DateTime, Text
from datetime import datetime
from typing import Optional
from pydantic import field_validator

class Task(SQLModel, table=True):
    """Task model for todo items."""
    id: int = Field(
        default=None,
        primary_key=True,
        description="Unique task identifier (auto-increment)"
    )
    user_id: str = Field(
        max_length=255,
        foreign_key="user.id",  # Foreign key relationship to User model
        description="Reference to owning user"
    )
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        sa_column=Column(Text),
        description="Task description (0-1000 characters)"
    )
    completed: bool = Field(
        default=False,
        description="Completion status"
    )
    priority: str = Field(
        default="medium",
        max_length=20,
        description="Task priority (low, medium, high)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (auto-updated)"
    )

    @field_validator('title')
    @classmethod
    def validate_title_length(cls, v):
        """Validate title length (1-200 characters)."""
        if len(v) < 1 or len(v) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return v

    @field_validator('description')
    @classmethod
    def validate_description_length(cls, v):
        """Validate description length (max 1000 characters)."""
        if v is not None and len(v) > 1000:
            raise ValueError('Description must be 1000 characters or less')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False
            }
        }