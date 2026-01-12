---
name: sp.web-scaffold
description: Scaffold a full-stack Next.js 16 + FastAPI monorepo with proper folder structure for Phase II. Use when starting Phase II web application development, creating frontend/backend structure, or setting up the monorepo.
---

# Web Application Scaffolder

Create a complete full-stack monorepo structure for the Phase II web application with Next.js 16 and latest stable dependencies.

## Prerequisites

- Node.js 20+ for Next.js 16
- Python 3.13+ for FastAPI
- UV package manager installed
- Git initialized

## Monorepo Structure

Generate this structure:
```
project/
├── frontend/                    # Next.js 16 application
│   ├── .gitignore
│   ├── .env.local
│   ├── next.config.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── postcss.config.js
│   ├── eslint.config.mjs
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── globals.css
│   │   │   ├── (auth)/
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── signin/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── signup/
│   │   │   │       └── page.tsx
│   │   │   └── dashboard/
│   │   │       ├── layout.tsx
│   │   │       └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   └── Modal.tsx
│   │   │   ├── tasks/
│   │   │   │   ├── TaskList.tsx
│   │   │   │   ├── TaskItem.tsx
│   │   │   │   ├── TaskForm.tsx
│   │   │   │   └── TaskFilter.tsx
│   │   │   └── auth/
│   │   │       ├── SignInForm.tsx
│   │   │       └── SignUpForm.tsx
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   └── utils.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   └── hooks/
│   │       └── useTasks.ts
│   └── CLAUDE.md
│
├── backend/                     # FastAPI application
│   ├── .gitignore
│   ├── .env
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── task.py
│   │   │   └── database.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── task.py
│   │   │   └── user.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   └── tasks.py
│   │   │   └── middleware/
│   │   │       ├── __init__.py
│   │   │       └── auth.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── task_service.py
│   │   └── db/
│   │       ├── __init__.py
│   │       └── connection.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_tasks.py
│   └── CLAUDE.md
│
├── docker-compose.yml
├── .gitignore
├── CLAUDE.md
├── README.md
└── constitution.md
```

## Frontend Configuration (Next.js 16)

### package.json
```json
{
  "name": "todo-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "16.0.0",
    "react": "19.0.0",
    "react-dom": "19.0.0",
    "better-auth": "1.1.0",
    "@tanstack/react-query": "5.60.0",
    "axios": "1.7.7"
  },
  "devDependencies": {
    "typescript": "5.6.3",
    "@types/node": "22.9.0",
    "@types/react": "19.0.0",
    "@types/react-dom": "19.0.0",
    "tailwindcss": "3.4.14",
    "postcss": "8.4.47",
    "autoprefixer": "10.4.20",
    "eslint": "9.14.0",
    "eslint-config-next": "16.0.0"
  }
}
```

### next.config.ts
```typescript
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
  images: {
    domains: [],
  },
};

export default nextConfig;
```

### tsconfig.json
```json
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### tailwind.config.ts
```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'neon-green': '#39ff14',
        'neon-green-alt': '#17ED61',
        'neon-green-dark': '#2ecc71',
        'neon-green-light': '#7fff00',
        dark: {
          900: '#0a0a0a',
          800: '#121212',
          700: '#1e1e1e',
        },
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
};

export default config;
```

## Backend Configuration (FastAPI + SQLModel)

### pyproject.toml
```toml
[project]
name = "todo-backend"
version = "0.1.0"
description = "FastAPI backend for The Evolution of Todo"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn>=0.32.0",
    "sqlmodel>=0.0.21",
    "psycopg[binary]>=3.2.3",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "pydantic>=2.10.1",
    "python-multipart>=0.0.12",
    "httpx>=0.28.0",
    "alembic>=1.15.1",
    "pydantic-settings>=2.6.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.3",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "black>=24.10.0",
    "ruff>=0.8.1",
    "mypy>=1.13.0",
    "httpx>=0.28.0",
]

[build-system]
requires = ["setuptools>=75.6.0"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
target-version = ['py313']

[tool.ruff]
line-length = 100
target-version = "py313"
```

### src/main.py
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="The Evolution of Todo API",
    description="Full-Stack Todo Web Application API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### src/config.py
```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "The Evolution of Todo"
    DATABASE_URL: str
    BETTER_AUTH_SECRET: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()
```

### src/models/task.py
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from uuid import uuid4


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
```

## Docker Configuration

### docker-compose.yml
```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/todo
      - BETTER_AUTH_SECRET=your-secret-here
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: todo
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## Guardrails

### Do
- Use Next.js 16 App Router for frontend
- Use SQLModel for database models
- Use Pydantic for request/response schemas
- Configure CORS for frontend origin
- Use environment variables for all secrets
- Create CLAUDE.md files in both frontend and backend
- Use React 19 with Next.js 16

### Do Not
- Skip authentication middleware
- Hardcode database URLs
- Mix frontend and backend code
- Use client-side routing for API calls

## Triggers

Use this skill when:
- User says "setup Phase II web application"
- User asks to "create monorepo structure"
- Starting Phase II development
- Need to scaffold Next.js 16 + FastAPI project
