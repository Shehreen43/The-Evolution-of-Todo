"""Task model for Phase I Todo Console App."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a todo task with validation.

    Attributes:
        title: Task title (1-200 characters, required)
        description: Task description (0-1000 characters, optional)
        priority: Task priority ('high', 'medium', 'low', default: 'medium')
        completed: Completion status (default: False)
        id: Unique identifier (auto-generated)
        created_at: Creation timestamp (auto-generated)
    """
    title: str
    description: str = ""
    priority: str = "medium"
    completed: bool = False
    id: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate task fields after initialization."""
        self._validate_title()
        self._validate_description()
        self._validate_priority()

    def _validate_title(self):
        """Validate title field: 1-200 characters, not empty/whitespace."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        if len(self.title) > 200:
            raise ValueError("Title must be 200 characters or less")

    def _validate_description(self):
        """Validate description field: 0-1000 characters."""
        if len(self.description) > 1000:
            raise ValueError("Description must be 1000 characters or less")

    def _validate_priority(self):
        """Validate priority field: must be 'high', 'medium', or 'low'."""
        valid_priorities = ['high', 'medium', 'low']
        if self.priority.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
        self.priority = self.priority.lower()  # Normalize to lowercase
