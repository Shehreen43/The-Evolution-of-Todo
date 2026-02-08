"""
MCP Tool: delete_task
Deletes an existing task for the user.
"""
from mcp.types import Tool, TextContent
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.task_advanced import Task  # Using advanced task model
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

# Tool definition
DELETE_TASK_TOOL = Tool(
    name="delete_task",
    description="Delete an existing task for the user. Use this when user wants to remove, delete, or eliminate a task.",
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
            }
        },
        "required": ["task_id", "user_id"]
    }
)


async def handle_delete_task(
    session: AsyncSession,
    task_id: int,
    user_id: str
) -> Dict[str, Any]:
    """
    Handle delete_task tool execution.

    Args:
        session: Database session
        task_id: Task identifier
        user_id: User identifier

    Returns:
        Dict with deletion result or error
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

        # Find the task
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id.strip())
        result = await session.execute(query)
        task = result.scalars().first()

        if not task:
            return {
                "error": f"Task {task_id} not found for user {user_id}",
                "status": "error"
            }

        # Delete the task
        await session.delete(task)
        await session.commit()

        logger.info(f"Deleted task {task_id} for user {user_id}")

        return {
            "task_id": task_id,
            "status": "deleted",
            "message": f"Task {task_id} has been deleted successfully"
        }

    except Exception as e:
        await session.rollback()
        logger.error(f"Error in delete_task: {str(e)}")
        return {
            "error": f"Failed to delete task: {str(e)}",
            "status": "error"
        }