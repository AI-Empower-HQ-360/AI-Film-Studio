"""Configuration settings for AI Film Studio"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# Model Configuration
MODEL_DIR = BASE_DIR / "models"
MODEL_CACHE_DIR = BASE_DIR / "data" / "model_cache"

# Data Configuration
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Generated output
GENERATED_DIR = DATA_DIR / "generated"

# Image Engine Configuration
IMAGE_OUTPUT_DIR = DATA_DIR / "generated" / "images"
IMAGE_DEFAULT_WIDTH = 1024
IMAGE_DEFAULT_HEIGHT = 576
IMAGE_DEFAULT_ASPECT_RATIO = "16:9"

# Model API Keys (load from environment)
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LEONARDO_API_KEY = os.getenv("LEONARDO_API_KEY", "")
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY", "")

# Default Model Provider
DEFAULT_MODEL_PROVIDER = os.getenv("DEFAULT_MODEL_PROVIDER", "sdxl")

# Generation Parameters
DEFAULT_GENERATION_STEPS = int(os.getenv("DEFAULT_GENERATION_STEPS", 50))
DEFAULT_CFG_SCALE = float(os.getenv("DEFAULT_CFG_SCALE", 7.5))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = BASE_DIR / "logs"
