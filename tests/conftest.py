"""Pytest fixtures and configuration for AI Film Studio tests"""

import sys
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Return path to test data directory"""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="function")
def temp_dir(tmp_path) -> Path:
    """Return temporary directory for test files"""
    return tmp_path


@pytest.fixture(scope="module")
def api_client() -> Generator[TestClient, None, None]:
    """FastAPI test client fixture"""
    from src.api.main import app

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
async def async_api_client() -> AsyncGenerator[AsyncClient, None]:
    """Async FastAPI test client fixture"""
    from httpx import ASGITransport

    from src.api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="function")
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing"""
    test_env = {
        "API_HOST": "localhost",
        "API_PORT": "8000",
        "LOG_LEVEL": "DEBUG",
    }
    for key, value in test_env.items():
        monkeypatch.setenv(key, value)
    return test_env


@pytest.fixture(scope="function")
def mock_aws_credentials(monkeypatch):
    """Mock AWS credentials for testing"""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")


@pytest.fixture(scope="function")
def mock_s3():
    """Mock S3 service using moto"""
    from moto import mock_s3

    with mock_s3():
        yield


@pytest.fixture(scope="function")
def mock_sqs():
    """Mock SQS service using moto"""
    from moto import mock_sqs

    with mock_sqs():
        yield


@pytest.fixture(scope="function")
def mock_redis():
    """Mock Redis using fakeredis"""
    import fakeredis

    redis_client = fakeredis.FakeStrictRedis()
    yield redis_client
    redis_client.flushall()


@pytest.fixture(scope="function")
def sample_script_data():
    """Sample script data for testing"""
    return {
        "title": "Test Film",
        "script": "A brave knight ventures into the unknown.",
        "genre": "fantasy",
        "duration": 60,
    }


@pytest.fixture(scope="function")
def sample_job_data():
    """Sample job data for testing"""
    return {
        "job_id": "test-job-123",
        "status": "pending",
        "script_id": "script-456",
        "created_at": "2024-01-01T00:00:00Z",
    }


@pytest.fixture(scope="function")
def sample_user_data():
    """Sample user data for testing"""
    return {
        "user_id": "user-789",
        "email": "test@example.com",
        "username": "testuser",
        "credits": 100,
    }


# Pytest configuration hooks
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "e2e: mark test as an end-to-end test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "async: mark test as async")


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location"""
    for item in items:
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
