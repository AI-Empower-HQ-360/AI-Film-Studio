"""Tests for API endpoints"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_root(client):
    """Test root endpoint returns HTML homepage"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert b"AI Film Studio" in response.content

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["version"] == "0.1.0"

def test_about():
    """Test about endpoint"""
    response = client.get("/about")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AI Film Studio"
    assert data["version"] == "0.1.0"
    assert "description" in data
    assert "author" in data
    assert "features" in data
    assert isinstance(data["features"], list)
    assert len(data["features"]) > 0
