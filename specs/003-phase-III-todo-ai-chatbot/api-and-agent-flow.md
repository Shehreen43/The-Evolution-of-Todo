# Phase III: Todo AI Chatbot - API and Agent Flow

## 4.1 API ENDPOINT SPECIFICATION

### 4.1.1 Chat Endpoint
**METHOD**: POST
**PATH**: /api/{user_id}/chat
**AUTHENTICATION**: Required (Better Auth token)
**CONTENT-TYPE**: application/json

**REQUEST BODY**:
```json
{
  "conversation_id": integer | null,  // null creates new conversation
  "message": string                   // User's natural language input
}
```

**RESPONSE BODY**:
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

**STATUS CODES**:
- 200: Success
- 400: Bad request (missing message)
- 401: Unauthorized (invalid token)
- 404: Conversation not found
- 500: Server error

**ERROR RESPONSE**:
```json
{
  "error": string,
  "detail": string
}
```

### 4.1.2 Request Validation
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

## 4.2 STATELESS REQUEST CYCLE

Step-by-step flow for each request:

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
   ├─ response: assistant message/
   └─ tool_calls: summary of tools used
REQUEST COMPLETE
└─ Server forgets everything (stateless)
```

## 4.3 OPENROUTER CONFIGURATION
```python
# backend/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL: str = "meta-llama/llama-3.1-8b-instruct:free"

    # Alternative free models
    FALLBACK_MODELS: list[str] = [
        "google/gemini-flash-1.5",
        "meta-llama/llama-3.1-8b-instruct:free"
    ]

    class Config:
        env_file = ".env"

# Initialize OpenAI client with OpenRouter
from openai import OpenAI

settings = Settings()
client = OpenAI(
    base_url=settings.OPENROUTER_BASE_URL,
    api_key=settings.OPENROUTER_API_KEY,
)
```

## 4.4 AGENT SYSTEM PROMPT
```python
SYSTEM_PROMPT = """You are a helpful and concise task management assistant.

Your purpose is to help users manage their todo list through natural conversation.

You have access to these tools:
- add_task: Create new tasks
- list_tasks: View tasks (all, pending, or completed)
- complete_task: Mark tasks as done
- delete_task: Remove tasks
- update_task: Modify task details

Guidelines:
1. Be conversational and friendly
2. Keep responses SHORT (under 50 words when possible) - they may be read aloud
3. Confirm actions clearly: "I've added 'Buy groceries' to your tasks"
4. When listing tasks, format them clearly
5. Ask for clarification if needed
6. Always use tools to perform actions - never just acknowledge
7. If user says "add task", "create task", "remember", etc. → use add_task
8. If user says "show tasks", "what's pending", "list" → use list_tasks
9. If user says "done with", "complete", "finished" → use complete_task
10. If user says "delete", "remove" → use delete_task
11. If user wants to change a task → use update_task

Example interactions:
User: "Add buy milk to my list"
You: [calls add_task] "I've added 'Buy milk' to your tasks!"

User: "What do I need to do?"
You: [calls list_tasks with status="pending"] "You have 3 pending tasks: 1. Buy milk, 2. Call mom, 3. Finish report"

User: "I'm done with task 1"
You: [calls complete_task] "Great! I've marked 'Buy milk' as completed."
"""
```

## 4.5 NATURAL LANGUAGE UNDERSTANDING

Map common phrases to tool calls:
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

## 4.6 CONVERSATION CONTEXT WINDOW
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

## 4.7 ERROR HANDLING
```python
# Graceful error responses
try:
    # Call OpenRouter
    response = client.chat.completions.create(...)
except OpenAIError as e:
    return JSONResponse(
        status_code=500,
        content={
            "error": "AI service error",
            "detail": "Unable to process your message. Please try again."
        }
    )
except DatabaseError as e:
    return JSONResponse(
        status_code=500,
        content={
            "error": "Database error",
            "detail": "Unable to save conversation. Please try again."
        }
    )
```

## 4.8 AUTHENTICATION FLOW
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