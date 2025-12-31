"""Task repository for in-memory storage."""

from typing import Optional
from src.models.task import Task


class TaskRepository:
    """In-memory task storage with CRUD operations.

    Stores tasks in a list with auto-incrementing IDs.
    Data is lost when the session ends.
    """

    def __init__(self):
        """Initialize empty task list and ID counter."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add(self, task: Task) -> Task:
        """Add a new task to storage with auto-generated ID.

        Args:
            task: Task instance to add (id will be overwritten)

        Returns:
            Task instance with assigned ID
        """
        task.id = self._next_id
        self._next_id += 1
        self._tasks.append(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task instance if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def get_all(self) -> list[Task]:
        """Retrieve all tasks.

        Returns:
            List of all tasks (may be empty)
        """
        return self._tasks.copy()

    def update(self, task: Task) -> Task:
        """Update an existing task.

        Args:
            task: Task instance with updated fields

        Returns:
            Updated task instance

        Raises:
            ValueError: If task with given ID not found
        """
        for i, existing_task in enumerate(self._tasks):
            if existing_task.id == task.id:
                self._tasks[i] = task
                return task
        raise ValueError(f"Task with ID {task.id} not found")

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            True if task was deleted, False if not found
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                return True
        return False

    def count(self) -> int:
        """Count total number of tasks.

        Returns:
            Number of tasks in storage
        """
        return len(self._tasks)
