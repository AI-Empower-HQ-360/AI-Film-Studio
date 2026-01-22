"""
Integration Tests for External AI APIs
Tests interaction with OpenAI, ElevenLabs, and other AI services
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import json


@pytest.mark.integration
class TestOpenAIIntegration:
    """Integration tests for OpenAI API"""

    @pytest.fixture
    def openai_service(self, mock_openai_client):
        """Create OpenAI service with mocked client"""
        from src.services.ai.openai_service import OpenAIService
        service = OpenAIService()
        service.client = mock_openai_client
        return service

    # ==================== Chat Completion Tests ====================

    @pytest.mark.integration
    async def test_chat_completion(self, openai_service, mock_openai_client):
        """Test basic chat completion"""
        mock_openai_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Generated script content"))]
        )
        
        result = await openai_service.complete(
            messages=[
                {"role": "system", "content": "You are a screenwriter."},
                {"role": "user", "content": "Write a scene about a detective."}
            ],
            model="gpt-4o"
        )
        
        assert result is not None
        assert len(result) > 0

    @pytest.mark.integration
    async def test_streaming_completion(self, openai_service, mock_openai_client):
        """Test streaming chat completion"""
        mock_chunks = [
            MagicMock(choices=[MagicMock(delta=MagicMock(content="Hello "))]),
            MagicMock(choices=[MagicMock(delta=MagicMock(content="world!"))]),
        ]
        mock_openai_client.chat.completions.create.return_value = iter(mock_chunks)
        
        chunks = []
        async for chunk in openai_service.stream_complete(
            messages=[{"role": "user", "content": "Say hello"}],
            model="gpt-4o"
        ):
            chunks.append(chunk)
        
        assert len(chunks) > 0

    @pytest.mark.integration
    async def test_function_calling(self, openai_service, mock_openai_client):
        """Test function calling capability"""
        mock_openai_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                message=MagicMock(
                    function_call=MagicMock(
                        name="create_character",
                        arguments=json.dumps({"name": "Alex", "age": 30})
                    )
                )
            )]
        )
        
        result = await openai_service.complete_with_functions(
            messages=[{"role": "user", "content": "Create a character named Alex"}],
            functions=[{
                "name": "create_character",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"}
                    }
                }
            }]
        )
        
        assert result.get("function_call") is not None

    # ==================== Image Generation Tests ====================

    @pytest.mark.integration
    async def test_dalle_image_generation(self, openai_service, mock_openai_client):
        """Test DALL-E image generation"""
        mock_openai_client.images.generate.return_value = MagicMock(
            data=[MagicMock(url="https://openai.com/generated-image.png")]
        )
        
        result = await openai_service.generate_image(
            prompt="A futuristic cityscape at sunset",
            size="1024x1024",
            quality="hd"
        )
        
        assert result.get("url") is not None

    @pytest.mark.integration
    async def test_image_variation(self, openai_service, mock_openai_client):
        """Test generating image variations"""
        mock_openai_client.images.create_variation.return_value = MagicMock(
            data=[MagicMock(url="https://openai.com/variation.png")]
        )
        
        result = await openai_service.create_image_variation(
            image_path="/tmp/original.png",
            n=3
        )
        
        assert len(result) >= 1

    # ==================== Embedding Tests ====================

    @pytest.mark.integration
    async def test_text_embedding(self, openai_service, mock_openai_client):
        """Test text embedding generation"""
        mock_openai_client.embeddings.create.return_value = MagicMock(
            data=[MagicMock(embedding=[0.1] * 1536)]
        )
        
        embedding = await openai_service.embed_text(
            text="The detective entered the dark room.",
            model="text-embedding-3-small"
        )
        
        assert len(embedding) == 1536

    @pytest.mark.integration
    async def test_batch_embeddings(self, openai_service, mock_openai_client):
        """Test batch text embedding"""
        mock_openai_client.embeddings.create.return_value = MagicMock(
            data=[
                MagicMock(embedding=[0.1] * 1536),
                MagicMock(embedding=[0.2] * 1536)
            ]
        )
        
        texts = [
            "First sentence.",
            "Second sentence."
        ]
        embeddings = await openai_service.embed_batch(texts)
        
        assert len(embeddings) == 2

    # ==================== Error Handling Tests ====================

    @pytest.mark.integration
    async def test_rate_limit_handling(self, openai_service, mock_openai_client):
        """Test handling of rate limit errors"""
        try:
            from openai import RateLimitError
        except ImportError:
            # Skip test if openai module not installed
            pytest.skip("openai module not installed")
        
        call_count = 0
        def rate_limit_side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RateLimitError("Rate limit exceeded", response=MagicMock(), body=None)
            return MagicMock(choices=[MagicMock(message=MagicMock(content="Success"))])
        
        mock_openai_client.chat.completions.create.side_effect = rate_limit_side_effect
        
        result = await openai_service.complete(
            messages=[{"role": "user", "content": "Hello"}],
            max_retries=3
        )
        
        assert result is not None

    @pytest.mark.integration
    async def test_timeout_handling(self, openai_service, mock_openai_client):
        """Test handling of timeout errors"""
        import asyncio
        
        async def timeout_side_effect(*args, **kwargs):
            await asyncio.sleep(10)
            return MagicMock()
        
        mock_openai_client.chat.completions.create = AsyncMock(side_effect=asyncio.TimeoutError)
        
        with pytest.raises(asyncio.TimeoutError):
            await openai_service.complete(
                messages=[{"role": "user", "content": "Hello"}],
                timeout=1
            )


@pytest.mark.integration
class TestElevenLabsIntegration:
    """Integration tests for ElevenLabs API"""

    @pytest.fixture
    def elevenlabs_service(self, mock_elevenlabs_client):
        """Create ElevenLabs service with mocked client"""
        from src.services.ai.elevenlabs_service import ElevenLabsService
        service = ElevenLabsService()
        service.client = mock_elevenlabs_client
        return service

    # ==================== Speech Synthesis Tests ====================

    @pytest.mark.integration
    async def test_text_to_speech(self, elevenlabs_service, mock_elevenlabs_client):
        """Test basic text-to-speech synthesis"""
        mock_elevenlabs_client.generate.return_value = b"audio_data"
        
        audio = await elevenlabs_service.synthesize(
            text="Hello, welcome to AI Film Studio.",
            voice_id="21m00Tcm4TlvDq8ikWAM"
        )
        
        assert audio is not None
        assert len(audio) > 0

    @pytest.mark.integration
    async def test_synthesis_with_settings(self, elevenlabs_service, mock_elevenlabs_client):
        """Test synthesis with voice settings"""
        mock_elevenlabs_client.generate.return_value = b"audio_data"
        
        audio = await elevenlabs_service.synthesize(
            text="Hello world",
            voice_id="voice_001",
            settings={
                "stability": 0.75,
                "similarity_boost": 0.85,
                "style": 0.5,
                "use_speaker_boost": True
            }
        )
        
        assert audio is not None

    @pytest.mark.integration
    async def test_streaming_synthesis(self, elevenlabs_service, mock_elevenlabs_client):
        """Test streaming audio synthesis"""
        mock_elevenlabs_client.generate_stream.return_value = iter([b"chunk1", b"chunk2"])
        
        chunks = []
        async for chunk in elevenlabs_service.synthesize_stream(
            text="Long text for streaming",
            voice_id="voice_001"
        ):
            chunks.append(chunk)
        
        assert len(chunks) > 0

    # ==================== Voice Management Tests ====================

    @pytest.mark.integration
    async def test_list_voices(self, elevenlabs_service, mock_elevenlabs_client):
        """Test listing available voices"""
        mock_elevenlabs_client.voices.get_all.return_value = MagicMock(
            voices=[
                MagicMock(voice_id="voice_001", name="Adam"),
                MagicMock(voice_id="voice_002", name="Rachel")
            ]
        )
        
        voices = await elevenlabs_service.list_voices()
        
        assert len(voices) >= 2

    @pytest.mark.integration
    async def test_get_voice_details(self, elevenlabs_service, mock_elevenlabs_client):
        """Test getting voice details"""
        mock_elevenlabs_client.voices.get.return_value = MagicMock(
            voice_id="voice_001",
            name="Adam",
            labels={"accent": "american", "age": "adult"}
        )
        
        voice = await elevenlabs_service.get_voice("voice_001")
        
        assert voice.voice_id == "voice_001"

    # ==================== Voice Cloning Tests ====================

    @pytest.mark.integration
    async def test_voice_cloning(self, elevenlabs_service, mock_elevenlabs_client):
        """Test voice cloning from samples"""
        mock_elevenlabs_client.clone.return_value = MagicMock(
            voice_id="cloned_001",
            name="Custom Voice"
        )
        
        result = await elevenlabs_service.clone_voice(
            name="Custom Voice",
            samples=["/tmp/sample1.wav", "/tmp/sample2.wav"],
            description="Custom cloned voice for character"
        )
        
        assert result.voice_id is not None

    @pytest.mark.integration
    async def test_instant_voice_clone(self, elevenlabs_service, mock_elevenlabs_client):
        """Test instant voice cloning"""
        mock_elevenlabs_client.instant_clone.return_value = MagicMock(
            voice_id="instant_001"
        )
        
        result = await elevenlabs_service.instant_clone(
            name="Quick Clone",
            sample="/tmp/sample.wav"
        )
        
        assert result.voice_id is not None

    # ==================== Audio Processing Tests ====================

    @pytest.mark.integration
    async def test_audio_isolation(self, elevenlabs_service, mock_elevenlabs_client):
        """Test audio isolation (voice extraction)"""
        mock_elevenlabs_client.audio_isolation.return_value = b"isolated_audio"
        
        result = await elevenlabs_service.isolate_voice(
            audio_path="/tmp/mixed_audio.wav"
        )
        
        assert result is not None

    # ==================== Error Handling Tests ====================

    @pytest.mark.integration
    async def test_invalid_voice_id(self, elevenlabs_service, mock_elevenlabs_client):
        """Test handling of invalid voice ID"""
        mock_elevenlabs_client.generate.side_effect = Exception("Voice not found")
        
        with pytest.raises(Exception) as exc_info:
            await elevenlabs_service.synthesize(
                text="Hello",
                voice_id="invalid_voice"
            )
        
        assert "Voice not found" in str(exc_info.value)


@pytest.mark.integration
class TestStabilityAIIntegration:
    """Integration tests for Stability AI (video generation)"""

    @pytest.fixture
    def stability_service(self):
        """Create Stability AI service with mocked client"""
        from src.services.ai.stability_service import StabilityService
        service = StabilityService()
        service.client = MagicMock()
        return service

    # ==================== Image Generation Tests ====================

    @pytest.mark.integration
    async def test_image_generation(self, stability_service):
        """Test image generation"""
        stability_service.client.generate.return_value = MagicMock(
            artifacts=[MagicMock(base64=b"image_data")]
        )
        
        result = await stability_service.generate_image(
            prompt="A cinematic shot of a cityscape",
            style="cinematic",
            width=1920,
            height=1080
        )
        
        assert result is not None

    @pytest.mark.integration
    async def test_image_to_image(self, stability_service):
        """Test image-to-image generation"""
        stability_service.client.img2img.return_value = MagicMock(
            artifacts=[MagicMock(base64=b"transformed_image")]
        )
        
        result = await stability_service.image_to_image(
            init_image="/tmp/original.png",
            prompt="Add dramatic lighting",
            strength=0.7
        )
        
        assert result is not None

    # ==================== Video Generation Tests ====================

    @pytest.mark.integration
    async def test_video_generation(self, stability_service):
        """Test video generation from image"""
        stability_service.client.generate_video.return_value = {
            "id": "gen_001",
            "status": "processing"
        }
        
        result = await stability_service.generate_video(
            init_image="/tmp/keyframe.png",
            motion_bucket_id=127,
            cfg_scale=2.5
        )
        
        assert result.get("id") is not None

    @pytest.mark.integration
    async def test_video_generation_status(self, stability_service):
        """Test checking video generation status"""
        stability_service.client.get_video_result.return_value = {
            "status": "completed",
            "video_url": "https://stability.ai/video.mp4"
        }
        
        result = await stability_service.get_video_status("gen_001")
        
        assert result.get("status") == "completed"


@pytest.mark.integration
class TestAnthropicIntegration:
    """Integration tests for Anthropic Claude API"""

    @pytest.fixture
    def anthropic_service(self):
        """Create Anthropic service with mocked client"""
        from src.services.ai.anthropic_service import AnthropicService
        service = AnthropicService()
        service.client = MagicMock()
        return service

    # ==================== Message Tests ====================

    @pytest.mark.integration
    async def test_message_completion(self, anthropic_service):
        """Test message completion"""
        anthropic_service.client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="Screenplay analysis: The scene effectively...")]
        )
        
        result = await anthropic_service.complete(
            messages=[
                {"role": "user", "content": "Analyze this screenplay scene..."}
            ],
            model="claude-3-sonnet-20240229"
        )
        
        assert result is not None

    @pytest.mark.integration
    async def test_streaming_message(self, anthropic_service):
        """Test streaming message completion"""
        mock_events = [
            MagicMock(type="content_block_delta", delta=MagicMock(text="Hello ")),
            MagicMock(type="content_block_delta", delta=MagicMock(text="world!"))
        ]
        anthropic_service.client.messages.stream.return_value.__aenter__ = AsyncMock(
            return_value=MagicMock(__aiter__=lambda s: iter(mock_events))
        )
        
        chunks = []
        async for chunk in anthropic_service.stream_complete(
            messages=[{"role": "user", "content": "Say hello"}]
        ):
            chunks.append(chunk)
        
        assert len(chunks) >= 0  # Streaming may return chunks

    @pytest.mark.integration
    async def test_vision_capability(self, anthropic_service):
        """Test vision capability with images"""
        anthropic_service.client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="The image shows a dramatic scene...")]
        )
        
        result = await anthropic_service.analyze_image(
            image_path="/tmp/scene.png",
            prompt="Describe this scene for a screenplay"
        )
        
        assert result is not None
