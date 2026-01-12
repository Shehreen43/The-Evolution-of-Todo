import pytest
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings


def create_test_token():
    """Create a test JWT token for testing."""
    payload = {
        "sub": "test_user_123",
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, settings.better_auth_secret, algorithm=settings.algorithm)
    return token


def test_task_crud_operations(client):
    """Test all CRUD operations for tasks."""
    # Create a test token
    token = create_test_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Test 1: Create a task
    create_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "medium"
    }
    response = client.post("/api/test_user_123/tasks", json=create_data, headers=headers)

    assert response.status_code == 201
    task_data = response.json()
    task_id = task_data["id"]
    assert task_data["title"] == "Test Task"
    assert task_data["description"] == "This is a test task"
    assert task_data["priority"] == "medium"

    # Test 2: Get the created task
    response = client.get(f"/api/test_user_123/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == "Test Task"

    # Test 3: List all tasks
    response = client.get("/api/test_user_123/tasks", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 1
    assert any(task["id"] == task_id for task in tasks)

    # Test 4: Update the task
    update_data = {
        "title": "Updated Test Task",
        "description": "This is an updated test task",
        "priority": "high"
    }
    response = client.put(f"/api/test_user_123/tasks/{task_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == "Updated Test Task"
    assert updated_task["priority"] == "high"

    # Test 5: Toggle completion
    response = client.patch(f"/api/test_user_123/tasks/{task_id}/complete", headers=headers)
    assert response.status_code == 200
    toggled_task = response.json()
    assert toggled_task["completed"] != retrieved_task["completed"]

    # Test 6: Delete the task
    response = client.delete(f"/api/test_user_123/tasks/{task_id}", headers=headers)
    assert response.status_code == 204

    # Verify the task was deleted
    response = client.get(f"/api/test_user_123/tasks/{task_id}", headers=headers)
    assert response.status_code == 404


def test_user_isolation(client):
    """Test that users can only access their own tasks."""
    # Create a task for user 1
    token_user1 = create_test_token()  # This creates a token for "test_user_123"
    headers_user1 = {"Authorization": f"Bearer {token_user1}"}

    # Create a task for user 1
    create_data = {
        "title": "User 1 Task",
        "description": "This belongs to user 1",
        "priority": "medium"
    }
    response = client.post("/api/test_user_123/tasks", json=create_data, headers=headers_user1)
    assert response.status_code == 201
    task_data = response.json()
    task_id = task_data["id"]

    # Create a token for user 2 (different user ID)
    payload_user2 = {
        "sub": "test_user_456",  # Different user ID
        "email": "test2@example.com",
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token_user2 = jwt.encode(payload_user2, settings.better_auth_secret, algorithm=settings.algorithm)
    headers_user2 = {"Authorization": f"Bearer {token_user2}"}

    # Try to access user 1's task with user 2's token
    # This should fail with 403 (forbidden) or 404 (not found)
    response = client.get(f"/api/test_user_123/tasks/{task_id}", headers=headers_user2)
    # User isolation should prevent access - either 403 or 404 is acceptable
    assert response.status_code in [403, 404], "User isolation failed - user 2 accessed user 1's task"

    # Clean up: delete the task with the correct user
    response = client.delete(f"/api/test_user_123/tasks/{task_id}", headers=headers_user1)
    assert response.status_code == 204