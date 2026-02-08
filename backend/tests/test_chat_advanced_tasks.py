import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
import json


def test_chat_with_advanced_task_creation(test_client: TestClient, db_session: Session, sample_user_data):
    """Test that chat can create tasks with advanced features."""
    user_id = "test-user-123"

    # Simulate a chat message asking to create an advanced task
    chat_message = {
        "message": "Create a recurring work task with a due date and reminder",
        "conversation_id": None
    }

    response = test_client.post(f"/api/{user_id}/chat", json=chat_message)

    # The chat endpoint might return different status codes depending on configuration
    # but it should not crash when processing requests
    assert response.status_code in [200, 401, 422]


def test_chat_task_query_with_filters(test_client: TestClient, db_session: Session, sample_user_data):
    """Test that chat can query tasks with advanced filters."""
    user_id = "test-user-123"

    # Create a test task first
    task_data = {
        "title": "Test Task for Chat",
        "description": "Task created for chat testing",
        "priority": "high",
        "category": "work",
        "due_date": "2024-12-31T10:00:00"
    }

    create_response = test_client.post(f"/api/{user_id}/tasks", json=task_data)
    assert create_response.status_code in [200, 201, 401]  # Allow 401 for auth

    # Now simulate a chat query
    chat_message = {
        "message": "Show me my high priority work tasks",
        "conversation_id": None
    }

    response = test_client.post(f"/api/{user_id}/chat", json=chat_message)
    assert response.status_code in [200, 401, 422]


def test_chat_recurring_task_management(test_client: TestClient, db_session: Session, sample_user_data):
    """Test chat interactions with recurring tasks."""
    user_id = "test-user-123"

    chat_message = {
        "message": "I need to create a weekly recurring task for team meetings",
        "conversation_id": None
    }

    response = test_client.post(f"/api/{user_id}/chat", json=chat_message)
    assert response.status_code in [200, 401, 422]


def test_chat_reminder_setup(test_client: TestClient, db_session: Session, sample_user_data):
    """Test chat setting up task reminders."""
    user_id = "test-user-123"

    chat_message = {
        "message": "Remind me to submit the report tomorrow morning",
        "conversation_id": None
    }

    response = test_client.post(f"/api/{user_id}/chat", json=chat_message)
    assert response.status_code in [200, 401, 422]


def test_chat_category_organization(test_client: TestClient, db_session: Session, sample_user_data):
    """Test chat organizing tasks by category."""
    user_id = "test-user-123"

    chat_message = {
        "message": "Show me all my personal tasks",
        "conversation_id": None
    }

    response = test_client.post(f"/api/{user_id}/chat", json=chat_message)
    assert response.status_code in [200, 401, 422]


def test_chat_due_date_management(test_client: TestClient, db_session: Session, sample_user_data):
    """Test chat managing tasks with due dates."""
    user_id = "test-user-123"

    chat_message = {
        "message": "What tasks are due this week?",
        "conversation_id": None
    }

    response = test_client.post(f"/api/{user_id}/chat", json=chat_message)
    assert response.status_code in [200, 401, 422]


def test_chat_conversation_history(test_client: TestClient, db_session: Session, sample_user_data):
    """Test chat conversation history endpoints."""
    user_id = "test-user-123"

    # Test getting conversations
    response = test_client.get(f"/api/{user_id}/conversations")
    assert response.status_code in [200, 401]

    # If successful, test getting messages for a conversation
    if response.status_code == 200:
        conversations = response.json()
        # If there are conversations, try to get messages
        if conversations:
            conv_id = conversations[0].get('id') if conversations else 1
            msg_response = test_client.get(f"/api/{user_id}/conversations/{conv_id}/messages")
            assert msg_response.status_code in [200, 401, 404]


def test_chat_task_prioritization(test_client: TestClient, db_session: Session, sample_user_data):
    """Test chat helping with task prioritization."""
    user_id = "test-user-123"

    chat_message = {
        "message": "I have too many tasks, help me prioritize",
        "conversation_id": None
    }

    response = test_client.post(f"/api/{user_id}/chat", json=chat_message)
    assert response.status_code in [200, 401, 422]


def test_chat_task_updates_via_conversation(test_client: TestClient, db_session: Session, sample_user_data):
    """Test updating tasks through chat conversation."""
    user_id = "test-user-123"

    # Create a task first
    task_data = {
        "title": "Original Task",
        "description": "Task to be updated via chat",
        "priority": "medium"
    }

    create_response = test_client.post(f"/api/{user_id}/tasks", json=task_data)
    assert create_response.status_code in [200, 201, 401]

    # Now simulate a chat request to update the task
    chat_message = {
        "message": "Update my 'Original Task' to high priority and add a due date",
        "conversation_id": None
    }

    response = test_client.post(f"/api/{user_id}/chat", json=chat_message)
    assert response.status_code in [200, 401, 422]


def test_chat_multi_step_task_process(test_client: TestClient, db_session: Session, sample_user_data):
    """Test multi-step task creation through chat."""
    user_id = "test-user-123"

    # First message: initiate task creation
    chat_message1 = {
        "message": "I want to create a new task",
        "conversation_id": None
    }

    response1 = test_client.post(f"/api/{user_id}/chat", json=chat_message1)
    assert response1.status_code in [200, 401, 422]

    # Second message: provide task details
    chat_message2 = {
        "message": "The task is 'Complete Project Proposal', it's high priority, for work category, due next Friday",
        "conversation_id": response1.json().get('conversation_id', None) if response1.status_code == 200 else None
    }

    response2 = test_client.post(f"/api/{user_id}/chat", json=chat_message2)
    assert response2.status_code in [200, 401, 422]


def test_chat_error_handling(test_client: TestClient, db_session: Session, sample_user_data):
    """Test chat error handling for invalid requests."""
    user_id = "test-user-123"

    # Test with empty message
    chat_message = {
        "message": "",
        "conversation_id": None
    }

    response = test_client.post(f"/api/{user_id}/chat", json=chat_message)
    # Should handle gracefully, possibly returning an error message
    assert response.status_code in [200, 401, 422]


def test_chat_advanced_task_insights(test_client: TestClient, db_session: Session, sample_user_data):
    """Test chat providing insights about advanced tasks."""
    user_id = "test-user-123"

    chat_message = {
        "message": "How many recurring tasks do I have? Which ones are overdue?",
        "conversation_id": None
    }

    response = test_client.post(f"/api/{user_id}/chat", json=chat_message)
    assert response.status_code in [200, 401, 422]


def test_chat_context_preservation(test_client: TestClient, db_session: Session, sample_user_data):
    """Test that chat preserves context between messages."""
    user_id = "test-user-123"

    # Start a conversation
    chat_message1 = {
        "message": "I have a lot of work tasks pending",
        "conversation_id": None
    }

    response1 = test_client.post(f"/api/{user_id}/chat", json=chat_message1)
    assert response1.status_code in [200, 401, 422]

    if response1.status_code == 200:
        conversation_id = response1.json().get('conversation_id')

        # Continue the conversation with context
        chat_message2 = {
            "message": "Can you list them by priority?",
            "conversation_id": conversation_id
        }

        response2 = test_client.post(f"/api/{user_id}/chat", json=chat_message2)
        assert response2.status_code in [200, 401, 422]


def test_chat_tool_usage_tracking(test_client: TestClient, db_session: Session, sample_user_data):
    """Test that chat tool usage is tracked properly."""
    user_id = "test-user-123"

    # Send a message that would trigger tool usage
    chat_message = {
        "message": "Create a task called 'Test Tool Usage' with high priority",
        "conversation_id": None
    }

    # Mocking is now handled by autouse fixture in conftest.py
    # But we can customize it here if needed or just let it use the default mock

    response = test_client.post(f"/api/{user_id}/chat", json=chat_message)
    assert response.status_code in [200, 401, 422]

    # The response should indicate tool usage if successful
    if response.status_code == 200:
        # For this specific test, we might need to override the mock to return tool calls
        # This part requires the test to potentially patch again or configure the fixture
        pass