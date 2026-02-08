"""
MCP Tool: complete_task
Marks a task as completed or incomplete for the user.
"""
from mcp.types import Tool, TextContent
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.task_advanced import Task  # Using advanced task model
from datetime import datetime
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

# Tool definition
COMPLETE_TASK_TOOL = Tool(
    name="complete_task",
    description="Mark a task as completed or incomplete for the user. Use this when user wants to mark, complete, or finish a task.",
    inputSchema={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "Task identifier"
            },
            "user_id": {
                "type": "string",
                "description": "User identifier"
            },
            "completed": {
                "type": "boolean",
                "default": True,
                "description": "Whether the task is completed (true) or incomplete (false)"
            }
        },
        "required": ["task_id", "user_id"]
    }
)


async def handle_complete_task(
    session: AsyncSession,
    task_id: int,
    user_id: str,
    completed: bool = True
) -> Dict[str, Any]:
    """
    Handle complete_task tool execution.

    Args:
        session: Database session
        task_id: Task identifier
        user_id: User identifier
        completed: Whether to mark as completed (True) or incomplete (False)

    Returns:
        Dict with updated task details or error
    """
    try:
        # Validate inputs
        if not user_id or not user_id.strip():
            return {
                "error": "user_id is required",
                "status": "error"
            }

        # Robust task_id conversion
        try:
            task_id = int(str(task_id).strip())
        except (ValueError, TypeError):
             return {
                "error": "task_id must be a valid number",
                "status": "error"
            }

        if task_id <= 0:
            return {
                "error": "task_id must be positive",
                "status": "error"
            }
        
        # Handle null/None completed (default to True if not specified, though logic suggests we want expicit intent)
        # But if model sends null, it likely implies "do the action", so True.
        if completed is None:
            completed = True

        # Find the task
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id.strip())
        result = await session.execute(query)
        task = result.scalars().first()

        if not task:
            return {
                "error": f"Task {task_id} not found for user {user_id}",
                "status": "error"
            }

        # Update completion status
        old_status = task.completed
        task.completed = completed
        task.updated_at = datetime.utcnow()

        # Commit changes
        session.add(task)
        await session.commit()
        await session.refresh(task)

        status_text = "completed" if completed else "incomplete"
        logger.info(f"Marked task {task.id} as {status_text} for user {user_id}")

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title,
            "completed": task.completed,
            "previous_status": old_status,
            "message": f"Task marked as {status_text}"
        }

    except Exception as e:
        await session.rollback()
        logger.error(f"Error in complete_task: {str(e)}")
        return {
            "error": f"Failed to update task completion status: {str(e)}",
            "status": "error"
        }