"""
Chat API routes for the AI Chatbot integration.
FIXED: Removed duplicate streaming route - now handled by streaming_chat.py
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from app.database.connection import get_db
from app.api.deps import get_current_user
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.api_contract import ChatRequest, ChatResponse, ConversationResponse, MessageResponse
from app.utils.jwt import TokenPayload
from app.services.voice_service import VoiceService

router = APIRouter(prefix="/api/{user_id}", tags=["chat"])

logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user)
):
    """
    Main chat endpoint - NON-STREAMING ONLY.
    For streaming responses, use /chat/stream endpoint.

    Args:
        user_id: User identifier from path parameter
        request: Chat request with conversation_id and message
        db: Database session dependency
        current_user: Authenticated user from JWT token

    Returns:
        ChatResponse with conversation_id, AI response, and tool calls
    """
    # Verify user access
    if current_user.sub != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's chat"
        )

    from app.services.chat_service import ChatService
    chat_service = ChatService(db)

    try:
        result = await chat_service.process_chat(
            user_id=user_id,
            request=request
        )

        # Handle response
        if isinstance(result, tuple) and len(result) >= 2:
            conversation_id, response_text = result[:2]
            executed_tool_calls = result[2] if len(result) > 2 else []
        else:
            conversation_id = getattr(result, 'conversation_id', None) or getattr(result, 'id', None)
            response_text = getattr(result, 'response', str(result) if result else "I processed your request.")
            executed_tool_calls = getattr(result, 'tool_calls', [])

        # Convert tool calls
        tool_calls_response = []
        if executed_tool_calls:
            for call in executed_tool_calls:
                if isinstance(call, dict):
                    tool_calls_response.append({
                        "tool": call.get("tool"),
                        "arguments": call.get("arguments", {}),
                        "result": call.get("result", {})
                    })
                else:
                    tool_calls_response.append({
                        "tool": getattr(call, 'tool', ''),
                        "arguments": getattr(call, 'arguments', {}),
                        "result": getattr(call, 'result', {})
                    })

        return ChatResponse(
            conversation_id=conversation_id or 0,
            response=response_text or "I processed your request.",
            tool_calls=tool_calls_response if tool_calls_response else None
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user)
):
    """List all conversations for the authenticated user."""
    if current_user.sub != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's conversations"
        )

    from sqlmodel import select

    statement = select(Conversation).where(Conversation.user_id == user_id)
    result = await db.execute(statement)
    conversations = result.scalars().all()

    return [ConversationResponse(
        id=conv.id,
        user_id=conv.user_id,
        title=conv.title,
        created_at=conv.created_at,
        updated_at=conv.updated_at
    ) for conv in conversations]


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    user_id: str,
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user)
):
    """Get all messages for a specific conversation."""
    if current_user.sub != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's conversations"
        )

    from sqlmodel import select

    # Verify conversation belongs to user
    conv_statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    conv_result = await db.execute(conv_statement)
    conversation = conv_result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or unauthorized"
        )

    # Query messages
    message_statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc())
    message_result = await db.execute(message_statement)
    messages = message_result.scalars().all()

    return [MessageResponse(
        id=msg.id,
        conversation_id=msg.conversation_id,
        user_id=msg.user_id,
        role=msg.role.value if hasattr(msg.role, 'value') else msg.role,
        content=msg.content,
        tool_calls=msg.tool_calls,
        created_at=msg.created_at
    ) for msg in messages]


@router.post("/audio/transcribe")
async def transcribe_audio(
    user_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user)
):
    """Transcribe uploaded audio file to text."""
    if current_user.sub != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's audio features"
        )

    try:
        audio_data = await file.read()
        transcription = await VoiceService.transcribe_audio(audio_data, user_id)
        return {"transcription": transcription}

    except Exception as e:
        logger.error(f"Error in audio transcription: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing audio: {str(e)}"
        )


@router.post("/audio/speak")
async def synthesize_speech(
    user_id: str,
    text: str,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(get_current_user)
):
    """Synthesize speech from text."""
    if current_user.sub != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's audio features"
        )

    try:
        audio_data = await VoiceService.synthesize_speech(text, user_id)
        
        from fastapi.responses import StreamingResponse
        import io
        
        return StreamingResponse(io.BytesIO(audio_data), media_type="audio/mpeg")

    except Exception as e:
        logger.error(f"Error in speech synthesis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error synthesizing speech: {str(e)}"
        )


@router.get("/__chat_ping")
async def chat_ping():
    """Sanity endpoint to verify chat routes are registered."""
    return {
        "ok": True, 
        "message": "Chat routes are working",
        "note": "For streaming, use /chat/stream endpoint"
    }


# NOTE: The /chat/stream endpoint is now in streaming_chat.py
# This prevents route conflicts and keeps streaming logic separate