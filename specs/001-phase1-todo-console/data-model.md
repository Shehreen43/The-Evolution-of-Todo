# Data Model: Phase 1 - In-Memory Todo Console App

## Task Entity

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Auto-incremented, unique | Primary identifier |
| `title` | String | 1-200 characters, required | Task title |
| `description` | String | 0-1000 characters, optional | Task details |
| `completed` | Boolean | Default: False | Completion status |
| `created_at` | DateTime | Auto-generated | Creation timestamp |

## Validation Rules

### Title Validation
- Minimum length: 1 character
- Maximum length: 200 characters
- Cannot be empty/whitespace only

### Description Validation
- Minimum length: 0 characters (optional)
- Maximum length: 1000 characters
- Can be empty string

### ID Management
- Sequential integers starting from 1
- Never reused during session
- Unique across all tasks

## Python Implementation

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    title: str
    description: str = ""
    completed: bool = False
    id: int = 0
    created_at: datetime = field(default_factory=datetime.now)
```

## Repository Interface

```python
class TaskRepository:
    def add(self, task: Task) -> Task
    def get_by_id(self, id: int) -> Optional[Task]
    def get_all(self) -> list[Task]
    def update(self, task: Task) -> Task
    def delete(self, id: int) -> bool
    def count(self) -> int
```

## Service Interface

```python
class TaskService:
    def create_task(self, title: str, description: str = "") -> Task
    def list_tasks(self) -> list[Task]
    def get_task(self, id: int) -> Optional[Task]
    def update_task(self, id: int, title: str = None, description: str = None) -> Task
    def delete_task(self, id: int) -> bool
    def toggle_complete(self, id: int) -> Task
```
