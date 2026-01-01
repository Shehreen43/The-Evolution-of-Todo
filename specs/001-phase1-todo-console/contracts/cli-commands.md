# CLI Command Contracts: Phase 1 - In-Memory Todo Console App

## Command Overview

All commands are invoked via the `todo` entry point.

## Commands

### add - Create a new task

```bash
todo add "Task title" [--description "Task description"]
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | String | Yes | Task title (1-200 chars) |
| --description | String | No | Task description (0-1000 chars) |

**Success Output:**
```
Task added with ID 1
```

**Error Output:**
```
Error: Title cannot be empty
Error: Title must be 200 characters or less
```

---

### list - View all tasks

```bash
todo list
```

**Success Output:**
```
ID | Status | Title
1  | [ ]    | Buy groceries
2  | [x]    | Meeting with team
```

**Empty List Output:**
```
No tasks found. Add a task to get started.
```

---

### get - View a specific task

```bash
todo get <id>
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | Integer | Yes | Task ID |

**Success Output:**
```
Task #1
Title: Buy groceries
Description: Milk, eggs, bread
Status: Pending
Created: 2025-12-30 10:30:00
```

**Error Output:**
```
Error: Task with ID 1 not found
```

---

### complete - Mark task as complete/incomplete

```bash
todo complete <id>
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | Integer | Yes | Task ID |

**Success Output:**
```
Task #1 marked as complete
```

**Toggle Output (if already complete):**
```
Task #1 marked as incomplete
```

**Error Output:**
```
Error: Task with ID 1 not found
```

---

### delete - Delete a task

```bash
todo delete <id>
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | Integer | Yes | Task ID |

**Success Output:**
```
Task #1 deleted
```

**Error Output:**
```
Error: Task with ID 1 not found
```

---

### update - Update task details

```bash
todo update <id> [--title "New title"] [--description "New description"]
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | Integer | Yes | Task ID |
| --title | String | No | New task title |
| --description | String | No | New task description |

**Success Output:**
```
Task #1 updated
```

**Error Output:**
```
Error: Task with ID 1 not found
Error: Title must be 200 characters or less
```

---

### help - Show help

```bash
todo help
# or
todo --help
```

Displays all available commands and usage information.

---

### version - Show version

```bash
todo version
```

**Output:**
```
Todo Console App v1.0.0
```
