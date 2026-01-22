"""
AI Film Studio - Global Test Configuration
Production-grade pytest fixtures and configuration
"""
import os
import sys
import pytest
import asyncio
from typing import Generator, AsyncGenerator, Dict, Any
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime
import tempfile
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from httpx import AsyncClient

# ==================== Environment Setup ====================

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables"""
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DEBUG"] = "true"
    os.environ["DATABASE_URL"] = "postgresql://test:test@localhost:5432/test_db"
    os.environ["REDIS_URL"] = "redis://localhost:6379/1"
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["AWS_ACCESS_KEY_ID"] = "test_key"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test_secret"
    os.environ["S3_BUCKET_ASSETS"] = "test-assets-bucket"
    os.environ["S3_BUCKET_CHARACTERS"] = "test-characters-bucket"
    os.environ["SQS_VIDEO_QUEUE"] = "test-video-queue"
    os.environ["SQS_VOICE_QUEUE"] = "test-voice-queue"
    yield
    # Cleanup if needed


# ==================== Event Loop ====================

@pytest.fixture(scope="function")
def event_loop():
    """Create an event loop for async tests - function-scoped to avoid closed loop issues"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    try:
        loop.close()
    except Exception:
        pass  # Ignore errors on cleanup


# ==================== API Client Fixtures ====================

@pytest.fixture(scope="module")
def test_client() -> Generator[TestClient, None, None]:
    """Synchronous test client for FastAPI"""
    from src.api.main import app
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Asynchronous test client for FastAPI"""
    from src.api.main import app
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# ==================== Database Fixtures ====================

@pytest.fixture(scope="function")
def mock_database():
    """Mock database connection"""
    db = MagicMock()
    db.execute = MagicMock(return_value=MagicMock())
    db.commit = MagicMock()
    db.rollback = MagicMock()
    db.close = MagicMock()
    return db


@pytest.fixture(scope="function")
def test_db_session(mock_database):
    """Provide a test database session"""
    yield mock_database
    mock_database.rollback()


# ==================== AWS Mock Fixtures ====================

@pytest.fixture
def mock_s3_client():
    """Mock S3 client for testing"""
    client = MagicMock()
    client.upload_file = MagicMock(return_value=True)
    client.download_file = MagicMock(return_value=True)
    client.delete_object = MagicMock(return_value={"DeleteMarker": True})
    client.list_objects_v2 = MagicMock(return_value={"Contents": []})
    client.generate_presigned_url = MagicMock(return_value="https://test-bucket.s3.amazonaws.com/test-key")
    return client


@pytest.fixture
def mock_sqs_client():
    """Mock SQS client for testing"""
    client = MagicMock()
    client.send_message = MagicMock(return_value={"MessageId": "test-message-id"})
    client.receive_message = MagicMock(return_value={"Messages": []})
    client.delete_message = MagicMock(return_value={})
    client.get_queue_url = MagicMock(return_value={"QueueUrl": "https://sqs.test.amazonaws.com/queue"})
    return client


@pytest.fixture
def mock_dynamodb_client():
    """Mock DynamoDB client for testing"""
    client = MagicMock()
    client.put_item = MagicMock(return_value={})
    client.get_item = MagicMock(return_value={"Item": {}})
    client.query = MagicMock(return_value={"Items": []})
    client.delete_item = MagicMock(return_value={})
    return client


# ==================== AI Service Mock Fixtures ====================

@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client"""
    client = MagicMock()
    client.chat.completions.create = MagicMock(return_value=MagicMock(
        choices=[MagicMock(message=MagicMock(content="Generated content"))]
    ))
    client.images.generate = MagicMock(return_value=MagicMock(
        data=[MagicMock(url="https://example.com/image.png")]
    ))
    return client


@pytest.fixture
def mock_elevenlabs_client():
    """Mock ElevenLabs client for voice synthesis"""
    client = MagicMock()
    client.generate = MagicMock(return_value=b"audio_data")
    client.voices.get_all = MagicMock(return_value=[
        {"voice_id": "voice1", "name": "Test Voice 1"},
        {"voice_id": "voice2", "name": "Test Voice 2"}
    ])
    return client


@pytest.fixture
def mock_replicate_client():
    """Mock Replicate client for video generation"""
    client = MagicMock()
    client.run = AsyncMock(return_value=["https://example.com/video.mp4"])
    return client


# ==================== Test Data Fixtures ====================

@pytest.fixture
def sample_script() -> Dict[str, Any]:
    """Sample script for testing"""
    return {
        "title": "Test Film",
        "description": "A test film for automation testing",
        "scenes": [
            {
                "scene_number": 1,
                "description": "Opening scene in a city",
                "dialogue": "Welcome to the future.",
                "duration": 30,
                "characters": ["protagonist"]
            },
            {
                "scene_number": 2,
                "description": "Action sequence",
                "dialogue": "We need to move now!",
                "duration": 45,
                "characters": ["protagonist", "sidekick"]
            }
        ],
        "characters": [
            {"id": "protagonist", "name": "Alex", "voice_id": "voice1"},
            {"id": "sidekick", "name": "Sam", "voice_id": "voice2"}
        ],
        "settings": {
            "language": "en",
            "style": "cinematic",
            "resolution": "1080p"
        }
    }


@pytest.fixture
def sample_character() -> Dict[str, Any]:
    """Sample character for testing"""
    return {
        "id": "char_001",
        "name": "Test Character",
        "description": "A test character for automation testing",
        "appearance": {
            "age": "30",
            "gender": "neutral",
            "hair_color": "brown",
            "eye_color": "blue"
        },
        "personality": {
            "traits": ["brave", "intelligent"],
            "voice_style": "confident"
        },
        "voice_id": "voice1"
    }


@pytest.fixture
def sample_project() -> Dict[str, Any]:
    """Sample project for testing"""
    return {
        "id": "proj_001",
        "name": "Test Project",
        "owner_id": "user_001",
        "status": "draft",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "settings": {
            "output_format": "mp4",
            "resolution": "1920x1080",
            "frame_rate": 30
        }
    }


@pytest.fixture
def sample_job() -> Dict[str, Any]:
    """Sample job for testing"""
    return {
        "id": "job_001",
        "project_id": "proj_001",
        "type": "video_generation",
        "status": "pending",
        "priority": 1,
        "payload": {
            "scene_id": "scene_001",
            "output_path": "s3://bucket/output/video.mp4"
        },
        "created_at": datetime.utcnow().isoformat()
    }


# ==================== File Fixtures ====================

@pytest.fixture
def temp_directory():
    """Create a temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_audio_file(temp_directory) -> str:
    """Create a sample audio file for testing"""
    audio_path = os.path.join(temp_directory, "test_audio.wav")
    # Create a minimal WAV file header
    with open(audio_path, "wb") as f:
        # RIFF header
        f.write(b"RIFF")
        f.write((36).to_bytes(4, "little"))
        f.write(b"WAVE")
        # fmt chunk
        f.write(b"fmt ")
        f.write((16).to_bytes(4, "little"))
        f.write((1).to_bytes(2, "little"))  # PCM
        f.write((1).to_bytes(2, "little"))  # channels
        f.write((44100).to_bytes(4, "little"))  # sample rate
        f.write((88200).to_bytes(4, "little"))  # byte rate
        f.write((2).to_bytes(2, "little"))  # block align
        f.write((16).to_bytes(2, "little"))  # bits per sample
        # data chunk
        f.write(b"data")
        f.write((0).to_bytes(4, "little"))
    return audio_path


@pytest.fixture
def sample_video_file(temp_directory) -> str:
    """Create a sample video file path for testing"""
    return os.path.join(temp_directory, "test_video.mp4")


@pytest.fixture
def sample_image_file(temp_directory) -> str:
    """Create a sample image file for testing"""
    image_path = os.path.join(temp_directory, "test_image.png")
    # Create a minimal PNG file
    with open(image_path, "wb") as f:
        # PNG signature
        f.write(b"\x89PNG\r\n\x1a\n")
        # IHDR chunk (1x1 pixel)
        f.write(b"\x00\x00\x00\x0dIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde")
        # IEND chunk
        f.write(b"\x00\x00\x00\x00IEND\xaeB`\x82")
    return image_path


# ==================== Performance Testing Fixtures ====================

@pytest.fixture
def performance_timer():
    """Timer for performance testing"""
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
            
        def start(self):
            self.start_time = datetime.now()
            
        def stop(self):
            self.end_time = datetime.now()
            
        @property
        def elapsed(self):
            if self.start_time and self.end_time:
                return (self.end_time - self.start_time).total_seconds()
            return None
            
        def assert_within(self, max_seconds: float):
            assert self.elapsed is not None, "Timer not stopped"
            assert self.elapsed <= max_seconds, f"Operation took {self.elapsed}s, expected <= {max_seconds}s"
    
    return Timer()


# ==================== Markers ====================

def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "e2e: mark test as end-to-end test")
    config.addinivalue_line("markers", "performance: mark test as performance test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "gpu: mark test as requiring GPU")
    config.addinivalue_line("markers", "aws: mark test as requiring AWS credentials")
