"""
MCP Tool: get_recurring_tasks
Retrieves a list of recurring tasks for the user.
"""
from mcp.types import Tool, TextContent
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.task_advanced import Task  # Using advanced task model
from typing import Dict, Any, List
import json
import logging

logger = logging.getLogger(__name__)

# Tool definition
GET_RECURRING_TASKS_TOOL = Tool(
    name="get_recurring_tasks",
    description="Retrieve a list of recurring tasks for the user. Use this when user wants to see, view, or check their recurring tasks.",
    inputSchema={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "User identifier"
            },
            "status": {
                "type": "string",
                "enum": ["all", "active", "inactive"],
                "default": "active",
                "description": "Filter recurring tasks by status"
            },
            "limit": {
                "type": "integer",
                "default": 10,
                "description": "Maximum number of tasks to return"
            }
        },
        "required": ["user_id"]
    }
)


async def handle_get_recurring_tasks(
    session: AsyncSession,
    user_id: str,
    status: str = "active",
    limit: int = 10
) -> Dict[str, Any]:
    """
    Handle get_recurring_tasks tool execution.

    Args:
        session: Database session
        user_id: User identifier
        status: Recurring task status filter ('all', 'active', 'inactive')
        limit: Maximum number of tasks to return

    Returns:
        Dict with list of recurring tasks or error
    """
    try:
        # Validate inputs
        if not user_id or not user_id.strip():
            return {
                "error": "user_id is required",
                "status": "error"
            }

        # Build query
        query = select(Task).where(
            Task.user_id == user_id.strip(),
            Task.is_recurring == True
        )

        if status == "active":
            # Active recurring tasks are those that are still scheduled
            from datetime import datetime
            from sqlalchemy import or_
            query = query.where(or_(Task.end_recurrence.is_(None), Task.end_recurrence > datetime.utcnow()))
        elif status == "inactive":
            # Inactive recurring tasks are those that have ended
            from datetime import datetime
            query = query.where(Task.end_recurrence.isnot(None)).where(Task.end_recurrence <= datetime.utcnow())

        query = query.limit(limit)

        # Execute query
        result = await session.execute(query)
        tasks = result.scalars().all()

        # Format response
        task_list = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "category": task.category,
                "is_recurring": task.is_recurring,
                "recurrence_pattern": task.recurrence_pattern,
                "next_occurrence": task.next_occurrence.isoformat() if task.next_occurrence else None,
                "end_recurrence": task.end_recurrence.isoformat() if task.end_recurrence else None,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
            task_list.append(task_dict)

        logger.info(f"Retrieved {len(task_list)} recurring tasks for user {user_id}")

        return {
            "tasks": task_list,
            "total_count": len(task_list),
            "status": "success"
        }

    except Exception as e:
        logger.error(f"Error in get_recurring_tasks: {str(e)}")
        return {
            "error": f"Failed to retrieve recurring tasks: {str(e)}",
            "status": "error"
        }