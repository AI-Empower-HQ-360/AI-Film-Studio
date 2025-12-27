"""Unit tests for configuration settings"""
import os
import pytest
from pathlib import Path


@pytest.mark.unit
class TestSettings:
    """Tests for configuration settings"""
    
    def test_base_dir_path(self):
        """Test BASE_DIR is correctly set"""
        from src.config.settings import BASE_DIR
        
        assert isinstance(BASE_DIR, Path)
        assert BASE_DIR.exists()
        assert (BASE_DIR / "src").exists()
    
    def test_default_api_host(self, monkeypatch):
        """Test default API_HOST value"""
        # Remove env var if exists
        monkeypatch.delenv("API_HOST", raising=False)
        
        # Re-import to get default value
        import importlib
        import src.config.settings as settings
        importlib.reload(settings)
        
        assert settings.API_HOST == "0.0.0.0"
    
    def test_default_api_port(self, monkeypatch):
        """Test default API_PORT value"""
        monkeypatch.delenv("API_PORT", raising=False)
        
        import importlib
        import src.config.settings as settings
        importlib.reload(settings)
        
        assert settings.API_PORT == 8000
    
    def test_environment_variable_loading(self, monkeypatch):
        """Test environment variables are loaded correctly"""
        monkeypatch.setenv("API_HOST", "localhost")
        monkeypatch.setenv("API_PORT", "9000")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        
        import importlib
        import src.config.settings as settings
        importlib.reload(settings)
        
        assert settings.API_HOST == "localhost"
        assert settings.API_PORT == 9000
        assert settings.LOG_LEVEL == "DEBUG"
    
    def test_default_log_level(self, monkeypatch):
        """Test default LOG_LEVEL value"""
        monkeypatch.delenv("LOG_LEVEL", raising=False)
        
        import importlib
        import src.config.settings as settings
        importlib.reload(settings)
        
        assert settings.LOG_LEVEL == "INFO"
    
    def test_path_configurations(self):
        """Test path configurations are set correctly"""
        from src.config.settings import (
            BASE_DIR, MODEL_DIR, MODEL_CACHE_DIR,
            DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, LOG_DIR
        )
        
        # All should be Path objects
        assert isinstance(MODEL_DIR, Path)
        assert isinstance(MODEL_CACHE_DIR, Path)
        assert isinstance(DATA_DIR, Path)
        assert isinstance(RAW_DATA_DIR, Path)
        assert isinstance(PROCESSED_DATA_DIR, Path)
        assert isinstance(LOG_DIR, Path)
        
        # Check relationships
        assert MODEL_DIR == BASE_DIR / "models"
        assert DATA_DIR == BASE_DIR / "data"
        assert RAW_DATA_DIR == DATA_DIR / "raw"
        assert PROCESSED_DATA_DIR == DATA_DIR / "processed"
        assert LOG_DIR == BASE_DIR / "logs"
    
    def test_model_cache_dir_path(self):
        """Test MODEL_CACHE_DIR path structure"""
        from src.config.settings import BASE_DIR, MODEL_CACHE_DIR
        
        assert MODEL_CACHE_DIR == BASE_DIR / "data" / "model_cache"
    
    def test_api_port_is_integer(self):
        """Test API_PORT is converted to integer"""
        from src.config.settings import API_PORT
        
        assert isinstance(API_PORT, int)
    
    def test_custom_api_port_conversion(self, monkeypatch):
        """Test custom API_PORT is converted to integer"""
        monkeypatch.setenv("API_PORT", "5000")
        
        import importlib
        import src.config.settings as settings
        importlib.reload(settings)
        
        assert settings.API_PORT == 5000
        assert isinstance(settings.API_PORT, int)
