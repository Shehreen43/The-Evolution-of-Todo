# Phase II: Full-Stack Todo Web Application

## Overview

This document provides a comprehensive overview of the Full-Stack Todo Web Application, the second phase in "The Evolution of Todo" project. This phase transforms the in-memory console application into a multi-user web application with persistent storage and user authentication.

---

## Purpose

The **Evolution of Todo** project simulates the real-world evolution of software systems, demonstrating how applications scale from simple scripts to distributed, cloud-native AI systems. Phase II bridges the gap between a single-user console application and a multi-user web platform.

### Key Objectives

1. **Persistent Storage**: Transition from in-memory data to Neon Serverless PostgreSQL database
2. **Multi-User Support**: Enable multiple users to have their own private task lists
3. **Authentication**: Implement secure user signup/signin using Better Auth with JWT tokens
4. **Web Interface**: Create a responsive web UI using Next.js 16+ with modern patterns
5. **RESTful API**: Expose all functionality through a well-designed API backend

### Why This Phase Matters

| Aspect | Phase I (Console) | Phase II (Web) |
|--------|-------------------|----------------|
| Users | Single user | Multiple users |
| Data Persistence | In-memory (lost on restart) | Persistent PostgreSQL |
| Access | CLI only | Web browser |
| Authentication | None | JWT-based auth |
| Deployment | Local script | Deployable web app |

---

## Current Phase: Phase II - Full-Stack Web Application

### Phase Status: **IN PROGRESS**

### Evolution Context

```
Phase I          Phase II          Phase III          Phase IV          Phase V
Console App  →   Web App      →   AI Chatbot    →   K8s Deploy   →   Cloud + Events
(In-Memory)      (PostgreSQL)      (MCP + OpenAI)     (Minikube)         (Kafka + Dapr)
```

### Phase II Deliverables

| Deliverable | Description | Status |
|-------------|-------------|--------|
| RESTful API | Backend endpoints for all CRUD operations | Pending |
| Next.js Frontend | Responsive web UI with App Router | Pending |
| Database Schema | SQLModel entities for users and tasks | Pending |
| Authentication | Better Auth + JWT integration | Pending |
| User Isolation | Each user sees only their own tasks | Pending |

### Success Criteria

- [ ] Users can create accounts and authenticate
- [ ] Authenticated users can perform all CRUD operations
- [ ] Task data persists across sessions
- [ ] API responses in JSON format
- [ ] Frontend fully responsive
- [ ] All endpoints secured with JWT verification
- [ ] Response time < 500ms for API calls

---

## Technology Stack

### Frontend

| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | Next.js 16+ | React framework with App Router |
| Language | TypeScript | Type-safe development |
| Styling | Tailwind CSS | Utility-first CSS |
| Auth | Better Auth | Authentication library |
| HTTP Client | Built-in fetch | API communication |
| Deployment | Vercel | Hosting platform |

### Backend

| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | FastAPI | Python web framework |
| Language | Python 3.13+ | Runtime environment |
| ORM | SQLModel | Database ORM (SQLAlchemy + Pydantic) |
| Database | Neon PostgreSQL | Serverless database |
| Auth | JWT (Python-jose) | Token verification |
| Server | Uvicorn + ASGI | ASGI server |

### Development Tools

| Tool | Purpose |
|------|---------|
| Claude Code | AI agent for implementation |
| Spec-Kit Plus | Specification management |
| UV | Python package manager |
| Git | Version control |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Login/    │  │   Task      │  │   API Client            │  │
│  │   Signup    │  │   Dashboard │  │   (JWT + Fetch)         │  │
│  └─────────────┘  └─────────────┘  └───────────┬─────────────┘  │
└────────────────────────────────────────────────┼─────────────────┘
                                                 │ HTTPS
                                                 │
┌────────────────────────────────────────────────┼─────────────────┐
│                      Backend (FastAPI)          │                 │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┴─────────────┐   │
│  │   JWT       │  │   Task      │  │   REST API Endpoints   │   │
│  │   Auth      │  │   Service   │  │   /api/{user_id}/tasks │   │
│  └─────────────┘  └─────────────┘  └───────────┬─────────────┘   │
│                          │                      │                 │
│                          ▼                      ▼                 │
│                ┌─────────────────────┐  ┌─────────────┐         │
│                │   SQLModel Layer    │  │   Database  │         │
│                │   (Task, User)      │  │   Neon PG   │         │
│                └─────────────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Features

### Basic Level Functionality

These five features form the MVP for Phase II, building upon Phase I's console implementation:

#### 1. Add Task

- [ ] User can create a new task with title (required) and description (optional)
- [ ] Title must be 1-200 characters
- [ ] Description can be 0-1000 characters
- [ ] New tasks default to incomplete status
- [ ] Task is associated with authenticated user

#### 2. Delete Task

- [ ] User can remove a task by ID
- [ ] Only tasks belonging to the user can be deleted
- [ ] Deletion is permanent (no soft delete for MVP)
- [ ] Success/failure response with appropriate message

#### 3. Update Task

- [ ] User can modify task title and/or description
- [ ] Only tasks belonging to the user can be updated
- [ ] Partial updates supported (update just title OR just description)
- [ ] Validation rules same as Create Task

#### 4. View Task List

- [ ] User can see all their tasks
- [ ] Tasks display with title, status, created date
- [ ] Only tasks belonging to the user are shown (user isolation)
- [ ] Responsive design for mobile and desktop

#### 5. Mark as Complete

- [ ] User can toggle task completion status
- [ ] Visual indication of completed vs pending tasks
- [ ] Only tasks belonging to the user can be toggled
- [ ] Completion timestamp recorded (optional for MVP)

### Feature Priority

| Priority | Feature | Phase | Points |
|----------|---------|-------|--------|
| P1 | Add Task | I (Console) | Basic |
| P1 | View Task List | I (Console) | Basic |
| P1 | Mark Complete | I (Console) | Basic |
| P1 | Delete Task | I (Console) | Basic |
| P2 | Update Task | I (Console) | Basic |
| P2 | Priorities/Tags | II+ (Intermediate) | Intermediate |
| P2 | Search/Filter | II+ (Intermediate) | Intermediate |
| P3 | Recurring Tasks | V (Advanced) | Advanced |
| P3 | Due Dates/Reminders | V (Advanced) | Advanced |

---

## Development Principles

### Spec-Driven Development

All implementation must follow the Spec-Driven Development (SDD) workflow:

```
1. Write/Refine Specification   → spec.md
2. Generate Architecture Plan    → plan.md
3. Break into Atomic Tasks       → tasks.md
4. Implement via Claude Code     → Code generation only
5. Test and Validate             → Verify against spec
```

### No Manual Coding Rule

**Constraint**: Code must not be written manually. All implementation is generated via Claude Code CLI using the specifications.

This approach ensures:
- Traceability from requirements to code
- Consistent code quality
- Documented decision-making
- Reproducible builds

### Monorepo Organization

The project uses a monorepo structure for better context sharing:

```
.specs/                    # All specifications
  /002-phaseII-.../
    /features/            # Feature specs
    /api/                 # API specs
    /database/            # Schema specs
    /ui/                  # UI specs
.frontend/                # Next.js application
.backend/                 # FastAPI application
```

### Authentication Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────────────┐
│   User      │────▶│  Frontend   │────▶│   Backend (FastAPI)     │
│  Browser    │     │  (Next.js)  │     │   - Verify JWT          │
│             │◀────│  - Better   │◀────│   - Extract user_id     │
│             │     │    Auth     │     │   - Filter by user      │
└─────────────┘     └─────────────┘     └─────────────────────────┘
```

### User Isolation

Every API request must:
1. Include JWT token in Authorization header
2. Verify token signature using shared secret
3. Extract user_id from token
4. Filter all database queries by user_id
5. Return only tasks belonging to that user

---

## Out of Scope for Phase II

The following are explicitly NOT included in Phase II:

- [ ] AI/Chatbot interface (Phase III)
- [ ] Kubernetes deployment (Phase IV)
- [ ] Kafka/Dapr event architecture (Phase V)
- [ ] Voice commands (Bonus)
- [ ] Urdu language support (Bonus)
- [ ] Advanced features (priorities, tags, search, filter, sort)

---

## Related Documents

| Document | Path | Purpose |
|----------|------|---------|
| Constitution | `.specify/memory/constitution.md` | Project governance |
| Phase II Spec | `.specs/002-phaseII-.../spec.md` | Feature requirements |
| Phase II Plan | `.specs/002-phaseII-.../plan.md` | Architecture decisions |
| Phase II Tasks | `.specs/002-phaseII-.../tasks.md` | Implementation tasks |
| API Spec | `.specs/002-phaseII-.../api/rest-endpoints.md` | API contracts |
| DB Schema | `.specs/002-phaseII-.../database/schema.md` | Entity definitions |
| UI Spec | `.specs/002-phaseII-.../ui/components.md` | Component designs |

---

## Version Information

| Item | Value |
|------|-------|
| Project | The Evolution of Todo |
| Current Phase | Phase II: Full-Stack Web Application |
| Phase Status | In Progress |
| Specification Version | 1.0.0 |
| Last Updated | 2026-01-07 |

---

## Quick Reference

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

### Authentication

- Header: `Authorization: Bearer <token>`
- Token: JWT signed with `BETTER_AUTH_SECRET`
- Verification: Python-jose on FastAPI side

### Database

- Provider: Neon Serverless PostgreSQL
- ORM: SQLModel
- Connection: `DATABASE_URL` environment variable
