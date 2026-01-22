"""
Unit Tests for Post-Production Engine
Tests voice, music, audio post, and video composition
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import uuid


@pytest.mark.unit
class TestPostProductionEngine:
    """Test suite for Post-Production Engine functionality"""

    @pytest.fixture
    def postproduction_engine(self):
        """Create a post-production engine instance"""
        from src.engines.postproduction_engine import PostProductionEngine
        return PostProductionEngine()

    @pytest.fixture
    def sample_voice_request(self):
        """Sample voice request"""
        from src.engines.postproduction_engine import SceneAwareVoiceRequest
        return SceneAwareVoiceRequest(
            character_id="char_001",
            dialogue_text="Hello, this is a test.",
            scene_id="scene_001",
            emotion="happy"
        )

    @pytest.fixture
    def sample_music_request(self):
        """Sample music request"""
        from src.engines.postproduction_engine import SceneAwareMusicRequest
        return SceneAwareMusicRequest(
            scene_id="scene_001",
            scene_description="Character enters room",
            duration=10.0,
            emotion="tense",
            intensity=0.7
        )

    @pytest.mark.asyncio
    async def test_generate_character_voice(self, postproduction_engine, sample_voice_request):
        """Test character voice generation"""
        with patch.object(postproduction_engine, 'voice_service') as mock_service:
            mock_response = MagicMock()
            mock_response.audio_url = "s3://audio.wav"
            mock_response.duration = 5.0
            mock_service.synthesize_speech = AsyncMock(return_value=mock_response)
            mock_service.VoiceSynthesisRequest = MagicMock(return_value=MagicMock())
            
            result = await postproduction_engine.generate_character_voice(
                request=sample_voice_request,
                job_id="job_001"
            )
            
            assert result is not None
            assert "audio_url" in result or "job_id" in result

    @pytest.mark.asyncio
    async def test_generate_scene_music(self, postproduction_engine, sample_music_request):
        """Test scene-aware music generation"""
        with patch.object(postproduction_engine, 'music_service') as mock_service:
            mock_response = MagicMock()
            mock_response.audio_url = "s3://music.wav"
            mock_response.duration = 10.0
            mock_service.generate_music = AsyncMock(return_value=mock_response)
            mock_service.MusicGenerationRequest = MagicMock(return_value=MagicMock())
            
            result = await postproduction_engine.generate_scene_music(
                request=sample_music_request,
                job_id="job_001"
            )
            
            assert result is not None
            assert "audio_url" in result or "job_id" in result

    @pytest.mark.asyncio
    async def test_audio_post_processing(self, postproduction_engine):
        """Test audio post-processing"""
        from src.engines.postproduction_engine import AudioPostRequest
        
        request = AudioPostRequest(
            video_id="video_001",
            dialogue_cleanup=True,
            noise_reduction=True,
            loudness_normalization=True,
            target_platform="youtube"
        )
        
        with patch.object(postproduction_engine, 'video_service') as mock_service:
            mock_service.process_audio = AsyncMock(return_value={
                "output_url": "s3://processed.mp4"
            })
            
            result = await postproduction_engine.process_audio_post(
                request=request,
                job_id="job_001"
            )
            
            assert result is not None

    @pytest.mark.asyncio
    async def test_lipsync_generation(self, postproduction_engine):
        """Test lip-sync generation"""
        with patch.object(postproduction_engine, 'lipsync_service') as mock_service:
            mock_response = MagicMock()
            mock_response.output_url = "s3://lipsync.mp4"
            mock_service.generate_lipsync = AsyncMock(return_value=mock_response)
            
            result = await postproduction_engine.generate_lipsync(
                video_id="video_001",
                audio_id="audio_001",
                character_id="char_001",
                job_id="job_001"
            )
            
            assert result is not None or isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_subtitle_generation(self, postproduction_engine):
        """Test subtitle generation"""
        with patch.object(postproduction_engine, 'subtitle_service') as mock_service:
            mock_response = MagicMock()
            mock_response.subtitles = [
                {"start": 0.0, "end": 2.0, "text": "Hello"},
                {"start": 2.0, "end": 4.0, "text": "World"}
            ]
            mock_service.generate_subtitles = AsyncMock(return_value=mock_response)
            
            result = await postproduction_engine.generate_subtitles(
                video_id="video_001",
                language="en",
                job_id="job_001"
            )
            
            assert result is not None or isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_multilingual_subtitles(self, postproduction_engine):
        """Test multilingual subtitle generation"""
        languages = ["en", "es", "fr", "de"]
        
        with patch.object(postproduction_engine, 'subtitle_service') as mock_service:
            mock_response = MagicMock()
            mock_response.subtitles = []
            mock_service.generate_subtitles = AsyncMock(return_value=mock_response)
            
            for lang in languages:
                result = await postproduction_engine.generate_subtitles(
                    video_id="video_001",
                    language=lang,
                    job_id=f"job_{lang}"
                )
                
                assert result is not None or isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_music_dialogue_mixing(self, postproduction_engine):
        """Test automatic music and dialogue mixing"""
        with patch.object(postproduction_engine, 'music_service') as mock_service:
            mock_service.mix = AsyncMock(return_value={
                "output_url": "s3://mixed.wav"
            })
            
            result = await postproduction_engine.mix_audio(
                dialogue_url="s3://dialogue.wav",
                music_url="s3://music.wav",
                dialogue_priority=0.8,
                job_id="job_001"
            )
            
            assert result is not None or isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_platform_specific_mastering(self, postproduction_engine):
        """Test platform-specific audio mastering"""
        platforms = ["youtube", "cinema", "ott", "social"]
        
        for platform in platforms:
            result = await postproduction_engine.master_for_platform(
                audio_url="s3://audio.wav",
                platform=platform,
                job_id=f"job_{platform}"
            )
            
            assert result is not None or isinstance(result, dict)

    def test_voice_request_validation(self, postproduction_engine):
        """Test voice request validation"""
        from src.engines.postproduction_engine import SceneAwareVoiceRequest
        
        # Valid request
        request = SceneAwareVoiceRequest(
            character_id="char_001",
            dialogue_text="Test",
            scene_id="scene_001"
        )
        
        assert request.character_id == "char_001"
        assert request.dialogue_text == "Test"

    def test_music_request_validation(self, postproduction_engine):
        """Test music request validation"""
        from src.engines.postproduction_engine import SceneAwareMusicRequest
        
        # Valid request
        request = SceneAwareMusicRequest(
            scene_id="scene_001",
            scene_description="Test scene",
            duration=10.0,
            emotion="happy",
            intensity=0.5
        )
        
        assert request.scene_id == "scene_001"
        assert request.intensity == 0.5
        assert 0.0 <= request.intensity <= 1.0
