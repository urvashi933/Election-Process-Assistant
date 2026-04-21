import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """
    Creates a test client for the FastAPI app.
    Used across all test files.
    """
    return TestClient(app)