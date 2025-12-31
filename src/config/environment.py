"""Environment Configuration for AI Film Studio"""
import os
from pathlib import Path
from enum import Enum

class Environment(str, Enum):
    """Environment enumeration"""
    DEVELOPMENT = "development"
    SANDBOX = "sandbox"
    STAGING = "staging"
    PRODUCTION = "production"

# Current environment
CURRENT_ENV = Environment(os.getenv("ENVIRONMENT", "development"))

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/ai_film_studio"
)

# Redis Configuration
REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# S3 Configuration
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "ai-film-studio-media-dev")
S3_CLOUDFRONT_URL = os.getenv("S3_CLOUDFRONT_URL", "https://d1234567890.cloudfront.net")

# SQS Configuration
SQS_QUEUE_URL = os.getenv(
    "SQS_QUEUE_URL",
    "https://sqs.us-east-1.amazonaws.com/.../ai-film-studio-jobs-dev"
)

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here-change-in-production")
JWT_ALGORITHM = "RS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 15
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ElevenLabs Configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Stripe Configuration
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# YouTube Configuration
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")

# Salesforce Configuration
SALESFORCE_INSTANCE_URL = os.getenv("SALESFORCE_INSTANCE_URL")
SALESFORCE_CLIENT_ID = os.getenv("SALESFORCE_CLIENT_ID")
SALESFORCE_CLIENT_SECRET = os.getenv("SALESFORCE_CLIENT_SECRET")
SALESFORCE_USERNAME = os.getenv("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD = os.getenv("SALESFORCE_PASSWORD")

# Model Configuration
MODEL_DIR = BASE_DIR / "models"
MODEL_CACHE_DIR = BASE_DIR / "data" / "model_cache"

# Data Configuration
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = BASE_DIR / "logs"

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Rate Limiting
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

# Environment-specific configurations
ENV_CONFIG = {
    Environment.DEVELOPMENT: {
        "debug": True,
        "gpu_instances_min": 0,
        "gpu_instances_max": 1,
        "monthly_cost_estimate": 335
    },
    Environment.SANDBOX: {
        "debug": True,
        "gpu_instances_min": 0,
        "gpu_instances_max": 2,
        "monthly_cost_estimate": 800
    },
    Environment.STAGING: {
        "debug": False,
        "gpu_instances_min": 1,
        "gpu_instances_max": 5,
        "monthly_cost_estimate": 1500
    },
    Environment.PRODUCTION: {
        "debug": False,
        "gpu_instances_min": 1,
        "gpu_instances_max": 20,
        "monthly_cost_estimate": 2600
    }
}

# Get current environment configuration
CURRENT_CONFIG = ENV_CONFIG[CURRENT_ENV]

# Feature flags
FEATURES = {
    "youtube_integration": os.getenv("FEATURE_YOUTUBE", "true").lower() == "true",
    "salesforce_sync": os.getenv("FEATURE_SALESFORCE", "true").lower() == "true",
    "multi_language": os.getenv("FEATURE_MULTILANG", "true").lower() == "true",
    "podcast_mode": os.getenv("FEATURE_PODCAST", "true").lower() == "true",
    "cultural_audio": os.getenv("FEATURE_CULTURAL_AUDIO", "true").lower() == "true",
}

# Subscription tiers configuration
SUBSCRIPTION_TIERS = {
    "free": {
        "price": 0,
        "credits_per_month": 3,
        "max_duration_minutes": 1,
        "watermark": True,
        "features": ["basic_voices"]
    },
    "standard": {
        "price": 9.99,
        "credits_per_month": 30,
        "max_duration_minutes": 3,
        "watermark": False,
        "features": ["standard_voices", "basic_music"]
    },
    "pro": {
        "price": 29.99,
        "credits_per_month": 100,
        "max_duration_minutes": 5,
        "watermark": False,
        "features": ["premium_voices", "advanced_music", "priority_queue"]
    },
    "enterprise": {
        "price": 299.99,
        "credits_per_month": 999999,
        "max_duration_minutes": 10,
        "watermark": False,
        "features": [
            "premium_voices",
            "advanced_music",
            "priority_queue",
            "white_label",
            "api_access",
            "custom_voices"
        ]
    }
}

# Supported languages
SUPPORTED_LANGUAGES = [
    "en", "es", "fr", "de", "hi", "ta", "te", "bn", "mr", "gu",
    "kn", "ml", "pa", "ja", "zh", "ko", "ar", "pt", "ru", "it"
]

def get_config(key: str, default=None):
    """Get configuration value"""
    return CURRENT_CONFIG.get(key, default)

def is_feature_enabled(feature: str) -> bool:
    """Check if a feature is enabled"""
    return FEATURES.get(feature, False)
