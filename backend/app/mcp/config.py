"""
MCP Server Configuration
Settings and configuration for the Model Context Protocol server.
"""
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class MCPConfig(BaseSettings):
    """
    Configuration settings for the MCP server.
    """
    # Server settings
    mcp_server_host: str = Field(default="localhost", description="Host to bind MCP server to")
    mcp_server_port: int = Field(default=8000, description="Port to bind MCP server to")
    mcp_server_ssl: bool = Field(default=False, description="Enable SSL for MCP server")

    # Database settings
    mcp_db_timeout: int = Field(default=30, description="Database operation timeout in seconds")
    mcp_db_pool_size: int = Field(default=5, description="Database connection pool size")

    # Tool settings
    mcp_tool_timeout: int = Field(default=10, description="Timeout for tool execution in seconds")
    mcp_max_results: int = Field(default=50, description="Maximum number of results to return")

    # Security settings
    mcp_rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    mcp_requests_per_minute: int = Field(default=100, description="Max requests per minute per user")

    # Logging settings
    mcp_log_level: str = Field(default="INFO", description="Logging level for MCP server")
    mcp_log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )

    class Config:
        env_prefix = "MCP_"
        case_sensitive = False
        extra = "allow"


# Global configuration instance
settings = MCPConfig()

# Convenience functions for accessing settings
def get_mcp_host() -> str:
    """Get the MCP server host."""
    return settings.mcp_server_host


def get_mcp_port() -> int:
    """Get the MCP server port."""
    return settings.mcp_server_port


def get_mcp_ssl() -> bool:
    """Get the MCP server SSL setting."""
    return settings.mcp_server_ssl


def get_db_timeout() -> int:
    """Get the database timeout setting."""
    return settings.mcp_db_timeout


def get_max_results() -> int:
    """Get the maximum results setting."""
    return settings.mcp_max_results


def get_rate_limit_enabled() -> bool:
    """Get the rate limiting setting."""
    return settings.mcp_rate_limit_enabled


def get_requests_per_minute() -> int:
    """Get the requests per minute setting."""
    return settings.mcp_requests_per_minute


# Validation functions
def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format.

    Args:
        user_id: User identifier to validate

    Returns:
        True if valid, False otherwise
    """
    if not user_id or not isinstance(user_id, str):
        return False

    # Basic validation: non-empty string, reasonable length
    user_id = user_id.strip()
    if not user_id or len(user_id) > 255:
        return False

    # Additional validation can be added here
    return True


def validate_task_id(task_id: int) -> bool:
    """
    Validate task ID format.

    Args:
        task_id: Task identifier to validate

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(task_id, int):
        return False

    return task_id > 0


def validate_priority(priority: str) -> bool:
    """
    Validate task priority value.

    Args:
        priority: Priority value to validate

    Returns:
        True if valid, False otherwise
    """
    if not priority or not isinstance(priority, str):
        return False

    valid_priorities = ["low", "medium", "high"]
    return priority.lower() in valid_priorities


def validate_status(status: str) -> bool:
    """
    Validate task status value.

    Args:
        status: Status value to validate

    Returns:
        True if valid, False otherwise
    """
    if not status or not isinstance(status, str):
        return False

    valid_statuses = ["all", "pending", "completed"]
    return status.lower() in valid_statuses


# Configuration utility functions
def get_mcp_server_url() -> str:
    """
    Get the full URL for the MCP server.

    Returns:
        Complete URL for the MCP server
    """
    protocol = "https" if settings.mcp_server_ssl else "http"
    return f"{protocol}://{settings.mcp_server_host}:{settings.mcp_server_port}"


def get_config_summary() -> dict:
    """
    Get a summary of the current configuration.

    Returns:
        Dictionary with configuration summary
    """
    return {
        "server_url": get_mcp_server_url(),
        "host": settings.mcp_server_host,
        "port": settings.mcp_server_port,
        "ssl_enabled": settings.mcp_server_ssl,
        "max_results": settings.mcp_max_results,
        "rate_limit_enabled": settings.mcp_rate_limit_enabled,
        "requests_per_minute": settings.mcp_requests_per_minute
    }


# Initialize settings instance
settings = MCPConfig()