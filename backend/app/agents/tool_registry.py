"""
Tool registry for managing available tools in the agent system.
"""
from typing import Dict, Callable, Any, List
from functools import wraps


class ToolRegistry:
    """Registry for managing available tools in the agent system."""

    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._tool_metadata: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, description: str = "", parameters: Dict[str, Any] = None):
        """
        Decorator to register a tool with the registry.

        Args:
            name: Name of the tool
            description: Description of what the tool does
            parameters: JSON schema for tool parameters
        """
        def decorator(func: Callable):
            self._tools[name] = func
            self._tool_metadata[name] = {
                "name": name,
                "description": description,
                "parameters": parameters or {},
                "function": func
            }
            return func
        return decorator

    def get_tool(self, name: str) -> Callable:
        """Get a tool function by name."""
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found in registry")
        return self._tools[name]

    def get_tool_metadata(self, name: str) -> Dict[str, Any]:
        """Get metadata for a tool."""
        if name not in self._tool_metadata:
            raise ValueError(f"Tool '{name}' not found in registry")
        return self._tool_metadata[name]

    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._tools.keys())

    def get_all_metadata(self) -> List[Dict[str, Any]]:
        """Get metadata for all tools."""
        return list(self._tool_metadata.values())


# Global tool registry instance
registry = ToolRegistry()


# Register the existing MCP tools
from app.mcp.tools.add_task import handle_add_task
from app.mcp.tools.list_tasks import handle_list_tasks
from app.mcp.tools.update_task import handle_update_task
from app.mcp.tools.delete_task import handle_delete_task
from app.mcp.tools.complete_task import handle_complete_task


@registry.register(
    name="add_task",
    description="Create a new task for the user. Use this when user wants to add, create, or remember something.",
    parameters={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Task title (required, max 200 characters)"
            },
            "description": {
                "type": "string",
                "description": "Optional task description (max 1000 characters)"
            }
        },
        "required": ["title"]
    }
)
def add_task_tool(db, **kwargs):
    """Wrapper for the add_task MCP tool."""
    return handle_add_task(db, **kwargs)


@registry.register(
    name="list_tasks",
    description="Retrieve a list of tasks for the user. Use this when user wants to see, view, or check their tasks.",
    parameters={
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["all", "pending", "completed"],
                "default": "all",
                "description": "Filter tasks by completion status"
            },
            "limit": {
                "type": "integer",
                "default": 10,
                "description": "Maximum number of tasks to return"
            }
        }
    }
)
def list_tasks_tool(db, **kwargs):
    """Wrapper for the list_tasks MCP tool."""
    return handle_list_tasks(db, **kwargs)


@registry.register(
    name="update_task",
    description="Update an existing task for the user.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "Task identifier to update"
            },
            "title": {
                "type": "string",
                "description": "New task title (max 200 characters)"
            },
            "description": {
                "type": "string",
                "description": "New task description (max 1000 characters)"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "Task priority level"
            }
        },
        "required": ["task_id"]
    }
)
def update_task_tool(db, **kwargs):
    """Wrapper for the update_task MCP tool."""
    return handle_update_task(db, **kwargs)


@registry.register(
    name="delete_task",
    description="Delete a task for the user.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "Task identifier to delete"
            }
        },
        "required": ["task_id"]
    }
)
def delete_task_tool(db, **kwargs):
    """Wrapper for the delete_task MCP tool."""
    return handle_delete_task(db, **kwargs)


@registry.register(
    name="complete_task",
    description="Mark a task as completed or incomplete for the user.",
    parameters={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "Task identifier to update"
            },
            "completed": {
                "type": "boolean",
                "default": True,
                "description": "Whether the task is completed (true) or not (false)"
            }
        },
        "required": ["task_id", "completed"]
    }
)
def complete_task_tool(db, **kwargs):
    """Wrapper for the complete_task MCP tool."""
    return handle_complete_task(db, **kwargs)


def get_available_tools() -> List[Dict[str, Any]]:
    """Get all available tools in the registry as OpenAI-compatible function definitions."""
    tools = []
    for metadata in registry.get_all_metadata():
        tools.append({
            "type": "function",
            "function": {
                "name": metadata["name"],
                "description": metadata["description"],
                "parameters": metadata["parameters"]
            }
        })
    return tools


def execute_tool(name: str, db, **kwargs) -> Any:
    """Execute a tool by name with the provided arguments."""
    tool_func = registry.get_tool(name)
    return tool_func(db, **kwargs)