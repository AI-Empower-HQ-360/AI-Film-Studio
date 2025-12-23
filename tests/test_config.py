"""Tests for the Config class."""

import pytest
import os
from pathlib import Path
from ai_film_studio.config import Config


@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file."""
    config_file = tmp_path / "config.yaml"
    config_content = """
api_keys:
  openai: test_openai_key
  stability: test_stability_key
output_dir: ./test_output
"""
    config_file.write_text(config_content)
    return config_file


def test_config_initialization():
    """Test Config initializes with defaults."""
    config = Config()
    assert config is not None
    assert 'api_keys' in config.config
    assert 'output_dir' in config.config


def test_config_with_file(temp_config_file):
    """Test Config loads from file."""
    config = Config(str(temp_config_file))
    assert config.get('api_keys.openai') == 'test_openai_key'
    assert config.get('api_keys.stability') == 'test_stability_key'
    assert config.get('output_dir') == './test_output'


def test_config_get_nested():
    """Test getting nested configuration values."""
    config = Config()
    config.set('nested.value.deep', 'test')
    assert config.get('nested.value.deep') == 'test'


def test_config_get_default():
    """Test getting value with default."""
    config = Config()
    assert config.get('nonexistent.key', 'default') == 'default'


def test_config_set():
    """Test setting configuration values."""
    config = Config()
    config.set('test_key', 'test_value')
    assert config.get('test_key') == 'test_value'


def test_config_set_nested():
    """Test setting nested configuration values."""
    config = Config()
    config.set('level1.level2.level3', 'nested_value')
    assert config.get('level1.level2.level3') == 'nested_value'


def test_config_environment_override():
    """Test environment variables override file config."""
    os.environ['OPENAI_API_KEY'] = 'env_key'
    config = Config()
    assert config.get('api_keys.openai') == 'env_key'
    del os.environ['OPENAI_API_KEY']
