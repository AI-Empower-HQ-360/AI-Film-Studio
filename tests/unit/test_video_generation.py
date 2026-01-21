"""
Unit Tests for Video Generation Service
Tests video rendering, processing, and output
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime
import asyncio


class TestVideoGenerationService:
    """Test suite for Video Generation Service"""

    @pytest.fixture
    def video_service(self):
        """Create video service instance"""
        from src.services.video_generation import VideoGenerationService
        return VideoGenerationService()

    @pytest.fixture
    def mock_video_processor(self):
        """Mock video processor"""
        processor = MagicMock()
        processor.render = AsyncMock(return_value={
            "output_path": "s3://bucket/output/video.mp4",
            "duration": 60.0,
            "resolution": "1920x1080",
            "fps": 30
        })
        processor.merge = AsyncMock(return_value="s3://bucket/merged.mp4")
        processor.add_audio = AsyncMock(return_value="s3://bucket/with_audio.mp4")
        return processor

    # ==================== Video Generation Tests ====================

    @pytest.mark.unit
    async def test_generate_video_from_scene(self, video_service, sample_script, mock_video_processor):
        """Test video generation from a scene"""
        with patch.object(video_service, 'processor', mock_video_processor):
            scene = sample_script['scenes'][0]
            result = await video_service.generate_from_scene(scene)
            
            assert result is not None
            assert 'output_path' in result
            mock_video_processor.render.assert_called_once()

    @pytest.mark.unit
    async def test_generate_video_with_settings(self, video_service, sample_script, mock_video_processor):
        """Test video generation with custom settings"""
        with patch.object(video_service, 'processor', mock_video_processor):
            scene = sample_script['scenes'][0]
            settings = {
                "resolution": "4K",
                "fps": 60,
                "codec": "h265"
            }
            result = await video_service.generate_from_scene(scene, settings=settings)
            
            assert result is not None

    @pytest.mark.unit
    async def test_generate_video_batch(self, video_service, sample_script, mock_video_processor):
        """Test batch video generation"""
        with patch.object(video_service, 'processor', mock_video_processor):
            results = await video_service.generate_batch(sample_script['scenes'])
            
            assert len(results) == len(sample_script['scenes'])

    @pytest.mark.unit
    def test_validate_video_settings(self, video_service):
        """Test video settings validation"""
        valid_settings = {
            "resolution": "1080p",
            "fps": 30,
            "codec": "h264"
        }
        assert video_service.validate_settings(valid_settings) is True

        invalid_settings = {
            "resolution": "invalid",
            "fps": -1
        }
        assert video_service.validate_settings(invalid_settings) is False

    # ==================== Video Processing Tests ====================

    @pytest.mark.unit
    async def test_merge_video_segments(self, video_service, mock_video_processor):
        """Test merging multiple video segments"""
        with patch.object(video_service, 'processor', mock_video_processor):
            segments = [
                "s3://bucket/segment1.mp4",
                "s3://bucket/segment2.mp4",
                "s3://bucket/segment3.mp4"
            ]
            result = await video_service.merge_segments(segments)
            
            assert result is not None
            mock_video_processor.merge.assert_called_once()

    @pytest.mark.unit
    async def test_add_audio_track(self, video_service, mock_video_processor):
        """Test adding audio track to video"""
        with patch.object(video_service, 'processor', mock_video_processor):
            result = await video_service.add_audio(
                video_path="s3://bucket/video.mp4",
                audio_path="s3://bucket/audio.wav"
            )
            
            assert result is not None
            mock_video_processor.add_audio.assert_called_once()

    @pytest.mark.unit
    async def test_add_subtitles(self, video_service, mock_video_processor):
        """Test adding subtitles to video"""
        mock_video_processor.add_subtitles = AsyncMock(return_value="s3://bucket/with_subs.mp4")
        
        with patch.object(video_service, 'processor', mock_video_processor):
            subtitles = [
                {"start": 0.0, "end": 2.0, "text": "Hello"},
                {"start": 2.0, "end": 4.0, "text": "World"}
            ]
            result = await video_service.add_subtitles(
                video_path="s3://bucket/video.mp4",
                subtitles=subtitles
            )
            
            assert result is not None

    @pytest.mark.unit
    async def test_apply_video_effects(self, video_service, mock_video_processor):
        """Test applying video effects"""
        mock_video_processor.apply_effects = AsyncMock(return_value="s3://bucket/with_effects.mp4")
        
        with patch.object(video_service, 'processor', mock_video_processor):
            effects = ["color_grade", "stabilize", "denoise"]
            result = await video_service.apply_effects(
                video_path="s3://bucket/video.mp4",
                effects=effects
            )
            
            assert result is not None

    # ==================== Video Analysis Tests ====================

    @pytest.mark.unit
    async def test_analyze_video_content(self, video_service, mock_video_processor):
        """Test video content analysis"""
        mock_video_processor.analyze = AsyncMock(return_value={
            "duration": 60.0,
            "scenes_detected": 5,
            "average_brightness": 0.65
        })
        
        with patch.object(video_service, 'processor', mock_video_processor):
            analysis = await video_service.analyze("s3://bucket/video.mp4")
            
            assert 'duration' in analysis
            assert 'scenes_detected' in analysis

    @pytest.mark.unit
    async def test_extract_frames(self, video_service, mock_video_processor):
        """Test frame extraction from video"""
        mock_video_processor.extract_frames = AsyncMock(return_value=[
            "frame_001.png", "frame_002.png", "frame_003.png"
        ])
        
        with patch.object(video_service, 'processor', mock_video_processor):
            frames = await video_service.extract_frames(
                video_path="s3://bucket/video.mp4",
                interval=1.0
            )
            
            assert len(frames) > 0

    @pytest.mark.unit
    async def test_generate_thumbnail(self, video_service, mock_video_processor):
        """Test thumbnail generation"""
        mock_video_processor.generate_thumbnail = AsyncMock(return_value="s3://bucket/thumb.jpg")
        
        with patch.object(video_service, 'processor', mock_video_processor):
            thumbnail = await video_service.generate_thumbnail(
                video_path="s3://bucket/video.mp4",
                timestamp=10.0
            )
            
            assert thumbnail is not None

    # ==================== Output Format Tests ====================

    @pytest.mark.unit
    async def test_export_to_mp4(self, video_service, mock_video_processor):
        """Test MP4 export"""
        mock_video_processor.export = AsyncMock(return_value="s3://bucket/output.mp4")
        
        with patch.object(video_service, 'processor', mock_video_processor):
            result = await video_service.export(
                video_path="s3://bucket/video.mp4",
                format="mp4"
            )
            
            assert result.endswith('.mp4')

    @pytest.mark.unit
    async def test_export_to_webm(self, video_service, mock_video_processor):
        """Test WebM export"""
        mock_video_processor.export = AsyncMock(return_value="s3://bucket/output.webm")
        
        with patch.object(video_service, 'processor', mock_video_processor):
            result = await video_service.export(
                video_path="s3://bucket/video.mp4",
                format="webm"
            )
            
            assert result.endswith('.webm')

    @pytest.mark.unit
    async def test_export_with_compression(self, video_service, mock_video_processor):
        """Test export with compression settings"""
        mock_video_processor.export = AsyncMock(return_value="s3://bucket/compressed.mp4")
        
        with patch.object(video_service, 'processor', mock_video_processor):
            result = await video_service.export(
                video_path="s3://bucket/video.mp4",
                format="mp4",
                compression_level=8
            )
            
            assert result is not None

    # ==================== Error Handling Tests ====================

    @pytest.mark.unit
    async def test_handle_invalid_video_path(self, video_service):
        """Test handling of invalid video path"""
        with pytest.raises((FileNotFoundError, ValueError)):
            await video_service.analyze("invalid/path/video.mp4")

    @pytest.mark.unit
    async def test_handle_corrupted_video(self, video_service, mock_video_processor):
        """Test handling of corrupted video file"""
        mock_video_processor.analyze = AsyncMock(side_effect=ValueError("Corrupted video"))
        
        with patch.object(video_service, 'processor', mock_video_processor):
            with pytest.raises(ValueError):
                await video_service.analyze("s3://bucket/corrupted.mp4")

    @pytest.mark.unit
    async def test_handle_unsupported_format(self, video_service):
        """Test handling of unsupported video format"""
        with pytest.raises(ValueError):
            await video_service.export(
                video_path="s3://bucket/video.mp4",
                format="unsupported_format"
            )

    # ==================== Performance Tests ====================

    @pytest.mark.unit
    @pytest.mark.performance
    async def test_video_generation_performance(self, video_service, sample_script, mock_video_processor, performance_timer):
        """Test video generation performance"""
        with patch.object(video_service, 'processor', mock_video_processor):
            performance_timer.start()
            
            scene = sample_script['scenes'][0]
            await video_service.generate_from_scene(scene)
            
            performance_timer.stop()
            # Should complete within 5 seconds for mocked operations
            performance_timer.assert_within(5.0)

    @pytest.mark.unit
    @pytest.mark.performance
    async def test_batch_processing_performance(self, video_service, mock_video_processor, performance_timer):
        """Test batch processing performance"""
        with patch.object(video_service, 'processor', mock_video_processor):
            scenes = [{"scene_number": i} for i in range(10)]
            
            performance_timer.start()
            await video_service.generate_batch(scenes)
            performance_timer.stop()
            
            # Batch should utilize parallel processing
            performance_timer.assert_within(10.0)

    # ==================== Queue Integration Tests ====================

    @pytest.mark.unit
    async def test_submit_to_queue(self, video_service, mock_sqs_client, sample_job):
        """Test submitting job to processing queue"""
        with patch.object(video_service, 'sqs_client', mock_sqs_client):
            job_id = await video_service.submit_job(sample_job)
            
            assert job_id is not None
            mock_sqs_client.send_message.assert_called_once()

    @pytest.mark.unit
    async def test_check_job_status(self, video_service, mock_sqs_client):
        """Test checking job status"""
        with patch.object(video_service, 'sqs_client', mock_sqs_client):
            status = await video_service.get_job_status("job_001")
            
            assert status in ["pending", "processing", "completed", "failed"]

    @pytest.mark.unit
    async def test_cancel_job(self, video_service, mock_sqs_client):
        """Test cancelling a job"""
        with patch.object(video_service, 'sqs_client', mock_sqs_client):
            cancelled = await video_service.cancel_job("job_001")
            
            assert cancelled is True
