"""
AI Model Configuration Module
Defines configurations for all AI/ML models used in AI Film Studio
"""
from typing import Dict, List, Optional
from enum import Enum

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    # Fallback for testing without pydantic
    HAS_PYDANTIC = False
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    def Field(*args, **kwargs):
        return None


class ModelProvider(str, Enum):
    """AI Model Provider Types"""
    STABILITY_AI = "stability_ai"
    RUNWAYML = "runwayml"
    HUGGINGFACE = "huggingface"
    OPENAI = "openai"
    ELEVENLABS = "elevenlabs"
    COQUI = "coqui"
    AZURE = "azure"
    GOOGLE = "google"
    DEEPL = "deepl"
    META = "meta"
    SELF_HOSTED = "self_hosted"


class VideoModelConfig(BaseModel):
    """Video Generation Model Configuration"""
    name: str
    provider: ModelProvider
    model_id: str
    api_endpoint: Optional[str] = None
    max_duration: int = Field(default=90, description="Maximum video duration in seconds")
    resolution: str = Field(default="1024x576", description="Output resolution")
    fps: int = Field(default=24, description="Frames per second")
    gpu_memory_required: int = Field(default=16, description="GPU memory in GB")
    estimated_time_per_second: float = Field(default=2.0, description="Processing time per second of video")


class VoiceModelConfig(BaseModel):
    """Voice Synthesis Model Configuration"""
    name: str
    provider: ModelProvider
    voice_id: str
    age_group: str  # baby, toddler, child, preteen, teen, young_adult, adult, mature
    gender: str  # male, female
    language: str = "en-US"
    sample_rate: int = Field(default=22050, description="Audio sample rate in Hz")
    supports_emotion: bool = Field(default=False, description="Supports emotion control")
    supports_cloning: bool = Field(default=False, description="Supports voice cloning")


class LipsyncModelConfig(BaseModel):
    """Lip-sync and Face Animation Model Configuration"""
    name: str
    model_id: str
    model_path: Optional[str] = None
    gpu_memory_required: int = Field(default=8, description="GPU memory in GB")
    supports_face_detection: bool = True
    supports_3d_animation: bool = False


class MusicModelConfig(BaseModel):
    """Music and Audio Generation Model Configuration"""
    name: str
    provider: ModelProvider
    model_id: str
    genre_support: List[str] = []
    duration_limit: int = Field(default=300, description="Maximum duration in seconds")
    supports_lyrics: bool = False
    supports_indian_classical: bool = False


class SubtitleModelConfig(BaseModel):
    """Subtitle Generation and Translation Model Configuration"""
    name: str
    provider: ModelProvider
    model_id: str
    supported_languages: List[str] = []
    supports_timestamps: bool = True
    supports_speaker_diarization: bool = False
    accuracy_score: float = Field(default=0.95, ge=0.0, le=1.0)


# Video Generation Models
VIDEO_MODELS = {
    "stable-video-diffusion": VideoModelConfig(
        name="Stable Video Diffusion",
        provider=ModelProvider.STABILITY_AI,
        model_id="stable-video-diffusion-img2vid-xt",
        api_endpoint="https://api.stability.ai/v1/generation",
        max_duration=90,
        resolution="1024x576",
        fps=24,
        gpu_memory_required=16,
        estimated_time_per_second=2.5
    ),
    "gen-2": VideoModelConfig(
        name="RunwayML Gen-2",
        provider=ModelProvider.RUNWAYML,
        model_id="gen-2",
        api_endpoint="https://api.runwayml.com/v1",
        max_duration=60,
        resolution="1280x720",
        fps=30,
        gpu_memory_required=24,
        estimated_time_per_second=3.0
    ),
    "animatediff": VideoModelConfig(
        name="AnimateDiff",
        provider=ModelProvider.HUGGINGFACE,
        model_id="guoyww/animatediff",
        max_duration=120,
        resolution="512x512",
        fps=16,
        gpu_memory_required=12,
        estimated_time_per_second=1.5
    ),
    "cogvideo": VideoModelConfig(
        name="CogVideo",
        provider=ModelProvider.SELF_HOSTED,
        model_id="THUDM/CogVideo",
        max_duration=60,
        resolution="480x480",
        fps=8,
        gpu_memory_required=20,
        estimated_time_per_second=4.0
    )
}

# Voice Synthesis Models - Baby Category
VOICE_MODELS_BABY = {
    "baby_boy_1": VoiceModelConfig(
        name="Baby Boy Voice 1",
        provider=ModelProvider.ELEVENLABS,
        voice_id="baby_boy_gentle_1",
        age_group="baby",
        gender="male",
        language="en-US",
        supports_emotion=False
    ),
    "baby_girl_1": VoiceModelConfig(
        name="Baby Girl Voice 1",
        provider=ModelProvider.ELEVENLABS,
        voice_id="baby_girl_gentle_1",
        age_group="baby",
        gender="female",
        language="en-US",
        supports_emotion=False
    )
}

# Voice Synthesis Models - Toddler Category
VOICE_MODELS_TODDLER = {
    "toddler_boy_1": VoiceModelConfig(
        name="Toddler Boy Voice 1",
        provider=ModelProvider.ELEVENLABS,
        voice_id="toddler_boy_playful_1",
        age_group="toddler",
        gender="male",
        language="en-US",
        supports_emotion=True
    ),
    "toddler_girl_1": VoiceModelConfig(
        name="Toddler Girl Voice 1",
        provider=ModelProvider.ELEVENLABS,
        voice_id="toddler_girl_playful_1",
        age_group="toddler",
        gender="female",
        language="en-US",
        supports_emotion=True
    )
}

# Voice Synthesis Models - Child Category (6-9 years)
VOICE_MODELS_CHILD = {
    "child_boy_1": VoiceModelConfig(
        name="Child Boy Voice 1",
        provider=ModelProvider.ELEVENLABS,
        voice_id="child_boy_energetic_1",
        age_group="child",
        gender="male",
        language="en-US",
        supports_emotion=True
    ),
    "child_girl_1": VoiceModelConfig(
        name="Child Girl Voice 1",
        provider=ModelProvider.ELEVENLABS,
        voice_id="child_girl_energetic_1",
        age_group="child",
        gender="female",
        language="en-US",
        supports_emotion=True
    )
}

# Voice Synthesis Models - Pre-teen Category (10-12 years)
VOICE_MODELS_PRETEEN = {
    "preteen_boy_1": VoiceModelConfig(
        name="Pre-teen Boy Voice 1",
        provider=ModelProvider.COQUI,
        voice_id="preteen_boy_1",
        age_group="preteen",
        gender="male",
        language="en-US",
        supports_emotion=True,
        supports_cloning=True
    ),
    "preteen_girl_1": VoiceModelConfig(
        name="Pre-teen Girl Voice 1",
        provider=ModelProvider.COQUI,
        voice_id="preteen_girl_1",
        age_group="preteen",
        gender="female",
        language="en-US",
        supports_emotion=True,
        supports_cloning=True
    )
}

# Voice Synthesis Models - Teen Category (13-17 years)
VOICE_MODELS_TEEN = {
    "teen_boy_1": VoiceModelConfig(
        name="Teen Boy Voice 1",
        provider=ModelProvider.OPENAI,
        voice_id="alloy",
        age_group="teen",
        gender="male",
        language="en-US",
        supports_emotion=False
    ),
    "teen_girl_1": VoiceModelConfig(
        name="Teen Girl Voice 1",
        provider=ModelProvider.OPENAI,
        voice_id="nova",
        age_group="teen",
        gender="female",
        language="en-US",
        supports_emotion=False
    )
}

# Voice Synthesis Models - Young Adult Category (18-24 years)
VOICE_MODELS_YOUNG_ADULT = {
    "young_adult_male_1": VoiceModelConfig(
        name="Young Adult Male Voice 1",
        provider=ModelProvider.ELEVENLABS,
        voice_id="young_male_confident_1",
        age_group="young_adult",
        gender="male",
        language="en-US",
        supports_emotion=True,
        supports_cloning=True
    ),
    "young_adult_female_1": VoiceModelConfig(
        name="Young Adult Female Voice 1",
        provider=ModelProvider.ELEVENLABS,
        voice_id="young_female_confident_1",
        age_group="young_adult",
        gender="female",
        language="en-US",
        supports_emotion=True,
        supports_cloning=True
    )
}

# Voice Synthesis Models - Adult Category (25-45 years)
VOICE_MODELS_ADULT = {
    "adult_male_1": VoiceModelConfig(
        name="Adult Male Voice 1",
        provider=ModelProvider.ELEVENLABS,
        voice_id="adam",
        age_group="adult",
        gender="male",
        language="en-US",
        supports_emotion=True,
        supports_cloning=True
    ),
    "adult_male_2": VoiceModelConfig(
        name="Adult Male Voice 2",
        provider=ModelProvider.AZURE,
        voice_id="en-US-GuyNeural",
        age_group="adult",
        gender="male",
        language="en-US",
        supports_emotion=True
    ),
    "adult_female_1": VoiceModelConfig(
        name="Adult Female Voice 1",
        provider=ModelProvider.ELEVENLABS,
        voice_id="rachel",
        age_group="adult",
        gender="female",
        language="en-US",
        supports_emotion=True,
        supports_cloning=True
    ),
    "adult_female_2": VoiceModelConfig(
        name="Adult Female Voice 2",
        provider=ModelProvider.AZURE,
        voice_id="en-US-JennyNeural",
        age_group="adult",
        gender="female",
        language="en-US",
        supports_emotion=True
    )
}

# Voice Synthesis Models - Mature Category (45+ years)
VOICE_MODELS_MATURE = {
    "mature_male_1": VoiceModelConfig(
        name="Mature Male Voice 1",
        provider=ModelProvider.ELEVENLABS,
        voice_id="sam",
        age_group="mature",
        gender="male",
        language="en-US",
        supports_emotion=True
    ),
    "mature_female_1": VoiceModelConfig(
        name="Mature Female Voice 1",
        provider=ModelProvider.ELEVENLABS,
        voice_id="bella",
        age_group="mature",
        gender="female",
        language="en-US",
        supports_emotion=True
    )
}

# Combine all voice models
VOICE_MODELS = {
    **VOICE_MODELS_BABY,
    **VOICE_MODELS_TODDLER,
    **VOICE_MODELS_CHILD,
    **VOICE_MODELS_PRETEEN,
    **VOICE_MODELS_TEEN,
    **VOICE_MODELS_YOUNG_ADULT,
    **VOICE_MODELS_ADULT,
    **VOICE_MODELS_MATURE
}

# Lip-sync and Animation Models
LIPSYNC_MODELS = {
    "wav2lip": LipsyncModelConfig(
        name="Wav2Lip",
        model_id="Rudrabha/Wav2Lip",
        model_path="models/wav2lip/wav2lip_gan.pth",
        gpu_memory_required=8,
        supports_face_detection=True,
        supports_3d_animation=False
    ),
    "fomm": LipsyncModelConfig(
        name="First Order Motion Model",
        model_id="AliaksandrSiarohin/first-order-model",
        model_path="models/fomm/vox-cpk.pth.tar",
        gpu_memory_required=10,
        supports_face_detection=True,
        supports_3d_animation=True
    ),
    "sadtalker": LipsyncModelConfig(
        name="SadTalker",
        model_id="OpenTalker/SadTalker",
        model_path="models/sadtalker/",
        gpu_memory_required=12,
        supports_face_detection=True,
        supports_3d_animation=True
    )
}

# Music Generation Models
MUSIC_MODELS = {
    "musicgen-small": MusicModelConfig(
        name="MusicGen Small",
        provider=ModelProvider.META,
        model_id="facebook/musicgen-small",
        genre_support=["pop", "rock", "jazz", "classical", "electronic"],
        duration_limit=300,
        supports_lyrics=False
    ),
    "musicgen-medium": MusicModelConfig(
        name="MusicGen Medium",
        provider=ModelProvider.META,
        model_id="facebook/musicgen-medium",
        genre_support=["pop", "rock", "jazz", "classical", "electronic", "ambient"],
        duration_limit=300,
        supports_lyrics=False
    ),
    "audiocraft": MusicModelConfig(
        name="AudioCraft",
        provider=ModelProvider.META,
        model_id="facebook/audiocraft",
        genre_support=["all"],
        duration_limit=600,
        supports_lyrics=False
    ),
    "indian-classical": MusicModelConfig(
        name="Indian Classical Music",
        provider=ModelProvider.SELF_HOSTED,
        model_id="custom/indian-classical-v1",
        genre_support=["carnatic", "hindustani", "devotional", "bhajan"],
        duration_limit=600,
        supports_lyrics=True,
        supports_indian_classical=True
    )
}

# Subtitle and Translation Models
SUBTITLE_MODELS = {
    "whisper-large-v3": SubtitleModelConfig(
        name="Whisper Large V3",
        provider=ModelProvider.OPENAI,
        model_id="openai/whisper-large-v3",
        supported_languages=["en", "hi", "es", "fr", "de", "it", "pt", "ja", "ko", "zh", "ar", "ru"],
        supports_timestamps=True,
        supports_speaker_diarization=False,
        accuracy_score=0.98
    ),
    "google-speech": SubtitleModelConfig(
        name="Google Cloud Speech-to-Text",
        provider=ModelProvider.GOOGLE,
        model_id="google-cloud-speech",
        supported_languages=["en-US", "hi-IN", "es-ES", "fr-FR", "de-DE"],
        supports_timestamps=True,
        supports_speaker_diarization=True,
        accuracy_score=0.96
    ),
    "azure-speech": SubtitleModelConfig(
        name="Azure Speech Services",
        provider=ModelProvider.AZURE,
        model_id="microsoft-azure-speech",
        supported_languages=["en-US", "hi-IN", "ta-IN", "te-IN", "ml-IN"],
        supports_timestamps=True,
        supports_speaker_diarization=True,
        accuracy_score=0.97
    )
}

# Translation Models
TRANSLATION_MODELS = {
    "google-translate": {
        "provider": ModelProvider.GOOGLE,
        "api_endpoint": "https://translation.googleapis.com/language/translate/v2",
        "supported_languages": ["en", "hi", "ta", "te", "ml", "kn", "bn", "mr", "gu", "pa", "ur", "sa"]
    },
    "deepl": {
        "provider": ModelProvider.DEEPL,
        "api_endpoint": "https://api-free.deepl.com/v2/translate",
        "supported_languages": ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "zh"]
    }
}

# GPU Instance Configurations
GPU_INSTANCE_CONFIGS = {
    "g4dn.xlarge": {
        "gpu": "NVIDIA T4",
        "vram_gb": 16,
        "vcpu": 4,
        "ram_gb": 16,
        "cost_per_hour": 0.526,
        "suitable_for": ["video_generation", "lipsync", "music_generation"]
    },
    "g4dn.2xlarge": {
        "gpu": "NVIDIA T4",
        "vram_gb": 16,
        "vcpu": 8,
        "ram_gb": 32,
        "cost_per_hour": 0.752,
        "suitable_for": ["video_generation", "lipsync", "music_generation", "parallel_processing"]
    },
    "g5.xlarge": {
        "gpu": "NVIDIA A10G",
        "vram_gb": 24,
        "vcpu": 4,
        "ram_gb": 16,
        "cost_per_hour": 1.006,
        "suitable_for": ["large_video_generation", "high_quality_rendering", "3d_animation"]
    },
    "p3.2xlarge": {
        "gpu": "NVIDIA V100",
        "vram_gb": 16,
        "vcpu": 8,
        "ram_gb": 61,
        "cost_per_hour": 3.06,
        "suitable_for": ["model_training", "large_batch_processing"]
    }
}

# Job Queue Configuration
JOB_QUEUE_CONFIG = {
    "video_generation": {
        "priority": "high",
        "timeout_seconds": 600,
        "retry_count": 3,
        "required_gpu_vram_gb": 16
    },
    "voice_synthesis": {
        "priority": "high",
        "timeout_seconds": 120,
        "retry_count": 3,
        "required_gpu_vram_gb": 0  # CPU only
    },
    "lipsync_animation": {
        "priority": "medium",
        "timeout_seconds": 300,
        "retry_count": 2,
        "required_gpu_vram_gb": 8
    },
    "music_generation": {
        "priority": "medium",
        "timeout_seconds": 240,
        "retry_count": 2,
        "required_gpu_vram_gb": 8
    },
    "podcast_video": {
        "priority": "medium",
        "timeout_seconds": 900,
        "retry_count": 2,
        "required_gpu_vram_gb": 16
    },
    "subtitle_generation": {
        "priority": "low",
        "timeout_seconds": 180,
        "retry_count": 3,
        "required_gpu_vram_gb": 8
    }
}


def get_video_model(model_name: str) -> VideoModelConfig:
    """Get video model configuration by name"""
    if model_name not in VIDEO_MODELS:
        raise ValueError(f"Video model '{model_name}' not found")
    return VIDEO_MODELS[model_name]


def get_voice_model(voice_id: str) -> VoiceModelConfig:
    """Get voice model configuration by voice ID"""
    if voice_id not in VOICE_MODELS:
        raise ValueError(f"Voice model '{voice_id}' not found")
    return VOICE_MODELS[voice_id]


def get_lipsync_model(model_name: str) -> LipsyncModelConfig:
    """Get lip-sync model configuration by name"""
    if model_name not in LIPSYNC_MODELS:
        raise ValueError(f"Lip-sync model '{model_name}' not found")
    return LIPSYNC_MODELS[model_name]


def get_music_model(model_name: str) -> MusicModelConfig:
    """Get music model configuration by name"""
    if model_name not in MUSIC_MODELS:
        raise ValueError(f"Music model '{model_name}' not found")
    return MUSIC_MODELS[model_name]


def get_subtitle_model(model_name: str) -> SubtitleModelConfig:
    """Get subtitle model configuration by name"""
    if model_name not in SUBTITLE_MODELS:
        raise ValueError(f"Subtitle model '{model_name}' not found")
    return SUBTITLE_MODELS[model_name]


def list_voices_by_age_group(age_group: str) -> List[VoiceModelConfig]:
    """List all voices for a specific age group"""
    return [voice for voice in VOICE_MODELS.values() if voice.age_group == age_group]


def list_voices_by_gender(gender: str) -> List[VoiceModelConfig]:
    """List all voices for a specific gender"""
    return [voice for voice in VOICE_MODELS.values() if voice.gender == gender]


def get_recommended_gpu_instance(job_type: str) -> str:
    """Get recommended GPU instance for a job type"""
    job_config = JOB_QUEUE_CONFIG.get(job_type)
    if not job_config:
        return "g4dn.xlarge"  # Default
    
    required_vram = job_config["required_gpu_vram_gb"]
    
    # Find the most cost-effective instance that meets requirements
    for instance_name, config in GPU_INSTANCE_CONFIGS.items():
        if config["vram_gb"] >= required_vram:
            return instance_name
    
    return "g5.xlarge"  # Fallback to high-end instance
