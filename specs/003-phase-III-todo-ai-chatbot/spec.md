# Technical Specification: AI Chatbot Integration for Todo Application (Phase III)

## 1. SYSTEM OVERVIEW

### 1.1 High-Level Architecture Diagram
```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Frontend      │    │   FastAPI        │    │   MCP Server     │
│   (ChatKit)     │◄──►│   Backend        │◄──►│   (Embedded)     │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌──────────────────┐    ┌──────────────────┐
                       │   OpenRouter     │    │   Database       │
                       │   (LLM Gateway)  │    │   (Neon PG)      │
                       └──────────────────┘    └──────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌──────────────────┐    ┌──────────────────┐
                       │   LLM (Llama3.1) │    │   Better Auth    │
                       │   or Gemini 1.5  │    │   (Authentication)│
                       └──────────────────┘    └──────────────────┘
```

### 1.2 Component Interaction Flow
1. **Frontend** (OpenAI ChatKit) sends natural language requests to backend
2. **FastAPI Backend** authenticates user and processes the request
3. **MCP Server** provides structured tools for AI to interact with todo functionality
4. **OpenRouter** routes requests to appropriate LLM (Llama 3.1 or Gemini Flash 1.5)
5. **Database** (Neon PostgreSQL) stores tasks, conversations, and messages
6. **Better Auth** handles user authentication and authorization

### 1.3 Data Flow Between Components
- **Frontend → Backend**: Natural language input via POST /api/{user_id}/chat
- **Backend → MCP**: Tool calls for task operations (add, list, complete, etc.)
- **Backend → OpenRouter**: Chat completion requests with conversation history
- **Backend ← OpenRouter**: AI responses with potential tool calls
- **Backend ↔ Database**: CRUD operations for tasks, conversations, and messages
- **All Components ↔ Better Auth**: User authentication and authorization

## 2. TECHNICAL ARCHITECTURE

### 2.1 Component Breakdown with Responsibilities

#### 2.1.1 Frontend (OpenAI ChatKit)
- **Responsibility**: User interface for chat interactions
- **Technology**: OpenAI ChatKit React component
- **Features**: Real-time chat interface, voice input/output integration
- **Integration Point**: API endpoint `/api/{user_id}/chat`

#### 2.1.2 FastAPI Backend
- **Responsibility**: API gateway, authentication, request processing
- **Technology**: Python FastAPI framework
- **Features**:
  - Authentication via Better Auth
  - Conversation management
  - Request/response validation
  - MCP server integration
- **Integration Points**: Database, MCP server, OpenRouter

#### 2.1.3 MCP Server (Model Context Protocol)
- **Responsibility**: Structured tool interface for AI agents
- **Technology**: Official MCP SDK (Python)
- **Features**:
  - Tool definitions for todo operations
  - Stateless design with database persistence
  - User authentication enforcement
- **Integration Points**: Database for operations

#### 2.1.4 OpenRouter
- **Responsibility**: LLM gateway and routing
- **Technology**: OpenRouter API
- **Features**:
  - Access to multiple LLMs (Llama 3.1, Gemini Flash 1.5)
  - Free/low-cost model access
  - Tool calling support
- **Integration Points**: LLM providers

#### 2.1.5 Database (Neon PostgreSQL)
- **Responsibility**: Data persistence
- **Technology**: Neon Serverless PostgreSQL
- **Features**:
  - Serverless scaling
  - SQLModel ORM
  - Efficient indexing
- **Integration Points**: All backend components

#### 2.1.6 Better Auth
- **Responsibility**: User authentication and session management
- **Technology**: Better Auth framework
- **Features**:
  - Secure user sessions
  - Token-based authentication
  - User data isolation
- **Integration Points**: All components requiring authentication

### 2.2 Technology Choices and Justifications

| Component | Technology | Justification |
|-----------|------------|---------------|
| Frontend UI | OpenAI ChatKit | Pre-built, tested chat interface with good UX |
| Backend | FastAPI | High-performance, easy to integrate with existing stack |
| AI Provider | OpenRouter | Access to free/low-cost models, good tool support |
| LLM | Llama 3.1 8B | Good balance of performance and cost for free tier |
| LLM | Gemini Flash 1.5 | Alternative high-quality model with good reasoning |
| MCP | Official MCP SDK | Standard protocol for AI tool integration |
| ORM | SQLModel | Type-safe, integrates well with FastAPI |
| Database | Neon PostgreSQL | Serverless, reliable, integrates with existing Phase II |
| Auth | Better Auth | Well-integrated with existing stack, secure |

### 2.3 Integration Points with Existing Phase II App

The AI chatbot seamlessly integrates with the existing Phase II infrastructure:

- **Database**: Leverages existing Neon PostgreSQL schema, adds new tables (Conversations, Messages)
- **Authentication**: Uses Better Auth tokens from Phase II for user validation
- **Task Operations**: Direct integration with existing Task model without modification
- **API Structure**: Extends existing FastAPI backend with new endpoints
- **User Sessions**: Maintains user identity through existing authentication system

## 3. DATABASE SCHEMA

### 3.1 Extended Schema for Chat Functionality

#### 3.1.1 Existing Task Model (From Phase II)
```python
# backend/models/task.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """
    Represents a todo task item.
    NOTE: This model may be extended in Phase III to add AI-specific fields
    while maintaining backward compatibility with Phase II functionality.
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Links to Better Auth user
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False
            }
        }
```

#### 3.1.2 New Conversation Model
```python
# backend/models/conversation.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    """
    Represents a chat conversation session.
    Each user can have multiple conversations.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Links to Better Auth user
    title: Optional[str] = Field(default="New Conversation", max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages (optional, for ORM convenience)
    messages: List["Message"] = Relationship(back_populates="conversation")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "title": "Todo Management Chat"
            }
        }
```

#### 3.1.3 New Message Model
```python
# backend/models/message.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from enum import Enum

class MessageRole(str, Enum):
    """Message role types following OpenAI convention"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

class Message(SQLModel, table=True):
    """
    Represents a single message in a conversation.
    Stores both user inputs and assistant responses.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(index=True)  # Denormalized for query efficiency
    role: MessageRole = Field(default=MessageRole.USER)
    content: str = Field(max_length=10000)  # Support long responses
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation (optional)
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": 1,
                "user_id": "user_123",
                "role": "user",
                "content": "Add a task to buy groceries"
            }
        }
```

### 3.2 Relationship with Existing Task Model
```
[User] 1--* [Conversation] 1--* [Message]
                    |
                    *--* [Task] (via AI operations)
```

- **User**: Identified by user_id from Better Auth (partitioning key)
- **Conversation**: Groups related messages in a chat session
- **Message**: Individual chat messages with role-based classification
- **Task**: Existing todo items from Phase II, now manageable via AI

### 3.3 Migration Strategy from Phase II
The migration from Phase II is additive-only:
1. **No Breaking Changes**: Existing Task model remains unchanged
2. **New Tables Added**: Conversations and Messages tables created
3. **User Data Preserved**: All existing tasks remain intact
4. **Authentication Intact**: Better Auth integration continues to work
5. **Database Schema Evolution**: Forward-compatible additions

### 3.4 Required Database Indexes
```sql
-- Primary indexes (auto-created)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- Composite indexes for common queries
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);
CREATE INDEX idx_conversations_user_created ON conversations(user_id, created_at);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
```

These indexes ensure efficient querying for:
- User-specific data retrieval
- Conversation history loading
- Message chronological ordering
- Task status filtering

## 4. API SPECIFICATIONS

### 4.1 Chat Endpoint
**METHOD**: POST
**PATH**: /api/{user_id}/chat
**AUTHENTICATION**: Required (Better Auth token)
**CONTENT-TYPE**: application/json

#### 4.1.1 Request Format
```json
{
  "conversation_id": integer | null,  // null creates new conversation
  "message": string                   // User's natural language input
}
```

#### 4.1.2 Response Format
```json
{
  "conversation_id": integer,
  "response": string,                 // AI assistant's text response
  "tool_calls": [                     // Optional: Tools that were invoked
    {
      "tool": string,                 // Tool name
      "arguments": object,            // Tool arguments
      "result": object                // Tool result
    }
  ]
}
```

#### 4.1.3 Status Codes
- 200: Success
- 400: Bad request (missing message)
- 401: Unauthorized (invalid token)
- 404: Conversation not found
- 500: Server error

#### 4.1.4 Error Response Format
```json
{
  "error": string,
  "detail": string
}
```

### 4.2 Request/Response Validation
```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str = Field(min_length=1, max_length=5000)

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: Optional[List[dict]] = None
```

### 4.3 Error Handling Patterns
- **Validation Errors**: Pre-execution parameter validation with clear error messages
- **Authentication Errors**: Token validation with appropriate 401 responses
- **Authorization Errors**: User ID verification with 403 responses
- **Business Logic Errors**: Domain-specific validation with 400 responses
- **Service Errors**: External service failures with 500 responses
- **Database Errors**: Persistence layer failures with 500 responses

## 5. MCP SERVER DESIGN

### 5.1 MCP Server Overview
The Model Context Protocol (MCP) server provides a structured interface for AI agents to interact with the todo application. The server is embedded within the FastAPI backend to maintain tight integration with existing functionality while providing standardized tool access for AI models.

**Key Design Principles**:
- **Architecture**: Embedded within FastAPI backend for seamless integration
- **Protocol**: Official MCP SDK (Python) for standardized tool access
- **State Management**: Stateless design with all state persisted in the database
- **Security**: User authentication enforced through user_id validation
- **Performance**: Optimized for low-latency tool calls from AI models

### 5.2 Server Initialization
```python
# backend/mcp/server.py
from mcp.server import Server
from mcp.types import Tool, TextContent

# Initialize MCP server
mcp_server = Server("todo-mcp-server")

# Tool definitions will be registered here
```

### 5.3 Tool Specifications

#### 5.3.1 Tool: add_task
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

#### 5.3.2 Tool: list_tasks
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

#### 5.3.3 Tool: complete_task
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

#### 5.3.4 Tool: delete_task
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

#### 5.3.5 Tool: update_task
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

### 5.4 Database Connection
```python
# MCP server uses the same database session as FastAPI
from backend.database import get_session

# Each tool handler receives session as parameter
async def handle_add_task(session: Session, user_id: str, title: str, description: str = None):
    # Implementation
    pass
```

### 5.5 Error Handling Strategy
All MCP tools implement consistent error handling with standardized error messages:

1. **Validation Errors**: Pre-execution parameter validation
2. **Authorization Errors**: User access verification
3. **Business Logic Errors**: Domain-specific validation
4. **Database Errors**: Persistence layer failures
5. **Generic Errors**: Unexpected system failures

Error responses follow the format: `{"error": "descriptive error message"}` with appropriate HTTP status codes.

## 6. AGENT BEHAVIOR

### 6.1 Natural Language Understanding Patterns
The AI agent recognizes common phrases and maps them to appropriate tools with measurable success rates:

**SUCCESS METRICS**:
- Intent recognition accuracy: >90% for common patterns
- False positive rate: <5% for ambiguous inputs
- Response time: <2 seconds for intent classification

```python
# Agent behavior patterns with measurable outcomes
INTENT_PATTERNS = {
    "add_task": [
        "add {task}",           # Success: Creates task in database
        "create {task}",       # Success: Creates task in database
        "new task {task}",     # Success: Creates task in database
        "remember to {task}",  # Success: Creates task in database
        "I need to {task}",    # Success: Creates task in database
        "don't forget {task}", # Success: Creates task in database
        "remind me to {task}"  # Success: Creates task in database
    ],

    "list_tasks": [
        "show tasks",           # Success: Returns >0 tasks with proper formatting
        "what's on my list",   # Success: Returns >0 tasks with proper formatting
        "what do I need to do", # Success: Returns >0 tasks with proper formatting
        "show pending",        # Success: Returns pending tasks only
        "what's completed",    # Success: Returns completed tasks only
        "list everything"      # Success: Returns all tasks
    ],

    "complete_task": [
        "done with {task}",    # Success: Marks task as completed in database
        "completed {task}",    # Success: Marks task as completed in database
        "finished {task}",     # Success: Marks task as completed in database
        "mark {task} as done", # Success: Marks task as completed in database
        "I did {task}"         # Success: Marks task as completed in database
    ],

    "delete_task": [
        "delete {task}",       # Success: Removes task from database
        "remove {task}",       # Success: Removes task from database
        "cancel {task}",       # Success: Removes task from database
        "forget about {task}"  # Success: Removes task from database
    ],

    "update_task": [
        "change {task} to {new_value}", # Success: Updates task in database
        "update {task}",               # Success: Updates task in database
        "rename {task}",               # Success: Updates task in database
        "edit {task}"                  # Success: Updates task in database
    ]
}
```

```python
# Agent behavior patterns (handled by LLM, but good to document)

INTENT PATTERNS = {
    "add_task": [
        "add {task}",
        "create {task}",
        "new task {task}",
        "remember to {task}",
        "I need to {task}",
        "don't forget {task}",
        "remind me to {task}"
    ],

    "list_tasks": [
        "show tasks",
        "what's on my list",
        "what do I need to do",
        "show pending",
        "what's completed",
        "list everything"
    ],

    "complete_task": [
        "done with {task}",
        "completed {task}",
        "finished {task}",
        "mark {task} as done",
        "I did {task}"
    ],

    "delete_task": [
        "delete {task}",
        "remove {task}",
        "cancel {task}",
        "forget about {task}"
    ],

    "update_task": [
        "change {task} to {new_value}",
        "update {task}",
        "rename {task}",
        "edit {task}"
    ]
}
```

### 6.2 Tool Selection Logic
The agent follows these decision rules:
1. **Intent Recognition**: Analyze user input to identify the intended action
2. **Parameter Extraction**: Extract relevant parameters (task titles, IDs, etc.)
3. **Tool Selection**: Choose the most appropriate tool based on intent
4. **Validation**: Ensure all required parameters are present
5. **Execution**: Call the selected tool with extracted parameters
6. **Response Generation**: Format the tool result into a natural language response

### 6.3 Response Generation Guidelines
- **Be conversational and friendly**
- **Keep responses SHORT (under 50 words when possible)** - they may be read aloud
- **Confirm actions clearly**: "I've added 'Buy groceries' to your tasks"
- **When listing tasks, format them clearly**
- **Ask for clarification if needed**
- **Always use tools to perform actions** - never just acknowledge

### 6.4 Error Handling and Fallback Strategies
- **Missing Information**: Ask user for required details
- **Ambiguous Requests**: Clarify with specific questions
- **Tool Failures**: Attempt alternative approaches or inform user of limitations
- **Authorization Issues**: Guide user toward resolving authentication problems
- **Database Errors**: Inform user of temporary issues and suggest retrying

## 7. CONVERSATION MANAGEMENT

### 7.1 Stateless Request Cycle
Each chat request follows this step-by-step flow:

```
REQUEST ARRIVES
├─ Extract user_id from path parameter
├─ Validate authentication token
└─ Parse request body (conversation_id, message)
CONVERSATION MANAGEMENT
├─ If conversation_id is null:
│  ├─ Create new Conversation record
│  └─ Set conversation_id = new_conversation.id
└─ If conversation_id provided:
   ├─ Verify conversation belongs to user
   └─ Raise 404 if not found or unauthorized
FETCH CONVERSATION HISTORY
├─ Query messages for conversation_id
├─ Order by created_at ASC
├─ Limit to last 50 messages (context window management)
└─ Build messages array: [{"role": "user"|"assistant", "content": "..."}]
SAVE USER MESSAGE
├─ Create Message record
│  ├─ conversation_id: from step 2
│  ├─ user_id: from path
│  ├─ role: "user"
│  ├─ content: request.message
│  └─ created_at: now()
└─ Commit to database
PREPARE AGENT CONTEXT
├─ System message: "You are a helpful task management assistant..."
├─ History: messages from step 3
├─ New user message: from step 4
└─ Tools: MCP tool definitions
CALL OPENROUTER
├─ Initialize OpenAI client with OpenRouter base URL
├─ Send request:
│  ├─ model: "meta-llama/llama-3.1-8b-instruct:free"
│  ├─ messages: from step 5
│  ├─ tools: MCP tool definitions
│  └─ tool_choice: "auto"
└─ Receive response
PROCESS TOOL CALLS (if any)
├─ For each tool_call in response:
│  ├─ Extract tool name and arguments
│  ├─ Validate arguments
│  ├─ Call corresponding MCP tool handler
│  ├─ Get tool result
│  └─ Store for response
└─ If tools were called:
   ├─ Send tool results back to OpenRouter
   └─ Get final response
SAVE ASSISTANT RESPONSE
├─ Create Message record
│  ├─ conversation_id: from step 2
│  ├─ user_id: from path
│  ├─ role: "assistant"
│  ├─ content: AI response text
│  ├─ tool_calls: JSON.stringify(tool_calls) if any
│  └─ created_at: now()
└─ Commit to database
RETURN RESPONSE
└─ Send ChatResponse to client
   ├─ conversation_id: from step 2
   ├─ response: assistant message
   └─ tool_calls: summary of tools used
REQUEST COMPLETE
└─ Server forgets everything (stateless)
```

### 7.2 History Retrieval and Context Building
```python
# Limit history to prevent token overflow
MAX_HISTORY_MESSAGES = 50

# When fetching history:
messages = session.exec(
    select(Message)
    .where(Message.conversation_id == conversation_id)
    .order_by(Message.created_at.desc())
    .limit(MAX_HISTORY_MESSAGES)
).all()

# Reverse to chronological order
messages.reverse()
```

### 7.3 Message Persistence Strategy
- **Immediate Persistence**: User and assistant messages are saved immediately
- **Atomic Operations**: Each message save is part of a transaction
- **Consistent Timestamps**: All timestamps use UTC for consistency
- **User Isolation**: Messages are stored with user_id for access control
- **Conversation Linking**: Messages are linked to conversations for organization

## 8. FRONTEND INTEGRATION

### 8.1 OpenAI ChatKit Implementation Approach
The frontend uses OpenAI ChatKit to provide a rich chat interface:

1. **Component Setup**: Initialize ChatKit with appropriate configuration
2. **Authentication**: Pass Better Auth token for API calls
3. **Customization**: Style the chat interface to match application branding
4. **Voice Integration**: Implement Web Speech API for STT and TTS

### 8.2 Component Structure
```jsx
<TodoChatKit
  userId={currentUser.id}
  apiEndpoint={`/api/${currentUser.id}/chat`}
  authToken={betterAuthToken}
  onMessage={(message) => handleNewMessage(message)}
  onError={(error) => handleChatError(error)}
/>
```

### 8.3 State Management
- **User Session**: Maintain user authentication state
- **Conversation State**: Track current conversation ID
- **Loading States**: Show appropriate loading indicators
- **Error States**: Handle and display API errors gracefully
- **Voice State**: Manage speech recognition and synthesis states

### 8.4 API Communication Patterns
- **WebSocket Connections**: For real-time chat experiences
- **Token Propagation**: Include auth tokens in all requests
- **Retry Logic**: Implement exponential backoff for failed requests
- **Rate Limiting**: Respect API rate limits to avoid blocking
- **Error Recovery**: Automatically recover from transient failures

## 9. SECURITY & AUTH

### 9.1 User Authentication Flow
```python
# Middleware to verify user_id matches token
from fastapi import Depends, HTTPException
from backend.auth import get_current_user

@app.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    # Verify user_id in path matches authenticated user
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Proceed with chat logic
    ...
```

### 9.2 User ID Propagation Through Layers
- **Path Parameter**: user_id extracted from URL path
- **Authentication Layer**: Verified against Better Auth token
- **Database Layer**: Enforced as foreign key constraint
- **MCP Layer**: User ID validated in all tool calls
- **Response Layer**: Ensures data isolation

### 9.3 Domain Allowlist Configuration for ChatKit
- **Allowed Origins**: Configure CORS for frontend domains
- **API Endpoints**: Restrict access to authorized endpoints only
- **Token Validation**: Verify authentication tokens for all requests
- **Rate Limiting**: Implement per-user rate limiting to prevent abuse

### 9.4 Data Protection Measures
- **Encryption at Rest**: Database encryption for sensitive data
- **Encryption in Transit**: HTTPS for all API communications
- **Access Logging**: Log all user actions for audit purposes
- **Data Retention**: Implement appropriate data retention policies

## 10. DEPLOYMENT CONSIDERATIONS

### 10.1 Environment Variables
```env
# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
DEFAULT_MODEL=meta-llama/llama-3.1-8b-instruct:free

# Database Configuration
DATABASE_URL=postgresql://...
NEON_DATABASE_URL=postgresql://...

# Authentication
BETTER_AUTH_SECRET=...

# Application Settings
MAX_HISTORY_MESSAGES=50
FALLBACK_MODELS=google/gemini-flash-1.5,meta-llama/llama-3.1-8b-instruct:free
```

### 10.2 Service Dependencies
- **OpenRouter API**: For LLM access (external dependency)
- **Neon PostgreSQL**: For data storage (external dependency)
- **Better Auth**: For user authentication (external dependency)
- **FastAPI Server**: Main application server (internal)
- **MCP Server**: Embedded within FastAPI (internal)

### 10.3 Scaling Considerations
- **Horizontal Scaling**: Multiple backend instances behind load balancer
- **Database Scaling**: Leverage Neon's serverless scaling
- **Caching**: Implement Redis for frequently accessed data
- **CDN**: Cache static assets for faster delivery
- **Connection Pooling**: Optimize database connection usage

### 10.4 Monitoring and Observability
- **Application Metrics**: Track API response times and error rates
- **Database Metrics**: Monitor query performance and connection pools
- **LLM Usage**: Track token usage and costs
- **User Engagement**: Monitor chat session length and frequency
- **Error Tracking**: Centralized logging for debugging

### 10.5 Cost Optimization
- **Free Tier Usage**: Leverage free models (Llama 3.1 8B, Gemini Flash 1.5)
- **Context Window Management**: Limit conversation history to reduce token usage
- **Caching**: Cache responses for common queries
- **Batch Operations**: Batch similar operations to reduce API calls
- **Resource Limits**: Implement appropriate resource limits to prevent runaway costs

### 10.6 Backup and Recovery
- **Database Backups**: Regular automated backups of PostgreSQL database
- **Configuration Backup**: Version control for all configuration files
- **Disaster Recovery**: Plan for service restoration in case of failures
- **Data Export**: Allow users to export their data for portability

This comprehensive specification provides a complete blueprint for implementing the AI chatbot integration into the existing Todo application, ensuring seamless integration with the existing Phase II infrastructure while adding sophisticated AI capabilities through the MCP protocol.