"""
Tests for AI Service Modules
"""
import pytest
from unittest.mock import AsyncMock, Mock
from src.services.video_generation import (
    VideoGenerationService,
    VideoGenerationRequest,
    VideoGenerationResponse
)
from src.services.voice_synthesis import (
    VoiceSynthesisService,
    VoiceSynthesisRequest,
    VoiceSynthesisResponse
)
from src.services.ai_job_manager import (
    AIJobManager,
    JobSubmissionRequest,
    JobType,
    JobPriority,
    JobStatus
)


@pytest.fixture
def video_service():
    """Fixture for video generation service"""
    return VideoGenerationService(s3_bucket="test-bucket")


@pytest.fixture
def voice_service():
    """Fixture for voice synthesis service"""
    return VoiceSynthesisService(s3_bucket="test-bucket")


@pytest.fixture
def job_manager():
    """Fixture for AI job manager"""
    return AIJobManager(queue_service="aws_sqs", auto_scaling=False)


class TestVideoGenerationService:
    """Tests for video generation service"""
    
    def test_estimate_processing_time(self, video_service):
        """Test processing time estimation"""
        time = video_service.estimate_processing_time("stable-video-diffusion", 30)
        assert time > 0
        assert time == 30 * 2.5  # duration * estimated_time_per_second
    
    def test_get_supported_models(self, video_service):
        """Test getting supported models"""
        models = video_service.get_supported_models()
        assert len(models) > 0
        assert all("name" in model for model in models)
        assert all("provider" in model for model in models)
    
    def test_get_job_status_not_found(self, video_service):
        """Test getting status of non-existent job"""
        status = video_service.get_job_status("non-existent-job")
        assert status["status"] == "not_found"


class TestVoiceSynthesisService:
    """Tests for voice synthesis service"""
    
    def test_get_available_voices(self, voice_service):
        """Test getting available voices"""
        voices = voice_service.get_available_voices()
        assert len(voices) > 0
        assert all("voice_id" in voice for voice in voices)
        assert all("age_group" in voice for voice in voices)
    
    def test_get_available_voices_with_filters(self, voice_service):
        """Test getting available voices with filters"""
        adult_voices = voice_service.get_available_voices(age_group="adult")
        assert all(voice["age_group"] == "adult" for voice in adult_voices)
        
        male_voices = voice_service.get_available_voices(gender="male")
        assert all(voice["gender"] == "male" for voice in male_voices)
    
    def test_get_voice_categories(self, voice_service):
        """Test getting voice categories"""
        categories = voice_service.get_voice_categories()
        assert "adult" in categories
        assert "child" in categories
        assert len(categories) > 0


class TestAIJobManager:
    """Tests for AI job manager"""
    
    @pytest.mark.asyncio
    async def test_submit_job(self, job_manager):
        """Test job submission"""
        request = JobSubmissionRequest(
            job_type=JobType.VIDEO_GENERATION,
            priority=JobPriority.HIGH,
            user_id="user123",
            parameters={"script": "test script"}
        )
        
        response = await job_manager.submit_job(request)
        
        assert response.job_id
        assert response.status == JobStatus.QUEUED
        assert response.job_type == JobType.VIDEO_GENERATION
        assert response.priority == JobPriority.HIGH
    
    @pytest.mark.asyncio
    async def test_get_job_status(self, job_manager):
        """Test getting job status"""
        # Submit a job first
        request = JobSubmissionRequest(
            job_type=JobType.VOICE_SYNTHESIS,
            priority=JobPriority.MEDIUM,
            user_id="user123",
            parameters={"text": "test"}
        )
        job = await job_manager.submit_job(request)
        
        # Get job status
        status = await job_manager.get_job_status(job.job_id)
        assert status.job_id == job.job_id
        assert status.status in [JobStatus.QUEUED, JobStatus.PROCESSING]
    
    @pytest.mark.asyncio
    async def test_cancel_job(self, job_manager):
        """Test job cancellation"""
        # Submit a job
        request = JobSubmissionRequest(
            job_type=JobType.MUSIC_GENERATION,
            priority=JobPriority.LOW,
            user_id="user123",
            parameters={"prompt": "test"}
        )
        job = await job_manager.submit_job(request)
        
        # Cancel the job
        result = await job_manager.cancel_job(job.job_id)
        assert result is True
        
        # Check job status
        status = await job_manager.get_job_status(job.job_id)
        assert status.status == JobStatus.CANCELLED
    
    @pytest.mark.asyncio
    async def test_register_worker(self, job_manager):
        """Test worker registration"""
        worker = await job_manager.register_worker(
            worker_id="worker-1",
            gpu_instance="g4dn.xlarge"
        )
        
        assert worker.worker_id == "worker-1"
        assert worker.gpu_instance == "g4dn.xlarge"
        assert worker.status == "idle"
    
    @pytest.mark.asyncio
    async def test_update_worker_status(self, job_manager):
        """Test updating worker status"""
        # Register worker first
        await job_manager.register_worker("worker-1", "g4dn.xlarge")
        
        # Update status
        await job_manager.update_worker_status(
            "worker-1",
            "busy",
            gpu_utilization=0.8,
            gpu_memory_used=12.5
        )
        
        worker = job_manager.workers["worker-1"]
        assert worker.status == "busy"
        assert worker.gpu_utilization == 0.8
        assert worker.gpu_memory_used == 12.5
    
    def test_get_queue_stats(self, job_manager):
        """Test getting queue statistics"""
        stats = job_manager.get_queue_stats()
        
        assert "total_jobs" in stats
        assert "queued_by_priority" in stats
        assert "total_workers" in stats
        assert "job_stats" in stats
    
    def test_get_gpu_recommendations(self, job_manager):
        """Test getting GPU recommendations"""
        recommendations = job_manager.get_gpu_recommendations()
        
        assert "instances" in recommendations
        assert "recommendations" in recommendations
        assert len(recommendations["instances"]) > 0


class TestVideoGenerationRequest:
    """Tests for video generation request model"""
    
    def test_valid_request(self):
        """Test valid request creation"""
        request = VideoGenerationRequest(
            script="Test script",
            character_images=["s3://bucket/image1.jpg"],
            duration=30
        )
        assert request.script == "Test script"
        assert request.duration == 30
        assert request.model_name == "stable-video-diffusion"
    
    def test_invalid_duration(self):
        """Test invalid duration validation"""
        with pytest.raises(Exception):  # Pydantic will raise ValidationError
            VideoGenerationRequest(
                script="Test",
                character_images=["s3://bucket/image1.jpg"],
                duration=0  # Invalid: must be >= 1
            )


class TestVoiceSynthesisRequest:
    """Tests for voice synthesis request model"""
    
    def test_valid_request(self):
        """Test valid request creation"""
        request = VoiceSynthesisRequest(
            text="Hello world",
            voice_id="adult_male_1"
        )
        assert request.text == "Hello world"
        assert request.voice_id == "adult_male_1"
        assert request.language == "en-US"
        assert request.speed == 1.0
    
    def test_custom_parameters(self):
        """Test request with custom parameters"""
        request = VoiceSynthesisRequest(
            text="Test",
            voice_id="child_girl_1",
            emotion="happy",
            speed=1.5,
            pitch=1.2
        )
        assert request.emotion == "happy"
        assert request.speed == 1.5
        assert request.pitch == 1.2


class TestJobSubmissionRequest:
    """Tests for job submission request model"""
    
    def test_valid_request(self):
        """Test valid job submission"""
        request = JobSubmissionRequest(
            job_type=JobType.PODCAST_VIDEO,
            priority=JobPriority.HIGH,
            user_id="user456",
            parameters={"title": "Test Podcast"}
        )
        assert request.job_type == JobType.PODCAST_VIDEO
        assert request.priority == JobPriority.HIGH
        assert request.max_retries == 3
    
    def test_custom_retries(self):
        """Test custom retry count"""
        request = JobSubmissionRequest(
            job_type=JobType.SUBTITLE_GENERATION,
            priority=JobPriority.LOW,
            user_id="user789",
            parameters={"audio_url": "s3://bucket/audio.mp3"},
            max_retries=5
        )
        assert request.max_retries == 5
