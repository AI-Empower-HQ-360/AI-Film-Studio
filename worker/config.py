from pydantic_settings import BaseSettings
from typing import Optional


class WorkerSettings(BaseSettings):
    """Worker configuration settings"""
    
    # Celery/Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # API connection
    BACKEND_API_URL: str = "http://localhost:8000/api/v1"
    
    # GPU settings
    DEVICE: str = "cuda"  # cuda, cpu, or mps
    GPU_MEMORY_FRACTION: float = 0.8
    
    # Generation settings
    IMAGE_WIDTH: int = 1024
    IMAGE_HEIGHT: int = 576
    VIDEO_FPS: int = 24
    VIDEO_DURATION: int = 3  # seconds per scene
    AUDIO_SAMPLE_RATE: int = 44100
    
    # Model paths (can be HuggingFace model IDs or local paths)
    IMAGE_MODEL: str = "stabilityai/stable-diffusion-xl-base-1.0"
    VIDEO_MODEL: str = "stabilityai/stable-video-diffusion-img2vid"
    AUDIO_MODEL: Optional[str] = None  # Placeholder for audio model
    
    # Storage
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: Optional[str] = None
    
    # Output paths
    TEMP_DIR: str = "/tmp/ai_film_studio"
    OUTPUT_DIR: str = "./output"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = WorkerSettings()
