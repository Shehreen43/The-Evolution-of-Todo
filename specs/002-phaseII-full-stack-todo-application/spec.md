# Phase II: Full-Stack Todo Web Application - Specification

This document provides the comprehensive specification for Phase II of "The Evolution of Todo" project, transforming the in-memory console application into a multi-user web application with persistent storage and authentication.

## 1. Executive Summary

### 1.1 Project Overview
- **Name:** The Evolution of Todo - Phase II
- **Phase:** Full-Stack Web Application
- **Goal:** Transform single-user console app to multi-user web app with authentication and persistent storage
- **Status:** In Development
- **Target:** Multi-user todo management platform

### 1.2 Phase Evolution Context
```
Phase I          Phase II          Phase III          Phase IV          Phase V
Console App  →   Web App      →   AI Chatbot    →   K8s Deploy   →   Cloud + Events
(In-Memory)      (PostgreSQL)      (MCP + OpenAI)     (Minikube)         (Kafka + Dapr)
```

### 1.3 Success Criteria
- [ ] Users can create accounts and authenticate securely
- [ ] Authenticated users can perform all CRUD operations on their tasks
- [ ] Task data persists across sessions in PostgreSQL
- [ ] All API responses in JSON format with proper error handling
- [ ] Frontend is fully responsive and accessible (WCAG 2.1 AA)
- [ ] All endpoints secured with JWT token verification
- [ ] Response time < 500ms for API calls
- [ ] Proper user data isolation (users only see their own tasks)

---

## 2. User Stories & Requirements

### 2.1 Authentication User Stories

#### US-AUTH-001: Sign Up
> **As a** new visitor,
> **I can** sign up with email, password, and name,
> **So that** I can create a personal account to manage my tasks.

**Acceptance Criteria:**
- [ ] Email address required with format validation
- [ ] Password minimum 8 characters (recommend mixing characters)
- [ ] Name optional
- [ ] Email uniqueness enforced in database
- [ ] Account created in database with hashed password
- [ ] Automatically sign in after successful signup
- [ ] Redirect to dashboard upon success
- [ ] Error messages for validation failures

#### US-AUTH-002: Sign In
> **As a** returning user,
> **I can** sign in with email and password,
> **So that** I can access my personal task list.

**Acceptance Criteria:**
- [ ] Email and password authentication
- [ ] Validate credentials against database
- [ ] Generate JWT token upon successful authentication
- [ ] Store token securely (httpOnly cookie or secure storage)
- [ ] Redirect to dashboard on success
- [ ] Show specific error message for invalid credentials
- [ ] Session persists across browser sessions

#### US-AUTH-003: Access My Tasks
> **As a** logged-in user,
> **I can** securely access my tasks through API requests,
> **So that** I can view and manage my personal todo list.

**Acceptance Criteria:**
- [ ] All API requests include JWT token in Authorization header
- [ ] Backend validates JWT token signature
- [ ] User ID extracted from token for data access
- [ ] Only tasks belonging to the authenticated user are returned
- [ ] Graceful handling of expired tokens
- [ ] 401 response for missing/invalid tokens

#### US-AUTH-004: Sign Out
> **As a** logged-in user,
> **I can** sign out of my account,
> **So that** I can prevent unauthorized access on shared devices.

**Acceptance Criteria:**
- [ ] Logout button available in the header
- [ ] Clear JWT token from storage
- [ ] Clear Better Auth session
- [ ] Redirect to sign-in page
- [ ] All subsequent API requests return 401

#### US-AUTH-005: User Data Isolation
> **As a** user,
> **I cannot** access other users' tasks,
> **So that** my data remains private and secure.

**Acceptance Criteria:**
- [ ] JWT user_id extracted from token, not request parameters
- [ ] All database queries include user_id filter
- [ ] 403 Forbidden response for unauthorized access attempts
- [ ] No cross-user data leakage in any API response
- [ ] Backend enforces isolation on every request

### 2.2 Task CRUD User Stories

#### US-CRUD-001: Create a New Task
> **As a** logged-in user,
> **I can** create a new task with a title and optional description,
> **So that** I can remember and track things I need to do.

**Acceptance Criteria:**
- [ ] Title field is required
- [ ] Title accepts 1-200 characters
- [ ] Description field is optional
- [ ] Description accepts 0-1000 characters
- [ ] Task is automatically associated with the logged-in user's ID
- [ ] New task appears at the top of the task list
- [ ] Visual feedback indicates successful creation
- [ ] Form clears after successful submission

#### US-CRUD-002: View All Tasks
> **As a** logged-in user,
> **I can** view all my tasks in a list,
> **So that** I can see what I need to do and track my progress.

**Acceptance Criteria:**
- [ ] Only tasks belonging to the logged-in user are displayed
- [ ] Task title is visible for each item
- [ ] Task description is visible (expandable or truncated)
- [ ] Completion status is visually indicated
- [ ] Creation date is displayed
- [ ] Empty state message shown when no tasks exist
- [ ] Tasks ordered by creation date (newest first)
- [ ] List is responsive on mobile and desktop

#### US-CRUD-003: Update a Task
> **As a** logged-in user,
> **I can** edit an existing task's title and/or description,
> **So that** I can correct mistakes or provide more details.

**Acceptance Criteria:**
- [ ] Can edit task title
- [ ] Can edit task description
- [ ] Changes persist immediately to the database
- [ ] Title validation same as create (1-200 characters, required)
- [ ] Description validation same as create (0-1000 characters, optional)
- [ ] Visual feedback indicates successful update
- [ ] Cancel button to discard changes

#### US-CRUD-004: Delete a Task
> **As a** logged-in user,
> **I can** delete a task I no longer need,
> **So that** I can keep my task list clean and relevant.

**Acceptance Criteria:**
- [ ] Delete button/option available for each task
- [ ] Confirmation dialog appears before deletion
- [ ] Task removed from UI immediately after confirmation
- [ ] No undo functionality required for basic version
- [ ] Visual feedback confirms deletion
- [ ] Only tasks owned by the user can be deleted

#### US-CRUD-005: Mark Task Complete
> **As a** logged-in user,
> **I can** toggle a task's completion status,
> **So that** I can track what I've accomplished.

**Acceptance Criteria:**
- [ ] Single click/tap toggles completion status
- [ ] Visual indication of completed state (strikethrough, checkmark, color change)
- [ ] Visual indication of incomplete state
- [ ] Status persists to database immediately
- [ ] No confirmation dialog required for toggle
- [ ] Completed tasks can be marked incomplete again
- [ ] Only tasks owned by the user can be toggled

---

## 3. Functional Requirements

### 3.1 Authentication Requirements

#### FR-AUTH-001: User Registration
| Requirement | Details |
|-------------|---------|
| **ID** | FR-AUTH-001 |
| **Priority** | Must Have |
| **Description** | Users must be able to create new accounts |
| **Preconditions** | User not logged in, on signup page |
| **Trigger** | Fill form, click "Sign Up" |
| **Main Flow** | 1. User enters email, password, name<br>2. Client validates email format<br>3. Client validates password strength<br>4. API call to create user<br>5. User created in database<br>6. JWT token generated<br>7. Redirect to dashboard |
| **Alternate Flow** | - Email exists: Show "Email already registered"<br>- Weak password: Show requirements<br>- Network error: Show retry option |
| **Postconditions** | User logged in, JWT stored |
| **Success Criteria** | New user can access dashboard |

#### FR-AUTH-002: User Login
| Requirement | Details |
|-------------|---------|
| **ID** | FR-AUTH-002 |
| **Priority** | Must Have |
| **Description** | Users must be able to log in to existing accounts |
| **Preconditions** | User not logged in, on login page |
| **Trigger** | Fill credentials, click "Sign In" |
| **Main Flow** | 1. User enters email and password<br>2. API call to authenticate<br>3. Verify credentials against database<br>4. Generate JWT token<br>5. Store token securely<br>6. Redirect to dashboard |
| **Alternate Flow** | - Wrong password: Show "Invalid credentials"<br>- User not found: Show "User not found"<br>- Network error: Show retry |
| **Postconditions** | User logged in, JWT stored |
| **Success Criteria** | User sees their dashboard |

#### FR-AUTH-003: User Logout
| Requirement | Details |
|-------------|---------|
| **ID** | FR-AUTH-003 |
| **Priority** | Must Have |
| **Description** | Users must be able to log out |
| **Preconditions** | User logged in |
| **Trigger** | Click "Logout" button |
| **Main Flow** | 1. User clicks logout<br>2. Clear JWT from storage<br>3. Clear Better Auth session<br>4. Redirect to login page |
| **Postconditions** | User logged out, no JWT |
| **Success Criteria** | User must log in again to access data |

#### FR-AUTH-004: JWT Verification Middleware
| Requirement | Details |
|-------------|---------|
| **ID** | FR-AUTH-004 |
| **Priority** | Must Have |
| **Description** | Backend verifies JWT on every request |
| **Implementation** | FastAPI dependency that extracts and verifies token |
| **Flow** | 1. Extract Authorization header<br>2. Parse "Bearer <token>"<br>3. Verify signature with shared secret<br>4. Decode payload<br>5. Extract user_id<br>6. Pass user_id to route handler |
| **Errors** | 401 if token missing, invalid, or expired |

#### FR-AUTH-005: User Isolation
| Requirement | Details |
|-------------|---------|
| **ID** | FR-AUTH-005 |
| **Priority** | Must Have |
| **Description** | Users can only access their own data |
| **Implementation** | Extract user_id from JWT, filter all queries |
| **Verification** | Compare JWT user_id with requested resource owner |
| **Errors** | 403 if trying to access another user's data |

### 3.2 Task CRUD Requirements

#### FR-CRUD-001: Create Task
| Requirement | Details |
|-------------|---------|
| **ID** | FR-CRUD-001 |
| **Priority** | Must Have |
| **Description** | Users must be able to create new tasks |
| **Preconditions** | User authenticated, on dashboard/task page |
| **Trigger** | Click "Add Task" button, fill form, submit |
| **Main Flow** | 1. User clicks "Add Task" button<br>2. Modal/form opens<br>3. User enters title (required) and description (optional)<br>4. User clicks "Create" button<br>5. API call with JWT token<br>6. Task saved with user_id<br>7. Task added to list UI |
| **Alternate Flow** | - Validation error: Show error message<br>- Network error: Show retry option |
| **Postconditions** | Task created, user sees confirmation, list updated |
| **Success Criteria** | Task appears in user's list with correct data |

#### FR-CRUD-002: View Tasks
| Requirement | Details |
|-------------|---------|
| **ID** | FR-CRUD-002 |
| **Priority** | Must Have |
| **Description** | Users must be able to view all their tasks |
| **Preconditions** | User authenticated, on dashboard |
| **Trigger** | Page load, navigate to tasks, pull-to-refresh |
| **Main Flow** | 1. Dashboard loads<br>2. API call with JWT token<br>3. Fetch tasks filtered by user_id<br>4. Display tasks in list |
| **Alternate Flow** | - Empty: Show empty state message<br>- Network error: Show retry button |
| **Postconditions** | Task list displayed |
| **Success Criteria** | Only user's tasks shown, ordered correctly |

#### FR-CRUD-003: Update Task
| Requirement | Details |
|-------------|---------|
| **ID** | FR-CRUD-003 |
| **Priority** | Must Have |
| **Description** | Users must be able to edit existing tasks |
| **Preconditions** | User authenticated, task exists and belongs to user |
| **Trigger** | Click edit icon/button on task |
| **Main Flow** | 1. User clicks edit on task<br>2. Edit modal/form opens with current values<br>3. User modifies title and/or description<br>4. User clicks "Save" button<br>5. API call with JWT token and updated data<br>6. Task updated in database<br>7. UI updates immediately |
| **Alternate Flow** | - Validation error: Show error message<br>- Network error: Show retry option<br>- Cancel: Discard changes |
| **Postconditions** | Task updated with new values |
| **Success Criteria** | Updated task shows in list with correct data |

#### FR-CRUD-004: Delete Task
| Requirement | Details |
|-------------|---------|
| **ID** | FR-CRUD-004 |
| **Priority** | Must Have |
| **Description** | Users must be able to delete tasks |
| **Preconditions** | User authenticated, task exists and belongs to user |
| **Trigger** | Click delete icon/button on task |
| **Main Flow** | 1. User clicks delete on task<br>2. Confirmation dialog appears<br>3. User confirms deletion<br>4. API call with JWT token<br>5. Task deleted from database<br>6. Task removed from UI |
| **Alternate Flow** | - Cancel: Dialog closes, no deletion<br>- Network error: Show error, task remains |
| **Postconditions** | Task removed from user's task list |
| **Success Criteria** | Task no longer appears in list |

#### FR-CRUD-005: Mark Complete
| Requirement | Details |
|-------------|---------|
| **ID** | FR-CRUD-005 |
| **Priority** | Must Have |
| **Description** | Users must be able to toggle task completion status |
| **Preconditions** | User authenticated, task exists and belongs to user |
| **Trigger** | Click checkbox/completion button on task |
| **Main Flow** | 1. User clicks completion toggle<br>2. UI updates immediately (optimistic)<br>3. API call with JWT token<br>4. Status persisted to database |
| **Alternate Flow** | - Network error: Revert UI, show error |
| **Postconditions** | Task completion status updated |
| **Success Criteria** | Visual change reflects completion state |

---

## 4. Technical Requirements

### 4.1 Authentication Technical Requirements

#### TR-AUTH-001: JWT Configuration
| Requirement | Details |
|-------------|---------|
| **ID** | TR-AUTH-001 |
| **Priority** | Must Have |
| **Algorithm** | HS256 (HMAC SHA-256) |
| **Secret** | BETTER_AUTH_SECRET environment variable |
| **Expiration** | 7 days (604800 seconds) |
| **Payload Claims** | sub (user_id), email, exp, iat, iss |

#### TR-AUTH-002: Token Storage
| Requirement | Details |
|-------------|---------|
| **ID** | TR-AUTH-002 |
| **Priority** | Should Have |
| **Frontend** | httpOnly cookie preferred, or localStorage |
| **Security** | Not accessible via JavaScript if possible |
| **Transmission** | Always over HTTPS |

#### TR-AUTH-003: Password Requirements
| Requirement | Details |
|-------------|---------|
| **ID** | TR-AUTH-003 |
| **Priority** | Must Have |
| **Minimum Length** | 8 characters |
| **Complexity** | At least one uppercase letter |
| **Storage** | Hashed (bcrypt/argon2) - handled by Better Auth |

#### TR-AUTH-004: Error Handling
| Requirement | Details |
|-------------|---------|
| **ID** | TR-AUTH-004 |
| **Priority** | Must Have |
| **401 Unauthorized** | Missing or invalid token |
| **403 Forbidden** | Valid token, wrong user |
| **422 Validation** | Invalid input data |
| **500 Server Error** | Generic error, no sensitive data |

### 4.2 Task CRUD Technical Requirements

#### TR-CRUD-001: Authentication Required
| Requirement | Details |
|-------------|---------|
| **ID** | TR-CRUD-001 |
| **Priority** | Must Have |
| **Description** | All task operations require authentication |
| **Implementation** | Every API request includes JWT in Authorization header |
| **Verification** | Backend verifies JWT before processing any request |
| **Error** | Return 401 Unauthorized if token missing/invalid |

#### TR-CRUD-002: User Isolation
| Requirement | Details |
|-------------|---------|
| **ID** | TR-CRUD-002 |
| **Priority** | Must Have |
| **Description** | Users can only access their own tasks |
| **Implementation** | All database queries include `WHERE user_id = ?` |
| **Verification** | Backend extracts user_id from JWT, not request |
| **Error** | Return 403 Forbidden if accessing another user's task |

#### TR-CRUD-003: Optimistic UI Updates
| Requirement | Details |
|-------------|---------|
| **ID** | TR-CRUD-003 |
| **Priority** | Should Have |
| **Description** | UI should update immediately for better UX |
| **Implementation** | Update local state before API call completes |
| **Rollback** | Revert state if API call fails |
| **Scope** | Mark complete, delete, update (not create) |

#### TR-CRUD-004: Error Handling
| Requirement | Details |
|-------------|---------|
| **ID** | TR-CRUD-004 |
| **Priority** | Must Have |
| **Network Errors** | Show retry button, offline indicator |
| **Validation Errors** | Show specific field errors |
| **Auth Errors** | Redirect to login |
| **Server Errors** | Show generic error message |

#### TR-CRUD-005: Loading States
| Requirement | Details |
|-------------|---------|
| **ID** | TR-CRUD-005 |
| **Priority** | Should Have |
| **Description** | Users should see loading indicators during async operations |
| **Implementation** | Show spinner or disabled state during API calls |
| **Scope** | Initial load, form submissions, deletions |
| **Duration** | < 100ms for optimistic updates, show for > 300ms |

---

## 5. System Architecture

### 5.1 High-Level Architecture
```
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
                │  │ email           │◀───────│ user_id (FK) ──────────┼─────┘
                │  │ name            │        │ title                   │     │
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

### 5.2 Technology Stack

#### Frontend
| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | Next.js 16+ | React framework with App Router |
| Language | TypeScript | Type safety |
| Styling | Tailwind CSS | Utility-first CSS |
| Auth | Better Auth | Session management |
| HTTP Client | Built-in fetch | API communication |
| Deployment | Vercel | Hosting platform |

#### Backend
| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | FastAPI | Python web framework |
| Language | Python 3.13+ | Runtime environment |
| ORM | SQLModel | Database ORM (SQLAlchemy + Pydantic) |
| Database | Neon PostgreSQL | Serverless database |
| Auth | JWT (Python-jose) | Token verification |
| Server | Uvicorn + ASGI | ASGI server |

#### Development Tools
| Tool | Purpose |
|------|---------|
| Claude Code | AI agent for implementation |
| Spec-Kit Plus | Specification management |
| UV | Python package manager |
| Git | Version control |

### 5.3 Component Architecture

#### Frontend Components
| Category | Components | Type |
|----------|------------|------|
| **Pages** | `page.tsx` (dashboard), `login/page.tsx`, `signup/page.tsx` | Server + Client |
| **UI** | `Button`, `Input`, `Card`, `Modal` | Client |
| **Tasks** | `TaskList`, `TaskItem`, `TaskForm` | Client |
| **Auth** | `AuthProvider`, `useAuth` | Client |
| **API** | `apiClient.ts`, `tasks/route.ts` | Server |

#### Backend Components
| Component | File | Purpose |
|-----------|------|---------|
| **Models** | `app/models/task.py`, `app/models/user.py` | SQLModel entities |
| **Schemas** | `app/schemas/task.py`, `app/schemas/user.py` | Pydantic validation |
| **Routes** | `app/api/routes/tasks.py` | API endpoints |
| **Services** | `app/services/task_service.py` | Business logic |
| **Dependencies** | `app/api/deps.py` | Auth and DB dependencies |

---

## 6. API Specification

### 6.1 Base URLs
| Environment | URL |
|-------------|-----|
| **Development** | `http://localhost:8000` |
| **Production** | `https://api.yourdomain.com` |

### 6.2 Authentication
All API endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

### 6.3 Common Response Codes
| Code | Name | Description |
|------|------|-------------|
| 200 | OK | Success |
| 201 | Created | Resource successfully created |
| 204 | No Content | Success with no response body |
| 400 | Bad Request | Validation error or invalid input |
| 401 | Unauthorized | Missing or invalid JWT token |
| 403 | Forbidden | Accessing another user's resource |
| 404 | Not Found | Resource does not exist |
| 500 | Internal Server Error | Server error |

### 6.4 Task Endpoints

#### 1. List All Tasks
**Endpoint:** `GET /api/{user_id}/tasks`

**Description:** Retrieve all tasks for the authenticated user.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | string | Yes | Must match authenticated user's ID from JWT |

**Query Parameters (Optional):**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| status | string | "all" | Filter by status: "all", "pending", "completed" |
| sort | string | "created" | Sort field: "created", "title", "updated" |
| order | string | "desc" | Sort order: "asc", "desc" |
| limit | integer | 100 | Maximum number of results |
| offset | integer | 0 | Number of results to skip |

**Success Response (200):**
```json
[
  {
    "id": 1,
    "user_id": "user_123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "medium",
    "completed": false,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

#### 2. Create Task
**Endpoint:** `POST /api/{user_id}/tasks`

**Description:** Create a new task for the authenticated user.

**Request Body:**
```json
{
  "title": "Task title (required, 1-200 chars)",
  "description": "Task description (optional, max 1000 chars)",
  "priority": "medium"
}
```

**Success Response (201):**
```json
{
  "id": 3,
  "user_id": "user_123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "high",
  "completed": false,
  "created_at": "2024-01-15T12:00:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

#### 3. Get Task Details
**Endpoint:** `GET /api/{user_id}/tasks/{id}`

**Description:** Retrieve details of a specific task.

**Success Response (200):** Same as single task object above

#### 4. Update Task
**Endpoint:** `PUT /api/{user_id}/tasks/{id}`

**Description:** Update an existing task's title and/or description.

**Request Body:**
```json
{
  "title": "Updated title (optional)",
  "description": "Updated description (optional)",
  "priority": "low"
}
```

**Success Response (200):** Updated task object

#### 5. Delete Task
**Endpoint:** `DELETE /api/{user_id}/tasks/{id}`

**Description:** Delete a task permanently.

**Success Response (200):**
```json
{
  "message": "Task deleted successfully",
  "id": 1
}
```

#### 6. Toggle Task Completion
**Endpoint:** `PATCH /api/{user_id}/tasks/{id}/complete`

**Description:** Toggle a task's completion status (complete/incomplete).

**Success Response (200):** Updated task object with toggled completed status

### 6.5 Authentication Endpoints

#### Sign Up
**Endpoint:** `POST /api/auth/signup`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

#### Sign In
**Endpoint:** `POST /api/auth/signin`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Success Response:**
```json
{
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2024-01-22T10:00:00Z"
}
```

---

## 7. Database Schema

### 7.1 Entity Relationship Diagram
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

### 7.2 Tables

#### 1. users (Managed by Better Auth)
**Purpose:** Store user account information

**Columns:**
| Column | Type | Constraints | Default | Description |
|--------|------|-------------|---------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | - | Unique user identifier (UUID format) |
| email | VARCHAR(255) | UNIQUE, NOT NULL | - | User's email address |
| name | VARCHAR(255) | NOT NULL | - | User's display name |
| password_hash | VARCHAR(255) | NOT NULL | - | Hashed password (bcrypt) |
| created_at | TIMESTAMP | - | CURRENT_TIMESTAMP | Account creation time |
| updated_at | TIMESTAMP | - | CURRENT_TIMESTAMP | Last update time |

**Indexes:**
| Index Type | Columns | Purpose |
|------------|---------|---------|
| PRIMARY KEY | id | Unique row identifier |
| UNIQUE | email | Fast lookup during login |

#### 2. tasks
**Purpose:** Store todo task information

**Columns:**
| Column | Type | Constraints | Default | Description |
|--------|------|-------------|---------|-------------|
| id | SERIAL | PRIMARY KEY | - | Auto-incrementing task identifier |
| user_id | VARCHAR(255) | NOT NULL, FK | - | Foreign key to users.id |
| title | VARCHAR(200) | NOT NULL | - | Task title |
| description | TEXT | - | NULL | Optional task description |
| completed | BOOLEAN | - | FALSE | Completion status |
| created_at | TIMESTAMP | - | CURRENT_TIMESTAMP | Task creation time |
| updated_at | TIMESTAMP | - | CURRENT_TIMESTAMP | Last update time |

**Indexes:**
| Index Type | Columns | Purpose |
|------------|---------|---------|
| PRIMARY KEY | id | Unique task identifier |
| INDEX | user_id | Filter user's tasks (critical) |
| INDEX | completed | Filter by status |
| INDEX | created_at | Sort by date |

**Foreign Keys:**
| Column | References | On Delete | Description |
|--------|------------|-----------|-------------|
| user_id | users.id | CASCADE | Deleting user deletes all their tasks |

---

## 8. User Interface Specification

### 8.1 Page Structure
```
app/
├── layout.tsx (root layout)
├── page.tsx (landing/home)
├── (auth)/
│   ├── layout.tsx (auth layout)
│   ├── signin/
│   │   └── page.tsx
│   └── signup/
│       └── page.tsx
└── dashboard/
    ├── layout.tsx (dashboard layout)
    └── page.tsx (main dashboard)
```

### 8.2 Pages

#### Landing Page (/)
**File:** `app/page.tsx`
**Type:** Public page (Server Component)

**Purpose:**
- Welcome page for unauthenticated users
- Marketing/intro content about the app

**Content:**
- Hero section with app description
- Key features showcase
- Call-to-action buttons: 'Get Started' → /signup, 'Sign In' → /signin
- Optional: testimonials, screenshots

#### Sign Up Page (/signup)
**File:** `app/(auth)/signup/page.tsx`
**Type:** Public page (Client Component)
**Route Group:** (auth) - uses auth layout

**Purpose:**
- User registration

**Components:**
- SignUpForm component
- Link to /signin ('Already have an account?')

**Form Fields:**
- Name (text input)
- Email (email input)
- Password (password input with show/hide)
- Confirm Password (password input)
- Submit button

#### Sign In Page (/signin)
**File:** `app/(auth)/signin/page.tsx`
**Type:** Public page (Client Component)
**Route Group:** (auth) - uses auth layout

**Purpose:**
- User login

**Components:**
- SignInForm component
- Link to /signup ('Don't have an account?')
- Optional: 'Forgot password?' link

**Form Fields:**
- Email (email input)
- Password (password input with show/hide)
- Optional: Remember me checkbox
- Submit button

#### Dashboard Page (/dashboard)
**File:** `app/dashboard/page.tsx`
**Type:** Protected page (Mixed - Server Component with Client Components)
**Layout:** Uses dashboard layout

**Purpose:**
- Main application interface
- View and manage tasks

**Components:**
- Navigation component (from layout)
- AddTaskForm component (client)
- TaskList component (client)
  - Multiple TaskItem components

### 8.3 Components

#### TaskList Component
**Purpose:** Display list of tasks with filtering and sorting

**Props:**
```typescript
interface TaskListProps {
  tasks: Task[]
  onTaskUpdate: (taskId: number, updates: Partial<Task>) => void
  onTaskDelete: (taskId: number) => void
  onTaskToggle: (taskId: number) => void
  isLoading?: boolean
  error?: string | null
}
```

#### TaskItem Component
**Purpose:** Display individual task with actions

**Props:**
```typescript
interface TaskItemProps {
  task: Task
  onUpdate: (updates: Partial<Task>) => void
  onDelete: () => void
  onToggle: () => void
}
```

#### AddTaskForm Component
**Purpose:** Form to create new tasks

**Props:**
```typescript
interface AddTaskFormProps {
  onSubmit: (task: CreateTaskData) => Promise<void>
}
```

#### EditTaskForm Component
**Purpose:** Edit existing task (modal or inline)

**Props:**
```typescript
interface EditTaskFormProps {
  task: Task
  onSave: (updates: Partial<Task>) => Promise<void>
  onCancel: () => void
}
```

#### SignUpForm Component
**Purpose:** User registration form

**Fields:**
- Name (required)
- Email (required, email format)
- Password (required, min 8 chars)
- Confirm Password (must match)

#### SignInForm Component
**Purpose:** User login form

**Fields:**
- Email (required)
- Password (required)

#### Navigation Component
**Purpose:** Main app navigation/header

**Features:**
- App logo/title
- User display (when logged in)
  - Show user name
  - Avatar (optional)
  - Sign out button
- Responsive: collapse to hamburger on mobile

### 8.4 UI Patterns

#### Buttons
| Variant | Tailwind Classes | Usage |
|---------|------------------|-------|
| Primary | `bg-blue-600 hover:bg-blue-700 text-white` | Main actions (submit, save) |
| Secondary | `bg-gray-600 hover:bg-gray-700 text-white` | Cancel, back |
| Danger | `bg-red-600 hover:bg-red-700 text-white` | Delete, confirm delete |
| Disabled | `opacity-50 cursor-not-allowed` | When action unavailable |

#### Inputs
| State | Tailwind Classes |
|-------|------------------|
| Default | `border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500` |
| Error | `border border-red-500 focus:ring-2 focus:ring-red-500` |
| Disabled | `bg-gray-100 cursor-not-allowed` |

#### Cards
| Property | Tailwind Classes |
|----------|------------------|
| Container | `bg-white rounded-lg shadow-md` |
| Padding | `p-4` or `p-6` |
| Border | `border border-gray-200` |
| Hover | `hover:shadow-lg transition-shadow` |

---

## 9. Security Considerations

### 9.1 Defense in Depth
```
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

### 9.2 User Isolation
Every database query must:
1. Include JWT token in Authorization header
2. Verify token signature using shared secret
3. Extract user_id from token
4. Filter all database queries by user_id
5. Return only tasks belonging to that user

### 9.3 Security Controls
| Control | Implementation |
|---------|----------------|
| **HTTPS** | All traffic encrypted in production |
| **Password Hashing** | bcrypt (handled by Better Auth) |
| **JWT Signing** | HS256 with shared secret |
| **Token Expiration** | 7 days (604800 seconds) |
| **User Isolation** | All queries filtered by user_id |
| **CORS** | Whitelist frontend origins only |
| **Secret Management** | Environment variables only |

### 9.4 Error Responses
| Status Code | Scenario | Response |
|-------------|----------|----------|
| 400 | Validation error | `{"detail": "Error message"}` |
| 401 | Missing/invalid token | `{"detail": "Could not validate credentials"}` |
| 403 | Valid token, wrong user | `{"detail": "Not authorized"}` |
| 404 | Resource not found | `{"detail": "Not found"}` |
| 500 | Server error | `{"detail": "Internal server error"}` |

---

## 10. Performance Considerations

### 10.1 Critical Indexes
| Query Pattern | Recommended Index |
|---------------|-------------------|
| List user's tasks | INDEX (user_id) |
| Filter pending tasks | INDEX (user_id, completed) WHERE completed = FALSE |
| Sort by date | INDEX (created_at DESC) |
| Filter by status | INDEX (completed) |

### 10.2 Optimization Tips
1. **Index foreign keys**: Always index `user_id` on tasks table
2. **Limit results**: Use pagination for large task lists
3. **Connection pooling**: Use for production performance
4. **Async operations**: Use async SQLModel for FastAPI

### 10.3 Loading States
| Page | Loading Indicator |
|------|-------------------|
| Landing | Static (SSG) - instant |
| Sign Up | Spinner on submit button |
| Sign In | Spinner on submit button |
| Dashboard | Skeleton loaders |

---

## 11. Development Guidelines

### 11.1 Frontend Guidelines
- Use server components by default for performance
- Only use client components when interactivity needed
- All styling via Tailwind CSS (no custom CSS)
- Use client components for interactivity with 'use client' directive
- Implement optimistic UI updates where appropriate
- Handle errors gracefully with proper states

### 11.2 Backend Guidelines
- Use async/await for all database operations
- Define types for all function parameters and returns
- Validate all API inputs with Pydantic schemas
- Define database models with SQLModel
- Always filter queries by user_id from JWT for user isolation
- Return proper HTTP status codes (401, 403, 404)
- Use dependency injection for auth and DB connections
- Keep business logic in service classes
- Configure CORS for frontend communication
- Use environment variables for secrets

### 11.3 API Client Pattern
All backend API calls go through a centralized client:
```typescript
// lib/api.ts
class ApiClient {
  private baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  private async getHeaders() {
    const session = await getSession();
    return {
      'Content-Type': 'application/json',
      ...(session?.token && { 'Authorization': `Bearer ${session.token}` }),
    };
  }

  // Implement get, post, put, delete, patch methods
}
```

---

## 12. Testing Strategy

### 12.1 Unit Tests
- API endpoint tests with mocked database
- Service layer tests with mocked database
- Component tests with mocked API
- Validation schema tests

### 12.2 Integration Tests
- End-to-end API tests with real database
- Authentication flow tests
- User isolation tests
- Database transaction tests

### 12.3 Performance Tests
- API response time tests
- Concurrent user tests
- Database query performance
- Memory usage monitoring

---

## 13. Deployment

### 13.1 Development Environment
| Service | Port | Protocol | Environment |
|---------|------|----------|-------------|
| **Frontend** | 3000 | HTTP | Development |
| **Backend** | 8000 | HTTP | Development |
| **PostgreSQL** | 5432 | TCP | Neon (Cloud) |

### 13.2 Production Deployment
| Component | Production Platform | URL |
|-----------|---------------------|-----|
| Frontend | Vercel | `https://your-app.vercel.app` |
| Backend | DigitalOcean/AWS | `https://api.your-domain.com` |
| Database | Neon | `ep-xxx.region.neon.tech` |

### 13.3 Environment Variables
#### Frontend (.env.local)
```env
# Frontend environment variables
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-32-character-secret-key-here
DATABASE_URL=postgresql+asyncpg://user:password@host/db
```

#### Backend (.env)
```env
# Backend environment variables
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/db
BETTER_AUTH_SECRET=your-32-character-secret-key-here
ALGORITHM=HS256
```

---

## 14. Related Documents

| Document | Path | Purpose |
|----------|------|---------|
| Architecture | `architecture.md` | System architecture |
| Overview | `overview.md` | Project overview |
| Task CRUD | `features/task-crud.md` | Task operations |
| Authentication | `features/authentication.md` | Auth flow |
| API Spec | `api/rest-endpoints.md` | API endpoints |
| Database Schema | `database/schema.md` | Entity definitions |
| UI Components | `ui/components.md` | Component specifications |
| UI Pages | `ui/pages.md` | Page specifications |

---

## 15. Version Information

| Item | Value |
|------|-------|
| Phase | Phase II: Full-Stack Web Application |
| Specification Version | 2.0.0 |
| Status | Draft |
| Last Updated | 2026-01-07 |
