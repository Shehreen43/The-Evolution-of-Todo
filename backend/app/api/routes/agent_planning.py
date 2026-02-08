"""
Agent Planning API routes for the AI Chatbot integration.
This module implements authenticated agent planning endpoints.
"""
from typing import AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, verify_user_access
from app.database.connection import get_db
from app.schemas.api_contract import (
    PlanRequest, PlanResponse,
    StreamingEvent, StreamingEventType
)
from app.agents.planner import AgentPlanner

router = APIRouter(prefix="/api/{user_id}", tags=["agent-planning"])


@router.post("/chat/planning",
             response_model=PlanResponse,
             summary="Generate execution plan for complex requests",
             description="Generate a structured plan for complex multi-step requests")
async def plan_request(
    user_id: str,
    request: PlanRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a structured execution plan for complex multi-step requests.

    This endpoint analyzes the user request and breaks it down into discrete,
    executable steps that can be executed by the agent system.
    """
    await verify_user_access(user_id, current_user)

    planner = AgentPlanner(db)

    # Generate the plan
    plan_steps = await planner.generate_plan(user_id, request)

    # If plan_only is True, return just the plan without executing
    if request.plan_only:
        return PlanResponse(
            conversation_id=request.conversation_id or 0,
            plan=plan_steps
        )

    # Otherwise, execute the plan and return the response
    response = await planner.execute_plan_with_streaming(user_id, request)

    return PlanResponse(
        conversation_id=request.conversation_id or 0,
        plan=plan_steps,
        response=response
    )


@router.post("/chat/planning/stream",
             summary="Stream plan generation and execution",
             description="Stream the plan generation and execution process with Server-Sent Events")
async def stream_plan_execution(
    user_id: str,
    request: PlanRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Stream the plan generation and execution process with Server-Sent Events.

    This endpoint streams both the planning phase and execution phase,
    allowing clients to see real-time progress of complex multi-step operations.
    """
    await verify_user_access(user_id, current_user)

    planner = AgentPlanner(db)

    async def event_generator():
        try:
            async for event_str in planner.stream_plan_execution(user_id, request):
                yield event_str
        except Exception as e:
            # Send error event if something goes wrong
            error_event = StreamingEvent(
                type=StreamingEventType.ERROR,
                data={"error": str(e)}
            )
            yield f"data: {error_event.model_dump_json()}\n\n"
            # Do NOT re-raise - terminate generator cleanly

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )


# Test endpoint to verify route registration
@router.get("/__agent_planning_ping",
            summary="Test endpoint for route registration",
            description="Simple endpoint to verify that agent planning routes are properly registered")
async def agent_planning_ping():
    """
    Test endpoint to verify that agent planning routes are properly registered.
    This helps confirm that the router is correctly included in the main app.
    """
    return {"status": "ok", "endpoint": "/api/{user_id}/chat/planning", "routes": "registered"}