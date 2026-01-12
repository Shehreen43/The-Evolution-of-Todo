# Phase II: System Architecture

This document describes the system architecture for the Full-Stack Todo Web Application, Phase II of "The Evolution of Todo" project.

---

## Architecture Overview

### High-Level Architecture

```mermaid
┌─────────────────────────────────────────────────────────────────────────────┐
│                        THE EVOLUTION OF TODO - PHASE II                       │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │   User Browser  │
                              │   (Any Client)  │
                              └────────┬────────┘
                                       │ HTTPS
                                       │
┌──────────────────────────────────────┼──────────────────────────────────────┐
│                                      ▼                                       │
│                         ┌─────────────────────────┐                          │
│                         │    Frontend (Next.js)   │                          │
│                         │    Port: 3000 (dev)     │                          │
│                         └────────────┬────────────┘                          │
│                                    │                                         │
│                         ┌──────────┴──────────┐                             │
│                         │                     │                             │
│                         ▼                     ▼                             │
│                ┌────────────────┐    ┌─────────────────┐                    │
│                │   Better Auth  │    │   API Client    │                    │
│                │   (Sessions)   │    │   (JWT + Fetch) │                    │
│                └────────────────┘    └────────┬────────┘                    │
│                                               │                              │
└───────────────────────────────────────────────┼──────────────────────────────┘
                                                │ HTTPS
                                                │
┌───────────────────────────────────────────────┼──────────────────────────────┐
│                                               ▼                              │
│                         ┌─────────────────────────────────────────┐          │
│                         │           Backend (FastAPI)              │          │
│                         │           Port: 8000 (dev)              │          │
│                         └────────────────────┬────────────────────┘          │
│                                              │                               │
│                         ┌────────────────────┴────────────────────┐          │
│                         │                                          │          │
│                         ▼                                          ▼          │
│                ┌─────────────────┐                       ┌─────────────────┐ │
│                │   JWT Auth      │                       │   Task Service  │ │
│                │   Middleware    │                       │   (Business     │ │
│                │   - Verify JWT  │                       │    Logic)       │ │
│                │   - Extract     │                       └────────┬────────┘ │
│                │     user_id     │                                │          │
│                └────────┬────────┘                                │          │
│                         │                                         │          │
│                         ▼                                         │          │
│                ┌─────────────────┐                                │          │
│                │   Error Handler │                                │          │
│                │   - 401 Unauthorized                           │          │
│                │   - 403 Forbidden │                             │          │
│                └────────┬────────┘                                │          │
│                         │                                         │          │
└─────────────────────────┼─────────────────────────────────────────┼──────────┘
                          │                                         │
                          ▼                                         ▼
                ┌─────────────────────────────────────────────────────────────┐
                │                   Neon PostgreSQL Database                   │
                │                                                             │
                │  ┌─────────────────┐        ┌─────────────────────────┐     │
                │  │     users       │        │         tasks           │     │
                │  │  (Better Auth)  │        │                         │     │
                │  ├─────────────────┤        ├─────────────────────────┤     │
                │  │ id (PK)         │        │ id (PK)                 │     │
                │  │ email           │        │ user_id (FK) ──────────┼─────┘
                │  │ name            │◀───────│ title                   │     │
                │  │ created_at      │        │ description             │     │
                │  └─────────────────┘        │ completed               │     │
                │                               created_at               │     │
                │                               updated_at               │     │
                │                               priority                 │     │
                │  Indexes:                    └─────────────────────────┘     │
                │  - users.id                                                │
                │  - tasks.user_id (filtering)                                │
                │  - tasks.completed (filtering)                              │
                └─────────────────────────────────────────────────────────────┘
```

### Architecture Pattern

| Aspect | Pattern | Rationale |
|--------|---------|-----------|
| **Overall** | Client-Server | Traditional web application model |
| **Frontend** | Single Page Application (SPA) with SSR | Next.js App Router hybrid |
| **Backend** | RESTful API | Simple, well-understood, great tooling |
| **Database** | Relational (PostgreSQL) | Structured data, ACID compliance |
| **Authentication** | JWT (Stateless) | Scalable, works across services |
| **ORM** | SQLModel | Type safety, Pydantic + SQLAlchemy |

### Communication Protocol

```
┌─────────────────────────────────────────────────────────────────┐
│                    API Communication Flow                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐                              ┌──────────────┐
│   Frontend   │                              │   Backend    │
│   (Next.js)  │                              │   (FastAPI)  │
└──────┬───────┘                              └──────┬───────┘
       │                                             │
       │  1. Request with JWT                        │
       │  ──────────────────────────────────────────▶│
       │                                             │
       │                                             │  2. Verify JWT
       │                                             │  3. Extract user_id
       │                                             │  4. Execute logic
       │                                             │  5. Query database
       │                                             │
       │  6. JSON Response                          │
       │  ◀─────────────────────────────────────────│
       │                                             │
       └─────────────────────────────────────────────┘

Request Headers:
  Content-Type: application/json
  Authorization: Bearer <jwt-token>

Response Format:
  {
    "success": true,
    "data": { ... },
    "message": "optional message"
  }
```

---

## Components

### 1. Frontend (Next.js 16+)

#### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | Next.js 16+ | React framework |
| Router | App Router | File-based routing |
| Language | TypeScript | Type safety |
| Styling | Tailwind CSS | Utility-first CSS |
| Auth | Better Auth | Session management |
| State | React Hooks | Local state |
| HTTP | Fetch API | API calls |

#### Architecture

```mermaid
┌─────────────────────────────────────────────────────────────┐
│                    Next.js Frontend Structure                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        app/                                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   layout.tsx                            ││
│  │  - Root layout                                          ││
│  │  - Providers (Auth, Theme)                             ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  ┌────────────────────┐  ┌────────────────────────────┐    │
│  │     page.tsx       │  │     login/                 │    │
│  │  - Dashboard       │  │  - page.tsx (login form)   │    │
│  │  - Task list       │  └────────────────────────────┘    │
│  └────────────────────┘                                     │
│                                                              │
│  ┌────────────────────┐  ┌────────────────────────────┐    │
│  │   api/             │  │     signup/                │    │
│  │  - tasks/route.ts  │  │  - page.tsx (signup form)  │    │
│  │  - client.ts       │  └────────────────────────────┘    │
│  └────────────────────┘                                     │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   components/                           ││
│  │  ┌───────────┐  ┌───────────┐  ┌───────────────────┐   ││
│  │  │ TaskList  │  │ TaskForm  │  │ AuthProvider      │   ││
│  │  │ TaskItem  │  │ Header    │  │ Button            │   ││
│  │  └───────────┘  └───────────┘  └───────────────────┘   ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

#### Component Categories

| Category | Components | Type |
|----------|------------|------|
| **Pages** | `page.tsx` (dashboard), `login/page.tsx`, `signup/page.tsx` | Server + Client |
| **UI** | `Button`, `Input`, `Card`, `Modal` | Client |
| **Tasks** | `TaskList`, `TaskItem`, `TaskForm` | Client |
| **Auth** | `AuthProvider`, `useAuth` | Client |
| **API** | `apiClient.ts`, `tasks/route.ts` | Server |

#### Better Auth Integration

```typescript
// auth.config.ts (Better Auth configuration)
import { betterAuth } from "better-auth"

export const auth = betterAuth({
  database: process.env.DATABASE_URL,
  secret: process.env.BETTER_AUTH_SECRET,
  emailAndPassword: {
    enabled: true
  },
  plugins: [
    // JWT plugin for token generation
    jwt() // Note: Better Auth has JWT plugin support
  ]
})
```

#### API Client with JWT Injection

```typescript
// lib/api-client.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

class ApiClient {
  private getToken(): string | null {
    // Get JWT from Better Auth session
    const session = useAuth.getState().session
    return session?.token || null
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken()

    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options.headers,
    }

    if (token) {
      (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Request failed")
    }

    return response.json()
  }

  // Task operations
  async getTasks() {
    return this.request<Task[]>("/api/tasks")
  }

  async createTask(data: CreateTaskData) {
    return this.request<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  async updateTask(id: number, data: UpdateTaskData) {
    return this.request<Task>(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  }

  async deleteTask(id: number) {
    return this.request<void>(`/api/tasks/${id}`, {
      method: "DELETE",
    })
  }

  async toggleComplete(id: number) {
    return this.request<Task>(`/api/tasks/${id}/complete`, {
      method: "PATCH",
    })
  }
}

export const api = new ApiClient()
```

---

### 2. Backend (FastAPI)

#### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | FastAPI | Web framework |
| Language | Python 3.13+ | Runtime |
| ORM | SQLModel | Database ORM |
| Auth | python-jose | JWT verification |
| Server | Uvicorn + ASGI | ASGI server |
| CORS | fastapi-cors | Cross-origin settings |

#### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Settings and environment
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # User model (Better Auth compatible)
│   │   └── task.py                # Task model
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py          # SQLModel engine setup
│   │   └── session.py             # Database session management
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                # Dependencies (get_current_user)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── tasks.py           # Task CRUD endpoints
│   │       └── auth.py            # Auth endpoints (if needed)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py        # Business logic
│   │   └── user_service.py        # User-related logic
│   │
│   └── schemas/
│       ├── __init__.py
│       ├── task.py                # Pydantic schemas
│       └── user.py                # User schemas
│
├── pyproject.toml
└── .env                           # Environment variables
```

#### API Endpoint Definitions

```python
# app/api/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.api.deps import get_current_user
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List all tasks for the authenticated user."""
    # Verify user ownership
    if user_id != current_user.sub:
        raise HTTPException(status_code=403, detail="Not authorized")

    service = TaskService(db)
    return await service.list_tasks(user_id)


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new task for the authenticated user."""
    if user_id != current_user.sub:
        raise HTTPException(status_code=403, detail="Not authorized")

    service = TaskService(db)
    return await service.create_task(user_id, task_data)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific task by ID."""
    if user_id != current_user.sub:
        raise HTTPException(status_code=403, detail="Not authorized")

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
    current_user: dict = Depends(get_current_user)
):
    """Update an existing task."""
    if user_id != current_user.sub:
        raise HTTPException(status_code=403, detail="Not authorized")

    service = TaskService(db)
    return await service.update_task(user_id, task_id, task_data)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    user_id: str,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a task."""
    if user_id != current_user.sub:
        raise HTTPException(status_code=403, detail="Not authorized")

    service = TaskService(db)
    await service.delete_task(user_id, task_id)
    return None


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Toggle task completion status."""
    if user_id != current_user.sub:
        raise HTTPException(status_code=403, detail="Not authorized")

    service = TaskService(db)
    return await service.toggle_complete(user_id, task_id)
```

#### JWT Authentication Middleware

```python
# app/api/deps.py
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel

# Security scheme
security = HTTPBearer()

# JWT settings (must match Better Auth config)
SECRET_KEY = "your-shared-secret-key"  # BETTER_AUTH_SECRET
ALGORITHM = "HS256"

class TokenPayload(BaseModel):
    sub: str      # User ID
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
        # Decode JWT token
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Extract user ID
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        return TokenPayload(sub=user_id, exp=payload.get("exp", 0))

    except JWTError:
        raise credentials_exception
```

#### FastAPI Application Entry Point

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import tasks

# Create FastAPI application
app = FastAPI(
    title="The Evolution of Todo - Phase II API",
    description="RESTful API for multi-user todo application",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)

# Health check endpoint
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

---

### 3. Database (Neon PostgreSQL)

#### Schema Overview

```mermaid
erDiagram
    USERS ||--o{ TASKS : "creates"

    USERS {
        string id PK "User ID (UUID)"
        string email UK "Email address"
        string name "Display name"
        timestamp created_at "Creation time"
        timestamp updated_at "Last update"
    }

    TASKS {
        int id PK "Task ID (auto)"
        string user_id FK "Owner user ID"
        string title "Task title (1-200 chars)"
        string description "Task description (0-1000 chars)"
        boolean completed "Completion status"
        timestamp created_at "Creation time"
        timestamp updated_at "Last update"
        string priority "Priority (high/medium/low)"
    }

    USERS }|..|| SESSIONS : "has"
    SESSIONS {
        string id PK "Session ID"
        string user_id FK "User ID"
        string token "JWT token"
        timestamp expires_at "Token expiration"
    }
```

#### SQLModel Definitions

```python
# app/models/user.py
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    """User model compatible with Better Auth."""
    id: str = Field(primary_key=True, max_length=255)
    email: str = Field(unique=True, max_length=255)
    name: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

```python
# app/models/task.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """Task model for todo items."""
    id: int = Field(default=None, primary_key=True, index=True)
    user_id: str = Field(
        foreign_key="user.id",
        index=True,
        max_length=255
    )
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", max_length=20)  # high, medium, low
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": "high"
            }
        }
```

#### Database Connection

```python
# app/database/connection.py
from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@host/db"

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

---

### 4. Authentication (Better Auth + JWT)

#### Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Database

    Note over User, Database: Login Flow

    User->>Frontend: Enter email/password
    Frontend->>Frontend: Validate input
    Frontend->>Database: Create user account (if signup)

    User->>Frontend: Submit credentials
    Frontend->>Better Auth: Sign in request
    Better Auth->>Database: Verify credentials
    Database-->>Better Auth: User data
    Better Auth->>Better Auth: Generate JWT
    Better Auth-->>Frontend: Session + JWT token
    Frontend-->>User: Logged in (dashboard)

    Note over User, Database: API Request Flow

    User->>Frontend: View tasks
    Frontend->>Frontend: Get JWT from session
    Frontend->>Backend: GET /api/{user_id}/tasks<br/>Authorization: Bearer <token>

    Backend->>Backend: Verify JWT signature
    Backend->>Backend: Extract user_id from token
    Backend->>Database: SELECT * FROM tasks<br/>WHERE user_id = ?
    Database-->>Backend: User's tasks only

    Backend-->>Frontend: JSON response with tasks
    Frontend-->>User: Display tasks
```

#### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user-123",       // User ID
    "email": "user@example.com",
    "name": "John Doe",
    "iat": 1704067200,       // Issued at
    "exp": 1704672000,       // Expiration (7 days)
    "iss": "better-auth"     // Issuer
  },
  "signature": "..."
}
```

#### Security Configuration

| Setting | Value | Rationale |
|---------|-------|-----------|
| **Algorithm** | HS256 | Symmetric, widely supported |
| **Secret** | BETTER_AUTH_SECRET | Shared between frontend/backend |
| **Expiration** | 7 days (604800 seconds) | Balance security/usability |
| **Token Location** | Authorization header | Standard practice |
| **Verification** | Required on every request | Prevent unauthorized access |

---

## Security Model

### Defense in Depth

```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Layers                              │
└─────────────────────────────────────────────────────────────────┘

Layer 1: Network Security
  HTTPS (TLS 1.3)     → Encrypt all traffic in transit
  CORS Configuration  → Whitelist allowed origins

Layer 2: Application Security
  JWT Verification    → Authenticate every API request
  Input Validation    → Pydantic schemas validate all inputs
  Error Handling      → No sensitive data in error messages

Layer 3: Data Security
  User Isolation      → Every query filtered by user_id
  Parameterized SQL   → SQLModel prevents SQL injection
  Database Secrets    → Environment variables only

Layer 4: Access Control
  401 Unauthorized    → Missing/invalid token
  403 Forbidden       → Valid token, wrong user
  404 Not Found       → Resource doesn't exist (or user doesn't own it)
```

### User Isolation

Every database query includes a user_id filter:

```python
# WRONG - Exposes all tasks to all users
async def get_tasks(db):
    return await db.exec(select(Task)).all()

# CORRECT - Only returns user's own tasks
async def get_tasks(user_id: str, db):
    return await db.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
```

### Error Responses

| Status Code | Scenario | Response |
|-------------|----------|----------|
| 400 | Invalid input | `{"detail": "Validation error"}` |
| 401 | Missing/invalid token | `{"detail": "Could not validate credentials"}` |
| 403 | Token valid, wrong user | `{"detail": "Not authorized"}` |
| 404 | Task not found | `{"detail": "Task not found"}` |
| 500 | Server error | `{"detail": "Internal server error"}` |

---

## Data Flow

### Request Processing Pipeline

```mermaid
flowchart TD
    A[HTTP Request] --> B{CORS Check}
    B -->|Allowed| C[Extract JWT Token]
    B -->|Denied| D[403 Forbidden]

    C --> E{Token Present?}
    E -->|No| F[401 Unauthorized]
    E -->|Yes| G[JWT Verification]

    G --> H{Valid Signature?}
    H -->|No| I[401 Unauthorized]
    H -->|Yes| J[Extract user_id]

    J --> K[Route to Handler]
    K --> L[Validate Request Body]
    L --> M{Validation OK?}
    M -->|No| N[400 Bad Request]
    M -->|Yes| O[Execute Business Logic]

    O --> P[Database Operation<br/>with user_id filter]
    P --> Q[Return JSON Response]

    N --> R[Error Response]
    F --> R
    I --> R
    D --> R
```

### Data Transformation

```
Frontend (JSON)
        │
        ▼
    API Request
        │
        ▼
JWT Verification → Extract user_id
        │
        ▼
Pydantic Validation → Create TaskCreate schema
        │
        ▼
Business Logic → TaskService.create_task(user_id, data)
        │
        ▼
SQLModel → INSERT INTO tasks (user_id, title, description, ...)
        │
        ▼
PostgreSQL → Returns created Task
        │
        ▼
SQLModel → Python object
        │
        ▼
Pydantic → TaskResponse schema
        │
        ▼
Frontend (JSON)
```

---

## Deployment Architecture

### Development Environment

```
┌─────────────────────────────────────────────────────────────────┐
│                   Development Environment                        │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────┐
    │                      Host Machine                         │
    │                                                          │
    │  ┌─────────────────────┐      ┌─────────────────────┐   │
    │  │  Frontend Server    │      │  Backend Server     │   │
    │  │  Next.js :3000      │      │  FastAPI :8000      │   │
    │  └──────────┬──────────┘      └──────────┬──────────┘   │
    │             │                             │              │
    │             └──────────┬──────────────────┘              │
    │                        │                                 │
    └────────────────────────┼─────────────────────────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │    Environment Variables     │
              │  NEXT_PUBLIC_API_URL         │
              │  BETTER_AUTH_SECRET          │
              │  DATABASE_URL (Neon PG)      │
              └──────────────────────────────┘
```

### Port Configuration

| Service | Port | Protocol | Environment |
|---------|------|----------|-------------|
| **Frontend** | 3000 | HTTP | Development |
| **Frontend** | 443 | HTTPS | Production (Vercel) |
| **Backend** | 8000 | HTTP | Development |
| **Backend** | 443 | HTTPS | Production |
| **PostgreSQL** | 5432 | TCP | Neon (Cloud) |

### Environment Variables

#### Frontend (.env.local)

```env
# Frontend environment variables
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-32-character-secret-key
```

#### Backend (.env)

```env
# Backend environment variables
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/db
BETTER_AUTH_SECRET=your-32-character-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

### Production Deployment

```
┌─────────────────────────────────────────────────────────────────┐
│                    Production Environment                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────┐           ┌─────────────────────────────┐
│   Vercel CDN        │           │   DigitalOcean/AWS          │
│   (Frontend)        │           │   (Backend + Dapr)          │
│   - Next.js App     │    HTTPS  │   - FastAPI Service         │
│   - Better Auth     │◀─────────▶│   - JWT Verification        │
└─────────────────────┘           └──────────────┬──────────────┘
                                                  │
                                                  ▼
                                    ┌─────────────────────────────┐
                                    │    Neon PostgreSQL          │
                                    │    (Serverless DB)          │
                                    └─────────────────────────────┘
```

| Component | Production Platform | URL |
|-----------|---------------------|-----|
| Frontend | Vercel | `https://your-app.vercel.app` |
| Backend | DigitalOcean/AWS | `https://api.your-domain.com` |
| Database | Neon | `ep-xxx.region.neon.tech` |

---

## Related Documents

| Document | Path | Purpose |
|----------|------|---------|
| Overview | `overview.md` | Project overview and features |
| Database Schema | `database/schema.md` | Detailed table definitions |
| API Spec | `api/rest-endpoints.md` | Endpoint contracts |
| UI Spec | `ui/components.md` | Frontend components |

---

## Version Information

| Item | Value |
|------|-------|
| Phase | Phase II: Full-Stack Web Application |
| Architecture Version | 2.0.0 |
| Last Updated | 2026-01-07 |
| Status | Draft |
