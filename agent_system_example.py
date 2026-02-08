#!/usr/bin/env python3
"""
Agent System Example - Demonstrates the complete agent planning and execution workflow

This example shows how to use the agent system with planning, execution, and response synthesis.
"""

import asyncio
import json
from typing import List

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.agents.planner import AgentPlanner
from app.agents.executor import AgentExecutor
from app.schemas.api_contract import PlanRequest, PlanStep
from app.database.connection import DATABASE_URL


async def example_agent_workflow():
    """Example demonstrating the complete agent workflow."""

    print("=== Agent System Example ===")
    print()

    # Create async database session (in a real app, you'd use your configured database)
    # For this example, we'll show the conceptual workflow

    print("1. Creating agent planner and executor...")
    # Note: In a real application, you would have a proper database session
    # db_session = AsyncSession(...) # Your actual database session
    # planner = AgentPlanner(db_session)
    # executor = AgentExecutor(db_session)

    print("2. Sample user request:")
    sample_request = PlanRequest(
        message="I need to add a task to buy groceries, then list all my tasks, and finally update the priority of my first task to high",
        conversation_id=None
    )
    print(f"   Request: {sample_request.message}")
    print()

    print("3. Planning Phase:")
    print("   The agent planner will break down the request into discrete steps:")
    print("   - Step 1: Add a new task 'buy groceries'")
    print("   - Step 2: List all tasks")
    print("   - Step 3: Update the priority of the first task to high")
    print()

    print("4. Execution Phase:")
    print("   Each step will be executed in sequence:")
    print("   - Tool 'add_task' called with arguments: {title: 'buy groceries'}")
    print("   - Tool 'list_tasks' called with arguments: {}")
    print("   - Tool 'update_task' called with arguments: {task_id: 1, priority: 'high'}")
    print()

    print("5. Response Synthesis Phase:")
    print("   The agent combines results from all steps into a coherent response:")
    print("   - 'I've added the task 'buy groceries' to your list.'")
    print("   - 'Here are your current tasks: [list of tasks]'")
    print("   - 'I've updated the priority of your first task to high.'")
    print()

    print("6. Persistence:")
    print("   - Each tool call is logged in the conversation history")
    print("   - The plan and execution results are stored in the database")
    print("   - The final response is saved as an assistant message")
    print()

    print("7. Streaming Example:")
    print("   The agent can stream the process with Server-Sent Events:")
    print("   - Event: {type: 'plan_step', data: {plan: [...], message: 'Plan generated'}}")
    print("   - Event: {type: 'plan_step', data: {step: {...}, message: 'Executing step'}}")
    print("   - Event: {type: 'tool_call', data: {tool_name: 'add_task', result: {...}}}")
    print("   - Event: {type: 'done', data: {final_response: '...', successful_steps: 3}}")
    print()

    print("8. MCP Tool Integration:")
    print("   The agent seamlessly integrates with MCP tools for CRUD operations:")
    print("   - add_task: Creates new tasks in the database")
    print("   - list_tasks: Retrieves tasks with filtering options")
    print("   - update_task: Modifies existing task properties")
    print("   - delete_task: Removes tasks from the database")
    print("   - complete_task: Toggles task completion status")
    print()

    print("=== Agent System Features ===")
    print("- Structured planning with JSON-formatted steps")
    print("- Sequential execution with error handling")
    print("- Real-time streaming of progress")
    print("- Complete conversation history tracking")
    print("- MCP tool integration for task management")
    print("- Persistent storage of plans and results")
    print("- Flexible response synthesis")
    print()

    print("The agent system enables complex multi-step operations while maintaining")
    print("full transparency of the process and complete audit trails.")


async def example_direct_usage():
    """Example showing direct usage of the agent classes."""

    print("\n=== Direct Usage Example ===")

    # This is pseudocode showing how you would use the system in practice
    print("""
# In a FastAPI route:
async def plan_and_execute(user_id: str, request: PlanRequest):
    # Get database session from dependency
    db: AsyncSession = ...

    # Create planner and execute the full workflow
    planner = AgentPlanner(db)

    # Option 1: Execute with streaming
    async def stream_response():
        async for event in planner.stream_plan_execution(user_id, request):
            yield event

    return StreamingResponse(stream_response(), media_type="text/event-stream")

    # Option 2: Execute and return final result
    # result = await planner.execute_plan_with_streaming(user_id, request)
    # return {"response": result}
    """)


if __name__ == "__main__":
    asyncio.run(example_agent_workflow())
    asyncio.run(example_direct_usage())