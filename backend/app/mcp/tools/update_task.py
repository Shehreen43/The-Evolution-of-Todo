"""
MCP Tool: update_task
Updates an existing task for the user.
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
UPDATE_TASK_TOOL = Tool(
    name="update_task",
    description="Update an existing task for the user. Use this when user wants to modify, edit, or change a task. Supports updating advanced features like due dates, reminders, categories, and recurring settings.",
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
            "title": {
                "type": "string",
                "description": "New task title (max 200 characters)"
            },
            "description": {
                "type": "string",
                "description": "New task description (max 1000 characters)"
            },
            "completed": {
                "type": "boolean",
                "description": "New completion status"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "New task priority"
            },
            "due_date": {
                "type": "string",
                "format": "date-time",
                "description": "New due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
            },
            "reminder_time": {
                "type": "string",
                "format": "date-time",
                "description": "New reminder time for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
            },
            "category": {
                "type": "string",
                "description": "New category or tag for the task (max 50 characters)"
            },
            "is_recurring": {
                "type": "boolean",
                "description": "Whether the task should repeat"
            },
            "recurrence_pattern": {
                "type": "string",
                "enum": ["daily", "weekly", "monthly", "yearly"],
                "description": "New pattern for recurring tasks"
            },
            "end_recurrence": {
                "type": "string",
                "format": "date-time",
                "description": "New end date for recurring tasks in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
            }
        },
        "required": ["task_id", "user_id"]
    }
)


async def handle_update_task(
    session: AsyncSession,
    task_id: int,
    user_id: str,
    title: str = None,
    description: str = None,
    completed: bool = None,
    priority: str = None,
    due_date: str = None,
    reminder_time: str = None,
    category: str = None,
    is_recurring: bool = None,
    recurrence_pattern: str = None,
    end_recurrence: str = None
) -> Dict[str, Any]:
    """
    Handle update_task tool execution with advanced features.

    Args:
        session: Database session
        task_id: Task identifier
        user_id: User identifier
        title: New task title
        description: New task description
        completed: New completion status
        priority: New task priority
        due_date: New due date in ISO format
        reminder_time: New reminder time in ISO format
        category: New task category
        is_recurring: New recurring status
        recurrence_pattern: New recurrence pattern
        end_recurrence: New end date for recurrence in ISO format

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

        # Find the task
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id.strip())
        result = await session.execute(query)
        task = result.scalars().first()

        if not task:
            return {
                "error": f"Task {task_id} not found for user {user_id}",
                "status": "error"
            }

        # Validate and update fields
        updates_made = []

        if title is not None:
            if len(title) < 1 or len(title) > 200:
                return {
                    "error": "Title must be between 1 and 200 characters",
                    "status": "error"
                }
            task.title = title.strip()
            updates_made.append("title")

        if description is not None:
            if len(description) > 1000:
                return {
                    "error": "Description must be 1000 characters or less",
                    "status": "error"
                }
            task.description = description.strip() if description else None
            updates_made.append("description")

        if completed is not None:
            task.completed = completed
            updates_made.append("completed")

        if priority is not None:
            valid_priorities = ["low", "medium", "high"]
            if priority not in valid_priorities:
                return {
                    "error": f"Priority must be one of: {valid_priorities}",
                    "status": "error"
                }
            task.priority = priority
            updates_made.append("priority")

        if due_date is not None:
            if due_date:
                try:
                    # Try to parse as ISO format first
                    parsed_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    task.due_date = parsed_date
                except ValueError:
                    # Try to parse natural language dates using dateutil
                    try:
                        from dateutil.parser import parse as date_parse
                        parsed_date = date_parse(due_date, fuzzy=True)
                        task.due_date = parsed_date
                    except:
                        return {
                            "error": "due_date must be in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ) or natural language (e.g., 'tomorrow', 'next Monday 2pm')",
                            "status": "error"
                        }
            else:
                task.due_date = None
            updates_made.append("due_date")

        if reminder_time is not None:
            if reminder_time:
                try:
                    # Try to parse as ISO format first
                    parsed_time = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))
                    task.reminder_time = parsed_time
                except ValueError:
                    # Try to parse natural language dates using dateutil
                    try:
                        from dateutil.parser import parse as date_parse
                        parsed_time = date_parse(reminder_time, fuzzy=True)
                        task.reminder_time = parsed_time
                    except:
                        return {
                            "error": "reminder_time must be in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ) or natural language (e.g., 'tomorrow', 'next Monday 2pm')",
                            "status": "error"
                        }
            else:
                task.reminder_time = None
            updates_made.append("reminder_time")

        if category is not None:
            if category:
                if len(category) > 50:
                    return {
                        "error": "Category must be 50 characters or less",
                        "status": "error"
                    }
                task.category = category.strip()
            else:
                task.category = None
            updates_made.append("category")

        if is_recurring is not None:
            task.is_recurring = is_recurring
            updates_made.append("is_recurring")

        if recurrence_pattern is not None:
            if recurrence_pattern:
                valid_patterns = ["daily", "weekly", "monthly", "yearly"]
                if recurrence_pattern not in valid_patterns:
                    return {
                        "error": f"recurrence_pattern must be one of: {valid_patterns}",
                        "status": "error"
                    }
                task.recurrence_pattern = recurrence_pattern
            else:
                task.recurrence_pattern = None
            updates_made.append("recurrence_pattern")

        if end_recurrence is not None:
            if end_recurrence:
                try:
                    # Try to parse as ISO format first
                    parsed_date = datetime.fromisoformat(end_recurrence.replace('Z', '+00:00'))
                    task.end_recurrence = parsed_date
                except ValueError:
                    # Try to parse natural language dates using dateutil
                    try:
                        from dateutil.parser import parse as date_parse
                        parsed_date = date_parse(end_recurrence, fuzzy=True)
                        task.end_recurrence = parsed_date
                    except:
                        return {
                            "error": "end_recurrence must be in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ) or natural language (e.g., 'tomorrow', 'next Monday 2pm')",
                            "status": "error"
                        }
            else:
                task.end_recurrence = None
            updates_made.append("end_recurrence")

        # Update timestamp
        task.updated_at = datetime.utcnow()

        # Commit changes
        session.add(task)
        await session.commit()
        await session.refresh(task)

        logger.info(f"Updated task {task.id} for user {user_id}, fields: {updates_made}")

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "reminder_time": task.reminder_time.isoformat() if task.reminder_time else None,
            "category": task.category,
            "is_recurring": task.is_recurring,
            "recurrence_pattern": task.recurrence_pattern,
            "end_recurrence": task.end_recurrence.isoformat() if task.end_recurrence else None,
            "updated_fields": updates_made
        }

    except Exception as e:
        await session.rollback()
        logger.error(f"Error in update_task: {str(e)}")
        return {
            "error": f"Failed to update task: {str(e)}",
            "status": "error"
        }