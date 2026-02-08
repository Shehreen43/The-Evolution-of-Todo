"""
Agent planner for generating structured plans from user input.
"""
import json
import logging
from typing import List, AsyncGenerator
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.api_contract import PlanStep, PlanRequest, StreamingEvent, StreamingEventType
from app.config import settings
from app.services.chat_service import get_openai_client
from app.models.message import Message, MessageRole


logger = logging.getLogger(__name__)


class AgentPlanner:
    """Class to generate structured plans for agent execution."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_plan(self, user_id: str, request: PlanRequest) -> List[PlanStep]:
        """
        Generate a structured plan based on user input.

        Args:
            user_id: User identifier
            request: Plan request containing the user message

        Returns:
            List of PlanStep objects representing the execution plan
        """
        user_message = request.message
        conversation_id = request.conversation_id

        # Prepare system message for planning
        system_message = {
            "role": "system",
            "content": """
You are a task planning assistant. Your job is to break down user requests into discrete, executable steps.
For each step, determine:
1. The action to take (e.g., 'add_task', 'list_tasks', 'update_task', etc.)
2. The arguments needed for the action
3. A description of what the step accomplishes

Respond in the following JSON format:
{
  "steps": [
    {
      "id": 1,
      "description": "What this step does",
      "tool_name": "the tool to use (or null if no tool needed)",
      "arguments": {"arg1": "value1", ...} (or null if no arguments)
    }
  ]
}
"""
        }

        # Prepare messages for the AI
        messages = [system_message]

        # Add conversation history if provided
        if conversation_id:
            from app.conversation_manager import get_conversation_history
            history = await get_conversation_history(self.db, conversation_id)
            for msg in history:
                messages.append({
                    "role": msg.role.value if hasattr(msg.role, 'value') else msg.role,
                    "content": msg.content
                })

        # Add the current user message
        messages.append({"role": "user", "content": user_message})

        try:
            # Get OpenAI client
            client = get_openai_client()

            # Call the AI to generate a plan
            response = await client.chat.completions.create(
                model=settings.default_model,
                messages=messages,
                response_format={"type": "json_object"},  # Force JSON response
                max_tokens=1000,
            )

            # Parse the plan from the response
            plan_content = response.choices[0].message.content
            plan_data = json.loads(plan_content)

            # Convert to PlanStep objects
            steps_data = plan_data.get("steps", [])
            plan_steps = []

            for idx, step_data in enumerate(steps_data):
                step = PlanStep(
                    id=step_data.get("id", idx + 1),
                    description=step_data.get("description", ""),
                    tool_name=step_data.get("tool_name"),
                    arguments=step_data.get("arguments"),
                    status="pending"
                )
                plan_steps.append(step)

            # If we have a conversation ID, save the plan as a message
            if conversation_id:
                plan_message = Message(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role=MessageRole.SYSTEM,
                    content=f"Planning: {json.dumps([step.model_dump() for step in plan_steps])}"
                )
                self.db.add(plan_message)
                await self.db.commit()

            return plan_steps

        except Exception as e:
            logger.error(f"Error generating plan: {str(e)}")
            raise

    async def execute_plan_with_streaming(
        self,
        user_id: str,
        request: PlanRequest
    ) -> str:
        """
        Execute a plan with streaming responses.

        Args:
            user_id: User identifier
            request: Plan request containing the user message

        Returns:
            Final response string
        """
        from .executor import AgentExecutor
        executor = AgentExecutor(self.db)

        # Generate the plan
        plan = await self.generate_plan(user_id, request)

        # Execute the plan with conversation ID for logging
        response = await executor.execute_plan(user_id, plan, request.conversation_id)

        # If we have a conversation ID, save the final response
        if request.conversation_id:
            assistant_message = Message(
                conversation_id=request.conversation_id,
                user_id=user_id,
                role=MessageRole.ASSISTANT,
                content=response
            )
            self.db.add(assistant_message)
            await self.db.commit()

        return response

    async def stream_plan_execution(
        self,
        user_id: str,
        request: PlanRequest
    ) -> AsyncGenerator[str, None]:
        """
        Stream the plan generation and execution process with Server-Sent Events.

        Args:
            user_id: User identifier
            request: Plan request containing the user message

        Yields:
            JSON-encoded SSE events for plan and execution updates
        """
        from .executor import AgentExecutor
        executor = AgentExecutor(self.db)

        # Generate the plan and stream it
        user_message = request.message
        conversation_id = request.conversation_id

        # Prepare system message for planning
        system_message = {
            "role": "system",
            "content": """
You are a task planning assistant. Your job is to break down user requests into discrete, executable steps.
For each step, determine:
1. The action to take (e.g., 'add_task', 'list_tasks', 'update_task', etc.)
2. The arguments needed for the action
3. A description of what the step accomplishes

Respond in the following JSON format:
{
  "steps": [
    {
      "id": 1,
      "description": "What this step does",
      "tool_name": "the tool to use (or null if no tool needed)",
      "arguments": {"arg1": "value1", ...} (or null if no arguments)
    }
  ]
}
"""
        }

        # Prepare messages for the AI
        messages = [system_message]

        # Add conversation history if provided
        if conversation_id:
            from app.conversation_manager import get_conversation_history
            history = await get_conversation_history(self.db, conversation_id)
            for msg in history:
                messages.append({
                    "role": msg.role.value if hasattr(msg.role, 'value') else msg.role,
                    "content": msg.content
                })

        # Add the current user message
        messages.append({"role": "user", "content": user_message})

        try:
            # Get OpenAI client
            client = get_openai_client()

            # Call the AI to generate a plan
            response = await client.chat.completions.create(
                model=settings.default_model,
                messages=messages,
                response_format={"type": "json_object"},  # Force JSON response
                max_tokens=1000,
            )

            # Parse the plan from the response
            plan_content = response.choices[0].message.content
            plan_data = json.loads(plan_content)

            # Convert to PlanStep objects
            steps_data = plan_data.get("steps", [])
            plan_steps = []

            for idx, step_data in enumerate(steps_data):
                step = PlanStep(
                    id=step_data.get("id", idx + 1),
                    description=step_data.get("description", ""),
                    tool_name=step_data.get("tool_name"),
                    arguments=step_data.get("arguments"),
                    status="pending"
                )
                plan_steps.append(step)

            # Stream the plan
            plan_event = StreamingEvent(
                type=StreamingEventType.PLAN_STEP,
                data={
                    "plan": [step.model_dump() for step in plan_steps],
                    "message": "Plan generated successfully"
                }
            )
            yield f"data: {plan_event.model_dump_json()}\n\n"

            # If we have a conversation ID, save the plan as a message
            if conversation_id:
                plan_message = Message(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role=MessageRole.SYSTEM,
                    content=f"Planning: {json.dumps([step.model_dump() for step in plan_steps])}"
                )
                self.db.add(plan_message)
                await self.db.commit()

            # Now execute the plan with streaming
            # We'll need to create a custom streaming execution method in the executor
            results = []

            for step in plan_steps:
                try:
                    # Update step status to executing and stream it
                    step.status = "executing"

                    step_event = StreamingEvent(
                        type=StreamingEventType.PLAN_STEP,
                        data={
                            "step": step.model_dump(),
                            "message": f"Executing step: {step.description}"
                        }
                    )
                    yield f"data: {step_event.model_dump_json()}\n\n"

                    # Execute the step based on its tool_name
                    if step.tool_name:
                        # Execute tool step and stream the result
                        tool_result = await executor.execute_tool_step(user_id, step, conversation_id)

                        tool_event = StreamingEvent(
                            type=StreamingEventType.TOOL_CALL,
                            data={
                                "step_id": step.id,
                                "tool_name": step.tool_name,
                                "arguments": step.arguments,
                                "result": tool_result,
                                "description": step.description
                            }
                        )
                        yield f"data: {tool_event.model_dump_json()}\n\n"

                        results.append({
                            "step_id": step.id,
                            "description": step.description,
                            "tool_name": step.tool_name,
                            "arguments": step.arguments,
                            "result": tool_result
                        })
                    else:
                        # For steps without tools, just record the description
                        results.append({
                            "step_id": step.id,
                            "description": step.description,
                            "result": step.description
                        })

                    # Mark step as completed and stream completion
                    step.status = "completed"

                    completion_event = StreamingEvent(
                        type=StreamingEventType.PLAN_STEP,
                        data={
                            "step": step.model_dump(),
                            "message": f"Completed step: {step.description}"
                        }
                    )
                    yield f"data: {completion_event.model_dump_json()}\n\n"

                except Exception as e:
                    logger.error(f"Error executing step {step.id}: {str(e)}")
                    step.status = "failed"

                    error_event = StreamingEvent(
                        type=StreamingEventType.ERROR,
                        data={
                            "step_id": step.id,
                            "error": str(e),
                            "description": step.description
                        }
                    )
                    yield f"data: {error_event.model_dump_json()}\n\n"

                    results.append({
                        "step_id": step.id,
                        "description": step.description,
                        "error": str(e)
                    })

            # Generate final response and stream it
            final_response = executor.generate_final_response(results)

            # If we have a conversation ID, save the final response
            if conversation_id:
                assistant_message = Message(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role=MessageRole.ASSISTANT,
                    content=final_response
                )
                self.db.add(assistant_message)
                await self.db.commit()

            # Send done event
            done_event = StreamingEvent(
                type=StreamingEventType.DONE,
                data={
                    "conversation_id": conversation_id,
                    "final_response": final_response,
                    "total_steps": len(plan_steps),
                    "successful_steps": len([r for r in results if "error" not in r])
                }
            )
            yield f"data: {done_event.model_dump_json()}\n\n"

        except Exception as e:
            logger.error(f"Error in plan streaming: {str(e)}")
            error_event = StreamingEvent(
                type=StreamingEventType.ERROR,
                data={"error": str(e)}
            )
            yield f"data: {error_event.model_dump_json()}\n\n"
            raise