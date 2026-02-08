"""
MCP Context Providers
Provides contextual information to the AI agent about user tasks.
"""
from mcp.server import Server
from mcp.types import TextContent
from sqlmodel import Session, select
from app.models.task import Task
from typing import List, Dict, Any
import logging
import json

logger = logging.getLogger(__name__)

def register_context_providers(mcp_server: Server, get_db_session):
    """
    Register all context providers with the MCP server.

    Args:
        mcp_server: MCP server instance
        get_db_session: Dependency to get database session
    """

    @mcp_server.read_resource()
    async def read_user_tasks(user_id: str) -> List[TextContent]:
        """
        Read user's tasks to provide context about their current todo list.

        Args:
            user_id: User identifier

        Returns:
            List of TextContent with user's tasks
        """
        try:
            # Get database session
            session: Session = next(get_db_session())

            # Query user's tasks
            query = select(Task).where(Task.user_id == user_id).limit(20)  # Limit to 20 tasks
            tasks = session.exec(query).all()

            # Format tasks as text content
            if tasks:
                task_summary = []
                for task in tasks:
                    status = "✓" if task.completed else "○"
                    task_info = f"{status} [{task.id}] {task.title}"
                    if task.description:
                        task_info += f" - {task.description[:100]}..." if len(task.description) > 100 else f" - {task.description}"
                    task_info += f" (Priority: {task.priority})"
                    task_summary.append(task_info)

                content = "\n".join(task_summary)
                return [TextContent(
                    uri=f"todo://user/{user_id}/tasks",
                    content=content,
                    mime_type="text/plain"
                )]
            else:
                return [TextContent(
                    uri=f"todo://user/{user_id}/tasks",
                    content=f"No tasks found for user {user_id}",
                    mime_type="text/plain"
                )]

        except Exception as e:
            logger.error(f"Error reading user tasks: {str(e)}")
            return [TextContent(
                uri=f"todo://user/{user_id}/tasks",
                content=f"Error retrieving tasks: {str(e)}",
                mime_type="text/plain"
            )]
        finally:
            if 'session' in locals():
                session.close()

    @mcp_server.read_resource()
    async def read_user_task_details(user_id: str, task_id: int) -> List[TextContent]:
        """
        Read details of a specific task for the user.

        Args:
            user_id: User identifier
            task_id: Task identifier

        Returns:
            List of TextContent with task details
        """
        try:
            # Get database session
            session: Session = next(get_db_session())

            # Query specific task
            query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            task = session.exec(query).first()

            if task:
                task_details = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }

                content = json.dumps(task_details, indent=2)
                return [TextContent(
                    uri=f"todo://user/{user_id}/task/{task_id}",
                    content=content,
                    mime_type="application/json"
                )]
            else:
                return [TextContent(
                    uri=f"todo://user/{user_id}/task/{task_id}",
                    content=f"Task {task_id} not found for user {user_id}",
                    mime_type="text/plain"
                )]

        except Exception as e:
            logger.error(f"Error reading task {task_id} for user {user_id}: {str(e)}")
            return [TextContent(
                uri=f"todo://user/{user_id}/task/{task_id}",
                content=f"Error retrieving task: {str(e)}",
                mime_type="text/plain"
            )]
        finally:
            if 'session' in locals():
                session.close()

    @mcp_server.list_resources()
    async def list_user_resources(user_id: str) -> List[Dict[str, str]]:
        """
        List available resources for the user.

        Args:
            user_id: User identifier

        Returns:
            List of resource URIs and descriptions
        """
        try:
            # Get database session
            session: Session = next(get_db_session())

            # Count user's tasks
            query = select(Task).where(Task.user_id == user_id)
            tasks = session.exec(query).all()
            task_count = len(tasks)

            resources = [
                {
                    "uri": f"todo://user/{user_id}/tasks",
                    "name": f"User Tasks ({task_count})",
                    "description": f"List of all tasks for user {user_id}"
                }
            ]

            # Add individual task resources
            for task in tasks[:10]:  # Limit to first 10 tasks to avoid too many resources
                resources.append({
                    "uri": f"todo://user/{user_id}/task/{task.id}",
                    "name": f"Task {task.id}: {task.title[:30]}...",
                    "description": f"Details for task {task.id}"
                })

            return resources

        except Exception as e:
            logger.error(f"Error listing resources for user {user_id}: {str(e)}")
            return [
                {
                    "uri": f"todo://user/{user_id}/error",
                    "name": "Error",
                    "description": f"Error listing resources: {str(e)}"
                }
            ]
        finally:
            if 'session' in locals():
                session.close()


# Example usage function
def setup_context_providers(mcp_server: Server, get_db_session):
    """
    Setup function to register context providers with the server.

    Args:
        mcp_server: MCP server instance
        get_db_session: Dependency to get database session
    """
    register_context_providers(mcp_server, get_db_session)
    logger.info("Context providers registered successfully")