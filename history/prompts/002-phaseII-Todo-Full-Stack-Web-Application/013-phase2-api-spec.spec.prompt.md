---
id: "013"
title: "Create Phase II REST API specification"
stage: "spec"
date: "2026-01-07"
surface: "agent"
model: "sonnet-4-5"
feature: "002-phaseII-full-stack-todo-application"
branch: "001-phase1-todo-console"
user: "Human"
command: "Create specs/002-phaseII-full-stack-todo-application/api/rest-endpoints.md that defines all REST API endpoints..."
labels: ["phase2","api","rest","specification","endpoints"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specs/002-phaseII-full-stack-todo-application/api/rest-endpoints.md"
tests: []
---

## Prompt

Create specs/002-phaseII-full-stack-todo-application/api/rest-endpoints.md that defines all REST API endpoints with:

## REST API Specification

### Base URLs:
- Development: http://localhost:8000
- Production: TBD (will be deployed URL)

### Authentication:
All endpoints require JWT token in header:
Authorization: Bearer <jwt_token>

### Common Response Codes:
- 200: Success
- 201: Created
- 400: Bad Request (validation error)
- 401: Unauthorized (missing or invalid token)
- 403: Forbidden (accessing another user's resource)
- 404: Not Found
- 500: Internal Server Error

### Endpoints:

#### 1. GET /api/{user_id}/tasks
Description: List all tasks for authenticated user
Path Parameters: user_id (must match authenticated user's ID)
Query Parameters: status (all/pending/completed), sort (created/title/updated), order (asc/desc)
Response: Array of task objects

#### 2. POST /api/{user_id}/tasks
Description: Create a new task
Request Body: title (required, 1-200 chars), description (optional, max 1000 chars)
Response (201): Created task object

#### 3. GET /api/{user_id}/tasks/{id}
Description: Get details of a specific task
Response (200): Task object
Response (404): Task not found

#### 4. PUT /api/{user_id}/tasks/{id}
Description: Update an existing task
Request Body: title, description (optional fields)
Response (200): Updated task object

#### 5. DELETE /api/{user_id}/tasks/{id}
Description: Delete a task
Response (200): Success message with deleted task ID

#### 6. PATCH /api/{user_id}/tasks/{id}/complete
Description: Toggle task completion status
Response (200): Updated task object with toggled completed status

### Error Response Format:
{
  "detail": "Error message"
}

### Security Notes:
- All endpoints verify JWT token
- user_id in URL must match JWT user_id
- 403 for accessing another user's tasks
- 401 for invalid/expired tokens

### CORS Configuration:
- Allow origin: http://localhost:3000
- Allow methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
- Allow headers: Content-Type, Authorization
- Allow credentials: true

Use proper markdown formatting with code blocks for JSON examples.

## Response snapshot

Created `.specs/002-phaseII-full-stack-todo-application/api/rest-endpoints.md` with comprehensive REST API specification:

**Base Configuration:**
- Development: http://localhost:8000
- Production: https://api.yourdomain.com
- Authentication: Bearer token in Authorization header

**Common Response Codes:**
- 200 OK, 201 Created, 204 No Content
- 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Error

**Task Endpoints (6 total):**

1. GET /api/{user_id}/tasks
   - Query params: status, sort, order, limit, offset
   - Returns array of task objects

2. POST /api/{user_id}/tasks
   - Body: title (required), description (optional), priority
   - Returns 201 with created task

3. GET /api/{user_id}/tasks/{id}
   - Returns single task or 404

4. PUT /api/{user_id}/tasks/{id}
   - Partial update support (title, description, priority)
   - Returns updated task

5. DELETE /api/{user_id}/tasks/{id}
   - Returns success message with task ID

6. PATCH /api/{user_id}/tasks/{id}/complete
   - Toggles completion status
   - Returns updated task

**Auth Endpoints (3 total):**
- POST /api/auth/signup - Create account
- POST /api/auth/signin - Get JWT token
- GET /api/auth/me - Get current user

**Additional Sections:**
- Error response format with examples
- Data models (Task object with field descriptions)
- Security notes with Mermaid flow diagram
- CORS configuration settings
- Rate limiting recommendations
- Versioning strategy
- cURL testing examples

## Outcome

- ✅ Impact: Created comprehensive Phase II REST API specification
- 🧪 Tests: None (specification only)
- 📁 Files: 1 created (rest-endpoints.md)
- 🔁 Next prompts: Create database/schema.md, ui/components.md
- 🧠 Reflection: N/A

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
