"""
Pydantic schemas for chat API endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    conversation_id: Optional[int] = None
    message: str = Field(min_length=1, max_length=5000)


class ToolCall(BaseModel):
    """Schema for tool calls in chat responses."""
    tool: str
    arguments: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    conversation_id: int
    response: str
    tool_calls: Optional[List[ToolCall]] = None


class ConversationResponse(BaseModel):
    """Response schema for conversation details."""
    id: int
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    """Response schema for message details."""
    id: int
    conversation_id: int
    user_id: str
    role: str
    content: str
    tool_calls: Optional[str] = None
    created_at: datetime