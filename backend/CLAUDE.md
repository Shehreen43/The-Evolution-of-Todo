# Backend Guidelines

## Stack
- Python 3.13+
- FastAPI (web framework)
- SQLModel (ORM - SQLAlchemy + Pydantic)
- Uvicorn (ASGI server)
- python-jose (JWT verification)
- PostgreSQL (Neon Serverless)

## Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Settings and environment variables
│   │
│   ├── models/              # SQLModel data models
│   │   ├── __init__.py
│   │   ├── user.py          # User model (managed by Better Auth)
│   │   ├── task.py          # Task model
│   │   └── session.py       # Session model
│   │
│   ├── schemas/             # Pydantic schemas (API request/response)
│   │   ├── __init__.py
│   │   ├── task.py          # TaskCreate, TaskUpdate, TaskResponse
│   │   └── user.py          # User schemas
│   │
│   ├── database/            # Database connection and setup
│   │   ├── __init__.py
│   │   ├── connection.py    # Async SQLModel engine
│   │   └── session.py       # Database session dependency
│   │
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies (get_current_user)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── tasks.py     # Task CRUD endpoints
│   │       └── auth.py      # Auth endpoints (if needed)
│   │
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── task_service.py  # Task CRUD operations
│   │   └── user_service.py  # User-related logic
│   │
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── jwt.py           # JWT verification utilities
│
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Python project configuration
├── .env                     # Environment variables
├── .env.example             # Environment variables template
├── .gitignore
└── README.md
```

## How to Run the Server

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# Or using uv: uv pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
DATABASE_URL=postgresql://user:password@localhost:5432/hackathon_todo
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=http://localhost:3000
```

### 3. Start the Server
```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the python module approach
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# For production (without reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. API Documentation
Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## Testing Commands

### 1. Unit Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_specific_file.py

# Run tests with verbose output
pytest -v

# Run tests in watch mode (rerun on file changes)
ptw  # or pytest-watch
```

### 2. API Testing
```bash
# Test endpoints using curl
curl -X GET http://localhost:8000/health
curl -X GET http://localhost:8000/docs

# Test with httpie (if installed)
http :8000/health
http :8000/docs
```

### 3. Database Tests
```bash
# Run database-specific tests
pytest tests/test_database.py

# Test migrations
alembic check
alembic revision --autogenerate -m "test migration"
```

## Common Development Tasks

### 1. Adding New Dependencies
```bash
# Using pip
pip install new-package
pip freeze > requirements.txt

# Using uv (recommended)
uv pip install new-package
uv pip freeze > requirements.txt
```

### 2. Database Operations
```bash
# Initialize database
python -c "from app.database.init_db import init_db; import asyncio; asyncio.run(init_db())"

# Create migration
alembic revision --autogenerate -m "description of changes"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

### 3. Code Quality Checks
```bash
# Run linters
flake8 app/
black app/  # Format code
isort app/  # Sort imports

# Type checking
mypy app/

# Security scanning
bandit -r app/
```

### 4. API Development Workflow
```bash
# 1. Create model in app/models/
# 2. Create schema in app/schemas/
# 3. Create service in app/services/
# 4. Create route in app/api/routes/
# 5. Import and include route in app/main.py
# 6. Test with server running
```

### 5. Environment Management
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Deactivate
deactivate

# Update dependencies
pip install -r requirements.txt --upgrade
```

## Database Models

### Task Model

```python
# app/models/task.py
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
    priority: str = Field(
        default="medium",
        max_length=20,
        description="Task priority: high, medium, or low"
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

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": "high"
            }
        }
```

### User Model

```python
# app/models/user.py
from sqlmodel import SQLModel, Field, Column, String, DateTime
from datetime import datetime

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
```

## Pydantic Schemas

```python
# app/schemas/task.py
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
```

## API Routes

### JWT Verification Dependency

```python
# app/api/deps.py
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel

security = HTTPBearer()

BETTER_AUTH_SECRET = "your-shared-secret-key"  # From environment
ALGORITHM = "HS256"

class TokenPayload(BaseModel):
    sub: str      # User ID
    email: str    # User email
    exp: int      # Expiration timestamp

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenPayload:
    """Verify JWT and extract user information."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            BETTER_AUTH_SECRET,
            algorithms=[ALGORITHM]
        )

        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None or email is None:
            raise credentials_exception

        return TokenPayload(sub=user_id, email=email, exp=payload.get("exp", 0))

    except JWTError:
        raise credentials_exception

async def verify_user_access(
    user_id: str,
    current_user: TokenPayload = Depends(get_current_user)
) -> str:
    """Verify that the authenticated user has access to the requested resource."""
    if user_id != current_user.sub:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's data"
        )
    return user_id
```

### Task Routes

```python
# app/api/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.connection import get_db
from app.api.deps import get_current_user, verify_user_access
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List all tasks for the authenticated user."""
    await verify_user_access(user_id, current_user)
    service = TaskService(db)
    return await service.list_tasks(user_id)

@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new task for the authenticated user."""
    await verify_user_access(user_id, current_user)
    service = TaskService(db)
    return await service.create_task(user_id, task_data)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific task by ID."""
    await verify_user_access(user_id, current_user)
    service = TaskService(db)
    task = await service.get_task(user_id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update an existing task."""
    await verify_user_access(user_id, current_user)
    service = TaskService(db)
    return await service.update_task(user_id, task_id, task_data)

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    user_id: str,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a task."""
    await verify_user_access(user_id, current_user)
    service = TaskService(db)
    await service.delete_task(user_id, task_id)
    return None

@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Toggle task completion status."""
    await verify_user_access(user_id, current_user)
    service = TaskService(db)
    return await service.toggle_complete(user_id, task_id)
```

## Services

```python
# app/services/task_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import List, Optional

from app.models.task import Task
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
        """Create a new task."""
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
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
        """Update a task."""
        task = await self.get_task(user_id, task_id)
        if not task:
            raise ValueError("Task not found")

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, user_id: str, task_id: int) -> None:
        """Delete a task."""
        task = await self.get_task(user_id, task_id)
        if task:
            await self.db.delete(task)
            await self.db.commit()

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
```

## Database Connection

```python
# app/database/connection.py
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

## FastAPI Application

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import tasks

app = FastAPI(
    title="The Evolution of Todo - Phase II API",
    description="RESTful API for multi-user todo application",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "https://your-app.vercel.app",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "phase": "2"}

@app.get("/")
async def root():
    return {
        "name": "The Evolution of Todo - Phase II",
        "status": "running",
        "endpoints": {
            "tasks": "/api/{user_id}/tasks"
        }
    }
```

## Environment Variables

```bash
# .env
DATABASE_URL="postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/db?sslmode=require"
BETTER_AUTH_SECRET="your-32-character-secret-key-here"
ALGORITHM=HS256
```

## pyproject.toml

```toml
[project]
name = "the-evolution-of-todo-backend"
version = "2.0.0"
description = "FastAPI backend for The Evolution of Todo"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "sqlmodel>=0.0.19",
    "python-jose[cryptography]>=3.3.3",
    "pydantic>=2.5.0",
    "asyncpg>=0.29.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.26.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
package = true
```

## Code Quality Rules

1. **Async/Await** - Use async database operations throughout
2. **Type Hints** - Define types for all function parameters and returns
3. **Pydantic Schemas** - Validate all API inputs with Pydantic
4. **SQLModel Models** - Define database models with SQLModel
5. **User Isolation** - Always filter queries by user_id from JWT
6. **Error Handling** - Return proper HTTP status codes (401, 403, 404)
7. **Dependency Injection** - Use FastAPI dependencies for auth and DB
8. **Service Layer** - Keep business logic in service classes
9. **CORS** - Configure allowed origins for frontend communication
10. **Environment Variables** - Never hardcode secrets
