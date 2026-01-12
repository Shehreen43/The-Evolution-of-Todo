# Feature: Task CRUD Operations

This document defines the Task CRUD (Create, Read, Update, Delete) operations feature for Phase II of "The Evolution of Todo" project.

## Overview

| Attribute | Value |
|-----------|-------|
| **Feature ID** | task-crud |
| **Priority** | P1 (Must Have) |
| **Phase** | Phase II (Full-Stack Web) |
| **Dependencies** | authentication |
| **Status** | Draft |

---

## User Stories

### US-001: Create a New Task

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

---

### US-002: View All Tasks

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

---

### US-003: Update a Task

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

---

### US-004: Delete a Task

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

---

### US-005: Mark Task Complete

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

## Functional Requirements

### FR-CRUD-001: Create Task

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

### FR-CRUD-002: View Tasks

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

### FR-CRUD-003: Update Task

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

### FR-CRUD-004: Delete Task

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

### FR-CRUD-005: Mark Complete

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

## Technical Requirements

### TR-CRUD-001: Authentication Required

| Requirement | Details |
|-------------|---------|
| **ID** | TR-CRUD-001 |
| **Priority** | Must Have |
| **Description** | All task operations require authentication |
| **Implementation** | Every API request includes JWT in Authorization header |
| **Verification** | Backend verifies JWT before processing any request |
| **Error** | Return 401 Unauthorized if token missing/invalid |

### TR-CRUD-002: User Isolation

| Requirement | Details |
|-------------|---------|
| **ID** | TR-CRUD-002 |
| **Priority** | Must Have |
| **Description** | Users can only access their own tasks |
| **Implementation** | All database queries include `WHERE user_id = ?` |
| **Verification** | Backend extracts user_id from JWT, not request |
| **Error** | Return 403 Forbidden if accessing another user's task |

### TR-CRUD-003: Optimistic UI Updates

| Requirement | Details |
|-------------|---------|
| **ID** | TR-CRUD-003 |
| **Priority** | Should Have |
| **Description** | UI should update immediately for better UX |
| **Implementation** | Update local state before API call completes |
| **Rollback** | Revert state if API call fails |
| **Scope** | Mark complete, delete, update (not create) |

### TR-CRUD-004: Error Handling

| Requirement | Details |
|-------------|---------|
| **ID** | TR-CRUD-004 |
| **Priority** | Must Have |
| **Description** | Graceful handling of network and validation errors |
| **Network Errors** | Show retry button, offline indicator |
| **Validation Errors** | Show specific field errors |
| **Auth Errors** | Redirect to login |
| **Server Errors** | Show generic error message |

### TR-CRUD-005: Loading States

| Requirement | Details |
|-------------|---------|
| **ID** | TR-CRUD-005 |
| **Priority** | Should Have |
| **Description** | Users should see loading indicators during async operations |
| **Implementation** | Show spinner or disabled state during API calls |
| **Scope** | Initial load, form submissions, deletions |
| **Duration** | < 100ms for optimistic updates, show for > 300ms |

---

## UI/UX Requirements

### UX-CRUD-001: Responsive Design

| Requirement | Details |
|-------------|---------|
| **ID** | UX-CRUD-001 |
| **Priority** | Must Have |
| **Description** | Task interface works on all screen sizes |
| **Mobile** | Touch-friendly, stacked layout, swipe actions optional |
| **Tablet** | Adaptive layout, comfortable spacing |
| **Desktop** | Full functionality, comfortable spacing |
| **Breakpoints** | 640px (sm), 768px (md), 1024px (lg), 1280px (xl) |

### UX-CRUD-002: Visual Feedback

| Requirement | Details |
|-------------|---------|
| **ID** | UX-CRUD-002 |
| **Priority** | Must Have |
| **Description** | Users receive clear visual feedback for actions |
| **Success** | Green checkmark, toast notification, or success message |
| **Error** | Red error message, shake animation on form |
| **Loading** | Spinner or skeleton loader |
| **Completion** | Checkmark icon, color change, strikethrough |

### UX-CRUD-003: Form Design

| Requirement | Details |
|-------------|---------|
| **ID** | UX-CRUD-003 |
| **Priority** | Must Have |
| **Description** | Task forms are intuitive and accessible |
| **Labels** | Clear labels for all fields |
| **Placeholders** | Helpful placeholder text |
| **Validation** | Real-time validation feedback |
| **Required Fields** | Clearly marked |
| **Buttons** | Primary (Create/Save), Secondary (Cancel) |

### UX-CRUD-004: Task List Display

| Requirement | Details |
|-------------|---------|
| **ID** | UX-CRUD-004 |
| **Priority** | Must Have |
| **Description** | Task list is clear and scannable |
| **Title** | Prominent, readable size |
| **Description** | Secondary, readable when expanded |
| **Status** | Clear visual indicator |
| **Actions** | Easy to identify and access |
| **Empty State** | Friendly message, call to action |

### UX-CRUD-005: Accessibility

| Requirement | Details |
|-------------|---------|
| **ID** | UX-CRUD-005 |
| **Priority** | Must Have |
| **Description** | Interface is usable by everyone |
| **Keyboard** | Full keyboard navigation |
| **Screen Reader** | ARIA labels, semantic HTML |
| **Focus** | Visible focus indicators |
| **Contrast** | WCAG AA compliant colors |
| **Motion** | Respect reduced motion preference |

---

## API Endpoints

### Task Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for user |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{task_id}` | Get a specific task |
| PUT | `/api/{user_id}/tasks/{task_id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{task_id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{task_id}/complete` | Toggle completion |

### Request/Response Schemas

#### Create Task

**Request:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": "user-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "completed": false,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T10:00:00Z"
}
```

#### List Tasks

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "user_id": "user-123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "high",
    "completed": false,
    "created_at": "2026-01-07T10:00:00Z",
    "updated_at": "2026-01-07T10:00:00Z"
  }
]
```

---

## Data Model

### Task Entity

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | int | PK, auto-increment | Unique task identifier |
| user_id | str | FK, max 255 | Reference to owning user |
| title | str | 1-200 chars, required | Task title |
| description | str | 0-1000 chars, optional | Task details |
| priority | str | enum: high/medium/low | Task priority |
| completed | bool | default: false | Completion status |
| created_at | datetime | auto-generated | Creation timestamp |
| updated_at | datetime | auto-generated | Last update timestamp |

---

## Validation Rules

### Title Validation

| Rule | Value | Error Message |
|------|-------|---------------|
| Required | true | "Title is required" |
| Minimum length | 1 | "Title cannot be empty" |
| Maximum length | 200 | "Title must be 200 characters or less" |

### Description Validation

| Rule | Value | Error Message |
|------|-------|---------------|
| Required | false | N/A (optional) |
| Maximum length | 1000 | "Description must be 1000 characters or less" |

### Priority Validation

| Rule | Value | Error Message |
|------|-------|---------------|
| Default | "medium" | N/A |
| Allowed values | "high", "medium", "low" | "Invalid priority value" |

---

## Edge Cases

| Edge Case | Handling |
|-----------|----------|
| Empty task list | Show empty state with "Add your first task" message |
| Network timeout | Show error, provide retry button |
| JWT expired | Redirect to login page |
| Task not found | Show "Task not found" message |
| Delete confirmation | Show modal with "Are you sure?" |
| Simultaneous edits | Last write wins (no conflict resolution for MVP) |
| Very long title | Truncate with ellipsis in list view |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| API response time | < 200ms | Backend metrics |
| Page load time | < 1s | Lighthouse |
| Task creation success | > 99% | Error tracking |
| User can complete all flows | 100% | User testing |

---

## Related Documents

| Document | Path | Purpose |
|----------|------|---------|
| Architecture | `architecture.md` | System architecture |
| API Spec | `api/rest-endpoints.md` | Endpoint details |
| Database Schema | `database/schema.md` | Table definitions |
| UI Components | `ui/components.md` | Component specs |

---

## Version Information

| Item | Value |
|------|-------|
| Feature | Task CRUD Operations |
| Version | 1.0.0 |
| Status | Draft |
| Last Updated | 2026-01-07 |
