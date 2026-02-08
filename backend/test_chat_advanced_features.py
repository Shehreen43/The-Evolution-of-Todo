#!/usr/bin/env python3
"""
Comprehensive test to verify chatbot works with advanced task features
"""

import asyncio
from datetime import datetime, timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.connection import async_engine
from app.services.streaming_service import StreamingChatService
from app.services.chat_service import ChatOrchestrationService
from app.schemas.api_contract import ChatRequest
from app.conversation_manager import create_conversation

async def test_chatbot_advanced_features():
    print("Testing Chatbot with Advanced Task Features...\n")

    # Create an async session for testing
    async with AsyncSession(async_engine) as session:
        user_id = "test_user_123"

        # Test 1: Create streaming chat service
        print("1. Testing Streaming Chat Service with Advanced Features:")
        streaming_service = StreamingChatService(session)

        # Test add_task with advanced features
        from app.schemas.api_contract import ToolCall
        add_task_call = ToolCall(
            id="test_add_1",
            name="add_task",
            arguments={
                "title": "Test Streaming Advanced Task",
                "description": "Test task with advanced features via streaming",
                "priority": "high",
                "due_date": (datetime.now() + timedelta(days=2)).isoformat(),
                "category": "streaming-test",
                "is_recurring": True,
                "recurrence_pattern": "weekly",
                "end_recurrence": (datetime.now() + timedelta(weeks=4)).isoformat()
            }
        )

        result = await streaming_service.execute_tool_call(add_task_call, user_id)
        if result.get("status") == "created":
            task_id_1 = result["task_id"]
            print(f"   - Successfully created task with advanced features: {task_id_1}")
            print(f"   - Advanced features - Priority: {result['priority']}, Category: {result['category']}")
            print(f"   - Recurring: {result['is_recurring']}, Pattern: {result['recurrence_pattern']}")
        else:
            print(f"   - Failed to create advanced task: {result.get('error')}")
            return False

        # Test update_task with advanced features
        update_task_call = ToolCall(
            id="test_update_1",
            name="update_task",
            arguments={
                "task_id": task_id_1,
                "priority": "medium",
                "category": "updated-streaming-test",
                "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
                "is_recurring": False
            }
        )

        update_result = await streaming_service.execute_tool_call(update_task_call, user_id)
        if update_result.get("status") == "updated":
            print(f"   - Successfully updated task with advanced features")
            print(f"   - Updated fields: {update_result['updated_fields']}")
        else:
            print(f"   - Failed to update advanced task: {update_result.get('error')}")
            return False

        # Test 2: Create orchestration chat service
        print("\n2. Testing Chat Orchestration Service with Advanced Features:")
        orchestration_service = ChatOrchestrationService(session)

        # Test list_tasks with advanced filters
        from types import SimpleNamespace
        list_task_call = SimpleNamespace(
            function=SimpleNamespace(
                name="list_tasks",
                arguments='{"category": "updated-streaming-test", "priority": "medium", "limit": 10}'
            )
        )

        list_result = await orchestration_service.execute_tool_call(list_task_call, user_id)
        if list_result.get("status") == "success":
            print(f"   - Successfully listed tasks with advanced filters, found {list_result['total_count']} tasks")
            if list_result['tasks']:
                task = list_result['tasks'][0]
                print(f"   - Task includes advanced fields: Category={task.get('category')}, Due Date={task.get('due_date')}")
        else:
            print(f"   - Failed to list tasks with filters: {list_result.get('error')}")
            return False

        # Test get_recurring_tasks
        recurring_task_call = SimpleNamespace(
            function=SimpleNamespace(
                name="get_recurring_tasks",
                arguments='{"status": "all", "limit": 10}'
            )
        )

        recurring_result = await orchestration_service.execute_tool_call(recurring_task_call, user_id)
        if recurring_result.get("status") == "success":
            print(f"   - Successfully retrieved recurring tasks, found {recurring_result['total_count']} tasks")
        else:
            print(f"   - Failed to retrieve recurring tasks: {recurring_result.get('error')}")
            return False

        # Test 3: Test conversation flow with advanced features
        print("\n3. Testing Complete Conversation Flow with Advanced Features:")

        # Create a conversation
        conversation = await create_conversation(session, user_id)
        conversation_id = conversation.id
        print(f"   - Created conversation: {conversation_id}")

        # Test the orchestration service with a complete flow
        user_message = "I need to create a high priority task called 'Complete project proposal' that is due tomorrow, categorized as 'work', and repeats weekly for a month."

        conv_id, response, tool_calls = await orchestration_service.process_conversation(
            user_id=user_id,
            user_message=user_message,
            conversation_id=conversation_id
        )

        print(f"   - Processed conversation with advanced request")
        print(f"   - Response: {response[:100]}...")  # First 100 chars
        print(f"   - Tool calls executed: {len(tool_calls)}")

        # Test 4: Verify all advanced features are properly integrated
        print("\n4. Verifying All Advanced Features Are Integrated:")

        # Direct tool call tests to ensure all advanced features work
        tools_to_test = [
            ("add_task", {
                "title": "Test All Advanced Features",
                "description": "Task with all advanced features",
                "priority": "high",
                "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
                "reminder_time": (datetime.now() + timedelta(hours=1)).isoformat(),
                "category": "comprehensive-test",
                "is_recurring": True,
                "recurrence_pattern": "daily",
                "end_recurrence": (datetime.now() + timedelta(days=7)).isoformat()
            }),
            ("list_tasks", {
                "category": "comprehensive-test",
                "priority": "high",
                "due_date_filter": "today",
                "limit": 5
            })
        ]

        for tool_name, args in tools_to_test:
            if tool_name == "add_task":
                tool_call = ToolCall(id=f"test_{tool_name}_2", name=tool_name, arguments=args)
                result = await streaming_service.execute_tool_call(tool_call, user_id)
            else:
                # For list_tasks, we need to create the mock object for orchestration service
                tool_call_ns = SimpleNamespace(
                    function=SimpleNamespace(
                        name=tool_name,
                        arguments=str(args).replace("'", '"')  # Convert to JSON-like string
                    )
                )
                result = await orchestration_service.execute_tool_call(tool_call_ns, user_id)

            if result.get("status") in ["created", "success", "updated"]:
                print(f"   - {tool_name} works with advanced features")
            else:
                print(f"   - {tool_name} failed: {result.get('error', 'Unknown error')}")
                return False

        print("\n- All tests passed! Chatbot works correctly with advanced task features.")
        print("\nAdvanced Features Supported:")
        print("  - Task creation with due dates, reminders, categories, and recurrence")
        print("  - Task updates with all advanced parameters")
        print("  - Advanced filtering (by category, priority, due date, etc.)")
        print("  - Recurring task management")
        print("  - Complete conversation flow with advanced requests")

        return True

if __name__ == "__main__":
    success = asyncio.run(test_chatbot_advanced_features())
    if not success:
        print("\n- Some tests failed.")
        exit(1)
    else:
        print("\n- All tests passed successfully!")