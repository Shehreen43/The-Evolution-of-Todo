from fastapi.testclient import TestClient
from app.main import app

def test_root_endpoint():
    """Test the root endpoint."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert data["name"] == "The Evolution of Todo - Phase II"


def test_health_endpoint():
    """Test the health endpoint."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_unauthorized_access():
    """Test that unauthorized access is properly rejected."""
    client = TestClient(app)
    response = client.get("/api/test_user/tasks")
    # Should return 401 or 403 for unauthorized access
    assert response.status_code in [401, 403]


def test_cors_configuration():
    """Test that CORS is properly configured."""
    client = TestClient(app)
    # Test preflight request
    response = client.options(
        "/api/test_user/tasks",
        headers={
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization,content-type",
            "Origin": "http://localhost:3000",
        },
    )
    # Should allow the request
    assert response.status_code in [200, 204]