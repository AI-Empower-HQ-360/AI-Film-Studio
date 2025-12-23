"""Tests for the Pipeline class."""

import pytest
from pathlib import Path
from ai_film_studio.pipeline import Pipeline
from ai_film_studio.config import Config


@pytest.fixture
def pipeline():
    """Create a Pipeline instance for testing."""
    return Pipeline()


@pytest.fixture
def sample_script(tmp_path):
    """Create a sample script file for testing."""
    script_file = tmp_path / "test_script.txt"
    script_file.write_text("""
    INT. COFFEE SHOP - DAY
    
    A young writer sits at a table, typing on a laptop.
    
    WRITER
    This is the beginning of something great.
    """)
    return script_file


def test_pipeline_initialization():
    """Test that Pipeline initializes correctly."""
    pipeline = Pipeline()
    assert pipeline is not None
    assert isinstance(pipeline.config, Config)


def test_pipeline_with_custom_config():
    """Test Pipeline initialization with custom config."""
    config = Config()
    pipeline = Pipeline(config)
    assert pipeline.config == config


def test_generate_with_valid_script(pipeline, sample_script):
    """Test generate method with a valid script."""
    result = pipeline.generate(
        script_path=str(sample_script),
        output_path="output.mp4"
    )
    
    assert result is not None
    assert 'status' in result
    assert 'script_path' in result
    assert 'output_path' in result


def test_generate_with_nonexistent_script(pipeline):
    """Test generate method with nonexistent script."""
    with pytest.raises(FileNotFoundError):
        pipeline.generate(
            script_path="nonexistent.txt",
            output_path="output.mp4"
        )


def test_generate_frames(pipeline, sample_script):
    """Test frame generation method."""
    result = pipeline.generate_frames(
        script_path=str(sample_script),
        output_dir="./frames"
    )
    
    assert result is not None
    assert 'status' in result


def test_analyze_script(pipeline, sample_script):
    """Test script analysis method."""
    result = pipeline.analyze_script(str(sample_script))
    
    assert result is not None
    assert 'status' in result
