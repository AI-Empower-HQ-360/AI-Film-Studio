"""Tests for project API endpoints"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


class TestProjectCreation:
    """Test project creation endpoints"""
    
    def test_create_project_without_auth(self):
        """Test creating project without authentication"""
        response = client.post(
            "/api/projects/create",
            json={
                "title": "Test Project",
                "script": "Test script content"
            }
        )
        assert response.status_code == 401  # Unauthorized without auth
    
    def test_create_project_missing_title(self):
        """Test creating project with missing title"""
        response = client.post(
            "/api/projects/create",
            json={
                "script": "Test script content"
                # Missing title
            }
        )
        assert response.status_code in [401, 422]  # Auth required or validation error


class TestProjectRetrieval:
    """Test project retrieval endpoints"""
    
    def test_list_projects_without_auth(self):
        """Test listing projects without authentication"""
        response = client.get("/api/projects/")
        assert response.status_code == 401  # Unauthorized without auth
    
    def test_get_project_without_auth(self):
        """Test getting specific project without authentication"""
        fake_uuid = "123e4567-e89b-12d3-a456-426614174000"
        response = client.get(f"/api/projects/{fake_uuid}")
        assert response.status_code == 401  # Unauthorized without auth
