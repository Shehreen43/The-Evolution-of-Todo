---
name: sp.auth-setup
description: Configure Better Auth with JWT authentication for Phase II web application. Use when implementing user authentication, setting up JWT middleware, or integrating Better Auth with FastAPI backend.
---

# Authentication Setup

Configure Better Auth on frontend with JWT verification middleware on FastAPI backend.

## Architecture Overview

```
Frontend (Next.js)          Backend (FastAPI)
┌─────────────────┐         ┌─────────────────┐
│  Better Auth    │────────▶│  JWT Middleware │
│  (Session)      │  JWT    │  - Verify token │
│                 │         │  - Extract user │
└─────────────────┘         └─────────────────┘
        │                           │
        │                           ▼
        │                  ┌─────────────────┐
        │                  │  Protected API  │
        │                  │  (user_id from  │
        │                  │   JWT claim)    │
        └──────────────────└─────────────────┘
```

## Frontend: Better Auth Configuration

### Install Better Auth
```bash
cd frontend && npm install better-auth
```

### src/lib/auth.ts
```typescript
import { createAuth } from "better-auth";

export const auth = createAuth({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  plugins: [],
  advanced: {
    cookiePrefix: "todo-app",
  },
});

// Helper to get the current session
export async function getSession() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });
  return session;
}

// Helper to sign in
export async function signIn(email: string, password: string) {
  return await auth.api.signIn.email({
    body: {
      email,
      password,
    },
  });
}

// Helper to sign up
export async function signUp(email: string, password: string, name: string) {
  return await auth.api.signUp.email({
    body: {
      email,
      password,
      name,
    },
  });
}

// Helper to sign out
export async function signOut() {
  return await auth.api.signOut({
    headers: await headers(),
  });
}
```

### src/app/(auth)/layout.tsx (Auth Provider)
```typescript
"use client";

import { AuthProvider } from "better-auth/react";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AuthProvider
      authBaseURL={process.env.NEXT_PUBLIC_API_URL}
      fetchOptions={{
        credentials: "include",
      }}
    >
      {children}
    </AuthProvider>
  );
}
```

### src/components/auth/SignInForm.tsx
```typescript
"use client";

import { useState } from "react";
import { signIn } from "@/lib/auth";
import { useRouter } from "next/navigation";

export function SignInForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const { data, error } = await signIn(email, password);
      if (error) {
        setError(error.message || "Invalid credentials");
        return;
      }
      router.push("/dashboard");
    } catch (err) {
      setError("An error occurred. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="text-red-500 text-sm">{error}</div>
      )}
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="mt-1 block w-full border rounded-lg px-4 py-2"
          required
        />
      </div>
      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="mt-1 block w-full border rounded-lg px-4 py-2"
          required
        />
      </div>
      <button
        type="submit"
        className="w-full bg-neon-green-alt text-black font-semibold rounded-lg py-2 hover:bg-neon-green transition-colors shadow-lg shadow-neon-green-alt/30"
      >
        Sign In
      </button>
    </form>
  );
}
```

## Backend: JWT Verification Middleware

### Install JWT Dependencies
```bash
cd backend && uv add python-jose[cryptography] passlib[bcrypt]
```

### src/api/deps.py
```python
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.connection import get_db

settings = get_settings()
security = HTTPBearer()


class TokenPayload(BaseModel):
    sub: str
    email: Optional[str] = None
    exp: Optional[int] = None


class CurrentUser(BaseModel):
    id: str
    email: Optional[str] = None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CurrentUser:
    """Verify JWT token and extract user information."""
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.ALGORITHM],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return CurrentUser(id=user_id, email=payload.get("email"))
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def verify_user_access(
    current_user: CurrentUser = Depends(get_current_user),
    user_id: str = None,
) -> CurrentUser:
    """Verify the authenticated user has access to the requested resource."""
    if user_id and user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )
    return current_user
```

### src/api/middleware/auth.py
```python
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from jose import jwt, JWTError

from app.config import get_settings

settings = get_settings()


async def jwt_middleware(request: Request):
    """Middleware to verify JWT token on all protected routes."""
    # Skip auth for public endpoints
    public_paths = ["/health", "/docs", "/openapi.json", "/api/auth"]
    if any(request.url.path.startswith(path) for path in public_paths):
        return

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Missing authorization header"},
        )

    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization scheme",
            )

        # Verify token
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.ALGORITHM],
        )

        # Attach user info to request state
        request.state.user_id = payload.get("sub")
        request.state.user_email = payload.get("email")

    except JWTError as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
        )


def add_auth_middleware(app):
    """Add JWT middleware to FastAPI app."""
    app.middleware("http")(jwt_middleware)
```

### src/api/routes/tasks.py (Protected Routes)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.api.deps import get_current_user, CurrentUser
from app.db.connection import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/{user_id}/tasks", tags=["tasks"])


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    user_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    status_filter: Optional[str] = None,
):
    """List all tasks for the authenticated user."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks",
        )

    service = TaskService(db)
    tasks = await service.get_user_tasks(user_id, status_filter)
    return {"tasks": tasks, "total": len(tasks)}


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new task for the authenticated user."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user",
        )

    service = TaskService(db)
    task = await service.create_task(user_id, task_data)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific task."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    service = TaskService(db)
    task = await service.get_task(task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a task."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task",
        )

    service = TaskService(db)
    task = await service.update_task(task_id, user_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a task."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task",
        )

    service = TaskService(db)
    deleted = await service.delete_task(task_id, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return {"message": "Task deleted successfully", "id": task_id}


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,
    task_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Toggle task completion status."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this task",
        )

    service = TaskService(db)
    task = await service.toggle_complete(task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task
```

## Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-32-character-secret-key-here
```

### Backend (.env)
```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
BETTER_AUTH_SECRET=your-32-character-secret-key-here
ALGORITHM=HS256
```

## JWT Token Structure

### Payload Claims
```json
{
  "sub": "user_uuid_here",
  "email": "user@example.com",
  "exp": 1735689600,
  "iat": 1735084800,
  "iss": "better-auth"
}
```

| Claim | Type | Description |
|-------|------|-------------|
| sub | string | User ID (UUID) |
| email | string | User's email address |
| exp | int | Expiration timestamp (Unix epoch) |
| iat | int | Issued at timestamp |
| iss | string | Token issuer |

## Guardrails

### Do
- Use HS256 algorithm for JWT signing
- Share the same BETTER_AUTH_SECRET between frontend and backend
- Extract user_id from JWT token, not request parameters
- Filter all database queries by user_id
- Return 401 for missing/invalid tokens
- Return 403 for access to other users' resources

### Do Not
- Store JWT in localStorage on production (use httpOnly cookies)
- Pass user_id in URL for authorization (use JWT claim)
- Return user data from other users in any response
- Skip token validation on protected endpoints

## Triggers

Use this skill when:
- User asks to "setup authentication"
- Implementing Better Auth on frontend
- Adding JWT verification to FastAPI
- Securing API endpoints with user isolation
