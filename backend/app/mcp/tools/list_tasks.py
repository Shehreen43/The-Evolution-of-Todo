"""
MCP Tool: list_tasks
Retrieves a list of tasks for the user.
"""
from mcp.types import Tool, TextContent
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task_advanced import Task  # Using advanced task model
from datetime import datetime
from typing import Dict, Any, List
import json
import logging

logger = logging.getLogger(__name__)

# Tool definition
LIST_TASKS_TOOL = Tool(
    name="list_tasks",
    description="Retrieve a list of tasks for the user. Use this when user wants to see, view, or check their tasks. Supports filtering by status, category, due date, and recurring status.",
    inputSchema={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "User identifier"
            },
            "status": {
                "type": "string",
                "enum": ["all", "pending", "completed"],
                "default": "all",
                "description": "Filter tasks by completion status"
            },
            "category": {
                "type": "string",
                "description": "Filter tasks by category"
            },
            "due_date_filter": {
                "type": "string",
                "enum": ["all", "today", "overdue", "week", "month"],
                "default": "all",
                "description": "Filter tasks by due date (today, overdue, week, month)"
            },
            "is_recurring": {
                "type": "boolean",
                "description": "Filter tasks by recurring status (true/false)"
            },
            "priority": {
                "type": "string",
                "enum": ["all", "low", "medium", "high"],
                "default": "all",
                "description": "Filter tasks by priority"
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


async def handle_list_tasks(
    session: AsyncSession,
    user_id: str,
    status: str = "all",
    category: str = None,
    due_date_filter: str = "all",
    is_recurring: bool = None,
    priority: str = "all",
    limit: int = 10
) -> Dict[str, Any]:
    """
    Handle list_tasks tool execution with advanced filtering.

    Args:
        session: Database session
        user_id: User identifier
        status: Task status filter ('all', 'pending', 'completed')
        category: Filter by task category
        due_date_filter: Filter by due date ('all', 'today', 'overdue', 'week', 'month')
        is_recurring: Filter by recurring status (True/False)
        priority: Filter by priority ('all', 'low', 'medium', 'high')
        limit: Maximum number of tasks to return

    Returns:
        Dict with list of tasks or error
    """
    try:
        # Validate inputs
        if not user_id or not user_id.strip():
            return {
                "error": "user_id is required",
                "status": "error"
            }

        # Build query
        query = select(Task).where(Task.user_id == user_id.strip())

        # Apply status filter
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        # Apply category filter
        if category:
            query = query.where(Task.category.ilike(f"%{category}%"))

        # Apply priority filter
        if priority != "all":
            query = query.where(Task.priority == priority)

        # Apply recurring filter
        if is_recurring is not None:
            query = query.where(Task.is_recurring == is_recurring)

        # Apply due date filter
        if due_date_filter != "all":
            now = datetime.utcnow()
            today = datetime(now.year, now.month, now.day)
            end_of_week = today.replace(day=today.day + 7)
            end_of_month = today.replace(day=1).replace(month=today.month + 1) if today.month < 12 else today.replace(year=today.year + 1, month=1)

            if due_date_filter == "today":
                query = query.where(Task.due_date.between(today, today.replace(hour=23, minute=59, second=59)))
            elif due_date_filter == "overdue":
                query = query.where(Task.due_date < now).where(Task.completed == False)
            elif due_date_filter == "week":
                query = query.where(Task.due_date.between(today, end_of_week))
            elif due_date_filter == "month":
                query = query.where(Task.due_date.between(today, end_of_month))

        # Add sorting by creation date (newest first)
        query = query.order_by(Task.created_at.desc())
        
        # Increase limit to 50 if not specified
        query = query.limit(limit if limit != 10 else 50)

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
                "reminder_time": task.reminder_time.isoformat() if task.reminder_time else None,
                "category": task.category,
                "is_recurring": task.is_recurring,
                "recurrence_pattern": task.recurrence_pattern,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
            task_list.append(task_dict)

        logger.info(f"Retrieved {len(task_list)} tasks for user {user_id} with filters: status={status}, category={category}, due_date_filter={due_date_filter}, is_recurring={is_recurring}, priority={priority}")

        return {
            "tasks": task_list,
            "total_count": len(task_list),
            "status": "success"
        }

    except Exception as e:
        logger.error(f"Error in list_tasks: {str(e)}")
        return {
            "error": f"Failed to retrieve tasks: {str(e)}",
            "status": "error"
        }