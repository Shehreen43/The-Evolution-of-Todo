"""
MCP Tool: add_task
Creates a new task for the user.
"""
from mcp.types import Tool, TextContent
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task_advanced import Task  # Using advanced task model
from datetime import datetime
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

# Tool definition
ADD_TASK_TOOL = Tool(
    name="add_task",
    description="Create a new task for the user. Use this when user wants to add, create, or remember something. Supports advanced features like due dates, reminders, categories, and recurring tasks.",
    inputSchema={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "User identifier"
            },
            "title": {
                "type": "string",
                "description": "Task title (required, max 200 characters)"
            },
            "description": {
                "type": "string",
                "description": "Optional task description (max 1000 characters)"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "default": "medium",
                "description": "Task priority level"
            },
            "due_date": {
                "type": "string",
                "format": "date-time",
                "description": "Due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
            },
            "reminder_time": {
                "type": "string",
                "format": "date-time",
                "description": "Reminder time for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
            },
            "category": {
                "type": "string",
                "description": "Category or tag for the task (max 50 characters)"
            },
            "is_recurring": {
                "type": "boolean",
                "default": False,
                "description": "Whether the task repeats"
            },
            "recurrence_pattern": {
                "type": "string",
                "enum": ["daily", "weekly", "monthly", "yearly"],
                "description": "Pattern for recurring tasks"
            },
            "end_recurrence": {
                "type": "string",
                "format": "date-time",
                "description": "End date for recurring tasks in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
            }
        },
        "required": ["user_id", "title"]
    }
)

async def handle_add_task(
    session: AsyncSession,
    user_id: str,
    title: str,
    description: str = None,
    priority: str = "medium",
    due_date: str = None,
    reminder_time: str = None,
    category: str = None,
    is_recurring: bool = False,
    recurrence_pattern: str = None,
    end_recurrence: str = None
) -> Dict[str, Any]:
    """
    Handle add_task tool execution with advanced features.

    Args:
        session: Database session
        user_id: User identifier
        title: Task title
        description: Optional task description
        priority: Task priority (low, medium, high)
        due_date: Due date in ISO format
        reminder_time: Reminder time in ISO format
        category: Task category
        is_recurring: Whether task is recurring
        recurrence_pattern: Recurrence pattern (daily, weekly, monthly, yearly)
        end_recurrence: End date for recurrence in ISO format

    Returns:
        Dict with task details or error
    """
    try:
        # Validate inputs
        if not user_id or not user_id.strip():
            return {
                "error": "user_id is required",
                "status": "error"
            }

        if not title or not title.strip():
            return {
                "error": "title cannot be empty",
                "status": "error"
            }

        if len(title) > 200:
            return {
                "error": "title must be 200 characters or less",
                "status": "error"
            }

        if description and len(description) > 1000:
            return {
                "error": "description must be 1000 characters or less",
                "status": "error"
            }

        # Validate priority
        valid_priorities = ["low", "medium", "high"]
        if priority not in valid_priorities:
            return {
                "error": f"priority must be one of: {valid_priorities}",
                "status": "error"
            }

        # Validate category length
        if category and len(category) > 50:
            return {
                "error": "category must be 50 characters or less",
                "status": "error"
            }

        # Validate recurrence settings
        if is_recurring:
            if not recurrence_pattern:
                return {
                    "error": "recurrence_pattern is required for recurring tasks",
                    "status": "error"
                }

            valid_patterns = ["daily", "weekly", "monthly", "yearly"]
            if recurrence_pattern not in valid_patterns:
                return {
                    "error": f"recurrence_pattern must be one of: {valid_patterns}",
                    "status": "error"
                }

        # Parse date strings if provided
        parsed_due_date = None
        parsed_reminder_time = None
        parsed_end_recurrence = None

        if due_date:
            try:
                # Try to parse as ISO format first
                parsed_due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except ValueError:
                # Try to parse natural language dates using dateutil
                try:
                    from dateutil.parser import parse as date_parse
                    parsed_due_date = date_parse(due_date, fuzzy=True)
                except:
                    return {
                        "error": "due_date must be in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ) or natural language (e.g., 'tomorrow', 'next Monday 2pm')",
                        "status": "error"
                    }

        if reminder_time:
            try:
                # Try to parse as ISO format first
                parsed_reminder_time = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))
            except ValueError:
                # Try to parse natural language dates using dateutil
                try:
                    from dateutil.parser import parse as date_parse
                    parsed_reminder_time = date_parse(reminder_time, fuzzy=True)
                except:
                    return {
                        "error": "reminder_time must be in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ) or natural language (e.g., 'tomorrow', 'next Monday 2pm')",
                        "status": "error"
                    }

        if end_recurrence:
            try:
                # Try to parse as ISO format first
                parsed_end_recurrence = datetime.fromisoformat(end_recurrence.replace('Z', '+00:00'))
            except ValueError:
                # Try to parse natural language dates using dateutil
                try:
                    from dateutil.parser import parse as date_parse
                    parsed_end_recurrence = date_parse(end_recurrence, fuzzy=True)
                except:
                    return {
                        "error": "end_recurrence must be in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ) or natural language (e.g., 'tomorrow', 'next Monday 2pm')",
                        "status": "error"
                    }

        # Create task with advanced features
        task = Task(
            user_id=user_id.strip(),
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False,
            priority=priority,
            due_date=parsed_due_date,
            reminder_time=parsed_reminder_time,
            category=category.strip() if category else None,
            is_recurring=is_recurring,
            recurrence_pattern=recurrence_pattern,
            end_recurrence=parsed_end_recurrence,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(task)
        await session.commit()
        

        logger.info(f"Created task {task.id} for user {user_id} with advanced features")

        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "reminder_time": task.reminder_time.isoformat() if task.reminder_time else None,
            "category": task.category,
            "is_recurring": task.is_recurring,
            "recurrence_pattern": task.recurrence_pattern,
            "end_recurrence": task.end_recurrence.isoformat() if task.end_recurrence else None
        }

    except Exception as e:
        await session.rollback()
        logger.error(f"Error in add_task: {str(e)}")
        return {
            "error": f"Failed to create task: {str(e)}",
            "status": "error"
        }