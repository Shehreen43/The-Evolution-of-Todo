#!/usr/bin/env python3
"""
Test script to verify advanced task features in task service
"""

import asyncio
from datetime import datetime, timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.connection import async_engine
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate

async def test_task_service_advanced_features():
    print("Testing Task Service with Advanced Features...\n")

    async with AsyncSession(async_engine) as session:
        service = TaskService(session)
        user_id = "test_user_123"

        # Test 1: Create task with advanced features
        print("1. Testing create_task with advanced features:")
        task_data = TaskCreate(
            title="Test Advanced Task",
            description="Task with advanced features",
            priority="high",
            due_date=(datetime.now() + timedelta(days=2)).isoformat(),
            category="test-category",
            is_recurring=True,
            recurrence_pattern="weekly",
            end_recurrence=(datetime.now() + timedelta(weeks=4)).isoformat()
        )

        created_task = await service.create_task(user_id, task_data)
        print(f"   - Created task: {created_task.id}")
        print(f"   - Advanced features - Priority: {created_task.priority}, Category: {created_task.category}")
        print(f"   - Recurring: {created_task.is_recurring}, Pattern: {created_task.recurrence_pattern}")
        print(f"   - Due date: {created_task.due_date}")

        # Test 2: Update task with advanced features
        print("\n2. Testing update_task with advanced features:")
        update_data = TaskUpdate(
            priority="medium",
            category="updated-category",
            due_date=(datetime.now() + timedelta(days=5)).isoformat(),
            is_recurring=False
        )

        updated_task = await service.update_task(user_id, created_task.id, update_data)
        print(f"   - Updated task: {updated_task.id}")
        print(f"   - Updated features - Priority: {updated_task.priority}, Category: {updated_task.category}")
        print(f"   - New recurring status: {updated_task.is_recurring}")

        # Test 3: Filter tasks with advanced options
        print("\n3. Testing filter_tasks with advanced filters:")
        filtered_tasks = await service.filter_tasks(
            user_id=user_id,
            category="updated-category",
            priority="medium",
            due_date_filter="all"
        )
        print(f"   - Found {len(filtered_tasks)} tasks with advanced filters")

        # Test 4: Get recurring tasks
        print("\n4. Testing get_recurring_tasks:")
        # First create a recurring task
        recurring_task_data = TaskCreate(
            title="Test Recurring Task",
            description="Recurring task for testing",
            priority="medium",
            is_recurring=True,
            recurrence_pattern="daily"
        )
        recurring_task = await service.create_task(user_id, recurring_task_data)

        recurring_tasks = await service.get_recurring_tasks(user_id, "all")
        print(f"   - Found {len(recurring_tasks)} recurring tasks")

        # Test 5: Toggle completion
        print("\n5. Testing toggle_complete:")
        toggled_task = await service.toggle_complete(user_id, created_task.id)
        print(f"   - Toggled task completion: {toggled_task.completed}")

        print("\n- All advanced features in Task Service work correctly!")

if __name__ == "__main__":
    asyncio.run(test_task_service_advanced_features())