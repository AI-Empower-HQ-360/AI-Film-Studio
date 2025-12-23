"""
Tests for utility modules.
"""

import pytest
import tempfile
from pathlib import Path

from ai_film_studio.utils import Config, get_logger


class TestConfig:
    """Test cases for Config."""

    def test_config_initialization(self) -> None:
        """Test that config initializes correctly."""
        config = Config()
        assert config is not None

    def test_config_get_set(self) -> None:
        """Test get and set operations."""
        config = Config()
        config.set("test.key", "value")
        assert config.get("test.key") == "value"

    def test_config_get_default(self) -> None:
        """Test get with default value."""
        config = Config()
        assert config.get("nonexistent", "default") == "default"

    def test_config_nested_set(self) -> None:
        """Test nested key setting."""
        config = Config()
        config.set("a.b.c", 123)
        assert config.get("a.b.c") == 123


class TestLogger:
    """Test cases for logger utility."""

    def test_get_logger(self) -> None:
        """Test getting a logger."""
        logger = get_logger("test")
        assert logger is not None
        assert logger.name == "test"
