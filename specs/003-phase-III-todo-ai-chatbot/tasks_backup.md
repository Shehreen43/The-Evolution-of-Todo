# Task Breakdown: AI Chatbot Integration for Todo Application (Phase III)

## Foundation Tasks (FOUND-XXX)

### FOUND-001: Project Structure Setup
**Category**: Foundation
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Create the project directory structure for Phase III backend components, following the existing project architecture and preparing for the AI chatbot implementation.

### Dependencies
- None

### Acceptance Criteria
- [ ] Backend directory structure created for Phase III components
- [ ] Proper subdirectories for models, api, mcp, handlers, etc.
- [ ] Frontend directory structure created for chat components
- [ ] Git ignore file updated to exclude unnecessary files

### Implementation Checklist
- [ ] Create `backend/mcp/` directory structure
- [ ] Create `backend/handlers/` directory structure
- [ ] Create `backend/prompts/` directory structure
- [ ] Create `backend/conversation_manager.py` file
- [ ] Create `frontend/src/components/` directory structure
- [ ] Create `frontend/src/hooks/` directory structure
- [ ] Create `frontend/src/services/` directory structure

### Files to Create/Modify
```
backend/mcp/__init__.py              [CREATE]   - MCP package initialization
backend/mcp/server.py                [CREATE]   - MCP server instance
backend/handlers/__init__.py         [CREATE]   - Handler package initialization
backend/prompts.py                   [CREATE]   - System prompt definitions
frontend/src/components/__init__.tsx [CREATE]   - Component exports
frontend/src/hooks/__init__.tsx      [CREATE]   - Hook exports
frontend/src/services/__init__.tsx   [CREATE]   - Service exports
```

### Technical Details

Key Functions/Classes: Project directory structure
External Dependencies: None
Configuration: None

### Testing Instructions
# Step 1: Verify directory structure exists
ls -la backend/mcp/
ls -la backend/handlers/
ls -la backend/prompts/
ls -la frontend/src/components/
ls -la frontend/src/hooks/
ls -la frontend/src/services/

# Step 2: Verify basic files created
cat backend/mcp/__init__.py
cat backend/mcp/server.py
# Should contain basic initialization code

# Step 3: Verify gitignore updates
grep -E "(__pycache__|node_modules|\.pyc|\.env)" .gitignore
# Should contain appropriate ignore patterns
```

### Potential Issues & Solutions
- **Issue**: Directory conflicts with existing files
  - **Solution**: Check existing directory structure before creating
- **Issue**: Incorrect file permissions on creation
  - **Solution**: Set proper permissions after creation

### Related Documentation
- Project structure conventions: Following existing Phase II patterns
- Python package structure: PEP 8 guidelines

---

### FOUND-002: Python Environment Configuration
**Category**: Foundation
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Initialize Python virtual environment with poetry for Phase III backend components, ensuring all dependencies are properly managed and isolated.

### Dependencies
- FOUND-001: Project Structure Setup (must be completed first)

### Acceptance Criteria
- [ ] Poetry virtual environment initialized successfully
- [ ] pyproject.toml configured with all required dependencies
- [ ] Dependencies installed without conflicts
- [ ] Environment activated and working properly

### Implementation Checklist
- [ ] Create `backend/pyproject.toml` with proper configuration
- [ ] Add required dependencies: fastapi, sqlmodel, openai, mcp, etc.
- [ ] Initialize poetry environment with `poetry install`
- [ ] Activate environment and verify dependencies work
- [ ] Add development dependencies for testing and linting

### Files to Create/Modify
```
backend/pyproject.toml              [CREATE]   - Poetry configuration file
backend/.env                        [CREATE]   - Environment variables file (gitignored)
backend/.venv                       [CREATE]   - Virtual environment (gitignored)
```

### Technical Details

Key Functions/Classes: Poetry dependency management
External Dependencies: poetry, python 3.9+
Configuration: Dependencies in pyproject.toml

### Testing Instructions
# Step 1: Initialize poetry environment
cd backend && poetry init
# Follow prompts to create pyproject.toml

# Step 2: Add dependencies to pyproject.toml
poetry add fastapi uvicorn sqlmodel openai mcp python-multipart python-jose[cryptography] passlib[bcrypt]

# Step 3: Install dependencies
poetry install

# Step 4: Test environment activation
poetry shell
python -c "import fastapi, sqlmodel, openai; print('All dependencies loaded')"
```

### Potential Issues & Solutions
- **Issue**: Dependency conflicts between packages
  - **Solution**: Use poetry's conflict resolution or specify compatible versions
- **Issue**: Python version compatibility issues
  - **Solution**: Ensure Python 3.9+ is installed and configured

### Related Documentation
- Poetry documentation: https://python-poetry.org/docs/
- FastAPI dependencies: https://fastapi.tiangolo.com/
- SQLModel dependencies: https://sqlmodel.tiangolo.com/

---

### FOUND-003: Dependency Installation
**Category**: Foundation
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Install all required dependencies for the AI chatbot project with specific versions to ensure compatibility and reproducible builds.

### Dependencies
- FOUND-002: Python Environment Configuration (must be completed first)

### Acceptance Criteria
- [ ] All core dependencies installed successfully
- [ ] MCP SDK installed and accessible
- [ ] OpenAI Python SDK installed and working
- [ ] SQLModel and FastAPI dependencies working
- [ ] Version conflicts resolved

### Implementation Checklist
- [ ] Install FastAPI and Uvicorn for web framework
- [ ] Install SQLModel for database operations
- [ ] Install OpenAI SDK for LLM integration
- [ ] Install MCP SDK for Model Context Protocol
- [ ] Install authentication libraries (Better Auth related)
- [ ] Install testing libraries (pytest, etc.)
- [ ] Install linting/formatting tools (black, ruff)

### Files to Create/Modify
```
backend/pyproject.toml              [MODIFY]   - Add all project dependencies
backend/poetry.lock                 [CREATE]   - Lock file with exact versions
```

### Technical Details

Key Functions/Classes: Dependency management with Poetry
External Dependencies:
- fastapi: Web framework
- sqlmodel: Database ORM
- openai: LLM integration
- mcp: Model Context Protocol
- python-multipart: Form data handling
- python-jose: JWT token handling
- passlib: Password hashing
- bcrypt: Password hashing algorithm

### Testing Instructions
# Step 1: Install all dependencies
cd backend
poetry add fastapi uvicorn sqlmodel openai mcp python-multipart python-jose[cryptography] passlib[bcrypt]
poetry add --group dev pytest pytest-asyncio httpx black ruff mypy

# Step 2: Verify dependencies work
poetry run python -c "
import fastapi
import sqlmodel
import openai
import mcp
print('All core dependencies imported successfully')
"
```

### Potential Issues & Solutions
- **Issue**: MCP SDK not available via standard channels
  - **Solution**: Install from official MCP repository or PyPI if available
- **Issue**: Version conflicts with existing dependencies
  - **Solution**: Use poetry's dependency resolution features

### Related Documentation
- MCP SDK: https://modelcontextprotocol.io/
- OpenAI SDK: https://platform.openai.com/docs/libraries/python
- SQLModel: https://sqlmodel.tiangolo.com/

---

### FOUND-004: Environment Variables Template
**Category**: Foundation
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 0.5 hours

### Description
Create .env.example template with all required environment variables for the AI chatbot application, documenting each variable's purpose.

### Dependencies
- FOUND-003: Dependency Installation (must be completed first)

### Acceptance Criteria
- [ ] .env.example file created with all required variables
- [ ] Each variable properly documented with comments
- [ ] Default values provided where appropriate
- [ ] Sensitive variables marked as required

### Implementation Checklist
- [ ] Create `.env.example` file in project root
- [ ] Add OpenRouter API key variable
- [ ] Add database connection variables
- [ ] Add authentication secret variables
- [ ] Add application configuration variables
- [ ] Document each variable with comments

### Files to Create/Modify
```
.env.example                        [CREATE]   - Environment variables template
```

### Technical Details

Key Functions/Classes: Environment configuration
External Dependencies: None
Configuration: All required environment variables

### Testing Instructions
# Step 1: Create .env.example file
cat .env.example
# Should contain all required environment variables

# Step 2: Verify file format
grep -E "^[A-Z_]+=" .env.example | head -5
# Should show environment variable assignments

# Step 3: Check for required variables
grep -E "(OPENROUTER_API_KEY|DATABASE_URL|BETTER_AUTH_SECRET)" .env.example
# Should find all critical variables
```

### Potential Issues & Solutions
- **Issue**: Missing critical environment variables
  - **Solution**: Review implementation plan for all required variables
- **Issue**: Variables with incorrect format
  - **Solution**: Follow standard environment variable naming conventions

### Related Documentation
- Environment variable best practices: https://12factor.net/config
- Security best practices for API keys: https://owasp.org/www-community/vulnerabilities/Secret_Guessing

---

### FOUND-005: Git Repository Setup
**Category**: Foundation
**Priority**: Critical
**Complexity**: Small


### Description
Update git repository configuration to properly track Phase III files while ignoring sensitive and temporary files.

### Dependencies
- FOUND-001: Project Structure Setup (must be completed first)

### Acceptance Criteria
- [ ] .gitignore updated to exclude sensitive files
- [ ] .gitignore includes Python and Node.js patterns
- [ ] Repository properly initialized for Phase III
- [ ] No sensitive files accidentally committed

### Implementation Checklist
- [ ] Update `.gitignore` with Python patterns
- [ ] Add Node.js patterns for frontend
- [ ] Include environment files in ignore list
- [ ] Add build artifacts to ignore list
- [ ] Add local configuration files to ignore list

### Files to Create/Modify
```
.gitignore                          [MODIFY]   - Git ignore patterns
```

### Technical Details

Key Functions/Classes: Git configuration
External Dependencies: Git
Configuration: Ignore patterns

### Testing Instructions
# Step 1: Check git status
git status
# Should not show any sensitive files

# Step 2: Verify gitignore patterns
cat .gitignore | grep -E "(\.env|__pycache__|node_modules|\.pyc)"
# Should show relevant ignore patterns

# Step 3: Test file addition
git add . && git status
# Should not include ignored files
```

### Potential Issues & Solutions
- **Issue**: Accidentally committing sensitive files
  - **Solution**: Regular review of git status and .gitignore
- **Issue**: Missing important ignore patterns
  - **Solution**: Use standard Python/Node.js .gitignore templates

### Related Documentation
- Git best practices: https://git-scm.com/book/en/v2
- GitHub recommended .gitignore: https://github.com/github/gitignore

---

## Database Tasks (DB-XXX)

### DB-001: Database Connection Setup
**Category**: Database
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1.5 hours

### Description
Configure Neon PostgreSQL connection with SQLModel engine setup, connection pooling, and health check endpoint for the AI chatbot application.

### Dependencies
- FOUND-003: Dependency Installation (must be completed first)

### Acceptance Criteria
- [ ] Database engine connects successfully to Neon
- [ ] Connection pooling configured properly
- [ ] Health check endpoint returns 200 status
- [ ] Database session management works correctly

### Implementation Checklist
- [ ] Create `backend/database.py` with SQLModel engine setup
- [ ] Implement connection pooling configuration
- [ ] Add health check endpoint for database connectivity
- [ ] Test database connection with sample query
- [ ] Configure proper error handling for connection issues

### Files to Create/Modify
```
backend/database.py                 [CREATE]   - Database connection and session management
backend/main.py                   [MODIFY]   - Add health check endpoint
```

### Technical Details

Key Functions/Classes:
- create_engine: SQLModel database engine
- Session: Database session class
- get_session: Session dependency generator
External Dependencies: sqlmodel, sqlalchemy
Configuration: DATABASE_URL environment variable

### Testing Instructions
# Step 1: Test database connection
poetry run python -c "
from backend.database import engine
from sqlmodel import create_engine
print('Database engine created successfully')
"

# Step 2: Test health check endpoint
curl http://localhost:8000/health/db
# Expected output: JSON with status: ok

# Step 3: Test session creation
poetry run python -c "
from backend.database import Session
with Session() as session:
    print('Database session created successfully')
"
```

### Potential Issues & Solutions
- **Issue**: Neon connection timeout or authentication failure
  - **Solution**: Verify connection string and credentials in environment
- **Issue**: Connection pooling configuration issues
  - **Solution**: Adjust pool size and timeout settings based on usage patterns

### Related Documentation
- SQLModel database: https://sqlmodel.tiangolo.com/tutorial/database/connect/
- Connection pooling: https://docs.sqlalchemy.org/en/14/core/pooling.html
- Neon PostgreSQL: https://neon.tech/docs

---

### DB-002: Extend Task Model (if needed)
**Category**: Database
**Priority**: Medium
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Verify and extend the existing Task model from Phase II if needed for AI chatbot functionality, ensuring no breaking changes to existing functionality.

### Dependencies
- DB-001: Database Connection Setup (must be completed first)

### Acceptance Criteria
- [ ] Existing Task model verified for compatibility
- [ ] No breaking changes to existing functionality
- [ ] Model properly integrated with SQLModel
- [ ] Proper indexes and constraints maintained

### Implementation Checklist
- [ ] Review existing `backend/models/task.py` from Phase II
- [ ] Verify model compatibility with current requirements
- [ ] Update model if necessary to support new features
- [ ] Ensure existing functionality remains unchanged
- [ ] Add any missing relationships or constraints

### Files to Create/Modify
```
backend/models/task.py              [MODIFY]   - Verify existing model and make necessary updates
```

### Technical Details

Key Functions/Classes: Task (SQLModel)
External Dependencies: sqlmodel, datetime, typing
Configuration: None required
Database Table Name: tasks

### Testing Instructions
# Step 1: Test model import
poetry run python -c "
from backend.models.task import Task
task = Task(user_id='test_user', title='Test task')
print('Task model imported successfully')
print(f'Task table: {Task.__tablename__}')
"


# Step 2: Verify existing functionality
poetry run python -c "
from backend.models.task import Task
from datetime import datetime

# Test creating a task
task = Task(
    user_id='user_test',
    title='Test task',
    description='Test description',
    completed=False,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)
print('Task creation works:', task.title == 'Test task')
"
```

### Potential Issues & Solutions
- **Issue**: Breaking changes to existing functionality
  - **Solution**: Maintain backward compatibility and run existing tests
- **Issue**: Missing required fields or validation
  - **Solution**: Ensure all Phase II functionality remains intact

### Related Documentation
- Phase II task model: Review existing implementation
- SQLModel relationships: https://sqlmodel.tiangolo.com/advanced/relationship-attributes/

---

### DB-003: Create Conversation Model
**Category**: Database
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Create the SQLModel Conversation class that represents a chat session. This model links users to their conversation histories and serves as the parent for Message records. Essential for tracking conversation context.

### Dependencies
- DB-001: Database Connection Setup (must be completed first)
- FOUND-003: Dependency Installation (must be completed first)

### Acceptance Criteria
- [ ] Conversation model defined with all required fields (id, user_id, title, created_at, updated_at)
- [ ] Proper SQLModel table configuration with __tablename__
- [ ] Index on user_id for query performance
- [ ] Relationship to Message model configured
- [ ] Model can be imported without errors
- [ ] Alembic can detect the new model

### Implementation Checklist
- [ ] Create file `backend/models/conversation.py`
- [ ] Import SQLModel, Field, Relationship, datetime, Optional, List
- [ ] Define Conversation class inheriting from SQLModel with table=True
- [ ] Add all fields with proper types and constraints
- [ ] Set __tablename__ = "conversations"
- [ ] Add user_id index
- [ ] Define relationship to messages
- [ ] Add Config class with example
- [ ] Export model in `backend/models/__init__.py`

### Files to Create/Modify
```
backend/models/conversation.py    [CREATE]   - Conversation SQLModel class
backend/models/__init__.py        [MODIFY]   - Export Conversation model
```

### Technical Details

Key Classes: Conversation (SQLModel)
External Dependencies: sqlmodel, datetime, typing
Configuration: None required
Database Table Name: conversations

### Testing Instructions
# Step 1: Start Python REPL in project directory
python

# Step 2: Test model import
from backend.models.conversation import Conversation
conv = Conversation(user_id="test_user", title="Test Chat")
print(conv)
# Expected output: Conversation object with fields populated

# Step 3: Verify Alembic detects the model
alembic revision --autogenerate -m "add conversation model"
# Expected: New migration file created with create_table operation
```

### Example Code/Usage
```python
from backend.models.conversation import Conversation
from datetime import datetime

# Create new conversation
conversation = Conversation(
    user_id="user_123",
    title="Shopping List Discussion",
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)

# After saving to DB, will have an id
# conversation.id -> 1
```

### Potential Issues & Solutions
- **Issue**: Import error for SQLModel
  - **Solution**: Ensure `pip install sqlmodel` completed in FOUND-003

- **Issue**: Alembic doesn't detect new model
  - **Solution**: Verify model imported in models/__init__.py and base.py includes all models

- **Issue**: Relationship to Message fails
  - **Solution**: Ensure Message model exists (created in DB-004)

### Related Documentation
- SQLModel Docs: https://sqlmodel.tiangolo.com/
- Alembic Migrations: https://alembic.sqlalchemy.org/

---

### DB-004: Create Message Model
**Category**: Database
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Create the SQLModel Message class that represents individual chat messages in conversations. This model includes role-based classification and tool call storage, essential for AI chatbot functionality.

### Dependencies
- DB-001: Database Connection Setup (must be completed first)
- DB-003: Create Conversation Model (must be completed first)

### Acceptance Criteria
- [ ] Message model defined with all required fields (id, conversation_id, user_id, role, content, tool_calls, created_at)
- [ ] Proper SQLModel table configuration with __tablename__
- [ ] Indexes on conversation_id and user_id for query performance
- [ ] Relationship to Conversation model configured
- [ ] MessageRole enum properly defined
- [ ] Model can be imported without errors
- [ ] Alembic can detect the new model

### Implementation Checklist
- [ ] Create file `backend/models/message.py`
- [ ] Import SQLModel, Field, Relationship, datetime, Optional, Enum
- [ ] Define MessageRole enum with USER, ASSISTANT, SYSTEM, TOOL values
- [ ] Define Message class inheriting from SQLModel with table=True
- [ ] Add all fields with proper types and constraints
- [ ] Set __tablename__ = "messages"
- [ ] Add conversation_id and user_id indexes
- [ ] Define relationship to conversation
- [ ] Add Config class with example
- [ ] Export model in `backend/models/__init__.py`

### Files to Create/Modify
```
backend/models/message.py           [CREATE]   - Message SQLModel class
backend/models/__init__.py          [MODIFY]   - Export Message model
```

### Technical Details

Key Classes: Message (SQLModel), MessageRole (Enum)
External Dependencies: sqlmodel, datetime, typing, enum
Configuration: None required
Database Table Name: messages

### Testing Instructions
# Step 1: Test model import
poetry run python -c "
from backend.models.message import Message, MessageRole
msg = Message(conversation_id=1, user_id='test_user', role=MessageRole.USER, content='Hello')
print('Message model imported successfully')
print(f'Role: {msg.role}')
print(f'Content: {msg.content}')
"

# Step 2: Verify Alembic detects the model
alembic revision --autogenerate -m "add message model"
# Expected: New migration file created with create_table operation

# Step 3: Test enum values
poetry run python -c "
from backend.models.message import MessageRole
print('Available roles:', [role.value for role in MessageRole])
# Expected: ['user', 'assistant', 'system', 'tool']
"
```

### Potential Issues & Solutions
- **Issue**: Circular import between Message and Conversation models
  - **Solution**: Use string references for relationships or adjust import order

- **Issue**: Foreign key constraint fails
  - **Solution**: Ensure conversation_id references existing conversation table

- **Issue**: Enum not working properly
  - **Solution**: Verify proper enum import and definition

### Related Documentation
- SQLModel relationships: https://sqlmodel.tiangolo.com/advanced/relationship-attributes/
- Python enums: https://docs.python.org/3/library/enum.html

---

### DB-005: Create Database Indexes
**Category**: Database
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Create all required database indexes for optimal query performance, including indexes on user_id, conversation_id, and composite indexes for common queries.

### Dependencies
- DB-003: Create Conversation Model (must be completed first)
- DB-004: Create Message Model (must be completed first)

### Acceptance Criteria
- [ ] Index on tasks.user_id created for user-specific queries
- [ ] Index on conversations.user_id created for user conversations
- [ ] Index on messages.conversation_id created for conversation messages
- [ ] Index on messages.user_id created for user message queries
- [ ] Composite index on messages(conversation_id, created_at) created
- [ ] Composite index on conversations(user_id, created_at) created
- [ ] Composite index on tasks(user_id, completed) created
- [ ] All indexes properly defined in models or migration scripts

### Implementation Checklist
- [ ] Verify indexes are defined in SQLModel models using `index=True`
- [ ] Create Alembic migration for any additional indexes not in model definitions
- [ ] Test index creation with migration
- [ ] Verify indexes exist in database after migration
- [ ] Document performance benefits of each index

### Files to Create/Modify
```
alembic/versions/[timestamp]_create_db_indexes.py    [CREATE]   - Index creation migration
backend/models/conversation.py                        [MODIFY]   - Add index definitions if needed
backend/models/message.py                            [MODIFY]   - Add index definitions if needed
```

### Technical Details

Key Functions/Classes: Database index definitions
External Dependencies: alembic, sqlmodel
Configuration: Index definitions in model fields

### Testing Instructions
# Step 1: Create index migration
alembic revision --autogenerate -m "add database indexes"
# Check the generated migration file

# Step 2: Apply the migration
alembic upgrade head

# Step 3: Verify indexes exist (using psql or your DB client)
# In psql: \d+ table_name to see indexes for a table
# Should show indexes on user_id, conversation_id, etc.
```

### Potential Issues & Solutions
- **Issue**: Migration fails due to existing indexes
  - **Solution**: Check if indexes already exist and update migration accordingly

- **Issue**: Performance degradation due to too many indexes
  - **Solution**: Monitor query performance and remove unnecessary indexes

- **Issue**: Index naming conflicts
  - **Solution**: Use explicit names for indexes to avoid conflicts

### Related Documentation
- SQLModel indexes: https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#indexes
- PostgreSQL indexing: https://www.postgresql.org/docs/current/indexes.html

---

### DB-006: Alembic Migration Script
**Category**: Database
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Create Alembic migration script for the new conversation and message tables, ensuring proper schema evolution from Phase II to Phase III.

### Dependencies
- DB-003: Create Conversation Model (must be completed first)
- DB-004: Create Message Model (must be completed first)

### Acceptance Criteria
- [ ] Migration script generated successfully with auto-detection
- [ ] Migration includes proper SQL for creating conversation and message tables
- [ ] Migration includes all necessary indexes
- [ ] Migration can be applied without errors
- [ ] Migration can be rolled back without errors
- [ ] Downgrade migration properly handles table removal

### Implementation Checklist
- [ ] Generate migration script with `alembic revision --autogenerate`
- [ ] Review and verify the generated migration script
- [ ] Test the migration upgrade process
- [ ] Test the migration downgrade process
- [ ] Update migration if needed to match requirements

### Files to Create/Modify
```
alembic/versions/[timestamp]_create_conversation_message_tables.py    [CREATE]   - Migration script
alembic.ini                                                           [MODIFY]   - Alembic configuration if needed
```

### Technical Details

Key Functions/Classes: Alembic revision and upgrade functions
External Dependencies: alembic, sqlmodel
Configuration: DATABASE_URL environment variable

### Testing Instructions
# Step 1: Generate migration script
alembic revision --autogenerate -m "Create conversation and message tables"

# Step 2: Review migration script
cat alembic/versions/[timestamp]_create_conversation_message_tables.py
# Should contain create_table operations for conversation and message tables

# Step 3: Apply migration
alembic upgrade head

# Step 4: Verify tables created
poetry run python -c "
from backend.database import Session
from backend.models.conversation import Conversation
from backend.models.message import Message
from sqlmodel import select

with Session() as session:
    # Check if tables exist by trying to query them
    conv_count = session.exec(select(Conversation)).all()
    msg_count = session.exec(select(Message)).all()
    print(f'Tables exist: Conversations={len(conv_count)}, Messages={len(msg_count)}')
"
```

### Potential Issues & Solutions
- **Issue**: Auto-generation creates incorrect migration
  - **Solution**: Manually review and modify the generated migration script

- **Issue**: Migration fails due to existing tables
  - **Solution**: Check if tables already exist and adjust migration accordingly

- **Issue**: Foreign key constraint violations during migration
  - **Solution**: Order table creation properly (parent tables before child tables)

### Related Documentation
- Alembic autogenerate: https://alembic.sqlalchemy.org/en/latest/autogenerate.html
- Alembic migrations: https://alembic.sqlalchemy.org/en/latest/tutorial.html

---

### DB-007: Deploy Schema to Neon
**Category**: Database
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Deploy the updated database schema with conversation and message tables to Neon PostgreSQL database, ensuring all indexes and constraints are properly applied.

### Dependencies
- DB-006: Alembic Migration Script (must be completed first)
- Proper DATABASE_URL configured in environment

### Acceptance Criteria
- [ ] Migration script applied successfully to Neon database
- [ ] Conversation table created with all required fields and indexes
- [ ] Message table created with all required fields and indexes
- [ ] Foreign key constraints properly set up
- [ ] All indexes created and functioning
- [ ] Database connectivity maintained after migration

### Implementation Checklist
- [ ] Set proper DATABASE_URL environment variable for Neon
- [ ] Run `alembic upgrade head` to apply migration to Neon
- [ ] Verify tables exist in Neon database
- [ ] Test basic CRUD operations on new tables
- [ ] Verify foreign key constraints work properly

### Files to Create/Modify
```
backend/.env    [MODIFY]   - Update with Neon DATABASE_URL
```

### Technical Details

Key Functions/Classes: Alembic upgrade process
External Dependencies: alembic, psycopg2-binary (for PostgreSQL)
Configuration: DATABASE_URL pointing to Neon

### Testing Instructions
# Step 1: Ensure environment is set for Neon
export DATABASE_URL="your_neon_connection_string"

# Step 2: Apply migration to Neon
alembic upgrade head

# Step 3: Verify tables exist in Neon
# Connect to Neon DB and run:
# SELECT * FROM information_schema.tables WHERE table_name IN ('conversations', 'messages');
# Should return the new tables

# Step 4: Test basic operations
poetry run python -c "
from backend.database import Session
from backend.models.conversation import Conversation
from sqlmodel import select
import os

# Connect to Neon DB
with Session() as session:
    # Create a test conversation
    conv = Conversation(user_id='test_user', title='Test from Neon')
    session.add(conv)
    session.commit()

    # Retrieve it back
    retrieved = session.exec(select(Conversation).where(Conversation.user_id == 'test_user')).first()
    print(f'Neon DB connection working: {retrieved.title}')
"
```

### Potential Issues & Solutions
- **Issue**: Connection timeout to Neon database
  - **Solution**: Check connection string, ensure Neon project is active, and verify network access

- **Issue**: Migration fails on Neon due to different SQL dialect
  - **Solution**: Update Alembic migration with Neon-compatible SQL

- **Issue**: Insufficient database privileges
  - **Solution**: Verify database user has DDL privileges for schema changes

### Related Documentation
- Neon PostgreSQL: https://neon.tech/docs
- Database connection strings: https://www.postgresql.org/docs/current/libpq-connect.html

---

### DB-008: Seed Test Data
**Category**: Database
**Priority**: Medium
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Seed the database with initial test data for conversations and messages to facilitate development and testing of the AI chatbot functionality.

### Dependencies
- DB-007: Deploy Schema to Neon (must be completed first)

### Acceptance Criteria
- [ ] Test conversations created for development
- [ ] Test messages created associated with conversations
- [ ] Test data includes various message roles (user, assistant, tool)
- [ ] Test data includes sample tool_calls JSON
- [ ] Seeding script is idempotent (safe to run multiple times)
- [ ] Test data properly cleaned up after testing if needed

### Implementation Checklist
- [ ] Create `backend/seed.py` script for seeding data
- [ ] Add sample conversations with different users
- [ ] Add sample messages with different roles
- [ ] Include messages with sample tool_calls
- [ ] Make script idempotent by checking for existing data
- [ ] Document the seeding process

### Files to Create/Modify
```
backend/seed.py                   [CREATE]   - Test data seeding script
backend/__main__.py               [MODIFY]   - Allow running seed as module (optional)
```

### Technical Details

Key Functions/Classes:
- seed_database(): Main seeding function
- create_sample_conversations(): Create sample conversation data
- create_sample_messages(): Create sample message data
External Dependencies: backend.database, backend.models
Configuration: None required

### Testing Instructions
# Step 1: Run seeding script
poetry run python -m backend.seed

# Step 2: Verify data created
poetry run python -c "
from backend.database import Session
from backend.models.conversation import Conversation
from backend.models.message import Message
from sqlmodel import select

with Session() as session:
    conv_count = session.exec(select(Conversation)).count()
    msg_count = session.exec(select(Message)).count()
    print(f'Test data created: Conversations={conv_count}, Messages={msg_count}')

    # Check if we have messages with different roles
    user_msgs = session.exec(select(Message).where(Message.role == 'user')).count()
    assistant_msgs = session.exec(select(Message).where(Message.role == 'assistant')).count()
    print(f'Role distribution: User={user_msgs}, Assistant={assistant_msgs}')
"
```

### Potential Issues & Solutions
- **Issue**: Seeding fails due to duplicate key constraints
  - **Solution**: Make seeding script idempotent by checking for existing data first

- **Issue**: Foreign key constraint violations
  - **Solution**: Create parent records (conversations) before child records (messages)

- **Issue**: Large amounts of test data affecting performance
  - **Solution**: Use minimal test data for development, larger sets for performance testing

### Related Documentation
- Database seeding best practices: https://www.citusdata.com/blog/2017/10/03/real-time-apps-with-citus/#data-seeding
- SQLModel bulk operations: https://sqlmodel.tiangolo.com/tutorial/bulk-operations/

---

### DB-009: Database Health Check Endpoint
**Category**: Database
**Priority**: High
**Complexity**: Small
**Estimated Time**: 0.5 hours

### Description
Add a health check endpoint that verifies database connectivity and basic functionality, essential for monitoring and deployment.

### Dependencies
- DB-001: Database Connection Setup (must be completed first)

### Acceptance Criteria
- [ ] Health check endpoint available at /health/db
- [ ] Endpoint returns 200 status when database is accessible
- [ ] Endpoint returns proper error when database is not accessible
- [ ] Response includes timestamp and status information
- [ ] Endpoint is protected and doesn't expose sensitive information

### Implementation Checklist
- [ ] Add health check route to `backend/main.py`
- [ ] Implement database connectivity check
- [ ] Return appropriate status codes and messages
- [ ] Add response model for health check
- [ ] Test the endpoint functionality

### Files to Create/Modify
```
backend/main.py                   [MODIFY]   - Add health check endpoint
backend/api/health.py             [CREATE]   - Health check API endpoints (optional separation)
```

### Technical Details

Key Functions/Classes:
- health_db(): Database health check endpoint
External Dependencies: fastapi, backend.database
Configuration: None required

### Testing Instructions
# Step 1: Start the server
uvicorn backend.main:app --reload

# Step 2: Test health check endpoint
curl -v http://localhost:8000/health/db
# Expected: HTTP 200 with JSON response like {"status": "ok", "timestamp": "...", "database": "connected"}

# Step 3: Test with Python
poetry run python -c "
import requests
response = requests.get('http://localhost:8000/health/db')
print(f'Status: {response.status_code}')
print(f'Response: {response.json()}')
"
```

### Potential Issues & Solutions
- **Issue**: Health check takes too long and causes timeouts
  - **Solution**: Implement minimal and fast database operation for health checks

- **Issue**: Health check exposes sensitive information
  - **Solution**: Only return necessary health status information

### Related Documentation
- Health check best practices: https://cloud.google.com/service-control/troubleshooting/health-checks
- FastAPI health checks: https://fastapi.tiangolo.com/advanced/health-check/

---

## MCP Server Tasks (MCP-XXX)

### MCP-001: MCP Project Structure
**Category**: MCP
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Create the proper directory structure and initialization files for the MCP (Model Context Protocol) server components, organizing the code following best practices.

### Dependencies
- FOUND-001: Project Structure Setup (must be completed first)

### Acceptance Criteria
- [ ] Proper MCP directory structure created with subdirectories
- [ ] __init__.py files created for proper Python package structure
- [ ] Configuration files created for MCP server
- [ ] Initial server file created with basic initialization
- [ ] Tools directory created for MCP tool implementations

### Implementation Checklist
- [ ] Create `backend/mcp/` directory
- [ ] Create `backend/mcp/__init__.py` for package structure
- [ ] Create `backend/mcp/server.py` for main server initialization
- [ ] Create `backend/mcp/config.py` for server configuration
- [ ] Create `backend/mcp/tools/` directory for tool implementations
- [ ] Create `backend/mcp/tools/__init__.py` for tools package

### Files to Create/Modify
```
backend/mcp/__init__.py             [CREATE]   - MCP package initialization
backend/mcp/server.py               [CREATE]   - MCP server instance
backend/mcp/config.py               [CREATE]   - MCP server configuration
backend/mcp/tools/__init__.py       [CREATE]   - Tools package initialization
backend/mcp/session.py              [CREATE]   - Database session management for MCP
```

### Technical Details

Key Functions/Classes:
- Server: MCP server class
- Config: MCP server configuration
External Dependencies: mcp (Model Context Protocol SDK)
Configuration: Server name, metadata, and settings

### Testing Instructions
# Step 1: Verify directory structure
ls -la backend/mcp/
# Should show: __init__.py, server.py, config.py, session.py, tools/

# Step 2: Test basic import
poetry run python -c "
from backend.mcp.server import mcp_server
print('MCP server structure created successfully')
"
```

### Potential Issues & Solutions
- **Issue**: Import errors due to missing package structure
  - **Solution**: Ensure all __init__.py files are created properly

- **Issue**: MCP SDK not installed properly
  - **Solution**: Verify MCP SDK installation from dependency step

### Related Documentation
- Model Context Protocol: https://modelcontextprotocol.io/
- Python packages: https://docs.python.org/3/tutorial/modules.html#packages

---

### MCP-002: MCP Server Initialization
**Category**: MCP
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Initialize the MCP server with proper project metadata, logging, and error handling, ensuring it's ready to register and serve tools.

### Dependencies
- MCP-001: MCP Project Structure (must be completed first)
- FOUND-003: Dependency Installation (must be completed first)

### Acceptance Criteria
- [ ] MCP server instance created with proper name and metadata
- [ ] Logging configured for MCP server operations
- [ ] Error handling initialized for server operations
- [ ] Server can be started without errors
- [ ] Proper shutdown handling implemented

### Implementation Checklist
- [ ] Create `backend/mcp/server.py` with server initialization
- [ ] Initialize Server instance with "todo-mcp-server" name
- [ ] Configure proper logging for the server
- [ ] Add error handling configuration
- [ ] Implement server start and shutdown functions

### Files to Create/Modify
```
backend/mcp/server.py               [MODIFY]   - Complete MCP server initialization
backend/mcp/config.py               [MODIFY]   - Update with server configuration
```

### Technical Details

Key Functions/Classes:
- mcp_server: Global MCP server instance
- start_server(): Function to start the MCP server
External Dependencies: mcp, logging
Configuration: Server metadata, logging level

### Testing Instructions
# Step 1: Test server initialization
poetry run python -c "
from backend.mcp.server import mcp_server
print('MCP server initialized:', mcp_server.name)
"

# Step 2: Verify imports work
poetry run python -c "
from mcp.server import Server
from mcp.types import Tool
print('MCP imports successful')
"
```

### Potential Issues & Solutions
- **Issue**: MCP SDK import errors
  - **Solution**: Ensure mcp package installed correctly in dependency step

- **Issue**: Server initialization fails
  - **Solution**: Check MCP SDK documentation for proper initialization pattern

### Related Documentation
- MCP Server API: https://modelcontextprotocol.com/
- MCP Python SDK: Refer to official MCP SDK documentation

---

### MCP-003: Database Session Management
**Category**: MCP
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Implement database session management for MCP tool handlers, ensuring proper dependency injection, lifecycle management, and error handling for database transactions.

### Dependencies
- MCP-002: MCP Server Initialization (must be completed first)
- DB-001: Database Connection Setup (must be completed first)

### Acceptance Criteria
- [ ] Database session dependency injection implemented for MCP tools
- [ ] Session lifecycle properly managed (creation, cleanup)
- [ ] Error handling and rollback logic implemented
- [ ] Session cleanup occurs automatically
- [ ] Transaction boundaries properly defined

### Implementation Checklist
- [ ] Create `backend/mcp/session.py` with session management
- [ ] Implement get_db_session dependency function
- [ ] Add proper error handling and rollback logic
- [ ] Implement session cleanup with context managers
- [ ] Test session creation and cleanup

### Files to Create/Modify
```
backend/mcp/session.py              [CREATE]   - Database session management for MCP
backend/mcp/utils.py                [CREATE]   - Helper functions for MCP operations
```

### Technical Details

Key Functions/Classes:
- get_db_session(): Session dependency for tools
- handle_db_transaction(): Transaction management wrapper
External Dependencies: backend.database, sqlmodel
Configuration: None required

### Testing Instructions
# Step 1: Test session management
poetry run python -c "
from backend.mcp.session import get_db_session
from backend.database import Session

# Test session creation
with get_db_session() as session:
    assert isinstance(session, Session)
    print('Session management working correctly')
"
```

### Potential Issues & Solutions
- **Issue**: Session not closed properly causing connection leaks
  - **Solution**: Use context managers to ensure session cleanup

- **Issue**: Transaction rollback not working properly
  - **Solution**: Implement proper exception handling with rollback

### Related Documentation
- SQLModel sessions: https://sqlmodel.tiangolo.com/tutorial/sessions/
- FastAPI dependency injection: https://fastapi.tiangolo.com/tutorial/dependencies/

---

### MCP-004: Tool Schema Definitions
**Category**: MCP
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Define the schema and parameters for all MCP tools that will be used by the AI to interact with the todo application, including proper validation and documentation.

### Dependencies
- MCP-003: Database Session Management (must be completed first)

### Acceptance Criteria
- [ ] Tool schema defined for add_task with proper parameters
- [ ] Tool schema defined for list_tasks with proper parameters
- [ ] Tool schema defined for complete_task with proper parameters
- [ ] Tool schema defined for delete_task with proper parameters
- [ ] Tool schema defined for update_task with proper parameters
- [ ] All schemas include proper descriptions and validation

### Implementation Checklist
- [ ] Define tool schema for add_task function
- [ ] Define tool schema for list_tasks function
- [ ] Define tool schema for complete_task function
- [ ] Define tool schema for delete_task function
- [ ] Define tool schema for update_task function
- [ ] Add proper parameter validation to each schema

### Files to Create/Modify
```
backend/mcp/tools/schemas.py        [CREATE]   - Tool schema definitions
backend/mcp/tools/__init__.py       [MODIFY]   - Export schemas
```

### Technical Details

Key Functions/Classes:
- add_task_schema: Schema for adding tasks
- list_tasks_schema: Schema for listing tasks
- complete_task_schema: Schema for completing tasks
- delete_task_schema: Schema for deleting tasks
- update_task_schema: Schema for updating tasks
External Dependencies: mcp, pydantic
Configuration: Tool parameter definitions

### Testing Instructions
# Step 1: Test schema imports
poetry run python -c "
from backend.mcp.tools.schemas import *
print('All tool schemas imported successfully')
"

# Step 2: Verify schema structure (example for add_task)
# Schemas should be compatible with MCP format requirements
```

### Potential Issues & Solutions
- **Issue**: Schema format not compatible with MCP requirements
  - **Solution**: Follow MCP documentation for proper schema structure

- **Issue**: Parameter validation not working as expected
  - **Solution**: Use proper Pydantic models for validation

### Related Documentation
- MCP Tool Schema: https://modelcontextprotocol.io/
- Pydantic validation: https://docs.pydantic.dev/

---

### MCP-005: Implement add_task Tool
**Category**: MCP
**Priority**: Critical
**Complexity**: Medium
**Estimated Time**: 2 hours

### Description
Create the add_task MCP tool that allows the AI to create new tasks for users, with proper validation, error handling, and database persistence.

### Dependencies
- MCP-004: Tool Schema Definitions (must be completed first)
- MCP-003: Database Session Management (must be completed first)

### Acceptance Criteria
- [ ] Tool schema properly defined for add_task
- [ ] Handler function works with sample data
- [ ] Input validation implemented for all parameters
- [ ] Error cases handled gracefully (empty title, missing user_id, etc.)
- [ ] Task successfully created in database
- [ ] Proper response format returned to AI

### Implementation Checklist
- [ ] Create `backend/mcp/tools/add_task.py` with implementation
- [ ] Implement handler function with all validation
- [ ] Add proper error handling for edge cases
- [ ] Return proper response format to MCP client
- [ ] Test with sample data and edge cases

### Files to Create/Modify
```
backend/mcp/tools/add_task.py       [CREATE]   - add_task tool implementation
backend/mcp/tools/__init__.py       [MODIFY]   - Export add_task tool
```

### Technical Details

Key Functions/Classes:
- handle_add_task(): Function to handle add_task requests
External Dependencies: sqlmodel, backend.models.task, backend.mcp.session
Configuration: Tool parameters for title and description

### Testing Instructions
# Step 1: Test add_task tool
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

### Potential Issues & Solutions
- **Issue**: Database transaction fails
  - **Solution**: Implement proper error handling and rollback

- **Issue**: Validation not catching all error cases
  - **Solution**: Add comprehensive validation for all parameters

### Related Documentation
- SQLModel operations: https://sqlmodel.tiangolo.com/tutorial/
- MCP Tool Development: https://modelcontextprotocol.com/

---

### MCP-006: Implement list_tasks Tool
**Category**: MCP
**Priority**: Critical
**Complexity**: Medium
**Estimated Time**: 2 hours

### Description
Create the list_tasks MCP tool that allows the AI to retrieve tasks for a user with filtering capabilities (all/pending/completed), with proper validation and error handling.

### Dependencies
- MCP-004: Tool Schema Definitions (must be completed first)
- MCP-003: Database Session Management (must be completed first)

### Acceptance Criteria
- [ ] Tool schema properly defined with filtering parameters
- [ ] Filtering logic works for all statuses (all/pending/completed)
- [ ] Pagination support implemented if needed
- [ ] All filter options tested successfully
- [ ] Proper response format with tasks array returned
- [ ] Error cases handled gracefully

### Implementation Checklist
- [ ] Create `backend/mcp/tools/list_tasks.py` with implementation
- [ ] Implement filtering logic for different status options
- [ ] Add validation for status parameter
- [ ] Return properly formatted response with metadata
- [ ] Test all filter options and edge cases

### Files to Create/Modify
```
backend/mcp/tools/list_tasks.py     [CREATE]   - list_tasks tool implementation
backend/mcp/tools/__init__.py       [MODIFY]   - Export list_tasks tool
```

### Technical Details

Key Functions/Classes:
- handle_list_tasks(): Function to handle list_tasks requests
External Dependencies: sqlmodel, backend.models.task, backend.mcp.session
Configuration: Filter parameters for status

### Testing Instructions
# Step 1: Test list_tasks tool
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

### Potential Issues & Solutions
- **Issue**: Query performance with large datasets
  - **Solution**: Implement proper indexing and consider pagination

- **Issue**: Invalid status values not handled properly
  - **Solution**: Add comprehensive validation for status parameter

### Related Documentation
- SQLModel queries: https://sqlmodel.tiangolo.com/tutorial/select/
- Filtering patterns: Follow established patterns from the application

---

### MCP-007: Implement complete_task Tool
**Category**: MCP
**Priority**: Critical
**Complexity**: Medium
**Estimated Time**: 1.5 hours

### Description
Create the complete_task MCP tool that allows the AI to mark tasks as completed, with proper validation, ownership verification, and error handling.

### Dependencies
- MCP-004: Tool Schema Definitions (must be completed first)
- MCP-003: Database Session Management (must be completed first)

### Acceptance Criteria
- [ ] Tool schema properly defined with required parameters
- [ ] Completion logic works correctly
- [ ] Ownership verification implemented
- [ ] Already-completed task case handled appropriately
- [ ] Edge cases handled properly
- [ ] Error cases handled gracefully

### Implementation Checklist
- [ ] Create `backend/mcp/tools/complete_task.py` with implementation
- [ ] Implement completion logic with ownership verification
- [ ] Add validation for task existence and user ownership
- [ ] Handle already-completed task case
- [ ] Return proper response format
- [ ] Test edge cases and error scenarios

### Files to Create/Modify
```
backend/mcp/tools/complete_task.py  [CREATE]   - complete_task tool implementation
backend/mcp/tools/__init__.py       [MODIFY]   - Export complete_task tool
```

### Technical Details

Key Functions/Classes:
- handle_complete_task(): Function to handle complete_task requests
External Dependencies: sqlmodel, backend.models.task, backend.mcp.session
Configuration: Task ID and user ID parameters

### Testing Instructions
# Step 1: Test complete_task tool
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

### Potential Issues & Solutions
- **Issue**: Attempting to complete non-existent task
  - **Solution**: Add proper validation for task existence

- **Issue**: User attempting to complete another user's task
  - **Solution**: Implement user ownership verification

### Related Documentation
- Task completion patterns: Follow existing application patterns
- Authorization: Implement proper user ownership checks

---

### MCP-008: Implement delete_task Tool
**Category**: MCP
**Priority**: Critical
**Complexity**: Medium
**Estimated Time**: 1.5 hours

### Description
Create the delete_task MCP tool that allows the AI to remove tasks from the database, with proper validation, ownership verification, and error handling.

### Dependencies
- MCP-004: Tool Schema Definitions (must be completed first)
- MCP-003: Database Session Management (must be completed first)

### Acceptance Criteria
- [ ] Tool schema properly defined with required parameters
- [ ] Deletion logic works correctly
- [ ] Ownership verification implemented
- [ ] Various deletion scenarios tested successfully
- [ ] Error cases handled gracefully
- [ ] Proper response format returned

### Implementation Checklist
- [ ] Create `backend/mcp/tools/delete_task.py` with implementation
- [ ] Implement deletion logic with ownership verification
- [ ] Add validation for task existence and user ownership
- [ ] Handle edge cases (task not found, unauthorized access)
- [ ] Return proper response format
- [ ] Test various deletion scenarios

### Files to Create/Modify
```
backend/mcp/tools/delete_task.py    [CREATE]   - delete_task tool implementation
backend/mcp/tools/__init__.py       [MODIFY]   - Export delete_task tool
```

### Technical Details

Key Functions/Classes:
- handle_delete_task(): Function to handle delete_task requests
External Dependencies: sqlmodel, backend.models.task, backend.mcp.session
Configuration: Task ID and user ID parameters

### Testing Instructions
# Step 1: Test delete_task tool
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

### Potential Issues & Solutions
- **Issue**: Attempting to delete non-existent task
  - **Solution**: Add proper validation for task existence

- **Issue**: User attempting to delete another user's task
  - **Solution**: Implement user ownership verification

### Related Documentation
- Task deletion patterns: Follow existing application patterns
- Soft vs hard delete: Consider implementation based on requirements

---

### MCP-009: Implement update_task Tool
**Category**: MCP
**Priority**: Critical
**Complexity**: Medium
**Estimated Time**: 2 hours

### Description
Create the update_task MCP tool that allows the AI to modify task title and description with partial update capability, proper validation, and error handling.

### Dependencies
- MCP-004: Tool Schema Definitions (must be completed first)
- MCP-003: Database Session Management (must be completed first)

### Acceptance Criteria
- [ ] Tool schema properly defined with optional update parameters
- [ ] Update logic works for title and description
- [ ] Validation for empty updates implemented
- [ ] Partial updates handled properly (update only provided fields)
- [ ] Error cases handled gracefully
- [ ] Ownership verification implemented

### Implementation Checklist
- [ ] Create `backend/mcp/tools/update_task.py` with implementation
- [ ] Implement update logic for title and description
- [ ] Add validation for empty updates and partial updates
- [ ] Implement ownership verification
- [ ] Handle edge cases (empty title, no updates provided)
- [ ] Return proper response format
- [ ] Test various update combinations

### Files to Create/Modify
```
backend/mcp/tools/update_task.py    [CREATE]   - update_task tool implementation
backend/mcp/tools/__init__.py       [MODIFY]   - Export update_task tool
```

### Technical Details

Key Functions/Classes:
- handle_update_task(): Function to handle update_task requests
External Dependencies: sqlmodel, backend.models.task, backend.mcp.session
Configuration: Task ID, user ID, and optional title/description parameters

### Testing Instructions
# Step 1: Test update_task tool
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

### Potential Issues & Solutions
- **Issue**: Attempting to update with empty title
  - **Solution**: Add validation to prevent empty titles

- **Issue**: Partial update not working correctly
  - **Solution**: Only update provided fields, leave others unchanged

### Related Documentation
- Partial update patterns: Follow established patterns from the application
- Validation: Implement proper validation for all input parameters

---

### MCP-010: Tool Registration System
**Category**: MCP
**Priority**: Critical
**Complexity**: Medium
**Estimated Time**: 1.5 hours

### Description
Register all 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) with the MCP server instance, making them available for the AI to use.

### Dependencies
- MCP-005: Implement add_task Tool (must be completed first)
- MCP-006: Implement list_tasks Tool (must be completed first)
- MCP-007: Implement complete_task Tool (must be completed first)
- MCP-008: Implement delete_task Tool (must be completed first)
- MCP-009: Implement update_task Tool (must be completed first)

### Acceptance Criteria
- [ ] All 5 tools registered with MCP server
- [ ] Each tool accessible through MCP interface
- [ ] Tools properly configured with schemas
- [ ] Registration process works without errors
- [ ] Tools can be invoked by the AI

### Implementation Checklist
- [ ] Create `backend/mcp/registration.py` with registration logic
- [ ] Register add_task tool with MCP server
- [ ] Register list_tasks tool with MCP server
- [ ] Register complete_task tool with MCP server
- [ ] Register delete_task tool with MCP server
- [ ] Register update_task tool with MCP server
- [ ] Update server initialization to include all tools

### Files to Create/Modify
```
backend/mcp/registration.py         [CREATE]   - Tool registration logic
backend/mcp/server.py               [MODIFY]   - Update with registered tools
```

### Technical Details

Key Functions/Classes:
- register_all_tools(): Function to register all tools
External Dependencies: mcp, backend.mcp.tools
Configuration: All 5 task management tools

### Testing Instructions
# Step 1: Test all tools registered and working
poetry run python -c "
from backend.mcp.server import mcp_server

# Check if tools are registered
tool_names = [tool.name for tool in mcp_server._tools]
expected_tools = ['add_task', 'list_tasks', 'complete_task', 'delete_task', 'update_task']
assert all(tool in tool_names for tool in expected_tools)
print('All tools registered:', tool_names)
"
```

### Potential Issues & Solutions
- **Issue**: Tool registration fails
  - **Solution**: Check that all tools are properly implemented and exported

- **Issue**: Duplicate tool names
  - **Solution**: Ensure each tool has a unique name in the registration

### Related Documentation
- MCP Tool Registration: https://modelcontextprotocol.com/
- Server configuration: Follow MCP SDK documentation

---

### MCP-011: Tool Error Handling
**Category**: MCP
**Priority**: High
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Implement comprehensive error handling for all MCP tools, ensuring consistent error responses and proper logging for debugging.

### Dependencies
- MCP-010: Tool Registration System (must be completed first)

### Acceptance Criteria
- [ ] Consistent error response format across all tools
- [ ] Proper logging of errors for debugging
- [ ] Validation errors handled gracefully
- [ ] Database errors handled gracefully
- [ ] Unauthorized access properly rejected
- [ ] Error messages are helpful but don't expose system details

### Implementation Checklist
- [ ] Create error handling utilities in `backend/mcp/errors.py`
- [ ] Update all tool handlers with proper error handling
- [ ] Add logging for error cases
- [ ] Implement validation error handling
- [ ] Test error scenarios for each tool

### Files to Create/Modify
```
backend/mcp/errors.py               [CREATE]   - Error handling utilities
backend/mcp/tools/add_task.py       [MODIFY]   - Add error handling
backend/mcp/tools/list_tasks.py     [MODIFY]   - Add error handling
backend/mcp/tools/complete_task.py  [MODIFY]   - Add error handling
backend/mcp/tools/delete_task.py    [MODIFY]   - Add error handling
backend/mcp/tools/update_task.py    [MODIFY]   - Add error handling
```

### Technical Details

Key Functions/Classes:
- MCPError: Base error class
- handle_tool_error(): Error handling wrapper
External Dependencies: logging
Configuration: Error response format

### Testing Instructions
# Step 1: Test error handling for missing user_id
poetry run python -c "
from backend.mcp.tools.add_task import handle_add_task
from backend.database import Session

try:
    with Session() as session:
        result = handle_add_task(session, '', 'Test task', 'Test description')
except Exception as e:
    print(f'Error handled properly: {type(e).__name__}')
"
```

### Potential Issues & Solutions
- **Issue**: Error messages exposing system details
  - **Solution**: Sanitize error messages before sending to client

- **Issue**: Unhandled exceptions crashing the server
  - **Solution**: Wrap all tool handlers with try-catch blocks

### Related Documentation
- Error handling best practices: https://docs.python.org/3/tutorial/errors.html
- Security considerations: Don't expose internal system details

---

### MCP-012: Tool Unit Tests
**Category**: MCP
**Priority**: High
**Complexity**: Medium
**Estimated Time**: 2 hours

### Description
Create comprehensive unit tests for all MCP tools to ensure they function correctly with various inputs, edge cases, and error scenarios.

### Dependencies
- MCP-010: Tool Registration System (must be completed first)

### Acceptance Criteria
- [ ] Unit tests for add_task tool covering all scenarios
- [ ] Unit tests for list_tasks tool covering all filter options
- [ ] Unit tests for complete_task tool covering all edge cases
- [ ] Unit tests for delete_task tool covering all scenarios
- [ ] Unit tests for update_task tool covering partial updates
- [ ] All tests pass successfully
- [ ] Test coverage is adequate

### Implementation Checklist
- [ ] Create `tests/test_mcp_tools.py` with comprehensive tests
- [ ] Write tests for add_task tool functionality
- [ ] Write tests for list_tasks tool filtering
- [ ] Write tests for complete_task tool validation
- [ ] Write tests for delete_task tool validation
- [ ] Write tests for update_task tool partial updates
- [ ] Write tests for error scenarios
- [ ] Run all tests and verify they pass

### Files to Create/Modify
```
tests/test_mcp_tools.py             [CREATE]   - Comprehensive tool test suite
tests/conftest.py                   [MODIFY]   - Test fixtures if needed
```

### Technical Details

Key Functions/Classes:
- TestAddTask: Test cases for add_task
- TestListTasks: Test cases for list_tasks
- TestCompleteTask: Test cases for complete_task
- TestDeleteTask: Test cases for delete_task
- TestUpdateTask: Test cases for update_task
External Dependencies: pytest, pytest-asyncio, backend.mcp.tools
Configuration: Test database setup

### Testing Instructions
# Step 1: Run MCP tool tests
pytest tests/test_mcp_tools.py -v
# Expected: All tests pass

# Step 2: Check test coverage
pytest --cov=backend.mcp.tools tests/test_mcp_tools.py
# Expected: Good coverage percentage
```

### Potential Issues & Solutions
- **Issue**: Tests require database setup
  - **Solution**: Use test database fixtures or in-memory database

- **Issue**: Tests affecting each other
  - **Solution**: Use proper test isolation with transactions or fresh data per test

### Related Documentation
- Pytest: https://docs.pytest.org/
- Test best practices: https://docs.python-guide.org/writing/tests/

---

## Backend API Tasks (BE-XXX)

### BE-001: OpenRouter Client Setup
**Category**: Backend
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1.5 hours

### Description
Configure OpenAI client with OpenRouter base URL and API key, implementing retry logic and proper error handling for LLM integration.

### Dependencies
- FOUND-003: Dependency Installation (must be completed first)
- FOUND-004: Environment Variables Template (must be completed first)

### Acceptance Criteria
- [ ] OpenAI SDK configured with OpenRouter base URL
- [ ] API key properly loaded from environment
- [ ] Basic connection test successful
- [ ] Retry logic implemented for failed requests
- [ ] Error handling configured for API failures

### Implementation Checklist
- [ ] Create `backend/ai_client.py` with OpenRouter client setup
- [ ] Configure OpenAI client with OpenRouter base URL
- [ ] Load API key from environment variables
- [ ] Implement retry logic for API calls
- [ ] Add proper error handling for API failures
- [ ] Create configuration module for OpenRouter settings

### Files to Create/Modify
```
backend/ai_client.py                [CREATE]   - OpenAI client setup with OpenRouter
backend/config.py                   [CREATE]   - OpenRouter configuration
```

### Technical Details

Key Functions/Classes:
- client: OpenRouter client instance
- create_client(): Client initialization function
External Dependencies: openai, python-dotenv
Configuration: OPENROUTER_API_KEY, OPENROUTER_BASE_URL

### Testing Instructions
# Step 1: Test OpenRouter connection
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

### Potential Issues & Solutions
- **Issue**: API key not found in environment
  - **Solution**: Verify environment variables are set correctly

- **Issue**: Connection timeout to OpenRouter
  - **Solution**: Implement retry logic and proper timeout handling

### Related Documentation
- OpenAI Python SDK: https://platform.openai.com/docs/libraries/python
- OpenRouter API: https://openrouter.ai/docs

---

### BE-002: System Prompt Configuration
**Category**: Backend
**Priority**: Critical
**Complexity**: Small
**Estimated Time**: 1 hour

### Description
Create and configure the system prompt for the task management assistant, focusing on conciseness, tool usage, and voice output optimization.

### Dependencies
- BE-001: OpenRouter Client Setup (must be completed first)

### Acceptance Criteria
- [ ] System prompt created with task management focus
- [ ] Tool usage instructions included and clear
- [ ] Example interactions provided for AI guidance
- [ ] Optimized for voice output (concise responses)
- [ ] Properly integrated with AI client

### Implementation Checklist
- [ ] Create `backend/prompts.py` with system prompt definition
- [ ] Define comprehensive system prompt for task management
- [ ] Include tool usage instructions and guidelines
- [ ] Add example interactions for better AI behavior
- [ ] Optimize for voice output with concise responses
- [ ] Add to configuration for easy updates

### Files to Create/Modify
```
backend/prompts.py                  [CREATE]   - System prompt definition
backend/config.py                   [MODIFY]   - Add system prompt to configuration
```

### Technical Details

Key Functions/Classes:
- SYSTEM_PROMPT: Main system prompt constant
External Dependencies: None
Configuration: System prompt text

### Testing Instructions
# Step 1: Test system prompt
poetry run python -c "
from backend.prompts import SYSTEM_PROMPT
print('System prompt length:', len(SYSTEM_PROMPT))
assert 'task management' in SYSTEM_PROMPT.lower()
assert 'tools' in SYSTEM_PROMPT.lower()
print('System prompt properly defined')
"
```

### Potential Issues & Solutions
- **Issue**: Prompt too long affecting token usage
  - **Solution**: Optimize prompt for brevity while maintaining clarity

- **Issue**: AI not following prompt instructions
  - **Solution**: Iterate on prompt to improve AI compliance

### Related Documentation
- Prompt engineering: Best practices for LLM prompting
- Voice output optimization: Guidelines for concise responses

---
