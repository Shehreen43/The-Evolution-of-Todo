"""
Streaming chat route compatible with Vercel AI SDK.
Update your streaming_chat.py route file with this code.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import json
import traceback

from app.api.deps import get_current_user, verify_user_access
from app.database.connection import get_db
from app.schemas.api_contract import ChatRequest
from app.services.streaming_service import StreamingChatService

router = APIRouter(prefix="/api/{user_id}", tags=["streaming-chat"])


@router.post("/chat/stream",
             summary="Stream chat responses with Vercel AI SDK format",
             description="Stream chat responses in format compatible with Vercel AI SDK")
async def stream_chat(
    user_id: str,
    request: ChatRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Stream chat responses using Vercel AI SDK compatible format.
    
    Expected format:
    - Text chunks: 0:"content"\n
    - Completion: d:{"finishReason":"stop"}\n
    - Errors: 3:{"error":"message"}\n
    """
    try:
        await verify_user_access(user_id, current_user)
    except Exception as e:
        print(f"[ERROR] User verification failed: {str(e)}")
        raise HTTPException(status_code=403, detail=str(e))

    service = StreamingChatService(db)

    async def event_generator():
        try:
            chunk_count = 0
            async for event_str in service.stream_chat_response(user_id, request):
                chunk_count += 1
                yield event_str
            print(f"[SUCCESS] Streamed {chunk_count} chunks successfully")
        except Exception as e:
            print(f"[ERROR] Streaming error: {str(e)}")
            print(traceback.format_exc())
            # Send error in Vercel AI SDK format
            error_data = json.dumps({"error": str(e)})
            yield f'3:{error_data}\n'
            yield 'd:{"finishReason":"error"}\n'

    return StreamingResponse(
        event_generator(),
        media_type="text/plain; charset=utf-8",  # CRITICAL: Must be text/plain
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Content-Type-Options": "nosniff",
            "Access-Control-Allow-Origin": "*",
        }
    )


# Test endpoint to verify route registration
@router.get("/__streaming_chat_ping",
            summary="Test endpoint for route registration",
            description="Verify streaming chat routes are properly registered")
async def streaming_chat_ping():
    """Test endpoint to verify routes are registered."""
    return {
        "status": "ok",
        "endpoint": "/api/{user_id}/chat/stream",
        "routes": "registered",
        "format": "vercel_ai_sdk"
    }