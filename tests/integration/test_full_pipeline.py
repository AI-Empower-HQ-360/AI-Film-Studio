"""
Integration tests for the full AI Film Studio pipeline.
Tests the complete workflow from script to final video.
"""
import pytest
import asyncio
import os
from pathlib import Path
from typing import Dict, Any

from src.services.video_generation import VideoGenerationService
from src.services.voice_synthesis import VoiceSynthesisService
from src.services.lipsync_animation import LipsyncAnimationService
from src.services.music_audio import MusicAudioService
from src.services.subtitle_multilang import SubtitleMultilangService


@pytest.fixture
def sample_script():
    """Sample script for testing"""
    return """
    A young explorer named Maya discovers a hidden world beneath the ocean.
    She encounters mysterious creatures and learns about an ancient civilization.
    """


@pytest.fixture
def test_config():
    """Test configuration"""
    return {
        "s3_bucket": os.getenv("TEST_S3_BUCKET", "ai-film-studio-test"),
        "gpu_device": os.getenv("GPU_DEVICE_ID", "0"),
        "test_duration": 30  # Short duration for faster testing
    }


class TestFullPipeline:
    """Integration tests for the complete video generation pipeline"""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_video_generation_pipeline(self, sample_script, test_config):
        """Test complete video generation from script to video"""
        # Initialize services
        video_service = VideoGenerationService(
            s3_bucket=test_config["s3_bucket"]
        )
        
        # Test script processing and video generation
        result = await video_service.generate_video({
            "script": sample_script,
            "duration": test_config["test_duration"],
            "style": "cinematic"
        })
        
        assert result.success is True
        assert result.video_url is not None
        assert result.job_id is not None
        assert result.duration == test_config["test_duration"]

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_voice_synthesis_pipeline(self, sample_script, test_config):
        """Test voice synthesis integration"""
        voice_service = VoiceSynthesisService(
            s3_bucket=test_config["s3_bucket"]
        )
        
        result = await voice_service.synthesize_voice({
            "text": sample_script,
            "voice_id": "professional-female-1",
            "language": "en-US"
        })
        
        assert result.success is True
        assert result.audio_url is not None
        assert result.duration > 0

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_lipsync_pipeline(self, test_config):
        """Test lip-sync animation integration"""
        lipsync_service = LipsyncAnimationService(
            s3_bucket=test_config["s3_bucket"]
        )
        
        # Mock video and audio URLs for testing
        result = await lipsync_service.generate_lipsync({
            "video_url": "s3://test-bucket/video.mp4",
            "audio_url": "s3://test-bucket/audio.wav",
            "model": "wav2lip"
        })
        
        assert result.success is True
        assert result.output_url is not None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_subtitle_generation_pipeline(self, test_config):
        """Test multilingual subtitle generation"""
        subtitle_service = SubtitleMultilangService(
            s3_bucket=test_config["s3_bucket"]
        )
        
        result = await subtitle_service.generate_subtitles({
            "audio_url": "s3://test-bucket/audio.wav",
            "languages": ["en", "es", "fr"],
            "format": "srt"
        })
        
        assert result.success is True
        assert len(result.subtitle_urls) == 3

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_music_audio_pipeline(self, test_config):
        """Test music and audio generation"""
        music_service = MusicAudioService(
            s3_bucket=test_config["s3_bucket"]
        )
        
        result = await music_service.generate_music({
            "mood": "dramatic",
            "duration": test_config["test_duration"],
            "genre": "cinematic"
        })
        
        assert result.success is True
        assert result.audio_url is not None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_end_to_end_pipeline(self, sample_script, test_config):
        """Test complete end-to-end workflow"""
        job_id = "test_job_" + str(asyncio.get_event_loop().time())
        
        # Stage 1: Video Generation
        video_service = VideoGenerationService(s3_bucket=test_config["s3_bucket"])
        video_result = await video_service.generate_video({
            "script": sample_script,
            "duration": test_config["test_duration"],
            "job_id": job_id
        })
        assert video_result.success is True
        
        # Stage 2: Voice Synthesis
        voice_service = VoiceSynthesisService(s3_bucket=test_config["s3_bucket"])
        voice_result = await voice_service.synthesize_voice({
            "text": sample_script,
            "voice_id": "professional-female-1",
            "job_id": job_id
        })
        assert voice_result.success is True
        
        # Stage 3: Lip-sync (if video and audio are available)
        if video_result.video_url and voice_result.audio_url:
            lipsync_service = LipsyncAnimationService(s3_bucket=test_config["s3_bucket"])
            lipsync_result = await lipsync_service.generate_lipsync({
                "video_url": video_result.video_url,
                "audio_url": voice_result.audio_url,
                "job_id": job_id
            })
            assert lipsync_result.success is True
        
        # Stage 4: Music Generation
        music_service = MusicAudioService(s3_bucket=test_config["s3_bucket"])
        music_result = await music_service.generate_music({
            "mood": "dramatic",
            "duration": test_config["test_duration"],
            "job_id": job_id
        })
        assert music_result.success is True
        
        # Stage 5: Subtitles
        subtitle_service = SubtitleMultilangService(s3_bucket=test_config["s3_bucket"])
        subtitle_result = await subtitle_service.generate_subtitles({
            "audio_url": voice_result.audio_url,
            "languages": ["en"],
            "job_id": job_id
        })
        assert subtitle_result.success is True

    @pytest.mark.integration
    def test_pipeline_error_handling(self, test_config):
        """Test error handling in pipeline"""
        video_service = VideoGenerationService(s3_bucket=test_config["s3_bucket"])
        
        # Test with invalid input
        with pytest.raises(ValueError):
            asyncio.run(video_service.generate_video({
                "script": "",  # Empty script should fail
                "duration": -1  # Invalid duration
            }))

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_concurrent_job_processing(self, sample_script, test_config):
        """Test handling multiple concurrent jobs"""
        video_service = VideoGenerationService(s3_bucket=test_config["s3_bucket"])
        
        # Create multiple jobs concurrently
        tasks = [
            video_service.generate_video({
                "script": sample_script,
                "duration": 10,
                "job_id": f"concurrent_job_{i}"
            })
            for i in range(3)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify all jobs completed
        assert len(results) == 3
        for result in results:
            if not isinstance(result, Exception):
                assert result.success is True
