from sqlmodel import Session, select
from typing import Dict, Any, Optional
import logging
from app.models.task_advanced import Task  # Using advanced task model with all features

logger = logging.getLogger(__name__)

async def handle_create_todo_task(
    session: Session,
    user_id: str,
    title: str,
    description: str = None,
    priority: str = "normal"
) -> Dict[str, Any]:
    """Create a new todo task."""
    try:
        # Validate inputs
        if not user_id or not user_id.strip():
            return {"error": "user_id is required", "status": "error"}

        if not title or not title.strip():
            return {"error": "title is required", "status": "error"}

        if len(title) > 200:
            return {"error": "title too long (max 200 chars)", "status": "error"}

        if description and len(description) > 1000:
            return {"error": "description too long (max 1000 chars)", "status": "error"}

        valid_priorities = ["low", "normal", "high", "urgent"]
        if priority not in valid_priorities:
            return {"error": f"priority must be one of: {valid_priorities}", "status": "error"}

        # Create task
        task = Task(
            user_id=user_id.strip(),
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False,
            priority=priority
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Created task {task.id} for user {user_id}")

        return {
            "status": "success",
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority
        }

    except Exception as e:
        session.rollback()
        logger.error(f"Error creating task: {e}")
        return {"error": f"Failed to create task: {str(e)}", "status": "error"}


async def handle_list_todo_tasks(
    session: Session,
    user_id: str,
    status: str = "all",
    priority: str = "all"
) -> Dict[str, Any]:
    """List user's todo tasks."""
    try:
        # Validate inputs
        if not user_id:
            return {"error": "user_id is required", "status": "error"}

        valid_statuses = ["all", "pending", "completed"]
        if status not in valid_statuses:
            return {"error": f"status must be one of: {valid_statuses}", "status": "error"}

        valid_priorities = ["all", "low", "normal", "high", "urgent"]
        if priority not in valid_priorities:
            return {"error": f"priority must be one of: {valid_priorities}", "status": "error"}

        # Build query
        statement = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)

        if priority != "all":
            statement = statement.where(Task.priority == priority)

        tasks = session.exec(statement).all()

        return {
            "status": "success",
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                    "priority": t.priority,
                    "created_at": t.created_at.isoformat() if t.created_at else None
                }
                for t in tasks
            ],
            "count": len(tasks)
        }

    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        return {"error": f"Failed to list tasks: {str(e)}", "status": "error"}


async def handle_update_todo_task(
    session: Session,
    task_id: int,
    user_id: str,
    title: str = None,
    description: str = None,
    priority: str = None,
    completed: bool = None
) -> Dict[str, Any]:
    """Update an existing todo task."""
    try:
        # Validate inputs
        if not user_id or not user_id.strip():
            return {"error": "user_id is required", "status": "error"}

        if task_id <= 0:
            return {"error": "task_id must be positive", "status": "error"}

        # Find task
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            return {"error": f"Task {task_id} not found for user {user_id}", "status": "error"}

        # Validate updates
        if title is not None:
            if not title.strip():
                return {"error": "title cannot be empty", "status": "error"}
            if len(title) > 200:
                return {"error": "title too long (max 200 chars)", "status": "error"}

        if description is not None and len(description) > 1000:
            return {"error": "description too long (max 1000 chars)", "status": "error"}

        if priority is not None:
            valid_priorities = ["low", "normal", "high", "urgent"]
            if priority not in valid_priorities:
                return {"error": f"priority must be one of: {valid_priorities}", "status": "error"}

        # Update task
        updates_made = []
        if title is not None:
            task.title = title.strip()
            updates_made.append("title")
        if description is not None:
            task.description = description.strip() if description else None
            updates_made.append("description")
        if priority is not None:
            task.priority = priority
            updates_made.append("priority")
        if completed is not None:
            task.completed = completed
            updates_made.append("completed")

        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Updated task {task.id} for user {user_id}, fields: {updates_made}")

        return {
            "status": "success",
            "task_id": task.id,
            "updated_fields": updates_made,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority
            }
        }

    except Exception as e:
        session.rollback()
        logger.error(f"Error updating task {task_id}: {e}")
        return {"error": f"Failed to update task: {str(e)}", "status": "error"}


async def handle_delete_todo_task(
    session: Session,
    task_id: int,
    user_id: str
) -> Dict[str, Any]:
    """Delete a todo task."""
    try:
        # Validate inputs
        if not user_id or not user_id.strip():
            return {"error": "user_id is required", "status": "error"}

        if task_id <= 0:
            return {"error": "task_id must be positive", "status": "error"}

        # Find task
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            return {"error": f"Task {task_id} not found for user {user_id}", "status": "error"}

        # Delete task
        session.delete(task)
        session.commit()

        logger.info(f"Deleted task {task_id} for user {user_id}")

        return {
            "status": "success",
            "task_id": task_id,
            "message": f"Task {task_id} deleted successfully"
        }

    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting task {task_id}: {e}")
        return {"error": f"Failed to delete task: {str(e)}", "status": "error"}


async def handle_mark_todo_completed(
    session: Session,
    task_id: int,
    user_id: str,
    completed: bool = True
) -> Dict[str, Any]:
    """Mark a todo task as completed or incomplete."""
    try:
        # Validate inputs
        if not user_id or not user_id.strip():
            return {"error": "user_id is required", "status": "error"}

        if task_id <= 0:
            return {"error": "task_id must be positive", "status": "error"}

        # Find task
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            return {"error": f"Task {task_id} not found for user {user_id}", "status": "error"}

        # Update completion status
        old_status = task.completed
        task.completed = completed
        session.add(task)
        session.commit()
        session.refresh(task)

        status_text = "completed" if completed else "incomplete"
        logger.info(f"Marked task {task_id} as {status_text} for user {user_id}")

        return {
            "status": "success",
            "task_id": task.id,
            "previous_status": old_status,
            "new_status": completed,
            "message": f"Task marked as {status_text}"
        }

    except Exception as e:
        session.rollback()
        logger.error(f"Error marking task {task_id} as {'completed' if completed else 'incomplete'}: {e}")
        return {"error": f"Failed to update task status: {str(e)}", "status": "error"}