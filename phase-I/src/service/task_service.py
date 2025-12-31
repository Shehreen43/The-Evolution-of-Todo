"""Task service for business logic and validation."""

from typing import Optional
from src.models.task import Task
from src.repository.task_repository import TaskRepository


class TaskService:
    """Business logic layer for task operations.

    Handles validation, coordinates repository operations,
    and provides high-level task management methods.
    """

    def __init__(self, repository: TaskRepository):
        """Initialize service with repository dependency.

        Args:
            repository: TaskRepository instance for data operations
        """
        self._repository = repository

    def create_task(self, title: str, description: str = "") -> Task:
        """Create a new task with validation.

        Args:
            title: Task title (1-200 characters)
            description: Optional task description (0-1000 characters)

        Returns:
            Created task with assigned ID

        Raises:
            ValueError: If validation fails
        """
        # Task validation happens in Task.__post_init__
        task = Task(title=title, description=description)
        return self._repository.add(task)

    def list_tasks(self) -> list[Task]:
        """List all tasks.

        Returns:
            List of all tasks (may be empty)
        """
        return self._repository.get_all()

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a specific task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task instance if found, None otherwise
        """
        return self._repository.get_by_id(task_id)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """Update task fields.

        Args:
            task_id: Unique task identifier
            title: New title (None to keep current)
            description: New description (None to keep current)

        Returns:
            Updated task

        Raises:
            ValueError: If task not found or validation fails
        """
        task = self._repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        # Update only provided fields
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        # Re-validate after updates
        task._validate_title()
        task._validate_description()

        return self._repository.update(task)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            True if deleted, False if not found
        """
        return self._repository.delete(task_id)

    def toggle_complete(self, task_id: int) -> Task:
        """Toggle task completion status.

        Args:
            task_id: Unique task identifier

        Returns:
            Updated task with toggled completion status

        Raises:
            ValueError: If task not found
        """
        task = self._repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        task.completed = not task.completed
        return self._repository.update(task)
