"""
Configuration utilities.
"""

from pathlib import Path
from typing import Any
import json


class Config:
    """Configuration management for AI Film Studio."""

    def __init__(self, config_path: str | Path | None = None) -> None:
        """
        Initialize configuration.

        Args:
            config_path: Path to configuration file.
        """
        self.config_path = Path(config_path) if config_path else None
        self._config: dict[str, Any] = {}
        if self.config_path and self.config_path.exists():
            self.load()

    def load(self) -> None:
        """Load configuration from file."""
        if self.config_path and self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)

    def save(self) -> None:
        """Save configuration to file."""
        if self.config_path:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key (supports dot notation).
            default: Default value if key not found.

        Returns:
            The configuration value or default.
        """
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: Configuration key (supports dot notation).
            value: Value to set.
        """
        keys = key.split(".")
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
