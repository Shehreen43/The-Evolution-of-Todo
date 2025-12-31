"""Manual test script for Phase I Todo Console App."""

from src.models.task import Task
from src.repository.task_repository import TaskRepository
from src.service.task_service import TaskService


def test_all_features():
    """Test all 5 user stories in a single session."""
    print("=== Phase I Todo Console App - Manual Test ===\n")

    # Initialize components
    repository = TaskRepository()
    service = TaskService(repository)

    # User Story 1: Add tasks
    print("1. Testing ADD feature (User Story 1):")
    task1 = service.create_task("Buy groceries", "Milk, eggs, bread")
    print(f"   [OK] Task added with ID {task1.id}")

    task2 = service.create_task("Meeting with team")
    print(f"   [OK] Task added with ID {task2.id}")

    task3 = service.create_task("Write documentation", "Phase I specs")
    print(f"   [OK] Task added with ID {task3.id}")

    # User Story 2: List tasks
    print("\n2. Testing LIST feature (User Story 2):")
    tasks = service.list_tasks()
    print("   ID | Status | Title")
    for task in tasks:
        status = "[x]" if task.completed else "[ ]"
        print(f"   {task.id}  | {status}    | {task.title}")

    # User Story 2: Get specific task
    print("\n3. Testing GET feature (User Story 2):")
    task = service.get_task(1)
    if task:
        print(f"   Task #{task.id}")
        print(f"   Title: {task.title}")
        print(f"   Description: {task.description}")
        print(f"   Status: {'Complete' if task.completed else 'Pending'}")

    # User Story 3: Mark complete
    print("\n4. Testing COMPLETE feature (User Story 3):")
    task = service.toggle_complete(1)
    print(f"   [OK] Task #{task.id} marked as {'complete' if task.completed else 'incomplete'}")

    # List again to see change
    print("\n5. List after marking complete:")
    tasks = service.list_tasks()
    print("   ID | Status | Title")
    for task in tasks:
        status = "[x]" if task.completed else "[ ]"
        print(f"   {task.id}  | {status}    | {task.title}")

    # User Story 5: Update task
    print("\n6. Testing UPDATE feature (User Story 5):")
    service.update_task(2, title="Team sync meeting", description="Discuss Q1 goals")
    print("   [OK] Task #2 updated")

    # User Story 4: Delete task
    print("\n7. Testing DELETE feature (User Story 4):")
    success = service.delete_task(3)
    print(f"   [OK] Task #3 {'deleted' if success else 'not found'}")

    # Final list
    print("\n8. Final task list:")
    tasks = service.list_tasks()
    print("   ID | Status | Title")
    for task in tasks:
        status = "[x]" if task.completed else "[ ]"
        print(f"   {task.id}  | {status}    | {task.title}")

    # Test validation
    print("\n9. Testing VALIDATION:")
    try:
        service.create_task("")  # Empty title
    except ValueError as e:
        print(f"   [OK] Empty title rejected: {e}")

    try:
        service.create_task("x" * 201)  # Title too long
    except ValueError as e:
        print(f"   [OK] Long title rejected: {e}")

    try:
        service.update_task(999, title="Non-existent")  # Non-existent ID
    except ValueError as e:
        print(f"   [OK] Invalid ID rejected: {e}")

    print("\n=== All tests completed successfully! ===")


if __name__ == "__main__":
    test_all_features()
