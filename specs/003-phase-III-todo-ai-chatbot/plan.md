# Implementation Plan: AI Chatbot Integration for Todo Application (Phase III)

## Technical Context

This plan outlines the implementation of an AI-powered chatbot interface for the existing Todo application. The solution will leverage MCP (Model Context Protocol) architecture, OpenRouter for LLM access, and browser-based voice capabilities to create a natural language interface for managing tasks.

## Constitution Check

Based on the project constitution, this implementation plan adheres to:
- Modular architecture principles with clear separation of concerns
- Security-first approach with proper authentication and authorization
- Cost-effective design using free-tier resources
- Type safety with Pydantic and SQLModel
- Testable components with isolated units

## Phase 0: Research & Analysis

### 0.1 Technology Stack Research
**Objective**: Validate all technology choices and identify potential integration challenges
- Research MCP SDK installation and configuration
- Verify OpenRouter integration with OpenAI Python SDK
- Investigate Web Speech API browser compatibility
- Analyze Neon PostgreSQL connection pooling

**Files to Create/Modify**:
- specs/003-phase-III-todo-ai-chatbot/research.md - Research findings and validation

**Dependencies**: None
**Verification**:
```bash
# Verify MCP SDK installation
pip install mcp

# Verify OpenAI SDK with OpenRouter
pip install openai

# Check Web Speech API support
node -e "console.log('Web Speech API availability varies by browser')"
```

**Success Criteria** (Updated to align with constitution's fail-fast principle):
- [ ] MCP SDK installs without conflicts OR identified blockers with workarounds
- [ ] OpenAI SDK works with OpenRouter base URL OR identified incompatibilities
- [ ] Web Speech API compatibility documented with supported browsers list
- [ ] Neon PostgreSQL connection pooling verified OR identified limitations
- [ ] All technology choices validated before proceeding OR research indicates STOP
- [ ] Failure scenarios include clear exit conditions for incompatible technologies


## Phase 1: Foundation & Database Setup

### Task 1.1: Environment Setup
**Objective**: Establish the development environment and project structure
**Implementation Steps**:
1. Create project directory structure for Phase III backend components
2. Initialize Python virtual environment with poetry
3. Install all required dependencies with specific versions
4. Create .env.example template with all required variables

**Files to Create/Modify**:
- backend/requirements.txt - Python dependencies for Phase III
- backend/pyproject.toml - Poetry configuration
- .env.example - Environment variable template
- backend/.env - Local environment file (gitignored)

**Dependencies**: None
**Verification**:
```bash
# Check environment setup
poetry install
poetry run python -c "import openai, mcp, sqlmodel, fastapi; print('All dependencies installed')"
```

**Success Criteria**:
- [ ] Virtual environment initialized successfully
- [ ] All dependencies install without conflicts
- [ ] .env.example contains all required variables
- [ ] Basic imports work without errors


### Task 1.2: Database Configuration
**Objective**: Configure Neon PostgreSQL connection with connection pooling
**Implementation Steps**:
1. Create database.py with SQLModel engine setup
2. Implement connection pooling configuration
3. Add health check endpoint for database connectivity
4. Test database connection with Neon credentials

**Files to Create/Modify**:
- backend/database.py - Database connection and session management
- backend/main.py - Add health check endpoint for database

**Dependencies**: Task 1.1
**Verification**:
```bash
# Test database connection
poetry run python -c "
from backend.database import engine
from sqlmodel import create_engine
print('Database engine created successfully')
"
```

**Success Criteria**:
- [ ] Database engine connects successfully to Neon
- [ ] Connection pooling configured properly
- [ ] Health check endpoint returns 200 status
- [ ] Database session management works


### Task 1.3: Database Models Implementation
**Objective**: Implement SQLModel database models for conversations and messages
**Implementation Steps**:
1. Create Conversation model with proper relationships
2. Create Message model with role-based classification
3. Extend existing Task model if needed (verify no changes required)
4. Implement proper indexes and constraints

**Files to Create/Modify**:
- backend/models/conversation.py - Conversation model definition
- backend/models/message.py - Message model definition
- backend/models/task.py - Verify existing model (no changes expected)

**Dependencies**: Task 1.2
**Verification**:
```bash
# Test model creation
poetry run python -c "
from backend.models.conversation import Conversation
from backend.models.message import Message
from backend.models.task import Task
print('All models imported successfully')
print('Conversation model:', Conversation.__tablename__)
print('Message model:', Message.__tablename__)
print('Task model:', Task.__tablename__)
"
```

**Success Criteria**:
- [ ] All models compile without errors
- [ ] Relationships defined correctly
- [ ] Proper indexing implemented
- [ ] SQLModel compatibility verified


### Task 1.4: Database Migration
**Objective**: Create and deploy database schema with Alembic
**Implementation Steps**:
1. Create Alembic migration script for new tables
2. Deploy schema to Neon database
3. Seed with test data for initial verification
4. Verify all tables exist and relationships work

**Files to Create/Modify**:
- alembic/versions/[timestamp]_create_conversation_message_tables.py - Migration script
- alembic.ini - Alembic configuration
- backend/seed.py - Test data seeding script

**Dependencies**: Task 1.3
**Verification**:
```bash
# Run migrations
alembic revision --autogenerate -m "Create conversation and message tables"
alembic upgrade head

# Verify tables exist
poetry run python -c "
from backend.database import Session
from backend.models.conversation import Conversation
from backend.models.message import Message
from sqlmodel import select

with Session() as session:
    conv_count = session.exec(select(Conversation)).all()
    msg_count = session.exec(select(Message)).all()
    print(f'Conversations: {len(conv_count)}, Messages: {len(msg_count)}')
"
```

**Success Criteria**:
- [ ] Migration script created successfully
- [ ] Schema deployed to Neon database
- [ ] Tables created with proper relationships
- [ ] Test data seeded and accessible


**Phase 1 Completion Criteria**:
- Database connection successful
- All tables created with proper relationships
- Can perform CRUD operations on each model
- Health check endpoint returns 200

## Phase 2: MCP Server Implementation

### Task 2.1: MCP Server Initialization
**Objective**: Set up the MCP server with proper initialization and configuration
**Implementation Steps**:
1. Install Official MCP SDK and verify installation
2. Create mcp/ directory structure with proper organization
3. Initialize MCP server instance with project metadata
4. Configure server with proper logging and error handling

**Files to Create/Modify**:
- backend/mcp/__init__.py - MCP package initialization
- backend/mcp/server.py - MCP server instance
- backend/mcp/config.py - MCP server configuration

**Dependencies**: Phase 1 complete
**Verification**:
```bash
# Test MCP server initialization
poetry run python -c "
from backend.mcp.server import mcp_server
print('MCP server initialized:', mcp_server.name)
"
```

**Success Criteria**:
- [ ] MCP SDK installed and accessible
- [ ] MCP server initializes without errors
- [ ] Proper project metadata configured
- [ ] Logging and error handling set up


### Task 2.2: Database Session Management for MCP
**Objective**: Implement dependency injection for database sessions in MCP handlers
**Implementation Steps**:
1. Create dependency injection mechanism for DB sessions
2. Implement session lifecycle management for MCP tools
3. Add error handling and rollback logic for transactions
4. Test session creation and cleanup functionality

**Files to Create/Modify**:
- backend/mcp/session.py - Database session management for MCP
- backend/mcp/utils.py - Helper functions for session handling

**Dependencies**: Task 2.1, Task 1.2
**Verification**:
```bash
# Test session management
poetry run python -c "
from backend.mcp.session import get_db_session
from backend.database import Session

# Test session creation
with get_db_session() as session:
    assert isinstance(session, Session)
    print('Session management working correctly')
"
```

**Success Criteria**:
- [ ] Database session dependency injection works
- [ ] Session lifecycle properly managed
- [ ] Error handling and rollbacks implemented
- [ ] Session cleanup occurs automatically


### Task 2.3: Implement add_task Tool
**Objective**: Create the add_task MCP tool with full functionality
**Implementation Steps**:
1. Define tool schema with parameters and description
2. Implement handler function with proper validation
3. Add input validation and error handling
4. Test with sample data and edge cases

**Files to Create/Modify**:
- backend/mcp/tools/add_task.py - add_task tool implementation
- backend/mcp/tools/__init__.py - Export the tool

**Dependencies**: Task 2.2
**Verification**:
```bash
# Test add_task tool
poetry run python -c "
from backend.mcp.tools.add_task import handle_add_task
from backend.database import Session
from backend.models.task import Task

# Create a test session
with Session() as session:
    result = handle_add_task(session, 'user_test', 'Test task', 'Test description')
    print('Add task result:', result)
    assert result['status'] == 'created'
    assert result['title'] == 'Test task'
    print('add_task tool working correctly')
"
```

**Success Criteria**:
- [ ] Tool schema properly defined
- [ ] Handler function works with sample data
- [ ] Input validation implemented
- [ ] Error cases handled gracefully


### Task 2.4: Implement list_tasks Tool
**Objective**: Create the list_tasks MCP tool with filtering capabilities
**Implementation Steps**:
1. Define tool schema with filtering parameters
2. Implement filtering logic for all/pending/completed tasks
3. Add pagination support for large result sets
4. Test all filter options and pagination

**Files to Create/Modify**:
- backend/mcp/tools/list_tasks.py - list_tasks tool implementation

**Dependencies**: Task 2.2
**Verification**:
```bash
# Test list_tasks tool
poetry run python -c "
from backend.mcp.tools.list_tasks import handle_list_tasks
from backend.database import Session

# Create a test session
with Session() as session:
    result = handle_list_tasks(session, 'user_test', 'all')
    print('List tasks result:', result)
    assert 'tasks' in result
    assert 'count' in result
    print('list_tasks tool working correctly')
"
```

**Success Criteria**:
- [ ] Tool schema properly defined with filters
- [ ] Filtering logic works for all statuses
- [ ] Pagination support implemented
- [ ] All filter options tested successfully


### Task 2.5: Implement complete_task Tool
**Objective**: Create the complete_task MCP tool with proper validation
**Implementation Steps**:
1. Define tool schema with required parameters
2. Implement completion logic with ownership verification
3. Handle already-completed task case appropriately
4. Test edge cases and error scenarios

**Files to Create/Modify**:
- backend/mcp/tools/complete_task.py - complete_task tool implementation

**Dependencies**: Task 2.2
**Verification**:
```bash
# Test complete_task tool
poetry run python -c "
from backend.mcp.tools.add_task import handle_add_task
from backend.mcp.tools.complete_task import handle_complete_task
from backend.database import Session

# Create a test session
with Session() as session:
    # First add a task
    add_result = handle_add_task(session, 'user_test', 'Complete test task', 'Test description')
    task_id = add_result['task_id']

    # Then complete it
    complete_result = handle_complete_task(session, 'user_test', task_id)
    print('Complete task result:', complete_result)
    assert complete_result['completed'] == True
    print('complete_task tool working correctly')
"
```

**Success Criteria**:
- [ ] Tool schema properly defined
- [ ] Completion logic works correctly
- [ ] Ownership verification implemented
- [ ] Edge cases handled properly


### Task 2.6: Implement delete_task Tool
**Objective**: Create the delete_task MCP tool with proper validation
**Implementation Steps**:
1. Define tool schema with required parameters
2. Implement deletion logic with ownership verification
3. Handle soft delete option if implemented
4. Test various deletion scenarios

**Files to Create/Modify**:
- backend/mcp/tools/delete_task.py - delete_task tool implementation

**Dependencies**: Task 2.2
**Verification**:
```bash
# Test delete_task tool
poetry run python -c "
from backend.mcp.tools.add_task import handle_add_task
from backend.mcp.tools.delete_task import handle_delete_task
from backend.database import Session

# Create a test session
with Session() as session:
    # First add a task
    add_result = handle_add_task(session, 'user_test', 'Delete test task', 'Test description')
    task_id = add_result['task_id']

    # Then delete it
    delete_result = handle_delete_task(session, 'user_test', task_id)
    print('Delete task result:', delete_result)
    assert delete_result['status'] == 'deleted'
    print('delete_task tool working correctly')
"
```

**Success Criteria**:
- [ ] Tool schema properly defined
- [ ] Deletion logic works correctly
- [ ] Ownership verification implemented
- [ ] Various scenarios tested successfully


### Task 2.7: Implement update_task Tool
**Objective**: Create the update_task MCP tool with partial update capability
**Implementation Steps**:
1. Define tool schema with optional update parameters
2. Implement update logic for title and description
3. Add validation for empty updates and partial updates
4. Test various update combinations

**Files to Create/Modify**:
- backend/mcp/tools/update_task.py - update_task tool implementation

**Dependencies**: Task 2.2
**Verification**:
```bash
# Test update_task tool
poetry run python -c "
from backend.mcp.tools.add_task import handle_add_task
from backend.mcp.tools.update_task import handle_update_task
from backend.database import Session

# Create a test session
with Session() as session:
    # First add a task
    add_result = handle_add_task(session, 'user_test', 'Original task', 'Original description')
    task_id = add_result['task_id']

    # Then update it
    update_result = handle_update_task(session, 'user_test', task_id, 'Updated task title')
    print('Update task result:', update_result)
    assert update_result['title'] == 'Updated task title'
    print('update_task tool working correctly')
"
```

**Success Criteria**:
- [ ] Tool schema properly defined with optional fields
- [ ] Update logic works for title and description
- [ ] Validation for empty updates implemented
- [ ] Partial updates handled properly


### Task 2.8: Tool Registration & Testing
**Objective**: Register all tools with MCP server and create comprehensive test suite
**Implementation Steps**:
1. Register all 5 tools with MCP server instance
2. Create test suite for each individual tool
3. Document tool interfaces and parameters
4. Verify tools can be invoked programmatically

**Files to Create/Modify**:
- backend/mcp/registration.py - Tool registration logic
- backend/mcp/server.py - Update with registered tools
- tests/test_mcp_tools.py - Comprehensive tool test suite

**Dependencies**: Tasks 2.3, 2.4, 2.5, 2.6, 2.7
**Verification**:
```bash
# Test all tools registered and working
poetry run python -c "
from backend.mcp.server import mcp_server
import inspect

# Check if tools are registered
tool_names = [tool.name for tool in mcp_server._tools]
expected_tools = ['add_task', 'list_tasks', 'complete_task', 'delete_task', 'update_task']
assert all(tool in tool_names for tool in expected_tools)
print('All tools registered:', tool_names)
"
```

**Success Criteria**:
- [ ] All 5 tools registered with MCP server
- [ ] Each tool successfully modifies database
- [ ] Error cases handled gracefully
- [ ] Tools can be invoked programmatically
- [ ] Unit tests pass for all tools


**Phase 2 Completion Criteria**:
- All 5 tools registered and callable
- Each tool successfully modifies database
- Error cases handled gracefully
- Tools can be invoked programmatically
- Unit tests pass for all tools

## Phase 3: AI Agent & Chat API

### Task 3.1: OpenRouter Client Setup
**Objective**: Configure OpenAI client with OpenRouter base URL and API key
**Implementation Steps**:
1. Install OpenAI Python SDK and configure for OpenRouter
2. Create configuration module for OpenRouter settings
3. Test connection with simple prompt to verify functionality
4. Implement retry logic for failed requests

**Files to Create/Modify**:
- backend/config.py - OpenRouter configuration
- backend/ai_client.py - OpenAI client setup with OpenRouter

**Dependencies**: Phase 1 complete
**Verification**:
```bash
# Test OpenRouter connection
poetry run python -c "
from backend.ai_client import client
import os

if os.getenv('OPENROUTER_API_KEY'):
    response = client.chat.completions.create(
        model='meta-llama/llama-3.1-8b-instruct:free',
        messages=[{'role': 'user', 'content': 'Hello, test connection'}],
        max_tokens=10
    )
    print('OpenRouter connection successful:', len(response.choices[0].message.content) > 0)
else:
    print('OpenRouter API key not set, skipping connection test')
"
```

**Success Criteria**:
- [ ] OpenAI SDK configured with OpenRouter base URL
- [ ] API key properly loaded from environment
- [ ] Connection test successful
- [ ] Retry logic implemented for failed requests


### Task 3.2: System Prompt Design
**Objective**: Create effective system prompt for task management assistant
**Implementation Steps**:
1. Create system prompt focused on conciseness and task management
2. Add tool usage instructions and guidelines
3. Include example interactions for better AI behavior
4. Optimize for voice output and store in configuration

**Files to Create/Modify**:
- backend/prompts.py - System prompt definition
- backend/config.py - Add system prompt to configuration

**Dependencies**: Task 3.1
**Verification**:
```bash
# Test system prompt
poetry run python -c "
from backend.prompts import SYSTEM_PROMPT
print('System prompt length:', len(SYSTEM_PROMPT))
assert 'task management' in SYSTEM_PROMPT.lower()
assert 'tools' in SYSTEM_PROMPT.lower()
print('System prompt properly defined')
"
```

**Success Criteria**:
- [ ] System prompt created with task management focus
- [ ] Tool usage instructions included
- [ ] Examples provided for AI guidance
- [ ] Optimized for voice output (concise responses)


### Task 3.3: Conversation Manager Module
**Objective**: Implement conversation management logic for chat history
**Implementation Steps**:
1. Create conversation_manager.py module
2. Implement conversation creation and retrieval logic
3. Implement history retrieval with configurable limits
4. Add context window management for token efficiency

**Files to Create/Modify**:
- backend/conversation_manager.py - Conversation management logic
- backend/models/conversation.py - Verify conversation model

**Dependencies**: Task 3.2, Phase 1
**Verification**:
```bash
# Test conversation manager
poetry run python -c "
from backend.conversation_manager import create_conversation, get_conversation_history
from backend.database import Session

with Session() as session:
    # Create a conversation
    conv = create_conversation(session, 'user_test', 'Test conversation')
    print('Conversation created with ID:', conv.id)

    # Verify it can be retrieved
    history = get_conversation_history(session, conv.id)
    print('History retrieved successfully')
"
```

**Success Criteria**:
- [ ] Conversation creation works correctly
- [ ] History retrieval with limits implemented
- [ ] Context window management for tokens
- [ ] Messages formatted properly for OpenRouter


### Task 3.4: Tool Calling Integration
**Objective**: Connect OpenRouter responses to MCP tool handlers
**Implementation Steps**:
1. Parse tool_calls from LLM response in the chat flow
2. Execute corresponding MCP tool handlers with parameters
3. Handle multiple tool calls in sequence
4. Format tool results for LLM to generate final response

**Files to Create/Modify**:
- backend/tool_integration.py - Tool calling integration logic
- backend/chat_handler.py - Updated chat processing with tool calls

**Dependencies**: Task 3.3, Task 2.8
**Verification**:
```bash
# Test tool calling integration
poetry run python -c "
# This would be a more complex integration test
# For now, verify imports work
try:
    from backend.tool_integration import execute_tool_calls
    print('Tool integration module loaded successfully')
except ImportError as e:
    print(f'Tool integration not yet implemented: {e}')
"
```

**Success Criteria**:
- [ ] Tool calls parsed from LLM responses
- [ ] MCP tool handlers executed with parameters
- [ ] Multiple tool calls handled sequentially
- [ ] Tool results formatted for LLM consumption

**Estimated Time**: 3 hours

### Task 3.5: Chat Endpoint Implementation
**Objective**: Create the main chat API endpoint with proper validation
**Implementation Steps**:
1. Create POST /api/{user_id}/chat route in FastAPI
2. Implement request validation with Pydantic models
3. Add authentication middleware for user verification
4. Implement complete stateless request cycle with error handling

**Files to Create/Modify**:
- backend/api/chat.py - Chat API endpoint
- backend/schemas/chat.py - Request/response schemas
- backend/main.py - Register chat endpoint

**Dependencies**: Task 3.4, Phase 2
**Verification**:
```bash
# Test chat endpoint creation
poetry run python -c "
from backend.main import app
import inspect

# Check if chat endpoint is registered
routes = [route.path for route in app.routes]
chat_routes = [route for route in routes if 'chat' in route]
print('Chat routes registered:', chat_routes)
assert '/api/{user_id}/chat' in routes or any('chat' in route for route in routes)
print('Chat endpoint properly registered')
"
```

**Success Criteria**:
- [ ] Chat endpoint responds to requests
- [ ] Request validation implemented with Pydantic
- [ ] Authentication middleware protects endpoint
- [ ] Complete request cycle implemented with error handling


### Task 3.6: Message Persistence
**Objective**: Implement saving of user and assistant messages to database
**Implementation Steps**:
1. Save user messages to database when received
2. Save assistant responses to database when generated
3. Store tool_calls as JSON for debugging and analytics
4. Handle database errors gracefully without breaking chat flow

**Files to Create/Modify**:
- backend/message_persistence.py - Message saving logic
- backend/chat_handler.py - Update with persistence calls

**Dependencies**: Task 3.5
**Verification**:
```bash
# Test message persistence
poetry run python -c "
from backend.database import Session
from backend.models.message import Message
from sqlmodel import select

with Session() as session:
    # Count messages before test
    initial_count = len(session.exec(select(Message)).all())
    print(f'Initial message count: {initial_count}')
    # Additional testing would happen during integration
"
```

**Success Criteria**:
- [ ] User messages saved to database
- [ ] Assistant responses saved to database
- [ ] Tool calls stored as JSON
- [ ] Database errors handled gracefully


### Task 3.7: Response Formatting
**Objective**: Format assistant responses for client consumption
**Implementation Steps**:
1. Format assistant response text for client display
2. Include tool_calls summary in response
3. Add conversation metadata to response
4. Optimize response size and add timing metrics

**Files to Create/Modify**:
- backend/response_formatter.py - Response formatting logic
- backend/api/chat.py - Update with response formatting

**Dependencies**: Task 3.6
**Verification**:
```bash
# Test response formatting
poetry run python -c "
# Response formatting will be tested during integration
print('Response formatter will be tested during integration')
"
```

**Success Criteria**:
- [ ] Assistant responses formatted for client
- [ ] Tool calls summary included
- [ ] Conversation metadata added
- [ ] Response size optimized and timing logged


### Task 3.8: Testing & Documentation
**Objective**: Create comprehensive tests and API documentation
**Implementation Steps**:
1. Create test conversations for various scenarios
2. Test all natural language patterns and tool mappings
3. Document API with OpenAPI/Swagger
4. Create integration tests covering full chat flow

**Files to Create/Modify**:
- tests/test_chat_api.py - Chat API integration tests
- tests/test_conversations.py - Conversation flow tests
- docs/api.md - API documentation

**Dependencies**: All previous tasks in Phase 3
**Verification**:
```bash
# Run chat API tests
# This will be implemented as part of the task
echo "Tests will be run as part of implementation"
```

**Success Criteria**:
- [ ] Test conversations created and working
- [ ] Natural language patterns tested
- [ ] API documented with OpenAPI
- [ ] Integration tests cover full flow
- [ ] Error responses clear and helpful
- [ ] Response times acceptable (<3s)


**Phase 3 Completion Criteria**:
- Chat endpoint responds to requests
- LLM successfully calls MCP tools
- Conversations persist across requests
- Can test via Swagger UI or curl
- Error responses are clear and helpful
- Response times are acceptable (<3s)

## Phase 4: Frontend & Voice Integration

### Task 4.1: Frontend Project Setup
**Objective**: Initialize React/Next.js project with proper configuration
**Implementation Steps**:
1. Initialize Next.js project with TypeScript configuration
2. Install OpenAI ChatKit package and dependencies
3. Set up Tailwind CSS for styling
4. Create basic project structure with pages and components

**Files to Create/Modify**:
- frontend/package.json - Frontend dependencies
- frontend/tsconfig.json - TypeScript configuration
- frontend/tailwind.config.js - Tailwind CSS setup
- frontend/pages/index.tsx - Main page with chat interface

**Dependencies**: Phase 3 complete
**Verification**:
```bash
# Test frontend setup (would be run from frontend directory)
# cd frontend && npm install && npm run dev
echo "Frontend setup will be verified by running development server"
```

**Success Criteria**:
- [ ] Next.js project initialized successfully
- [ ] OpenAI ChatKit installed and configured
- [ ] TypeScript configured properly
- [ ] Tailwind CSS working for styling


### Task 4.2: ChatKit Configuration
**Objective**: Configure OpenAI ChatKit with backend API integration
**Implementation Steps**:
1. Configure ChatKit with backend API URL and endpoints
2. Set up authentication headers for API calls
3. Configure message formatting for proper display
4. Add error boundary for graceful error handling

**Files to Create/Modify**:
- frontend/src/components/ChatKitWrapper.tsx - ChatKit wrapper component
- frontend/src/config/chat.ts - Chat configuration
- frontend/src/utils/auth.ts - Authentication utilities

**Dependencies**: Task 4.1
**Verification**:
```bash
# Test ChatKit configuration
echo "ChatKit configuration will be tested by running the component"
```

**Success Criteria**:
- [ ] ChatKit configured with backend API
- [ ] Authentication headers properly set
- [ ] Message formatting works correctly
- [ ] Error boundary catches and handles errors


### Task 4.3: Chat API Client
**Objective**: Create API client service for chat endpoint communication
**Implementation Steps**:
1. Create API client service for POST /api/{user_id}/chat
2. Implement request/response typing with TypeScript
3. Add proper error handling for API failures
4. Implement loading states for better UX

**Files to Create/Modify**:
- frontend/src/services/chat-api.ts - Chat API client
- frontend/src/types/chat.ts - Chat-related TypeScript types
- frontend/src/hooks/useChat.ts - Chat hook for state management

**Dependencies**: Task 4.2
**Verification**:
```bash
# Test API client
echo "API client will be tested by making actual API calls"
```

**Success Criteria**:
- [ ] API client service implemented
- [ ] TypeScript types properly defined
- [ ] Error handling implemented
- [ ] Loading states working


### Task 4.4: Chat UI Components
**Objective**: Build reusable chat UI components
**Implementation Steps**:
1. Create ChatContainer component for layout
2. Implement MessageList component for displaying messages
3. Create MessageInput component for user input
4. Add typing indicators and loading states

**Files to Create/Modify**:
- frontend/src/components/ChatContainer.tsx - Main chat container
- frontend/src/components/MessageList.tsx - Message list display
- frontend/src/components/MessageInput.tsx - Input field component
- frontend/src/components/TypingIndicator.tsx - Typing indicator

**Dependencies**: Task 4.3
**Verification**:
```bash
# Test UI components
echo "UI components will be tested by rendering in development mode"
```

**Success Criteria**:
- [ ] Chat container properly laid out
- [ ] Message list displays messages correctly
- [ ] Message input accepts and submits messages
- [ ] Typing indicators show when loading


### Task 4.5: Web Speech API - Speech Recognition (STT)
**Objective**: Implement speech-to-text functionality using Web Speech API
**Implementation Steps**:
1. Check browser compatibility for SpeechRecognition
2. Implement SpeechRecognition hook with proper state management
3. Create microphone button component for voice input
4. Add recording indicator and error handling

**Files to Create/Modify**:
- frontend/src/hooks/useSpeechRecognition.ts - STT hook
- frontend/src/components/MicrophoneButton.tsx - Microphone UI component
- frontend/src/utils/speech.ts - Speech utility functions

**Dependencies**: Task 4.4
**Verification**:
```bash
# Test STT functionality
echo "STT will be tested in browser environment"
```

**Success Criteria**:
- [ ] Browser compatibility checked
- [ ] Speech recognition hook working
- [ ] Microphone button UI implemented
- [ ] Recording indicator shows properly
- [ ] Error handling for permissions implemented


### Task 4.6: Web Speech API - Speech Synthesis (TTS)
**Objective**: Implement text-to-speech functionality using Web Speech API
**Implementation Steps**:
1. Implement SpeechSynthesis hook for voice output
2. Add "read aloud" functionality for assistant responses
3. Configure voice settings (rate, pitch, volume)
4. Add play/pause/stop controls and speech queue management

**Files to Create/Modify**:
- frontend/src/hooks/useSpeechSynthesis.ts - TTS hook
- frontend/src/components/VoiceControls.tsx - Voice playback controls
- frontend/src/utils/speech.ts - Update with TTS functions

**Dependencies**: Task 4.5
**Verification**:
```bash
# Test TTS functionality
echo "TTS will be tested in browser environment"
```

**Success Criteria**:
- [ ] Speech synthesis hook working
- [ ] "Read aloud" functionality implemented
- [ ] Voice settings configurable
- [ ] Play/pause/stop controls available
- [ ] Speech queue managed properly


### Task 4.7: Voice Mode Integration
**Objective**: Integrate voice input/output into the chat flow
**Implementation Steps**:
1. Connect STT output to chat input for voice commands
2. Auto-trigger TTS for assistant responses
3. Add voice mode toggle switch
4. Implement continuous listening if needed

**Files to Create/Modify**:
- frontend/src/components/VoiceModeToggle.tsx - Voice mode toggle
- frontend/src/contexts/VoiceContext.tsx - Voice state management
- frontend/src/components/ChatContainer.tsx - Update with voice integration

**Dependencies**: Task 4.6
**Verification**:
```bash
# Test voice integration
echo "Voice integration will be tested end-to-end in browser"
```

**Success Criteria**:
- [ ] Voice input connected to chat input
- [ ] TTS auto-triggers for responses
- [ ] Voice mode toggle works
- [ ] Continuous listening implemented if needed


### Task 4.8: State Management
**Objective**: Implement comprehensive state management for chat application
**Implementation Steps**:
1. Manage conversation state across components
2. Handle message history with proper updates
3. Manage loading states throughout the app
4. Persist conversation_id and handle reconnections

**Files to Create/Modify**:
- frontend/src/store/chatSlice.ts - Redux slice for chat state (or Zustand store)
- frontend/src/contexts/ChatContext.tsx - Chat state context
- frontend/src/hooks/useConversation.ts - Conversation state hook

**Dependencies**: Task 4.7
**Verification**:
```bash
# Test state management
echo "State management will be tested through component interactions"
```

**Success Criteria**:
- [ ] Conversation state managed properly
- [ ] Message history updates correctly
- [ ] Loading states displayed appropriately
- [ ] Conversation ID persists and reconnects work


### Task 4.9: Authentication Integration
**Objective**: Integrate with Better Auth for user authentication
**Implementation Steps**:
1. Integrate with existing Better Auth system
2. Add login/logout flow to frontend
3. Store and manage auth tokens securely
4. Add protected routes and token refresh

**Files to Create/Modify**:
- frontend/src/services/auth.ts - Authentication service
- frontend/src/components/LoginButton.tsx - Login UI component
- frontend/src/middleware.ts - Protected route middleware

**Dependencies**: Task 4.8
**Verification**:
```bash
# Test authentication integration
echo "Authentication will be tested with actual Better Auth integration"
```

**Success Criteria**:
- [ ] Better Auth integration working
- [ ] Login/logout flow functional
- [ ] Auth tokens stored securely
- [ ] Protected routes implemented
- [ ] Token refresh handled


### Task 4.10: Error Handling & UX Polish
**Objective**: Implement comprehensive error handling and user experience improvements
**Implementation Steps**:
1. Add user-friendly error messages throughout the app
2. Implement retry logic for failed operations
3. Create empty states and loading skeletons
4. Add success confirmations and offline detection

**Files to Create/Modify**:
- frontend/src/components/ErrorBoundary.tsx - Error boundary component
- frontend/src/components/EmptyState.tsx - Empty state component
- frontend/src/components/LoadingSkeleton.tsx - Loading skeleton
- frontend/src/hooks/useOnlineStatus.ts - Online/offline detection

**Dependencies**: Task 4.9
**Verification**:
```bash
# Test error handling and UX
echo "Error handling and UX will be tested through various scenarios"
```

**Success Criteria**:
- [ ] Error messages display properly to users
- [ ] Retry logic implemented for failures
- [ ] Empty states show when appropriate
- [ ] Loading skeletons provide feedback
- [ ] Success confirmations work
- [ ] Offline detection implemented

**Phase 4 Completion Criteria**:
- Chat UI renders and is responsive
- Can type messages and receive responses
- Voice input converts speech to text
- Voice output reads responses aloud
- Authentication works end-to-end
- Error states display properly
- Works on both desktop and mobile browsers

## Phase 5: Deployment, Testing & Polish

### Task 5.1: Environment Configuration
**Objective**: Prepare production environment configuration and security settings
**Implementation Steps**:
1. Create production .env template with all required variables
2. Document all environment variables with descriptions
3. Configure OpenRouter domain allowlist for production
4. Configure proper CORS settings and security headers

**Files to Create/Modify**:
- .env.production - Production environment template
- docs/deployment.md - Deployment documentation
- backend/main.py - Update CORS and security settings

**Dependencies**: Phase 4 complete
**Verification**:
```bash
# Verify environment configuration
echo "Environment configuration will be verified during deployment"
```

**Success Criteria**:
- [ ] Production environment template created
- [ ] All environment variables documented
- [ ] OpenRouter domain allowlist configured
- [ ] CORS and security headers properly set


### Task 5.2: Backend Deployment Preparation
**Objective**: Prepare backend for production deployment with monitoring
**Implementation Steps**:
1. Add health check endpoints for deployment monitoring
2. Implement structured logging for production
3. Add request/response logging for debugging
4. Configure rate limiting to prevent abuse

**Files to Create/Modify**:
- backend/api/health.py - Health check endpoints
- backend/logging_config.py - Structured logging configuration
- backend/middleware/rate_limit.py - Rate limiting middleware
- backend/main.py - Register health checks and logging

**Dependencies**: Task 5.1
**Verification**:
```bash
# Test health endpoints
curl -v http://localhost:8000/health/db
curl -v http://localhost:8000/health/api
```

**Success Criteria**:
- [ ] Health check endpoints available
- [ ] Structured logging implemented
- [ ] Request/response logging working
- [ ] Rate limiting configured properly


### Task 5.3: Frontend Deployment Preparation
**Objective**: Prepare frontend for production deployment and optimization
**Implementation Steps**:
1. Optimize build for production with tree shaking
2. Implement environment variable management for frontend
3. Configure for deployment platforms (Vercel/Netlify)
4. Optimize bundle size and implement lazy loading

**Files to Create/Modify**:
- frontend/next.config.js - Next.js production configuration
- frontend/public/vercel.json - Vercel deployment config
- frontend/src/utils/build.ts - Build optimization utilities

**Dependencies**: Task 5.2
**Verification**:
```bash
# Test production build
# cd frontend && npm run build
echo "Production build will be tested during build process"
```

**Success Criteria**:
- [ ] Production build succeeds
- [ ] Bundle size optimized
- [ ] Environment variables managed properly
- [ ] Lazy loading implemented where appropriate


### Task 5.4: End-to-End Testing
**Objective**: Conduct comprehensive testing of complete user flows
**Implementation Steps**:
1. Test complete user flows from login to chat completion
2. Test all natural language commands and tool mappings
3. Test voice input/output functionality
4. Test error scenarios and edge cases

**Files to Create/Modify**:
- tests/e2e/test_full_flow.py - Full user flow tests
- tests/e2e/test_voice_features.py - Voice functionality tests
- tests/e2e/test_error_scenarios.py - Error scenario tests

**Dependencies**: Task 5.3
**Verification**:
```bash
# Run end-to-end tests
pytest tests/e2e/ -v
```

**Success Criteria**:
- [ ] Complete user flows tested successfully
- [ ] Natural language commands work
- [ ] Voice input/output tested
- [ ] Error scenarios handled properly
- [ ] Edge cases covered


### Task 5.5: Security Hardening
**Objective**: Implement security measures to protect the application
**Implementation Steps**:
1. Validate all user inputs and sanitize where necessary
2. Implement rate limiting to prevent abuse
3. Add CSRF protection where needed
4. Review and enhance authentication flow security

**Files to Create/Modify**:
- backend/security.py - Security utilities and validation
- backend/middleware/security.py - Security middleware
- backend/main.py - Update with security measures

**Dependencies**: Task 5.4
**Verification**:
```bash
# Test security measures
# Run security-focused tests
pytest tests/security/ -v
```

**Success Criteria**:
- [ ] Input validation implemented everywhere
- [ ] Rate limiting prevents abuse
- [ ] CSRF protection added where needed
- [ ] Authentication flow secured


### Task 5.6: Documentation
**Objective**: Create comprehensive documentation for the application
**Implementation Steps**:
1. Update README.md with Phase III setup instructions
2. Document all API endpoints with examples
3. Create user guide for chatbot features
4. Document deployment process and troubleshooting

**Files to Create/Modify**:
- README.md - Updated with Phase III instructions
- docs/api-reference.md - Complete API documentation
- docs/user-guide.md - User guide for chat features
- docs/troubleshooting.md - Troubleshooting guide

**Dependencies**: Task 5.5
**Verification**:
```bash
# Verify documentation exists and is accurate
ls -la docs/
cat docs/api-reference.md | head -20
```

**Success Criteria**:
- [ ] README updated with Phase III instructions
- [ ] API endpoints fully documented
- [ ] User guide created and comprehensive
- [ ] Deployment process documented
- [ ] Troubleshooting section complete


### Task 5.7: Monitoring & Observability
**Objective**: Implement monitoring and observability for production
**Implementation Steps**:
1. Add application logging for monitoring
2. Set up error tracking with centralized logging
3. Add performance monitoring for key metrics
4. Create health dashboard for ops team

**Files to Create/Modify**:
- backend/monitoring.py - Monitoring utilities
- backend/metrics.py - Application metrics
- backend/main.py - Register monitoring endpoints

**Dependencies**: Task 5.6
**Verification**:
```bash
# Test monitoring endpoints
curl -v http://localhost:8000/metrics
```

**Success Criteria**:
- [ ] Application logging implemented
- [ ] Error tracking configured
- [ ] Performance metrics available
- [ ] Health dashboard accessible


### Task 5.8: Final Polish
**Objective**: Clean up code and optimize for production readiness
**Implementation Steps**:
1. Remove console.logs and debug code from production
2. Optimize database queries and add indexes if needed
3. Run linters and formatters on all code
4. Update dependencies to latest stable versions

**Files to Create/Modify**:
- Various files - Cleanup and optimization
- pyproject.toml - Update dependencies
- frontend/package.json - Update frontend dependencies

**Dependencies**: Task 5.7
**Verification**:
```bash
# Run linting and formatting
# Backend
poetry run black .
poetry run ruff check .

# Frontend
cd frontend && npm run lint && npm run format
```

**Success Criteria**:
- [ ] Debug code removed from production
- [ ] Database queries optimized
- [ ] Code formatted and linted
- [ ] Dependencies updated to stable versions


**Phase 5 Completion Criteria**:
- Application deployed and accessible
- All features working in production
- Documentation complete and accurate
- Monitoring in place
- No critical bugs
- Performance acceptable
- Security reviewed

## Dependency Graph

```
Phase 1: Foundation & Database Setup
├─ Task 1.1: Environment Setup (🔧)
├─ Task 1.2: Database Configuration (💾) - depends on 1.1
├─ Task 1.3: Database Models (💾) - depends on 1.2
└─ Task 1.4: Database Migration (💾) - depends on 1.3

Phase 2: MCP Server Implementation
├─ Task 2.1: MCP Server Initialization (🤖) - depends on Phase 1
├─ Task 2.2: Database Session Management (🤖) - depends on 2.1, 1.2
├─ Task 2.3: Implement add_task Tool (🤖) - depends on 2.2
├─ Task 2.4: Implement list_tasks Tool (🤖) - depends on 2.2
├─ Task 2.5: Implement complete_task Tool (🤖) - depends on 2.2
├─ Task 2.6: Implement delete_task Tool (🤖) - depends on 2.2
├─ Task 2.7: Implement update_task Tool (🤖) - depends on 2.2
└─ Task 2.8: Tool Registration & Testing (🤖) - depends on 2.3-2.7

Phase 3: AI Agent & Chat API
├─ Task 3.1: OpenRouter Client Setup (🤖) - depends on Phase 1
├─ Task 3.2: System Prompt Design (🤖) - depends on 3.1
├─ Task 3.3: Conversation Manager (🤖) - depends on 3.2, Phase 1
├─ Task 3.4: Tool Calling Integration (🤖) - depends on 3.3, Phase 2
├─ Task 3.5: Chat Endpoint Implementation (🤖) - depends on 3.4, Phase 2
├─ Task 3.6: Message Persistence (🤖) - depends on 3.5
├─ Task 3.7: Response Formatting (🤖) - depends on 3.6
└─ Task 3.8: Testing & Documentation (🤖) - depends on all Phase 3 tasks

Phase 4: Frontend & Voice Integration
├─ Task 4.1: Frontend Project Setup (🎨) - depends on Phase 3
├─ Task 4.2: ChatKit Configuration (🎨) - depends on 4.1
├─ Task 4.3: Chat API Client (🎨) - depends on 4.2
├─ Task 4.4: Chat UI Components (🎨) - depends on 4.3
├─ Task 4.5: Web Speech API - STT (🎨) - depends on 4.4
├─ Task 4.6: Web Speech API - TTS (🎨) - depends on 4.5
├─ Task 4.7: Voice Mode Integration (🎨) - depends on 4.6
├─ Task 4.8: State Management (🎨) - depends on 4.7
├─ Task 4.9: Authentication Integration (🎨) - depends on 4.8
└─ Task 4.10: Error Handling & UX (🎨) - depends on 4.9

Phase 5: Deployment, Testing & Polish
├─ Task 5.1: Environment Configuration (🚀) - depends on Phase 4
├─ Task 5.2: Backend Deployment Preparation (🚀) - depends on 5.1
├─ Task 5.3: Frontend Deployment Preparation (🚀) - depends on 5.2
├─ Task 5.4: End-to-End Testing (🚀) - depends on 5.3
├─ Task 5.5: Security Hardening (🚀) - depends on 5.4
├─ Task 5.6: Documentation (🚀) - depends on 5.5
├─ Task 5.7: Monitoring & Observability (🚀) - depends on 5.6
└─ Task 5.8: Final Polish (🚀) - depends on 5.7
```

## Risk Assessment

### Phase 1 Risks:
- Database connection issues with Neon PostgreSQL
- Migration conflicts or failures
- Schema validation problems

### Phase 2 Risks:
- MCP SDK compatibility issues
- Tool registration failures
- Database session management conflicts

### Phase 3 Risks:
- OpenRouter API connectivity problems
- Tool calling integration complexity
- Rate limiting from API providers

### Phase 4 Risks:
- Web Speech API browser compatibility
- Authentication integration challenges
- Performance issues with real-time features

### Phase 5 Risks:
- Security vulnerabilities in production
- Scalability issues under load
- Monitoring gaps leading to undetected issues

## Time Estimates

- Phase 1: 6.5 hours
- Phase 2: 14 hours
- Phase 3: 16 hours
- Phase 4: 21 hours
- Phase 5: 16.5 hours
- **Total Estimated Time: 74 hours**

## Testing Strategy

- **Unit Tests**: Individual functions and components
- **Integration Tests**: API endpoints with database
- **End-to-End Tests**: Complete user flows
- **Performance Tests**: Response times and load handling
- **Security Tests**: Input validation and access control

## Rollback Plan

- Database: Use Alembic to downgrade schema changes
- Backend: Revert to previous version with git tags
- Frontend: Deploy previous build version
- Configuration: Rollback environment variables
- Dependencies: Use lock files to revert to known good versions

## Success Metrics

- ✅ AI chatbot successfully integrated with existing todo functionality
- ✅ Natural language processing works for all task operations
- ✅ Voice input/output functional across supported browsers
- ✅ MCP tools properly integrated and accessible to AI
- ✅ All existing Phase II functionality preserved
- ✅ Security and authentication maintained
- ✅ Performance acceptable (responses under 3 seconds)
- ✅ Proper error handling and user feedback
- ✅ Production-ready with monitoring and logging
- ✅ Comprehensive documentation provided

This implementation plan provides a complete roadmap for developing the AI Chatbot integration for the Todo application, following the MCP architecture with OpenRouter and voice capabilities.
