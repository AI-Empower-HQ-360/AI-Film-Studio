"""
Unit Tests for Voice Synthesis Service
Tests voice generation, cloning, and audio processing
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio


class TestVoiceSynthesisService:
    """Test suite for Voice Synthesis Service"""

    @pytest.fixture
    def voice_service(self):
        """Create voice service instance"""
        from src.services.voice_synthesis import VoiceSynthesisService
        return VoiceSynthesisService()

    @pytest.fixture
    def mock_voice_engine(self):
        """Mock voice synthesis engine"""
        engine = MagicMock()
        engine.synthesize = AsyncMock(return_value={
            "audio_url": "s3://bucket/audio.wav",
            "duration": 5.0,
            "sample_rate": 44100
        })
        engine.clone_voice = AsyncMock(return_value={
            "voice_id": "cloned_voice_001",
            "status": "ready"
        })
        return engine

    # ==================== Voice Synthesis Tests ====================

    @pytest.mark.unit
    async def test_synthesize_speech(self, voice_service, mock_voice_engine):
        """Test basic speech synthesis"""
        with patch.object(voice_service, 'engine', mock_voice_engine):
            result = await voice_service.synthesize(
                text="Hello, this is a test.",
                voice_id="voice_001"
            )
            
            assert result is not None
            assert 'audio_url' in result
            mock_voice_engine.synthesize.assert_called_once()

    @pytest.mark.unit
    async def test_synthesize_with_emotion(self, voice_service, mock_voice_engine):
        """Test speech synthesis with emotion"""
        with patch.object(voice_service, 'engine', mock_voice_engine):
            result = await voice_service.synthesize(
                text="I'm so happy!",
                voice_id="voice_001",
                emotion="happy",
                emotion_intensity=0.8
            )
            
            assert result is not None

    @pytest.mark.unit
    async def test_synthesize_with_ssml(self, voice_service, mock_voice_engine):
        """Test SSML-enhanced speech synthesis"""
        with patch.object(voice_service, 'engine', mock_voice_engine):
            ssml_text = '<speak><prosody rate="slow">Hello</prosody></speak>'
            result = await voice_service.synthesize(
                text=ssml_text,
                voice_id="voice_001",
                use_ssml=True
            )
            
            assert result is not None

    @pytest.mark.unit
    async def test_synthesize_multilingual(self, voice_service, mock_voice_engine):
        """Test multilingual speech synthesis"""
        with patch.object(voice_service, 'engine', mock_voice_engine):
            result = await voice_service.synthesize(
                text="Bonjour, comment allez-vous?",
                voice_id="voice_001",
                language="fr"
            )
            
            assert result is not None

    @pytest.mark.unit
    async def test_batch_synthesis(self, voice_service, mock_voice_engine):
        """Test batch speech synthesis"""
        with patch.object(voice_service, 'engine', mock_voice_engine):
            texts = [
                {"text": "First line", "voice_id": "voice_001"},
                {"text": "Second line", "voice_id": "voice_002"},
                {"text": "Third line", "voice_id": "voice_001"}
            ]
            results = await voice_service.synthesize_batch(texts)
            
            assert len(results) == 3

    # ==================== Voice Cloning Tests ====================

    @pytest.mark.unit
    async def test_clone_voice(self, voice_service, mock_voice_engine, sample_audio_file):
        """Test voice cloning from audio sample"""
        with patch.object(voice_service, 'engine', mock_voice_engine):
            result = await voice_service.clone_voice(
                audio_samples=[sample_audio_file],
                voice_name="Custom Voice"
            )
            
            assert result is not None
            assert 'voice_id' in result

    @pytest.mark.unit
    async def test_clone_voice_multiple_samples(self, voice_service, mock_voice_engine, temp_directory):
        """Test voice cloning with multiple samples"""
        import os
        # Create multiple sample files
        samples = []
        for i in range(3):
            path = os.path.join(temp_directory, f"sample_{i}.wav")
            with open(path, "wb") as f:
                f.write(b"fake audio data")
            samples.append(path)
        
        with patch.object(voice_service, 'engine', mock_voice_engine):
            result = await voice_service.clone_voice(
                audio_samples=samples,
                voice_name="Multi-Sample Voice"
            )
            
            assert result is not None

    @pytest.mark.unit
    async def test_fine_tune_cloned_voice(self, voice_service, mock_voice_engine):
        """Test fine-tuning a cloned voice"""
        mock_voice_engine.fine_tune = AsyncMock(return_value={"status": "tuned"})
        
        with patch.object(voice_service, 'engine', mock_voice_engine):
            result = await voice_service.fine_tune_voice(
                voice_id="cloned_voice_001",
                parameters={"pitch_shift": 0.5, "speed": 1.1}
            )
            
            assert result is not None

    # ==================== Voice Management Tests ====================

    @pytest.mark.unit
    def test_list_available_voices(self, voice_service, mock_elevenlabs_client):
        """Test listing available voices"""
        with patch.object(voice_service, 'client', mock_elevenlabs_client):
            voices = voice_service.list_voices()
            
            assert isinstance(voices, list)
            assert len(voices) > 0

    @pytest.mark.unit
    def test_get_voice_info(self, voice_service, mock_elevenlabs_client):
        """Test getting voice information"""
        mock_elevenlabs_client.voices.get = MagicMock(return_value={
            "voice_id": "voice_001",
            "name": "Test Voice",
            "category": "premade"
        })
        
        with patch.object(voice_service, 'client', mock_elevenlabs_client):
            info = voice_service.get_voice_info("voice_001")
            
            assert info['voice_id'] == "voice_001"
            assert 'name' in info

    @pytest.mark.unit
    async def test_delete_cloned_voice(self, voice_service, mock_voice_engine):
        """Test deleting a cloned voice"""
        mock_voice_engine.delete_voice = AsyncMock(return_value=True)
        
        with patch.object(voice_service, 'engine', mock_voice_engine):
            deleted = await voice_service.delete_voice("cloned_voice_001")
            
            assert deleted is True

    # ==================== Audio Processing Tests ====================

    @pytest.mark.unit
    async def test_normalize_audio(self, voice_service, sample_audio_file):
        """Test audio normalization"""
        result = await voice_service.normalize_audio(sample_audio_file)
        
        assert result is not None

    @pytest.mark.unit
    async def test_trim_silence(self, voice_service, sample_audio_file):
        """Test silence trimming"""
        result = await voice_service.trim_silence(
            audio_path=sample_audio_file,
            threshold=-40
        )
        
        assert result is not None

    @pytest.mark.unit
    async def test_apply_audio_effects(self, voice_service, sample_audio_file):
        """Test applying audio effects"""
        effects = ["reverb", "compression", "eq"]
        result = await voice_service.apply_effects(
            audio_path=sample_audio_file,
            effects=effects
        )
        
        assert result is not None

    @pytest.mark.unit
    async def test_merge_audio_tracks(self, voice_service, temp_directory):
        """Test merging multiple audio tracks"""
        import os
        tracks = []
        for i in range(3):
            path = os.path.join(temp_directory, f"track_{i}.wav")
            with open(path, "wb") as f:
                f.write(b"fake audio")
            tracks.append(path)
        
        result = await voice_service.merge_tracks(tracks)
        
        assert result is not None

    # ==================== Voice Settings Tests ====================

    @pytest.mark.unit
    def test_set_voice_parameters(self, voice_service):
        """Test setting voice parameters"""
        params = {
            "stability": 0.7,
            "similarity_boost": 0.8,
            "style": 0.5,
            "use_speaker_boost": True
        }
        result = voice_service.set_voice_parameters("voice_001", params)
        
        assert result is not None

    @pytest.mark.unit
    def test_validate_voice_parameters(self, voice_service):
        """Test voice parameter validation"""
        valid_params = {"stability": 0.5, "similarity_boost": 0.7}
        assert voice_service.validate_parameters(valid_params) is True
        
        invalid_params = {"stability": 1.5}  # Out of range
        assert voice_service.validate_parameters(invalid_params) is False

    # ==================== Error Handling Tests ====================

    @pytest.mark.unit
    async def test_handle_empty_text(self, voice_service):
        """Test handling empty text input"""
        with pytest.raises(ValueError):
            await voice_service.synthesize(text="", voice_id="voice_001")

    @pytest.mark.unit
    async def test_handle_invalid_voice_id(self, voice_service, mock_voice_engine):
        """Test handling invalid voice ID"""
        mock_voice_engine.synthesize = AsyncMock(side_effect=ValueError("Voice not found"))
        
        with patch.object(voice_service, 'engine', mock_voice_engine):
            with pytest.raises(ValueError):
                await voice_service.synthesize(
                    text="Hello",
                    voice_id="invalid_voice"
                )

    @pytest.mark.unit
    async def test_handle_rate_limit(self, voice_service, mock_voice_engine):
        """Test handling API rate limits"""
        mock_voice_engine.synthesize = AsyncMock(side_effect=Exception("Rate limit exceeded"))
        
        with patch.object(voice_service, 'engine', mock_voice_engine):
            with pytest.raises(Exception):
                await voice_service.synthesize(
                    text="Hello",
                    voice_id="voice_001"
                )

    @pytest.mark.unit
    async def test_handle_audio_too_long(self, voice_service, mock_voice_engine):
        """Test handling audio that's too long"""
        long_text = "word " * 10000  # Very long text
        
        mock_voice_engine.synthesize = AsyncMock(side_effect=ValueError("Text too long"))
        
        with patch.object(voice_service, 'engine', mock_voice_engine):
            with pytest.raises(ValueError):
                await voice_service.synthesize(
                    text=long_text,
                    voice_id="voice_001"
                )

    # ==================== Queue Integration Tests ====================

    @pytest.mark.unit
    async def test_submit_synthesis_job(self, voice_service, mock_sqs_client):
        """Test submitting synthesis job to queue"""
        with patch.object(voice_service, 'sqs_client', mock_sqs_client):
            job_id = await voice_service.submit_job({
                "text": "Hello world",
                "voice_id": "voice_001"
            })
            
            assert job_id is not None

    @pytest.mark.unit
    async def test_get_synthesis_job_status(self, voice_service, mock_sqs_client):
        """Test getting synthesis job status"""
        with patch.object(voice_service, 'sqs_client', mock_sqs_client):
            status = await voice_service.get_job_status("job_001")
            
            assert status in ["pending", "processing", "completed", "failed"]

    # ==================== Performance Tests ====================

    @pytest.mark.unit
    @pytest.mark.performance
    async def test_synthesis_performance(self, voice_service, mock_voice_engine, performance_timer):
        """Test synthesis performance"""
        with patch.object(voice_service, 'engine', mock_voice_engine):
            performance_timer.start()
            
            await voice_service.synthesize(
                text="This is a performance test.",
                voice_id="voice_001"
            )
            
            performance_timer.stop()
            performance_timer.assert_within(2.0)

    @pytest.mark.unit
    @pytest.mark.performance
    async def test_batch_synthesis_performance(self, voice_service, mock_voice_engine, performance_timer):
        """Test batch synthesis performance"""
        with patch.object(voice_service, 'engine', mock_voice_engine):
            texts = [{"text": f"Line {i}", "voice_id": "voice_001"} for i in range(20)]
            
            performance_timer.start()
            await voice_service.synthesize_batch(texts)
            performance_timer.stop()
            
            performance_timer.assert_within(10.0)
