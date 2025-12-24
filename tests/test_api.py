"""Tests for API endpoints"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint returns HTML"""
    response = client.get("/")
    assert response.status_code == 200
    # Check if response is HTML content
    assert "text/html" in response.headers.get("content-type", "")

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["version"] == "0.1.0"

def test_home_data():
    """Test home data endpoint"""
    response = client.get("/api/v1/data/home")
    assert response.status_code == 200
    data = response.json()
    assert "stats" in data
    assert "recent_activity" in data
    assert "total_projects" in data["stats"]
    assert "completed_projects" in data["stats"]
    assert "processing_projects" in data["stats"]
    assert "api_status" in data["stats"]

