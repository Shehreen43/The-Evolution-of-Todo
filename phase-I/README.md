# Phase I - In-Memory Todo Console App

A simple command-line todo application with in-memory storage built with Python 3.11+.

## Features

- **Add tasks** with title and optional description
- **View all tasks** in a formatted table
- **Get task details** by ID
- **Mark tasks complete/incomplete** (toggle)
- **Delete tasks** by ID
- **Update task** title and description

## Installation

```bash
# Navigate to phase-I directory
cd phase-I

# Install in development mode
pip install -e .
```

## Usage

### Basic Commands

```bash
# Add a task
todo add "Buy groceries" --description "Milk, eggs, bread"

# List all tasks
todo list

# Get task details
todo get 1

# Mark task as complete (toggle)
todo complete 1

# Update task
todo update 1 --title "New title" --description "New description"

# Delete task
todo delete 1

# Show help
todo --help

# Show version
todo --version
```

### Quick Verification

Run the manual test script to verify all features:

```bash
python test_manual.py
```

Expected output shows all 5 user stories working correctly with validation.

## Architecture

The application follows a layered architecture:

```
src/
├── models/
│   └── task.py           # Task dataclass with validation
├── repository/
│   └── task_repository.py # In-memory storage (list-based)
├── service/
│   └── task_service.py    # Business logic layer
└── cli/
    └── main.py            # CLI interface (argparse)
```

## Data Model

**Task Entity:**
- `id`: Integer (auto-generated, unique)
- `title`: String (1-200 characters, required)
- `description`: String (0-1000 characters, optional)
- `completed`: Boolean (default: False)
- `created_at`: DateTime (auto-generated)

## Limitations

- **In-memory storage**: Tasks are lost when the session ends
- **Single-user**: No authentication or multi-user support
- **No persistence**: No database or file storage
- **No advanced features**: No search, filter, sort, priorities, or tags

These limitations are by design for Phase I and will be addressed in future phases.

## Success Criteria

All success criteria from specs/001-phase1-todo-console/spec.md have been met:

- ✅ Users can add a task and see it in the list
- ✅ All 5 basic operations (add, view, update, delete, mark complete) work without errors
- ✅ Task IDs remain stable during session (no duplicates)
- ✅ Error messages clearly indicate what went wrong
- ✅ Console interface responds instantly (<1 second)

## Testing

Run the comprehensive manual test:

```bash
python test_manual.py
```

This tests all 5 user stories and validation rules.

## Technical Details

- **Python Version**: 3.11+
- **Dependencies**: None (uses stdlib only)
- **CLI Framework**: argparse (stdlib)
- **Storage**: In-memory list
- **Package Manager**: pip (compatible with UV)

## Next Steps

Phase II will add:
- Persistent storage (SQLite database)
- Search and filter functionality
- Task priorities and tags
- Due dates and reminders
