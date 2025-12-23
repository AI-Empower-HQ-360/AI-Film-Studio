"""
Core configuration for AI Film Studio backend.
"""
from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Film Studio"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/aifilmstudio"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AWS S3 (for signed URLs)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "ai-film-studio-outputs"
    S3_SIGNED_URL_EXPIRATION: int = 3600  # 1 hour
    
    # Cost Governance
    MAX_COST_PER_JOB: float = 100.0
    MAX_COST_PER_USER_DAILY: float = 500.0
    
    # Job Settings
    MAX_RETRIES: int = 3
    JOB_TIMEOUT_SECONDS: int = 3600
    
    # Moderation
    ENABLE_CONTENT_MODERATION: bool = True
    MODERATION_THRESHOLD: float = 0.8
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
