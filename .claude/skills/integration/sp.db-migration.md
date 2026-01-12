---
name: sp.db-migration
description: Generate SQLModel database migrations for schema changes. Use when creating database tables, modifying schemas, or setting up Alembic migrations for Phase II+ applications with SQLModel.
---

# Database Migration Generator

Generate SQLModel database models and Alembic migrations for the todo application.

## Database Models

### src/models/task.py
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from uuid import uuid4


class Task(SQLModel, table=True):
    """Task model for storing todo items."""
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: str = Field(foreign_key="users.id", index=True, nullable=False)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    priority: Optional[str] = Field(default="medium", max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "priority": "high",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }


class User(SQLModel, table=True):
    """User model for authentication (referenced by Better Auth)."""
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: List["Task"] = Relationship(back_populates="user")


class TaskRelationship(SQLModel, table=True):
    """Self-referential for task dependencies (optional Phase V)."""
    id: Optional[int] = Field(default=None, primary_key=True)
    parent_task_id: int = Field(foreign_key="task.id", index=True)
    child_task_id: int = Field(foreign_key="task.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        table_name = "task_relationships"
```

### src/schemas/task.py
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    """Base Task schema with common fields."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(None, max_length=20)


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: int
    user_id: str
    completed: bool
    priority: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """Schema for task list response."""
    tasks: list[TaskResponse]
    total: int
```

## Pydantic Schemas

### src/schemas/user.py
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a user."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: Optional[str] = Field(None, max_length=255)


class UserResponse(BaseModel):
    """Schema for user response."""
    id: str
    email: str
    name: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: UserResponse
```

## Database Connection

### src/db/connection.py
```python
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# Synchronous engine (for development)
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Asynchronous engine (recommended for production)
async_engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.DEBUG,
)

# Session factories
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine
)

AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    bind=async_engine
)


def get_db():
    """Get synchronous database session."""
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    """Get asynchronous database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(bind=sync_engine)
```

## Alembic Migration Setup

### alembic.ini
```ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers = console
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers = console
qualname = alembic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

### alembic/env.py
```python
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from app.models.task import Task, User
from app.config import get_settings

settings = get_settings()

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """Run migrations in async mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()
```

### alembic/versions/001_initial_migration.py
```python
"""Initial migration

Revision ID: 001
Revises:
Create Date: 2024-01-15

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create tasks table
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('priority', sa.String(length=20), nullable=True, default='medium'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_task_user_id', 'user_id'),
        sa.Index('ix_task_completed', 'completed'),
        sa.Index('ix_task_created_at', 'created_at'),
    )

    # Create users table (for reference)
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.Index('ix_users_email', 'email'),
    )

    # Add foreign key (after users table exists)
    op.create_foreign_key(
        'fk_task_user_id_users',
        'task', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    op.drop_table('task')
    op.drop_table('users')
```

### Migration Commands
```bash
# Initialize Alembic
cd backend && alembic init alembic

# Create a new migration
alembic revision -m "migration_description"

# Run migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show migration history
alembic history

# Generate SQL for migration (without running)
alembic upgrade --sql +1
```

## Index Strategy

| Table | Index | Purpose |
|-------|-------|---------|
| tasks | (user_id) | Filter by user |
| tasks | (completed) | Filter by status |
| tasks | (user_id, completed) | Compound filter |
| tasks | (created_at DESC) | Sort by date |
| users | (email) | Login lookup |
| users | (id) | Foreign key reference |

## Guardrails

### Do
- Use SQLModel for all database operations
- Create migrations for all schema changes
- Index foreign keys and frequently queried columns
- Use async sessions for FastAPI
- Set CASCADE delete for user->tasks relationship

### Do Not
- Modify models without creating migrations
- Skip indexes on foreign keys
- Use synchronous blocking calls in async routes
- Hardcode connection strings

## Triggers

Use this skill when:
- User asks to "create database models"
- Setting up SQLModel with FastAPI
- Creating Alembic migrations
- Modifying database schema
- Configuring database connection
