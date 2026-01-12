from sqlmodel import SQLModel, Field, Column, String, DateTime
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from pydantic import field_validator
import re

if TYPE_CHECKING:
    from .task import Task  # Avoid circular import for type checking

class User(SQLModel, table=True):
    """User model for authentication (managed by Better Auth)."""
    id: str = Field(
        primary_key=True,
        max_length=255,
        description="Unique user identifier (UUID)"
    )
    email: str = Field(
        unique=True,
        max_length=255,
        description="User email address (unique)"
    )
    name: str = Field(
        max_length=255,
        description="User display name"
    )
    password_hash: str = Field(
        max_length=255,
        description="Bcrypt hashed password"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )

    # Relationship to tasks (optional - only if you want bidirectional relationship)
    # tasks: List["Task"] = Relationship(back_populates="user")

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format."""
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Invalid email format')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe"
            }
        }