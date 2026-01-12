import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch


@pytest.fixture
def client():
    """Create a test client for the API."""
    # Temporarily override the database URL for testing
    with patch.dict(os.environ, {"DATABASE_URL": "sqlite+aiosqlite:///./test_backend.db"}):
        yield TestClient(app)


@pytest.fixture
def sample_token():
    """Provide a sample JWT token for testing."""
    # This is a mock token - in real tests we'd create a proper one
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIxMjMiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjk5OTk5OTk5OTl9.example_signature"