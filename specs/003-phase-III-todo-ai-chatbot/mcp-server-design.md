# Phase III: Todo AI Chatbot - MCP Server Design

## 3.1 MCP SERVER OVERVIEW
The Model Context Protocol (MCP) server provides a structured interface for AI agents to interact with the todo application. The server is embedded within the FastAPI backend to maintain tight integration with existing functionality while providing standardized tool access for AI models.

**Key Design Principles:**
- **Architecture**: Embedded within FastAPI backend for seamless integration
- **Protocol**: Official MCP SDK (Python) for standardized tool access
- **State Management**: Stateless design with all state persisted in the database
- **Security**: User authentication enforced through user_id validation
- **Performance**: Optimized for low-latency tool calls from AI models

## 3.2 SERVER INITIALIZATION
```python
# backend/mcp/server.py
from mcp.server import Server
from mcp.types import Tool, TextContent

# Initialize MCP server
mcp_server = Server("todo-mcp-server")

# Tool definitions will be registered here
```

## 3.3 TOOL SPECIFICATIONS

### 3.3.1 Tool: add_task
**PURPOSE**: Create a new task for the user

**PARAMETERS**:
- `user_id` (string, required): User identifier
- `title` (string, required): Task title (max 200 chars)
- `description` (string, optional): Task description (max 1000 chars)

**RETURNS**:
```json
{
  "task_id": integer,
  "status": "created",
  "title": string,
  "description": string | null,
  "completed": false
}
```

**ERROR CASES**:
- Missing user_id → "user_id is required"
- Empty title → "title cannot be empty"
- Database error → "Failed to create task: {error}"

**IMPLEMENTATION PSEUDOCODE**:
1. Validate user_id and title
2. Create Task instance with SQLModel
3. Add to database session
4. Commit transaction
5. Return task details

**EXAMPLE CALL**:
Input:
```json
{
  "user_id": "user_123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

Output:
```json
{
  "task_id": 42,
  "status": "created",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}
```

### 3.3.2 Tool: list_tasks
**PURPOSE**: Retrieve tasks based on filter criteria

**PARAMETERS**:
- `user_id` (string, required): User identifier
- `status` (string, optional): Filter by status
  - `"all"` (default): Return all tasks
  - `"pending"`: Only incomplete tasks
  - `"completed"`: Only completed tasks

**RETURNS**:
```json
{
  "tasks": [
    {
      "id": integer,
      "title": string,
      "description": string | null,
      "completed": boolean,
      "created_at": ISO datetime,
      "updated_at": ISO datetime
    }
  ],
  "count": integer,
  "filter": string
}
```

**ERROR CASES**:
- Missing user_id → "user_id is required"
- Invalid status → "status must be 'all', 'pending', or 'completed'"
- Database error → "Failed to retrieve tasks: {error}"

**IMPLEMENTATION PSEUDOCODE**:
1. Validate user_id
2. Build query based on status filter
3. Execute query with user_id filter
4. Convert results to dict list
5. Return tasks array with metadata

**EXAMPLE CALL**:
Input:
```json
{
  "user_id": "user_123",
  "status": "pending"
}
```

Output:
```json
{
  "tasks": [
    {
      "id": 42,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2025-01-12T10:00:00Z",
      "updated_at": "2025-01-12T10:00:00Z"
    }
  ],
  "count": 1,
  "filter": "pending"
}
```

### 3.3.3 Tool: complete_task
**PURPOSE**: Mark a task as completed

**PARAMETERS**:
- `user_id` (string, required): User identifier
- `task_id` (integer, required): Task identifier

**RETURNS**:
```json
{
  "task_id": integer,
  "status": "completed",
  "title": string,
  "completed": true,
  "updated_at": ISO datetime
}
```

**ERROR CASES**:
- Missing user_id or task_id → "user_id and task_id are required"
- Task not found → "Task {task_id} not found"
- Task doesn't belong to user → "Unauthorized access to task"
- Already completed → "Task already completed"
- Database error → "Failed to complete task: {error}"

**IMPLEMENTATION PSEUDOCODE**:
1. Validate user_id and task_id
2. Query task by id and user_id
3. Check if task exists and belongs to user
4. Update completed = True
5. Update updated_at timestamp
6. Commit transaction
7. Return updated task details

**EXAMPLE CALL**:
Input:
```json
{
  "user_id": "user_123",
  "task_id": 42
}
```

Output:
```json
{
  "task_id": 42,
  "status": "completed",
  "title": "Buy groceries",
  "completed": true,
  "updated_at": "2025-01-12T11:30:00Z"
}
```

### 3.3.4 Tool: delete_task
**PURPOSE**: Remove a task from the database

**PARAMETERS**:
- `user_id` (string, required): User identifier
- `task_id` (integer, required): Task identifier

**RETURNS**:
```json
{
  "task_id": integer,
  "status": "deleted",
  "title": string
}
```

**ERROR CASES**:
- Missing user_id or task_id → "user_id and task_id are required"
- Task not found → "Task {task_id} not found"
- Task doesn't belong to user → "Unauthorized access to task"
- Database error → "Failed to delete task: {error}"

**IMPLEMENTATION PSEUDOCODE**:
1. Validate user_id and task_id
2. Query task by id and user_id
3. Check if task exists and belongs to user
4. Store title for response
5. Delete from database
6. Commit transaction
7. Return deletion confirmation

**EXAMPLE CALL**:
Input:
```json
{
  "user_id": "user_123",
  "task_id": 42
}
```

Output:
```json
{
  "task_id": 42,
  "status": "deleted",
  "title": "Buy groceries"
}
```

### 3.3.5 Tool: update_task
**PURPOSE**: Modify task title and/or description

**PARAMETERS**:
- `user_id` (string, required): User identifier
- `task_id` (integer, required): Task identifier
- `title` (string, optional): New title (max 200 chars)
- `description` (string, optional): New description (max 1000 chars)

**RETURNS**:
```json
{
  "task_id": integer,
  "status": "updated",
  "title": string,
  "description": string | null,
  "completed": boolean,
  "updated_at": ISO datetime
}
```

**ERROR CASES**:
- Missing user_id or task_id → "user_id and task_id are required"
- No updates provided → "At least one of title or description must be provided"
- Task not found → "Task {task_id} not found"
- Task doesn't belong to user → "Unauthorized access to task"
- Empty title → "title cannot be empty"
- Database error → "Failed to update task: {error}"

**IMPLEMENTATION PSEUDOCODE**:
1. Validate user_id and task_id
2. Check at least one update field provided
3. Query task by id and user_id
4. Check if task exists and belongs to user
5. Update provided fields
6. Update updated_at timestamp
7. Commit transaction
8. Return updated task details

**EXAMPLE CALL**:
Input:
```json
{
  "user_id": "user_123",
  "task_id": 42,
  "title": "Buy groceries and fruits"
}
```

Output:
```json
{
  "task_id": 42,
  "status": "updated",
  "title": "Buy groceries and fruits",
  "description": "Milk, eggs, bread",
  "completed": false,
  "updated_at": "2025-01-12T12:00:00Z"
}
```

## 3.4 DATABASE CONNECTION
```python
# MCP server uses the same database session as FastAPI
from backend.database import get_session

# Each tool handler receives session as parameter
async def handle_add_task(session: Session, user_id: str, title: str, description: str = None):
    # Implementation
    pass
```

## 3.5 ERROR HANDLING STRATEGY
All MCP tools implement consistent error handling with standardized error messages:

1. **Validation Errors**: Pre-execution parameter validation
2. **Authorization Errors**: User access verification
3. **Business Logic Errors**: Domain-specific validation
4. **Database Errors**: Persistence layer failures
5. **Generic Errors**: Unexpected system failures

Error responses follow the format: `{"error": "descriptive error message"}` with appropriate HTTP status codes.