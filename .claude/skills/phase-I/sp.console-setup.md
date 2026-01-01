---
name: phase-I-todo-console
description: Step-by-step instructions for implementing the Phase-I In-Memory Todo Console App using Claude Code and Spec-Kit Plus. Includes all basic features: add, delete, update, view, and mark tasks complete.
---

# Phase-I: In-Memory Todo Console App

Implement the Phase-I console todo application following spec-driven development.

## Preconditions

Verify:
- Python 3.13+ installed
- UV package manager available
- Project structure created with constitution, specs folder, and src directory

## Implementation Workflow

### 1. Initialize Project Structure

Create directory structure:
```
project/
├── src/
│   └── todo/
│       ├── __init__.py
│       ├── models.py
│       ├── repository.py
│       ├── service.py
│       └── cli.py
├── specs/
├── .claude/
├── CLAUDE.md
└── constitution.md
```

### 2. Define Task Model

Create Task class with fields:
- id: integer, auto-incrementing
- title: string, required, 1-200 characters
- description: string, optional, max 1000 characters
- completed: boolean, default false
- created_at: timestamp

### 3. Implement In-Memory Repository

Create repository for task storage:
- Use list as in-memory store
- Implement add(task), get(id), get_all(), update(id, task), delete(id)
- Auto-generate sequential IDs

### 4. Implement Task Service

Create service layer with methods:
- create_task(title, description)
- list_tasks()
- get_task(id)
- update_task(id, title, description)
- delete_task(id)
- mark_complete(id)

### 5. Implement CLI Interface

Create command-line interface with commands:
- add <title> [--description <desc>]
- list
- get <id>
- update <id> [--title <title>] [--description <desc>]
- delete <id>
- complete <id>

### 6. Create Entry Point

Create main.py that:
- Imports and runs CLI
- Handles keyboard interrupt gracefully

## File Structure

### src/todo/__init__.py
Export main components.

### src/todo/models.py
Define Task dataclass.

### src/todo/repository.py
Implement InMemoryTaskRepository.

### src/todo/service.py
Implement TaskService using repository.

### src/todo/cli.py
Implement argparse-based CLI.

### src/todo/main.py
Entry point with CLI execution.

## Guardrails

### Do
- Use dataclass for Task model
- Validate title length (1-200 chars)
- Handle task not found errors
- Provide clear command-line feedback
- Follow clean code principles

### Do Not
- Use database or persistent storage
- Add authentication
- Add priorities or tags (Phase II)
- Add search or filter (Phase II)

### Defer
- UI improvements
- Configuration files
- Testing framework

## Triggers

Use this skill when:
- User asks to implement Phase-I todo console app
- User says "create a todo console application"
- Starting the console app implementation
