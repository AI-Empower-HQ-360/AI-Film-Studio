"""
Pytest configuration for integration tests.
"""
import pytest
import os
import asyncio
from typing import Generator


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_environment():
    """Setup test environment variables"""
    os.environ["ENVIRONMENT"] = "test"
    os.environ["TEST_S3_BUCKET"] = "ai-film-studio-test"
    os.environ["GPU_DEVICE_ID"] = "0"
    yield
    # Cleanup after tests


@pytest.fixture
def mock_s3_bucket():
    """Mock S3 bucket for testing"""
    return "ai-film-studio-test"


@pytest.fixture
def test_api_key():
    """Test API key"""
    return os.getenv("TEST_API_KEY", "test_key_12345")


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (requires services running)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow (may take minutes to complete)"
    )
    config.addinivalue_line(
        "markers", "gpu: mark test as requiring GPU"
    )
