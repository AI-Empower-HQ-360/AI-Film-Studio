"""
Tests for AI Model Configuration
"""
import pytest
from src.config.ai_models import (
    get_video_model,
    get_voice_model,
    get_lipsync_model,
    get_music_model,
    get_subtitle_model,
    list_voices_by_age_group,
    list_voices_by_gender,
    get_recommended_gpu_instance,
    VIDEO_MODELS,
    VOICE_MODELS,
    LIPSYNC_MODELS,
    MUSIC_MODELS,
    SUBTITLE_MODELS
)


def test_get_video_model():
    """Test getting video model configuration"""
    model = get_video_model("stable-video-diffusion")
    assert model.name == "Stable Video Diffusion"
    assert model.max_duration == 90
    assert model.gpu_memory_required == 16


def test_get_video_model_not_found():
    """Test getting non-existent video model"""
    with pytest.raises(ValueError):
        get_video_model("non-existent-model")


def test_get_voice_model():
    """Test getting voice model configuration"""
    model = get_voice_model("adult_male_1")
    assert model.name == "Adult Male Voice 1"
    assert model.age_group == "adult"
    assert model.gender == "male"


def test_get_voice_model_not_found():
    """Test getting non-existent voice model"""
    with pytest.raises(ValueError):
        get_voice_model("non-existent-voice")


def test_list_voices_by_age_group():
    """Test listing voices by age group"""
    adult_voices = list_voices_by_age_group("adult")
    assert len(adult_voices) > 0
    for voice in adult_voices:
        assert voice.age_group == "adult"


def test_list_voices_by_gender():
    """Test listing voices by gender"""
    male_voices = list_voices_by_gender("male")
    assert len(male_voices) > 0
    for voice in male_voices:
        assert voice.gender == "male"


def test_get_lipsync_model():
    """Test getting lip-sync model configuration"""
    model = get_lipsync_model("wav2lip")
    assert model.name == "Wav2Lip"
    assert model.supports_face_detection is True
    assert model.gpu_memory_required == 8


def test_get_music_model():
    """Test getting music model configuration"""
    model = get_music_model("musicgen-small")
    assert model.name == "MusicGen Small"
    assert "pop" in model.genre_support
    assert model.duration_limit == 300


def test_get_subtitle_model():
    """Test getting subtitle model configuration"""
    model = get_subtitle_model("whisper-large-v3")
    assert model.name == "Whisper Large V3"
    assert "en" in model.supported_languages
    assert model.supports_timestamps is True


def test_get_recommended_gpu_instance():
    """Test GPU instance recommendation"""
    instance = get_recommended_gpu_instance("video_generation")
    assert instance in ["g4dn.xlarge", "g4dn.2xlarge", "g5.xlarge"]


def test_all_video_models_have_required_fields():
    """Test that all video models have required fields"""
    for model_name, model in VIDEO_MODELS.items():
        assert model.name
        assert model.provider
        assert model.model_id
        assert model.max_duration > 0
        assert model.gpu_memory_required > 0


def test_all_voice_models_have_required_fields():
    """Test that all voice models have required fields"""
    for voice_id, voice in VOICE_MODELS.items():
        assert voice.name
        assert voice.provider
        assert voice.voice_id
        assert voice.age_group in ["baby", "toddler", "child", "preteen", "teen", "young_adult", "adult", "mature"]
        assert voice.gender in ["male", "female"]


def test_all_lipsync_models_have_required_fields():
    """Test that all lip-sync models have required fields"""
    for model_name, model in LIPSYNC_MODELS.items():
        assert model.name
        assert model.model_id
        assert model.gpu_memory_required > 0


def test_all_music_models_have_required_fields():
    """Test that all music models have required fields"""
    for model_name, model in MUSIC_MODELS.items():
        assert model.name
        assert model.provider
        assert model.model_id
        assert model.duration_limit > 0


def test_all_subtitle_models_have_required_fields():
    """Test that all subtitle models have required fields"""
    for model_name, model in SUBTITLE_MODELS.items():
        assert model.name
        assert model.provider
        assert model.model_id
        assert len(model.supported_languages) > 0
        assert 0 <= model.accuracy_score <= 1
