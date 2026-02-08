"""
MCP Server initialization and configuration.
Provides tool interface for AI agent to interact with todo tasks.
"""
from mcp.server import Server
from mcp.types import Tool, TextContent
from typing import Any, Dict, List
import logging

# Import configuration
from ..config import settings, get_config_summary

logger = logging.getLogger(__name__)

# Initialize MCP server with configuration
mcp_server = Server("todo-mcp-server")

# Tool registry
_tools: Dict[str, Tool] = {}

def register_tool(tool: Tool) -> None:
    """
    Register a tool with the MCP server.

    Args:
        tool: Tool instance to register
    """
    _tools[tool.name] = tool
    logger.info(f"Registered tool: {tool.name}")

@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    """
    Return list of available tools to the AI agent.

    Returns:
        List of registered Tool instances
    """
    return list(_tools.values())

def get_server() -> Server:
    """
    Get the MCP server instance.

    Returns:
        Configured MCP server
    """
    return mcp_server

# Import and register all tools
from ..tools.add_task import ADD_TASK_TOOL
from ..tools.list_tasks import LIST_TASKS_TOOL
from ..tools.update_task import UPDATE_TASK_TOOL
from ..tools.delete_task import DELETE_TASK_TOOL
from ..tools.complete_task import COMPLETE_TASK_TOOL
from ..tools.get_recurring_tasks import GET_RECURRING_TASKS_TOOL

register_tool(ADD_TASK_TOOL)
register_tool(LIST_TASKS_TOOL)
register_tool(UPDATE_TASK_TOOL)
register_tool(DELETE_TASK_TOOL)
register_tool(COMPLETE_TASK_TOOL)
register_tool(GET_RECURRING_TASKS_TOOL)

# Import and setup context providers
from ..context_providers import setup_context_providers
from ...database.connection import get_sync_session  # Use sync session for MCP tools

# Setup context providers (pass the session dependency)
setup_context_providers(mcp_server, get_sync_session)

# Log server initialization (moved to avoid import-time execution issues)
try:
    from ..config import get_config_summary
    logger.info(f"MCP Server initialized with config: {get_config_summary()}")
except ImportError:
    logger.info("MCP Server initialized")