"""
API Contract Definitions for Frontend-Backend Communication
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Union, Dict, Any
from datetime import datetime
from enum import Enum
from app.models.message import MessageRole


class APIVersion(str, Enum):
    """API Version enumeration"""
    V1 = "v1"


class APIError(BaseModel):
    """Standard API error response"""
    error: str
    message: str
    code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[Dict[str, Any]] = None


class APIResponseEnvelope(BaseModel):
    """Standard API response envelope"""
    success: bool
    data: Optional[Any] = None
    error: Optional[APIError] = None
    metadata: Optional[Dict[str, Any]] = None


class PaginationMeta(BaseModel):
    """Pagination metadata"""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    total: int
    pages: int
    has_next: bool
    has_prev: bool


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user_id: str
    email: str


class UserResponse(BaseModel):
    """User information response"""
    id: str
    email: str
    name: str
    created_at: datetime
    updated_at: datetime


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    """Task priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskRequest(BaseModel):
    """Request schema for creating/updating tasks"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM
    completed: Optional[bool] = False


class TaskResponse(BaseModel):
    """Response schema for tasks"""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime


# Removed MessageRole Enum - now imported from app.models.message


class ToolCall(BaseModel):
    """Tool call schema"""
    id: str
    name: str
    arguments: Dict[str, Any]


class MessageResponse(BaseModel):
    """Response schema for chat messages"""
    id: int
    conversation_id: int
    user_id: str
    role: MessageRole
    content: str
    tool_calls: Optional[List[ToolCall]] = None
    created_at: datetime


class ConversationResponse(BaseModel):
    """Response schema for conversations"""
    id: int
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime


class ChatRequest(BaseModel):
    """Request schema for chat endpoint"""
    message: str = Field(min_length=1, max_length=5000)
    conversation_id: Optional[int] = None
    stream: Optional[bool] = False


class ChatResponse(BaseModel):
    """Response schema for chat endpoint"""
    conversation_id: int
    response: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class StreamingEventType(str, Enum):
    """Streaming event types"""
    TOKEN = "token"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    PLAN_STEP = "plan_step"
    DONE = "done"
    ERROR = "error"


class StreamingEvent(BaseModel):
    """Streaming event schema"""
    type: StreamingEventType
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PlanStep(BaseModel):
    """Plan step schema"""
    id: int
    description: str
    tool_name: Optional[str] = None
    arguments: Optional[Dict[str, Any]] = None
    status: Literal["pending", "executing", "completed", "failed"] = "pending"


class PlanRequest(BaseModel):
    """Request schema for planning endpoint"""
    message: str = Field(min_length=1, max_length=5000)
    conversation_id: Optional[int] = None
    plan_only: Optional[bool] = False


class PlanResponse(BaseModel):
    """Response schema for planning endpoint"""
    conversation_id: int
    plan: List[PlanStep]
    response: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VoiceTranscribeRequest(BaseModel):
    """Request schema for voice transcription"""
    audio_data: bytes  # This will be handled via multipart/form-data in practice


class VoiceTranscribeResponse(BaseModel):
    """Response schema for voice transcription"""
    transcription: str
    confidence: Optional[float] = None
    duration: Optional[float] = None


class VoiceSynthesizeRequest(BaseModel):
    """Request schema for voice synthesis"""
    text: str = Field(min_length=1, max_length=5000)
    voice: Optional[str] = "default"


class VoiceSynthesizeResponse(BaseModel):
    """Response schema for voice synthesis"""
    audio_url: str
    duration: Optional[float] = None