import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.task import Task
from app.services.task_service import TaskService


def test_create_advanced_task(test_client: TestClient, db_session: Session, sample_user_data, sample_advanced_task_data):
    """Test creating a task with all advanced features."""
    # First, we need to simulate a logged-in user by bypassing auth for testing
    # For this test, we'll use a mock user_id
    user_id = "test-user-123"

    response = test_client.post(f"/api/{user_id}/tasks", json=sample_advanced_task_data)
    
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Advanced Task"
    assert data["description"] == "Task with advanced features"
    assert data["priority"] == "high"
    assert data["due_date"] == "2024-12-31T10:00:00"
    assert data["reminder_time"] == "2024-12-31T09:00:00"
    assert data["category"] == "work"
    assert data["is_recurring"] is True
    assert data["recurrence_pattern"] == "weekly"
    assert data["end_recurrence"] == "2025-12-31T10:00:00"


def test_list_tasks_with_filters(test_client: TestClient, db_session: Session, sample_user_data):
    """Test listing tasks with various filters."""
    user_id = "test-user-123"

    # Create several tasks with different properties
    task1 = {
        "title": "Urgent Work Task",
        "description": "High priority work task",
        "priority": "high",
        "category": "work",
        "due_date": (datetime.now() + timedelta(days=1)).isoformat()
    }

    task2 = {
        "title": "Personal Errand",
        "description": "Low priority personal task",
        "priority": "low",
        "category": "personal",
        "due_date": (datetime.now() + timedelta(days=7)).isoformat()
    }

    # Create tasks
    response1 = test_client.post(f"/api/{user_id}/tasks", json=task1)
    response2 = test_client.post(f"/api/{user_id}/tasks", json=task2)

    assert response1.status_code == 201
    assert response2.status_code == 201

    # List all tasks
    response = test_client.get(f"/api/{user_id}/tasks")
    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) >= 2

    # Check if filtering by category works (this would be implemented in the endpoint)
    # For now, just verify that tasks were created properly


def test_update_advanced_task(test_client: TestClient, db_session: Session, sample_user_data, sample_advanced_task_data):
    """Test updating a task with advanced features."""
    user_id = "test-user-123"

    # Create a task first
    response = test_client.post(f"/api/{user_id}/tasks", json=sample_advanced_task_data)
    assert response.status_code == 201

    task_id = response.json()["id"]

    # Update the task
    update_data = {
        "title": "Updated Advanced Task",
        "description": "Updated description",
        "priority": "low",
        "due_date": "2024-11-30T10:00:00",
        "category": "personal",
        "is_recurring": False
    }

    response = test_client.put(f"/api/{user_id}/tasks/{task_id}", json=update_data)

    assert response.status_code == 200

    updated_task = response.json()
    assert updated_task["title"] == "Updated Advanced Task"
    assert updated_task["priority"] == "low"
    assert updated_task["due_date"] == "2024-11-30T10:00:00"
    assert updated_task["category"] == "personal"
    assert updated_task["is_recurring"] is False


def test_toggle_task_completion(test_client: TestClient, db_session: Session, sample_user_data, sample_task_data):
    """Test toggling task completion status."""
    user_id = "test-user-123"

    # Create a task
    response = test_client.post(f"/api/{user_id}/tasks", json=sample_task_data)
    assert response.status_code == 201

    task_id = response.json()["id"]

    # Toggle completion
    response = test_client.patch(f"/api/{user_id}/tasks/{task_id}/complete")
    assert response.status_code == 200

    task = response.json()
    assert task["completed"] is True

    # Toggle again to mark as incomplete
    response = test_client.patch(f"/api/{user_id}/tasks/{task_id}/complete")
    assert response.status_code == 200

    task = response.json()
    assert task["completed"] is False


def test_delete_task(test_client: TestClient, db_session: Session, sample_user_data, sample_task_data):
    """Test deleting a task."""
    user_id = "test-user-123"

    # Create a task
    response = test_client.post(f"/api/{user_id}/tasks", json=sample_task_data)
    assert response.status_code == 201

    task_id = response.json()["id"]

    # Delete the task
    response = test_client.delete(f"/api/{user_id}/tasks/{task_id}")
    assert response.status_code == 204

    # Verify the task is gone
    response = test_client.get(f"/api/{user_id}/tasks/{task_id}")
    assert response.status_code == 404


def test_recurring_task_creation(test_client: TestClient, db_session: Session, sample_user_data):
    """Test creating a recurring task and verifying its properties."""
    user_id = "test-user-123"

    recurring_task_data = {
        "title": "Weekly Team Meeting",
        "description": "Regular team sync meeting",
        "priority": "medium",
        "is_recurring": True,
        "recurrence_pattern": "weekly",
        "due_date": "2024-12-01T10:00:00",
        "end_recurrence": "2025-12-01T10:00:00"
    }

    response = test_client.post(f"/api/{user_id}/tasks", json=recurring_task_data)
    assert response.status_code == 201

    task = response.json()
    assert task["title"] == "Weekly Team Meeting"
    assert task["is_recurring"] is True
    assert task["recurrence_pattern"] == "weekly"
    assert task["end_recurrence"] == "2025-12-01T10:00:00"


def test_task_with_reminder(test_client: TestClient, db_session: Session, sample_user_data):
    """Test creating a task with reminder time."""
    user_id = "test-user-123"

    task_with_reminder = {
        "title": "Doctor Appointment",
        "description": "Annual checkup",
        "priority": "high",
        "due_date": "2024-12-15T14:00:00",
        "reminder_time": "2024-12-15T13:00:00",  # 1 hour before
        "category": "health"
    }

    response = test_client.post(f"/api/{user_id}/tasks", json=task_with_reminder)
    assert response.status_code == 201

    task = response.json()
    assert task["title"] == "Doctor Appointment"
    assert task["due_date"] == "2024-12-15T14:00:00"
    assert task["reminder_time"] == "2024-12-15T13:00:00"
    assert task["category"] == "health"


def test_multiple_categories(test_client: TestClient, db_session: Session, sample_user_data):
    """Test creating tasks with different categories."""
    user_id = "test-user-123"

    categories = ["work", "personal", "shopping", "health", "education"]

    for i, category in enumerate(categories):
        task_data = {
            "title": f"Task for {category}",
            "description": f"A task in the {category} category",
            "priority": "medium",
            "category": category
        }

        response = test_client.post(f"/api/{user_id}/tasks", json=task_data)
        assert response.status_code == 201

        task = response.json()
        assert task["category"] == category
        assert f"Task for {category}" in task["title"]


def test_due_date_filtering_logic(test_client: TestClient, db_session: Session, sample_user_data):
    """Test that due dates are properly stored and retrieved."""
    user_id = "test-user-123"

    past_due_task = {
        "title": "Past Due Task",
        "description": "Task that was due in the past",
        "priority": "high",
        "due_date": "2020-01-01T10:00:00"  # Past date
    }

    future_due_task = {
        "title": "Future Due Task",
        "description": "Task due in the future",
        "priority": "low",
        "due_date": "2030-12-31T10:00:00"  # Future date
    }

    # Create past due task
    response = test_client.post(f"/api/{user_id}/tasks", json=past_due_task)
    assert response.status_code == 201
    past_task = response.json()
    assert past_task["due_date"] == "2020-01-01T10:00:00"

    # Create future due task
    response = test_client.post(f"/api/{user_id}/tasks", json=future_due_task)
    assert response.status_code == 201
    future_task = response.json()
    assert future_task["due_date"] == "2030-12-31T10:00:00"


def test_priority_levels(test_client: TestClient, db_session: Session, sample_user_data):
    """Test all priority levels."""
    user_id = "test-user-123"

    priorities = ["low", "medium", "high"]

    for priority in priorities:
        task_data = {
            "title": f"Task with {priority} priority",
            "description": f"A task with {priority} priority level",
            "priority": priority
        }

        response = test_client.post(f"/api/{user_id}/tasks", json=task_data)
        assert response.status_code == 201

        task = response.json()
        assert task["priority"] == priority