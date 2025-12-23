"""
Tests for the Film Pipeline.
"""

import pytest
from ai_film_studio import FilmPipeline
from ai_film_studio.utils import Config


class TestFilmPipeline:
    """Test cases for FilmPipeline."""

    def test_pipeline_initialization(self) -> None:
        """Test that pipeline initializes correctly."""
        pipeline = FilmPipeline()
        assert pipeline is not None
        assert pipeline.script_parser is not None
        assert pipeline.scene_analyzer is not None
        assert pipeline.shot_generator is not None
        assert pipeline.video_assembler is not None
        assert pipeline.exporter is not None

    def test_pipeline_with_config(self) -> None:
        """Test pipeline initialization with config."""
        config = Config()
        config.set("output.format", "mp4")
        pipeline = FilmPipeline(config=config)
        assert pipeline.config is not None
