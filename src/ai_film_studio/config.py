"""Configuration management for AI Film Studio."""

import os
from pathlib import Path
from typing import Optional
import yaml


class Config:
    """Configuration manager for AI Film Studio settings."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to configuration file. If None, uses default.
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        
    def _get_default_config_path(self) -> Path:
        """Get default configuration file path."""
        return Path.home() / ".ai_film_studio" / "config.yaml"
    
    def _load_config(self) -> dict:
        """Load configuration from file or environment."""
        config = {}
        
        # Load from file if exists
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f) or {}
        
        # Override with environment variables
        config.setdefault('api_keys', {})
        config['api_keys']['openai'] = os.getenv('OPENAI_API_KEY', 
                                                   config['api_keys'].get('openai', ''))
        config['api_keys']['stability'] = os.getenv('STABILITY_API_KEY',
                                                      config['api_keys'].get('stability', ''))
        config['api_keys']['elevenlabs'] = os.getenv('ELEVENLABS_API_KEY',
                                                       config['api_keys'].get('elevenlabs', ''))
        
        # Default settings
        config.setdefault('output_dir', './output')
        config.setdefault('cache_dir', './cache')
        config.setdefault('models', {
            'text_model': 'gpt-4',
            'image_model': 'stable-diffusion-xl',
            'voice_model': 'eleven_monolingual_v1'
        })
        config.setdefault('video', {
            'fps': 24,
            'resolution': '1920x1080',
            'format': 'mp4',
            'codec': 'libx264'
        })
        
        return config
    
    def get(self, key: str, default=None):
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'api_keys.openai')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
                
        return value if value is not None else default
    
    def set(self, key: str, value):
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file."""
        config_dir = os.path.dirname(self.config_path)
        os.makedirs(config_dir, exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
