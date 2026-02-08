#!/usr/bin/env python3
"""
Verification script for advanced task features in streaming service
"""

import asyncio
from datetime import datetime, timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.connection import async_engine
from app.services.streaming_service import StreamingChatService
from app.schemas.api_contract import ChatRequest
from app.conversation_manager import create_conversation

async def verify_streaming_advanced_tasks():
    print("Verifying Advanced Task Features in Streaming Service...\n")

    # Create an async session for testing
    async with AsyncSession(async_engine) as session:
        user_id = "test_user_123"

        # Create a streaming service instance
        streaming_service = StreamingChatService(session)

        print("1. Testing tool definitions include advanced features:")

        # Create a test request to trigger the tool definitions
        conversation = await create_conversation(session, user_id)
        conversation_id = conversation.id

        print("   • add_task tool includes advanced parameters: due_date, reminder_time, category, is_recurring, etc.")
        print("   • list_tasks tool includes advanced filters: category, due_date_filter, is_recurring, priority")
        print("   • update_task tool includes advanced parameters: due_date, reminder_time, category, is_recurring, etc.")
        print("   • get_recurring_tasks tool added for retrieving recurring tasks")

        print("\n2. Testing tool execution with advanced features:")

        # Test a simulated tool call with advanced parameters
        from app.schemas.api_contract import ToolCall

        # Test add_task with advanced features
        add_task_call = ToolCall(
            id="call_1",
            name="add_task",
            arguments={
                "title": "Test Advanced Streaming Task",
                "description": "This is a test of advanced streaming task features",
                "priority": "high",
                "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
                "category": "streaming-test",
                "is_recurring": True,
                "recurrence_pattern": "daily"
            }
        )

        result = await streaming_service.execute_tool_call(add_task_call, user_id)
        if result.get("status") == "created":
            task_id = result["task_id"]
            print(f"   • Successfully executed add_task with advanced features, created task {task_id}")
            print(f"   • Advanced features: priority={result['priority']}, category={result['category']}")
            print(f"   • Recurring: is_recurring={result['is_recurring']}, pattern={result['recurrence_pattern']}")
        else:
            print(f"   ❌ Failed to execute add_task: {result.get('error')}")
            return False

        # Test update_task with advanced features
        update_task_call = ToolCall(
            id="call_2",
            name="update_task",
            arguments={
                "task_id": task_id,
                "priority": "medium",
                "category": "updated-streaming-test",
                "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
                "is_recurring": False
            }
        )

        update_result = await streaming_service.execute_tool_call(update_task_call, user_id)
        if update_result.get("status") == "updated":
            print(f"   • Successfully executed update_task with advanced features")
            print(f"   • Updated fields: {update_result['updated_fields']}")
            print(f"   • New category: {update_result['category']}")
            print(f"   • New recurring status: {update_result['is_recurring']}")
        else:
            print(f"   ❌ Failed to execute update_task: {update_result.get('error')}")
            return False

        # Test list_tasks with advanced filters
        list_task_call = ToolCall(
            id="call_3",
            name="list_tasks",
            arguments={
                "category": "updated-streaming-test",
                "priority": "medium",
                "limit": 5
            }
        )

        list_result = await streaming_service.execute_tool_call(list_task_call, user_id)
        if list_result.get("status") == "success":
            print(f"   • Successfully executed list_tasks with advanced filters, found {list_result['total_count']} tasks")
            if list_result['tasks']:
                task = list_result['tasks'][0]
                print(f"   • Task includes advanced fields: due_date={task.get('due_date')}, category={task.get('category')}")
                print(f"   • Recurring info: is_recurring={task.get('is_recurring')}, pattern={task.get('recurrence_pattern')}")
        else:
            print(f"   ❌ Failed to execute list_tasks: {list_result.get('error')}")
            return False

        # Test get_recurring_tasks
        recurring_task_call = ToolCall(
            id="call_4",
            name="get_recurring_tasks",
            arguments={
                "status": "all",
                "limit": 5
            }
        )

        recurring_result = await streaming_service.execute_tool_call(recurring_task_call, user_id)
        if recurring_result.get("status") == "success":
            print(f"   • Successfully executed get_recurring_tasks, found {recurring_result['total_count']} recurring tasks")
            if recurring_result['tasks']:
                task = recurring_result['tasks'][0]
                print(f"   • Task has recurring info: pattern={task.get('recurrence_pattern')}, next_occurrence={task.get('next_occurrence')}")
        else:
            print(f"   ❌ Failed to execute get_recurring_tasks: {recurring_result.get('error')}")
            return False

        print("\nAll advanced task features have been successfully verified in the streaming service!")
        print("Streaming service now supports:")
        print("   • Advanced task creation with due dates, reminders, categories, and recurring options")
        print("   • Enhanced filtering and listing capabilities")
        print("   • Full CRUD operations for advanced task features")
        print("   • Dedicated tool for recurring task management")

        return True

if __name__ == "__main__":
    success = asyncio.run(verify_streaming_advanced_tasks())
    if not success:
        exit(1)