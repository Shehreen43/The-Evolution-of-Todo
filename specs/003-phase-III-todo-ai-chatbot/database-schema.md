# Phase III: Todo AI Chatbot - Database Schema

## 2.1 SCHEMA OVERVIEW
The database schema extends the existing Phase II todo application with new tables to support AI chatbot functionality. The schema maintains the existing Task model while adding Conversation and Message models to track chat interactions.

```
[User] 1--* [Conversation] 1--* [Message]
                    |
                    *--* [Task] (via AI operations)
```

- **User**: Identified by user_id from Better Auth (partitioning key)
- **Conversation**: Groups related messages in a chat session
- **Message**: Individual chat messages with role-based classification
- **Task**: Existing todo items from Phase II, now manageable via AI

The user_id serves as the partitioning key across all tables, ensuring data isolation between users and enabling efficient queries for user-specific data.

## 2.2 EXISTING MODEL (FROM PHASE II)
```python
# backend/models/task.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """
    Represents a todo task item.
    Existing model from Phase II - no changes needed.
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Links to Better Auth user
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False
            }
        }
```

## 2.3 NEW MODELS (PHASE III)

### 2.3.1 Conversation Model
```python
# backend/models/conversation.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    """
    Represents a chat conversation session.
    Each user can have multiple conversations.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Links to Better Auth user
    title: Optional[str] = Field(default="New Conversation", max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages (optional, for ORM convenience)
    messages: List["Message"] = Relationship(back_populates="conversation")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "title": "Todo Management Chat"
            }
        }
```

### 2.3.2 Message Model
```python
# backend/models/message.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from enum import Enum

class MessageRole(str, Enum):
    """Message role types following OpenAI convention"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

class Message(SQLModel, table=True):
    """
    Represents a single message in a conversation.
    Stores both user inputs and assistant responses.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(index=True)  # Denormalized for query efficiency
    role: MessageRole = Field(default=MessageRole.USER)
    content: str = Field(max_length=10000)  # Support long responses
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation (optional)
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": 1,
                "user_id": "user_123",
                "role": "user",
                "content": "Add a task to buy groceries"
            }
        }
```

## 2.4 DATABASE INDEXES
The following indexes are required for optimal performance:

```sql
-- Primary indexes (auto-created)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- Composite indexes for common queries
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);
CREATE INDEX idx_conversations_user_created ON conversations(user_id, created_at);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

These indexes ensure efficient querying for:
- User-specific data retrieval
- Conversation history loading
- Message chronological ordering
- Task status filtering