"""
Tests for script module.
"""

import pytest
from ai_film_studio.script import ScriptParser, ScriptGenerator


class TestScriptParser:
    """Test cases for ScriptParser."""

    def test_parser_initialization(self) -> None:
        """Test that parser initializes correctly."""
        parser = ScriptParser()
        assert parser is not None
        assert parser.scenes == []

    def test_parse_empty_script(self) -> None:
        """Test parsing an empty script."""
        parser = ScriptParser()
        scenes = parser.parse("")
        assert scenes == []


class TestScriptGenerator:
    """Test cases for ScriptGenerator."""

    def test_generator_initialization(self) -> None:
        """Test that generator initializes correctly."""
        generator = ScriptGenerator()
        assert generator is not None
        assert generator.model == "default"

    def test_generator_with_custom_model(self) -> None:
        """Test generator with custom model."""
        generator = ScriptGenerator(model="gpt-4")
        assert generator.model == "gpt-4"
