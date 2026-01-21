"""
Pytest Configuration and Global Fixtures
Advanced test setup for AI Film Studio Testing Framework
"""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime, timedelta
import json
import asyncio
from typing import Dict, Any, List, Optional
import time


# ==============================================================================
# PYTEST CONFIGURATION
# ==============================================================================

def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "gpu: Tests requiring GPU")
    config.addinivalue_line("markers", "aws: Tests requiring AWS services")
    config.addinivalue_line("markers", "smoke: Smoke tests for quick validation")
    config.addinivalue_line("markers", "regression: Regression tests")
    config.addinivalue_line("markers", "security: Security tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on markers and options"""
    skip_slow = pytest.mark.skip(reason="Skipping slow tests (use --run-slow)")
    skip_gpu = pytest.mark.skip(reason="Skipping GPU tests (use --run-gpu)")
    
    for item in items:
        if "slow" in item.keywords and not config.getoption("--run-slow", default=False):
            item.add_marker(skip_slow)
        if "gpu" in item.keywords and not config.getoption("--run-gpu", default=False):
            item.add_marker(skip_gpu)


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption("--run-slow", action="store_true", help="Run slow tests")
    parser.addoption("--run-gpu", action="store_true", help="Run GPU tests")
    parser.addoption("--run-aws", action="store_true", help="Run AWS integration tests")


# ==============================================================================
# ASYNC EVENT LOOP FIXTURE
# ==============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ==============================================================================
# HTTP CLIENT FIXTURES
# ==============================================================================

@pytest.fixture
def test_client():
    """Create synchronous test client"""
    from fastapi.testclient import TestClient
    try:
        from src.main import app
    except ImportError:
        # Create mock app if main app doesn't exist
        from fastapi import FastAPI
        app = FastAPI()
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Create async test client for API testing"""
    from httpx import AsyncClient, ASGITransport
    try:
        from src.main import app
    except ImportError:
        from fastapi import FastAPI
        app = FastAPI()
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# ==============================================================================
# DATABASE FIXTURES
# ==============================================================================

@pytest.fixture
def mock_database():
    """Mock database connection pool"""
    mock_pool = MagicMock()
    mock_pool.acquire = AsyncMock()
    mock_pool.release = AsyncMock()
    mock_pool.execute = AsyncMock()
    mock_pool.fetch_one = AsyncMock()
    mock_pool.fetch_all = AsyncMock()
    mock_pool.transaction = MagicMock()
    return mock_pool


@pytest.fixture
async def db_session(mock_database):
    """Create database session for testing"""
    session = MagicMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    yield session


# ==============================================================================
# AWS SERVICE FIXTURES
# ==============================================================================

@pytest.fixture
def mock_s3_client():
    """Mock S3 client"""
    client = MagicMock()
    client.put_object = AsyncMock(return_value={"ETag": "test-etag"})
    client.get_object = AsyncMock(return_value={
        "Body": MagicMock(read=AsyncMock(return_value=b"test-content"))
    })
    client.delete_object = AsyncMock(return_value={})
    client.list_objects_v2 = AsyncMock(return_value={"Contents": []})
    client.generate_presigned_url = MagicMock(return_value="https://presigned-url")
    client.copy_object = AsyncMock(return_value={"CopyObjectResult": {}})
    client.create_multipart_upload = AsyncMock(return_value={"UploadId": "upload-id"})
    client.upload_part = AsyncMock(return_value={"ETag": "part-etag"})
    client.complete_multipart_upload = AsyncMock(return_value={"Location": "s3://bucket/key"})
    return client


@pytest.fixture
def mock_sqs_client():
    """Mock SQS client"""
    client = MagicMock()
    client.send_message = AsyncMock(return_value={"MessageId": "msg-id"})
    client.receive_message = AsyncMock(return_value={"Messages": []})
    client.delete_message = AsyncMock(return_value={})
    client.send_message_batch = AsyncMock(return_value={"Successful": [], "Failed": []})
    client.get_queue_attributes = AsyncMock(return_value={"Attributes": {}})
    client.purge_queue = AsyncMock(return_value={})
    return client


@pytest.fixture
def mock_dynamodb_client():
    """Mock DynamoDB client"""
    client = MagicMock()
    client.put_item = AsyncMock(return_value={})
    client.get_item = AsyncMock(return_value={"Item": {}})
    client.delete_item = AsyncMock(return_value={})
    client.query = AsyncMock(return_value={"Items": []})
    client.scan = AsyncMock(return_value={"Items": []})
    client.update_item = AsyncMock(return_value={})
    return client


@pytest.fixture
def mock_sns_client():
    """Mock SNS client"""
    client = MagicMock()
    client.publish = AsyncMock(return_value={"MessageId": "sns-msg-id"})
    client.subscribe = AsyncMock(return_value={"SubscriptionArn": "arn:aws:sns:..."})
    return client


# ==============================================================================
# AI SERVICE FIXTURES
# ==============================================================================

@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client"""
    client = MagicMock()
    
    # Chat completions
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content="AI generated content"))]
    client.chat.completions.create = AsyncMock(return_value=mock_completion)
    
    # Images
    mock_image = MagicMock()
    mock_image.data = [MagicMock(url="https://openai.com/image.png")]
    client.images.generate = AsyncMock(return_value=mock_image)
    
    # Embeddings
    mock_embedding = MagicMock()
    mock_embedding.data = [MagicMock(embedding=[0.1] * 1536)]
    client.embeddings.create = AsyncMock(return_value=mock_embedding)
    
    return client


@pytest.fixture
def mock_elevenlabs_client():
    """Mock ElevenLabs client"""
    client = MagicMock()
    client.generate = AsyncMock(return_value=b"audio_bytes")
    client.generate_stream = MagicMock(return_value=iter([b"chunk1", b"chunk2"]))
    
    mock_voices = MagicMock()
    mock_voices.voices = [
        MagicMock(voice_id="voice_001", name="Adam"),
        MagicMock(voice_id="voice_002", name="Rachel")
    ]
    client.voices.get_all = MagicMock(return_value=mock_voices)
    client.voices.get = MagicMock(return_value=MagicMock(voice_id="voice_001"))
    
    client.clone = AsyncMock(return_value=MagicMock(voice_id="cloned_001"))
    client.audio_isolation = AsyncMock(return_value=b"isolated_audio")
    
    return client


@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic Claude client"""
    client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Claude response")]
    client.messages.create = AsyncMock(return_value=mock_response)
    return client


# ==============================================================================
# SAMPLE DATA FIXTURES
# ==============================================================================

@pytest.fixture
def sample_script():
    """Sample script data for testing"""
    return {
        "id": "script_001",
        "title": "Test Film",
        "format": "screenplay",
        "characters": [
            {
                "id": "char_001",
                "name": "Alex Johnson",
                "age": 32,
                "occupation": "Detective",
                "personality": ["determined", "analytical", "compassionate"],
                "voice_profile": {
                    "type": "adult_male",
                    "accent": "american",
                    "tone": "confident"
                }
            },
            {
                "id": "char_002",
                "name": "Sarah Chen",
                "age": 28,
                "occupation": "Scientist",
                "personality": ["brilliant", "curious", "reserved"],
                "voice_profile": {
                    "type": "adult_female",
                    "accent": "neutral",
                    "tone": "intellectual"
                }
            }
        ],
        "scenes": [
            {
                "scene_number": 1,
                "location": "INT. DETECTIVE OFFICE - DAY",
                "description": "A cluttered detective office. Papers everywhere.",
                "dialogue": [
                    {"character": "Alex", "text": "The evidence doesn't add up."},
                    {"character": "Sarah", "text": "Let me run another analysis."}
                ],
                "action": ["Alex paces nervously", "Sarah types rapidly on laptop"],
                "duration": 45
            },
            {
                "scene_number": 2,
                "location": "EXT. CITY STREET - NIGHT",
                "description": "Rain-soaked streets, neon lights reflecting.",
                "dialogue": [
                    {"character": "Alex", "text": "We need to move fast."}
                ],
                "action": ["They run through the rain"],
                "duration": 30
            }
        ],
        "metadata": {
            "genre": "thriller",
            "target_duration": 120,
            "rating": "PG-13",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    }


@pytest.fixture
def sample_character():
    """Sample character data"""
    return {
        "id": "char_001",
        "name": "Alex Johnson",
        "age": 32,
        "gender": "male",
        "occupation": "Detective",
        "personality_traits": ["determined", "analytical", "compassionate"],
        "appearance": {
            "height": "6ft",
            "build": "athletic",
            "hair": "dark brown",
            "eyes": "green",
            "distinctive_features": ["scar on left cheek"]
        },
        "voice": {
            "id": "voice_001",
            "type": "baritone",
            "accent": "american",
            "speaking_style": "measured, thoughtful"
        },
        "relationships": {
            "char_002": "colleague",
            "char_003": "antagonist"
        },
        "arc": "protagonist",
        "created_at": datetime.now().isoformat()
    }


@pytest.fixture
def sample_project():
    """Sample project data"""
    return {
        "id": "proj_001",
        "name": "The Investigation",
        "description": "A thriller about a detective uncovering a conspiracy",
        "status": "in_progress",
        "owner_id": "user_001",
        "type": "short_film",
        "settings": {
            "video_quality": "1080p",
            "frame_rate": 24,
            "aspect_ratio": "16:9",
            "color_profile": "cinematic"
        },
        "scripts": ["script_001"],
        "characters": ["char_001", "char_002"],
        "assets": {
            "videos": [],
            "audio": [],
            "images": []
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }


@pytest.fixture
def sample_job():
    """Sample processing job data"""
    return {
        "id": "job_001",
        "type": "video_generation",
        "status": "pending",
        "priority": 1,
        "input": {
            "scene_id": "scene_001",
            "script_id": "script_001",
            "project_id": "proj_001"
        },
        "output": None,
        "progress": 0,
        "retries": 0,
        "max_retries": 3,
        "created_at": datetime.now().isoformat(),
        "started_at": None,
        "completed_at": None,
        "error": None
    }


# ==============================================================================
# PERFORMANCE TESTING FIXTURES
# ==============================================================================

@pytest.fixture
def performance_timer():
    """Timer utility for performance tests"""
    class PerformanceTimer:
        def __init__(self):
            self.start_time: Optional[float] = None
            self.end_time: Optional[float] = None
            self.checkpoints: List[Dict[str, Any]] = []
        
        def start(self):
            self.start_time = time.perf_counter()
            self.checkpoints = []
        
        def checkpoint(self, name: str):
            if self.start_time:
                elapsed = time.perf_counter() - self.start_time
                self.checkpoints.append({"name": name, "elapsed": elapsed})
        
        def stop(self):
            self.end_time = time.perf_counter()
        
        @property
        def elapsed(self) -> float:
            if self.start_time is None:
                return 0
            end = self.end_time or time.perf_counter()
            return end - self.start_time
        
        def assert_within(self, max_seconds: float, msg: str = ""):
            assert self.elapsed <= max_seconds, \
                f"Performance assertion failed: {self.elapsed:.3f}s > {max_seconds}s. {msg}"
        
        def report(self) -> Dict[str, Any]:
            return {
                "total_elapsed": self.elapsed,
                "checkpoints": self.checkpoints
            }
    
    return PerformanceTimer()


# ==============================================================================
# UTILITY FIXTURES
# ==============================================================================

@pytest.fixture
def temp_file(tmp_path):
    """Create temporary file for testing"""
    def _create_temp_file(content: bytes = b"test content", name: str = "test_file.txt"):
        file_path = tmp_path / name
        file_path.write_bytes(content)
        return file_path
    return _create_temp_file


@pytest.fixture
def mock_environment():
    """Mock environment variables"""
    original_env = {}
    
    def _set_env(**kwargs):
        import os
        for key, value in kwargs.items():
            if key in os.environ:
                original_env[key] = os.environ[key]
            os.environ[key] = value
    
    yield _set_env
    
    # Restore original environment
    import os
    for key, value in original_env.items():
        os.environ[key] = value


@pytest.fixture
def capture_logs():
    """Capture log output for assertions"""
    import logging
    from io import StringIO
    
    class LogCapture:
        def __init__(self):
            self.stream = StringIO()
            self.handler = logging.StreamHandler(self.stream)
            self.handler.setLevel(logging.DEBUG)
        
        def attach(self, logger_name: str = None):
            logger = logging.getLogger(logger_name)
            logger.addHandler(self.handler)
            return self
        
        @property
        def output(self) -> str:
            return self.stream.getvalue()
        
        def contains(self, text: str) -> bool:
            return text in self.output
        
        def clear(self):
            self.stream.truncate(0)
            self.stream.seek(0)
    
    return LogCapture()


# ==============================================================================
# ASSERTION HELPERS
# ==============================================================================

@pytest.fixture
def assert_valid_json():
    """Assert that a string is valid JSON"""
    def _assert_valid_json(data: str) -> dict:
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON: {e}")
    return _assert_valid_json


@pytest.fixture
def assert_datetime_recent():
    """Assert that a datetime is recent (within threshold)"""
    def _assert_datetime_recent(dt: datetime, threshold_seconds: int = 60):
        now = datetime.now()
        diff = abs((now - dt).total_seconds())
        assert diff <= threshold_seconds, \
            f"Datetime {dt} is not within {threshold_seconds}s of now ({now})"
    return _assert_datetime_recent


@pytest.fixture
def assert_matches_schema():
    """Assert that data matches a JSON schema"""
    from jsonschema import validate, ValidationError
    
    def _assert_matches_schema(data: dict, schema: dict):
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            pytest.fail(f"Schema validation failed: {e.message}")
    return _assert_matches_schema
