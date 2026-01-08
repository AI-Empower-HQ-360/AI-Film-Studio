"""Configuration settings for AI Film Studio"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent. parent

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

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = BASE_DIR / "logs"

# Salesforce CRM Configuration
SALESFORCE_USERNAME = os.getenv("SALESFORCE_USERNAME", "")
SALESFORCE_PASSWORD = os.getenv("SALESFORCE_PASSWORD", "")
SALESFORCE_SECURITY_TOKEN = os.getenv("SALESFORCE_SECURITY_TOKEN", "")
SALESFORCE_DOMAIN = os.getenv("SALESFORCE_DOMAIN", "login")
SALESFORCE_API_VERSION = os.getenv("SALESFORCE_API_VERSION", "58.0")
SALESFORCE_CONSUMER_KEY = os.getenv("SALESFORCE_CONSUMER_KEY", "")
SALESFORCE_CONSUMER_SECRET = os.getenv("SALESFORCE_CONSUMER_SECRET", "")
SALESFORCE_SYNC_ENABLED = os.getenv("SALESFORCE_SYNC_ENABLED", "false").lower() == "true"
