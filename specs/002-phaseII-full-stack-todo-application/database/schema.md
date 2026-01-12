# Database Schema Specification

This document defines the database schema for the Full-Stack Todo Web Application, Phase II of "The Evolution of Todo" project.

## Overview

| Attribute | Value |
|-----------|-------|
| **Database** | Neon Serverless PostgreSQL |
| **ORM** | SQLModel |
| **Status** | Draft |

---

## Entity Relationship Diagram

```mermaid
erDiagram
    USERS ||--o{ TASKS : "owns"

    USERS {
        string id PK "UUID"
        string email UK "Email"
        string name "Display name"
        string password_hash "Hashed password"
        datetime created_at "Creation time"
        datetime updated_at "Update time"
    }

    TASKS {
        int id PK "Auto increment"
        string user_id FK "Reference to user"
        string title "Task title"
        string description "Task description"
        boolean completed "Completion status"
        datetime created_at "Creation time"
        datetime updated_at "Update time"
    }
```

---

## Tables

### 1. users (Managed by Better Auth)

**Purpose:** Store user account information

#### Columns

| Column | Type | Constraints | Default | Description |
|--------|------|-------------|---------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | - | Unique user identifier (UUID format) |
| email | VARCHAR(255) | UNIQUE, NOT NULL | - | User's email address |
| name | VARCHAR(255) | NOT NULL | - | User's display name |
| password_hash | VARCHAR(255) | NOT NULL | - | Hashed password (bcrypt) |
| created_at | TIMESTAMP | - | CURRENT_TIMESTAMP | Account creation time |
| updated_at | TIMESTAMP | - | CURRENT_TIMESTAMP | Last update time |

#### Indexes

| Index Type | Columns | Purpose |
|------------|---------|---------|
| PRIMARY KEY | id | Unique row identifier |
| UNIQUE | email | Fast lookup during login |

#### Constraints

| Constraint | Rule | Enforcement |
|------------|------|-------------|
| UNIQUE | email | Database level |
| NOT NULL | email, name, password_hash | Database level |
| Email format | Valid email pattern | Application level |

#### Notes

- This table is primarily managed by Better Auth
- Do not modify directly except through Better Auth APIs
- Password is hashed using bcrypt
- Never expose `password_hash` in API responses

---

### 2. tasks

**Purpose:** Store todo task information

#### Columns

| Column | Type | Constraints | Default | Description |
|--------|------|-------------|---------|-------------|
| id | SERIAL | PRIMARY KEY | - | Auto-incrementing task identifier |
| user_id | VARCHAR(255) | NOT NULL, FK | - | Foreign key to users.id |
| title | VARCHAR(200) | NOT NULL | - | Task title |
| description | TEXT | - | NULL | Optional task description |
| completed | BOOLEAN | - | FALSE | Completion status |
| created_at | TIMESTAMP | - | CURRENT_TIMESTAMP | Task creation time |
| updated_at | TIMESTAMP | - | CURRENT_TIMESTAMP | Last update time |

#### Indexes

| Index Type | Columns | Purpose |
|------------|---------|---------|
| PRIMARY KEY | id | Unique task identifier |
| INDEX | user_id | Filter user's tasks (critical) |
| INDEX | completed | Filter by status |
| INDEX | created_at | Sort by date |

#### Foreign Keys

| Column | References | On Delete | Description |
|--------|------------|-----------|-------------|
| user_id | users.id | CASCADE | Deleting user deletes all their tasks |

#### Constraints

| Constraint | Rule | Enforcement |
|------------|------|-------------|
| NOT NULL | user_id, title | Database level |
| title length | 1-200 characters | Application + DB |
| description length | 0-1000 characters | Application level |

#### Triggers

```sql
-- Trigger to auto-update updated_at
CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## Relationships

```
users (1) ----< (many) tasks

One user can have many tasks
Each task belongs to exactly one user
Cascade delete: deleting a user deletes all their tasks
```

### Relationship Diagram

```mermaid
flowchart LR
    User[users table] -->|has many| Tasks[tasks table]
    Tasks -->|belongs to| User

    User -->|id| user_id[user_id FK in tasks]
    Tasks -->|ON DELETE CASCADE| UserDelete[User deleted]
```

---

## SQLModel Implementation

### Base Configuration

```python
# backend/app/database/connection.py
from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@host/db?sslmode=require"

# Async engine for FastAPI
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Session factory
async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    """Dependency for getting async database session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initialize database tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

### User Model

```python
# backend/app/models/user.py
from sqlmodel import SQLModel, Field, Column, String, DateTime
from datetime import datetime

class User(SQLModel, table=True):
    """User model for authentication."""
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
```

### Task Model

```python
# backend/app/models/task.py
from sqlmodel import SQLModel, Field, Column, String, Boolean, Integer, DateTime, Text, ForeignKey
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """Task model for todo items."""
    id: int = Field(
        default=None,
        primary_key=True,
        description="Unique task identifier (auto-increment)"
    )
    user_id: str = Field(
        foreign_key="user.id",
        max_length=255,
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
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )
```

---

## Migration Strategy

### Development (Auto-create)

```python
# Create tables on startup
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

### Production (Alembic - Future)

```python
# alembic/versions/001_initial_schema.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now()),
    )

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String(255), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('completed', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now()),
    )

    # Create indexes
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_completed', 'tasks', ['completed'])
    op.create_index('idx_tasks_created_at', 'tasks', ['created_at'])

def downgrade():
    op.drop_index('idx_tasks_created_at', table_name='tasks')
    op.drop_index('idx_tasks_completed', table_name='tasks')
    op.drop_index('idx_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')
    op.drop_table('users')
```

---

## Performance Considerations

### Critical Indexes

| Query Pattern | Recommended Index |
|---------------|-------------------|
| List user's tasks | INDEX (user_id) |
| Filter pending tasks | INDEX (user_id, completed) WHERE completed = FALSE |
| Sort by date | INDEX (created_at DESC) |
| Filter by status | INDEX (completed) |

### Optimization Tips

1. **Index foreign keys**: Always index `user_id` on tasks table
2. **Limit results**: Use pagination for large task lists
3. **Connection pooling**: Use for production performance
4. **Async operations**: Use async SQLModel for FastAPI

---

## Security Considerations

| Concern | Mitigation |
|---------|------------|
| Password exposure | Never expose `password_hash` in API |
| SQL injection | Use SQLModel (parameterized queries) |
| User data isolation | Always filter by `user_id` from JWT |
| JWT user_id vs URL | Validate JWT user_id matches URL user_id |

---

## Connection String Format

### Standard Connection

```
postgresql://[username]:[password]@[host]:[port]/[database]
```

### With SSL (Required for Neon)

```
postgresql://[username]:[password]@[host]/[database]?sslmode=require
```

### Environment Variable

```bash
# .env
DATABASE_URL="postgresql://user:password@ep-xxx.region.neon.tech/db?sslmode=require"
```

---

## Sample Data

### Insert Sample User

```sql
INSERT INTO users (id, email, name, password_hash, created_at, updated_at)
VALUES (
    'user_123',
    'john@example.com',
    'John Doe',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.X6YL6NX6DdK2e',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
```

### Insert Sample Tasks

```sql
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at)
VALUES
    ('user_123', 'Buy groceries', 'Milk, eggs, bread', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('user_123', 'Complete project', 'Finish the todo app', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('user_123', 'Call mom', 'Weekly check-in', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
```

---

## Related Documents

| Document | Path | Purpose |
|----------|------|---------|
| Architecture | `architecture.md` | System architecture |
| API Spec | `api/rest-endpoints.md` | API endpoints |
| Authentication | `features/authentication.md` | Auth flow |
| Task CRUD | `features/task-crud.md` | Task operations |

---

## Version Information

| Item | Value |
|------|-------|
| Schema Version | 1.0.0 |
| Status | Draft |
| Last Updated | 2026-01-07 |
