"""Tests for API endpoints"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.services.storage import get_job_store
from src.services.queue import get_task_queue

client = TestClient(app)


@pytest.fixture
def setup_services():
    """Setup and cleanup services for each test"""
    store = get_job_store()
    queue = get_task_queue()
    
    # Clear before test
    store.clear()
    queue.clear()
    
    yield
    
    # Clear after test
    store.clear()
    queue.clear()


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["version"] == "0.1.0"


def test_create_job_endpoint(setup_services):
    """Test job creation endpoint"""
    response = client.post(
        "/api/v1/jobs",
        json={
            "user_id": "user123",
            "script": "SCENE 1: INT. ROOM - DAY\nSHOT 1: Wide - 5s\nTest shot",
            "title": "Test Film"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["user_id"] == "user123"
    assert data["title"] == "Test Film"
    assert data["status"] == "queued"
    assert data["estimated_cost"] > 0


def test_create_job_invalid_script(setup_services):
    """Test job creation with invalid script"""
    response = client.post(
        "/api/v1/jobs",
        json={
            "user_id": "user123",
            "script": "",  # Empty script
            "title": "Invalid"
        }
    )
    
    assert response.status_code == 400


def test_get_job_endpoint(setup_services):
    """Test get job endpoint"""
    # Create a job first
    create_response = client.post(
        "/api/v1/jobs",
        json={
            "user_id": "user123",
            "script": "Test script content",
            "title": "Test Film"
        }
    )
    
    job_id = create_response.json()["id"]
    
    # Get the job
    response = client.get(f"/api/v1/jobs/{job_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job_id


def test_get_nonexistent_job(setup_services):
    """Test getting non-existent job"""
    response = client.get("/api/v1/jobs/nonexistent-id")
    assert response.status_code == 404


def test_get_job_state(setup_services):
    """Test get job state endpoint"""
    # Create a job first
    create_response = client.post(
        "/api/v1/jobs",
        json={
            "user_id": "user123",
            "script": "SCENE 1: INT. ROOM - DAY\nSHOT 1: Wide - 5s\nTest",
            "title": "Test"
        }
    )
    
    job_id = create_response.json()["id"]
    
    # Get job state
    response = client.get(f"/api/v1/jobs/{job_id}/state")
    
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == job_id
    assert "total_scenes" in data
    assert "total_shots" in data


def test_list_jobs(setup_services):
    """Test list jobs endpoint"""
    # Create a couple of jobs
    client.post(
        "/api/v1/jobs",
        json={
            "user_id": "user123",
            "script": "Test script 1",
            "title": "Film 1"
        }
    )
    
    client.post(
        "/api/v1/jobs",
        json={
            "user_id": "user456",
            "script": "Test script 2",
            "title": "Film 2"
        }
    )
    
    # List all jobs
    response = client.get("/api/v1/jobs")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["jobs"]) == 2


def test_list_jobs_filtered_by_user(setup_services):
    """Test list jobs filtered by user"""
    # Create jobs for different users
    client.post(
        "/api/v1/jobs",
        json={
            "user_id": "user123",
            "script": "Test script 1",
            "title": "Film 1"
        }
    )
    
    client.post(
        "/api/v1/jobs",
        json={
            "user_id": "user456",
            "script": "Test script 2",
            "title": "Film 2"
        }
    )
    
    # List jobs for specific user
    response = client.get("/api/v1/jobs?user_id=user123")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["jobs"][0]["user_id"] == "user123"

