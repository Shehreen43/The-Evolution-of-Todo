from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from enum import Enum

class MessageRole(str, Enum):
    """Message role enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

# Updated Task model with advanced features
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str  # From authentication system
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
     
    # Advanced features
    priority: str = Field(default="medium", sa_column_kwargs={"server_default": "medium"})  # low, medium, high
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    category: Optional[str] = Field(default=None, max_length=50)  # tags/categories

    # Recurring task fields
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = Field(default=None, max_length=20)  # daily, weekly, monthly, yearly
    next_occurrence: Optional[datetime] = None
    end_recurrence: Optional[datetime] = None

    # Foreign key for recurring tasks to link to parent
    parent_task_id: Optional[int] = Field(default=None, foreign_key="task.id")

# Conversation model for chatbot
class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    title: Optional[str] = Field(default=None, max_length=200)

# Message model for chatbot
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    conversation_id: int = Field(foreign_key="conversation.id")
    role: MessageRole  # Changed from str to MessageRole
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Additional fields for advanced chat features
    message_metadata: Optional[str] = None  # JSON string for additional message metadata