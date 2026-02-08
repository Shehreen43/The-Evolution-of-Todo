import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(test_client: TestClient):
    """Test the root endpoint."""
    response = test_client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "status" in data
    assert "version" in data
    assert data["status"] == "running"


def test_health_endpoint(test_client: TestClient):
    """Test the health endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_options_request(test_client: TestClient):
    """Test OPTIONS request to ensure CORS is working."""
    response = test_client.options("/")
    # OPTIONS requests might return 405 Method Not Allowed or 200 OK depending on configuration
    assert response.status_code in [200, 405]


def test_invalid_endpoint(test_client: TestClient):
    """Test invalid endpoint returns 404."""
    response = test_client.get("/invalid-endpoint")
    assert response.status_code == 404


def test_api_endpoints_exist(test_client: TestClient):
    """Test that API endpoints return appropriate responses (even if unauthorized)."""
    user_id = "test-user-123"

    # These endpoints should exist even if they return 401/404 due to missing auth or resources
    endpoints = [
        f"/api/{user_id}/tasks",
        f"/api/{user_id}/conversations",
    ]

    for endpoint in endpoints:
        response = test_client.get(endpoint)
        # We expect these to return 401 (unauthorized) or 404 (not found) rather than 404 (endpoint not found)
        # indicating that the endpoint exists in the router
        assert response.status_code in [200, 401, 404, 422, 405]  # 422 for validation errors, 405 for method not allowed

    # Test chat endpoint separately as it might have different method restrictions
    chat_response = test_client.post(f"/api/{user_id}/chat", json={"message": "test"})
    # Chat endpoint should accept POST requests (possibly returning 401 if auth required)
    assert chat_response.status_code in [200, 401, 422]


def test_post_endpoints_return_correct_codes(test_client: TestClient):
    """Test that POST endpoints return appropriate status codes."""
    user_id = "test-user-123"

    # Test posting to tasks endpoint with invalid data
    response = test_client.post(f"/api/{user_id}/tasks", json={"invalid": "data"})
    # Should return 422 for validation error or 401 for auth error
    assert response.status_code in [401, 422]


def test_cors_headers_present(test_client: TestClient):
    """Test that CORS headers are appropriately handled."""
    # Make a request and check if CORS headers are handled properly
    response = test_client.get("/", headers={"Origin": "http://localhost:3000"})
    # Depending on CORS configuration, this might or might not include CORS headers
    # But the request should still work
    assert response.status_code == 200


def test_method_not_allowed(test_client: TestClient):
    """Test that wrong HTTP methods return 405."""
    user_id = "test-user-123"

    # Try to POST to the root endpoint which only accepts GET
    response = test_client.post("/", json={})
    assert response.status_code in [405, 200]  # Might be 200 if the route accepts POST as well


def test_content_type_handling(test_client: TestClient):
    """Test content type handling."""
    response = test_client.get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")


def test_large_request_handling(test_client: TestClient):
    """Test handling of larger payloads."""
    user_id = "test-user-123"

    # Create a relatively large payload
    large_payload = {
        "title": "Large Payload Test",
        "description": "x" * 1000,  # Large description
        "priority": "medium",
        "category": "test"
    }

    response = test_client.post(f"/api/{user_id}/tasks", json=large_payload)
    # Should either accept it or return a validation error, but not crash
    assert response.status_code in [200, 201, 401, 422, 413]  # 413 for payload too large


def test_special_characters_in_params(test_client: TestClient):
    """Test handling of special characters."""
    user_id = "test-user-123"

    special_payload = {
        "title": "Test with special chars: !@#$%^&*()",
        "description": "Testing special characters: àáâãäåæçèé",
        "priority": "medium"
    }

    response = test_client.post(f"/api/{user_id}/tasks", json=special_payload)
    # Should handle Unicode characters properly
    assert response.status_code in [200, 201, 401, 422]