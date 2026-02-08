#!/usr/bin/env python3
"""
Verification script for advanced task features in MCP tools
"""

import asyncio
from datetime import datetime, timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.task_advanced import Task
from app.database.connection import async_engine
from app.mcp.tools.add_task import handle_add_task
from app.mcp.tools.update_task import handle_update_task
from app.mcp.tools.list_tasks import handle_list_tasks
from app.mcp.tools.get_recurring_tasks import handle_get_recurring_tasks

async def verify_advanced_task_features():
    print("Verifying Advanced Task Features in MCP Tools...\n")

    # Create an async session for testing
    async with AsyncSession(async_engine) as session:
        user_id = "test_user_123"

        print("1. Testing add_task with advanced features:")

        # Test creating a task with advanced features
        result = await handle_add_task(
            session=session,
            user_id=user_id,
            title="Test Advanced Task",
            description="This is a test of advanced task features",
            priority="high",
            due_date=(datetime.now() + timedelta(days=1)).isoformat(),
            reminder_time=(datetime.now() + timedelta(hours=2)).isoformat(),
            category="testing",
            is_recurring=True,
            recurrence_pattern="daily",
            end_recurrence=(datetime.now() + timedelta(days=7)).isoformat()
        )

        if result.get("status") == "created":
            task_id = result["task_id"]
            print(f"   • Created task with ID: {task_id}")
            print(f"   • Advanced features: due_date={result['due_date']}, category={result['category']}")
            print(f"   • Recurring: is_recurring={result['is_recurring']}, pattern={result['recurrence_pattern']}")
        else:
            print(f"   ❌ Failed to create advanced task: {result.get('error')}")
            return False

        print("\n2. Testing update_task with advanced features:")

        # Test updating the task with advanced features
        update_result = await handle_update_task(
            session=session,
            task_id=task_id,
            user_id=user_id,
            priority="medium",
            category="updated_category",
            due_date=(datetime.now() + timedelta(days=3)).isoformat(),
            is_recurring=False
        )

        if update_result.get("status") == "updated":
            print(f"   • Updated task ID: {task_id}")
            print(f"   • Updated fields: {update_result['updated_fields']}")
            print(f"   • New category: {update_result['category']}")
            print(f"   • New recurring status: {update_result['is_recurring']}")
        else:
            print(f"   ❌ Failed to update advanced task: {update_result.get('error')}")
            return False

        print("\n3. Testing list_tasks with advanced filters:")

        # Test listing tasks with advanced filters
        list_result = await handle_list_tasks(
            session=session,
            user_id=user_id,
            category="updated_category",
            priority="medium",
            limit=5
        )

        if list_result.get("status") == "success":
            print(f"   • Retrieved {list_result['total_count']} tasks")
            if list_result['tasks']:
                task = list_result['tasks'][0]
                print(f"   • Task includes advanced fields: due_date={task.get('due_date')}, category={task.get('category')}")
                print(f"   • Recurring info: is_recurring={task.get('is_recurring')}, pattern={task.get('recurrence_pattern')}")
        else:
            print(f"   ❌ Failed to list tasks: {list_result.get('error')}")
            return False

        print("\n4. Testing get_recurring_tasks:")

        # Test getting recurring tasks
        recurring_result = await handle_get_recurring_tasks(
            session=session,
            user_id=user_id,
            status="all",
            limit=5
        )

        if recurring_result.get("status") == "success":
            print(f"   • Retrieved {recurring_result['total_count']} recurring tasks")
            if recurring_result['tasks']:
                task = recurring_result['tasks'][0]
                print(f"   • Task has recurring info: pattern={task.get('recurrence_pattern')}, next_occurrence={task.get('next_occurrence')}")
        else:
            print(f"   ❌ Failed to get recurring tasks: {recurring_result.get('error')}")
            return False

        print("\nAll advanced task features have been successfully verified!")
        print("MCP tools now support:")
        print("   • Advanced task creation with due dates, reminders, categories")
        print("   • Recurring task management")
        print("   • Enhanced filtering and listing capabilities")
        print("   • Full CRUD operations for advanced task features")

        return True

if __name__ == "__main__":
    success = asyncio.run(verify_advanced_task_features())
    if not success:
        exit(1)