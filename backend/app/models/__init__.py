"""
SQLModel models for the application.

This module imports all models to ensure they are registered with SQLModel's metadata
exactly once, preventing the "table already defined" error during testing.
"""

# Import models to register them with SQLModel metadata
from .task import Task  # noqa: F401
from .conversation import Conversation  # noqa: F401
from .message import Message  # noqa: F401

__all__ = ["Task", "Conversation", "Message"]