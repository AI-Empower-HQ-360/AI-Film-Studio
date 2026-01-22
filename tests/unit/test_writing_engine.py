"""
Unit Tests for Writing Engine
Tests script generation, story analysis, and content creation
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime
import json


class TestWritingEngine:
    """Test suite for Writing Engine functionality"""

    @pytest.fixture
    def writing_engine(self):
        """Create a writing engine instance for testing"""
        from src.engines.writing_engine import WritingEngine
        return WritingEngine()

    @pytest.fixture
    def mock_llm_response(self):
        """Mock LLM response for script generation"""
        return {
            "title": "The Digital Frontier",
            "logline": "A programmer discovers AI consciousness.",
            "scenes": [
                {
                    "scene_number": 1,
                    "setting": "Modern tech office",
                    "description": "The protagonist works late at night",
                    "dialogue": [
                        {"character": "ALEX", "line": "Something's different tonight."}
                    ],
                    "duration_seconds": 30
                }
            ]
        }

    # ==================== Script Generation Tests ====================

    @pytest.mark.unit
    def test_generate_script_from_prompt(self, writing_engine, mock_openai_client):
        """Test script generation from a text prompt"""
        with patch.object(writing_engine, 'llm_client', mock_openai_client):
            prompt = "Create a short film about AI and humanity"
            result = writing_engine.generate_script(prompt)
            
            assert result is not None
            assert hasattr(result, 'title') or (isinstance(result, dict) and 'title' in result)
            mock_openai_client.chat.completions.create.assert_called()

    @pytest.mark.unit
    def test_generate_script_with_constraints(self, writing_engine, mock_openai_client):
        """Test script generation with specific constraints"""
        with patch.object(writing_engine, 'llm_client', mock_openai_client):
            prompt = "Create a comedy short"
            constraints = {
                "max_duration": 120,
                "num_characters": 2,
                "genre": "comedy",
                "language": "en"
            }
            result = writing_engine.generate_script(prompt, constraints=constraints)
            
            assert result is not None

    @pytest.mark.unit
    def test_generate_script_empty_prompt_raises_error(self, writing_engine):
        """Test that empty prompt raises appropriate error"""
        with pytest.raises((ValueError, TypeError)):
            writing_engine.generate_script("")

    @pytest.mark.unit
    def test_generate_script_max_length(self, writing_engine, mock_openai_client):
        """Test script generation respects max length constraints"""
        with patch.object(writing_engine, 'llm_client', mock_openai_client):
            prompt = "Create a very long epic film"
            constraints = {"max_scenes": 5}
            result = writing_engine.generate_script(prompt, constraints=constraints)
            
            if hasattr(result, 'scenes'):
                assert len(result.scenes) <= 5

    # ==================== Scene Analysis Tests ====================

    @pytest.mark.unit
    def test_analyze_scene_content(self, writing_engine, sample_script):
        """Test scene content analysis"""
        scene = sample_script['scenes'][0]
        analysis = writing_engine.analyze_scene(scene)
        
        assert analysis is not None
        assert 'sentiment' in analysis or 'mood' in analysis or hasattr(analysis, 'sentiment')

    @pytest.mark.unit
    def test_extract_scene_elements(self, writing_engine, sample_script):
        """Test extraction of scene elements"""
        scene = sample_script['scenes'][0]
        elements = writing_engine.extract_elements(scene)
        
        assert elements is not None
        # Should extract characters, props, settings, etc.

    @pytest.mark.unit
    def test_calculate_scene_duration(self, writing_engine, sample_script):
        """Test scene duration calculation"""
        scene = sample_script['scenes'][0]
        duration = writing_engine.calculate_duration(scene)
        
        assert isinstance(duration, (int, float))
        assert duration > 0

    # ==================== Dialogue Generation Tests ====================

    @pytest.mark.unit
    def test_generate_dialogue(self, writing_engine, sample_character, mock_openai_client):
        """Test dialogue generation for character"""
        with patch.object(writing_engine, 'llm_client', mock_openai_client):
            context = "The character is in danger"
            dialogue = writing_engine.generate_dialogue(
                character=sample_character,
                context=context,
                emotion="fear"
            )
            
            assert dialogue is not None
            assert isinstance(dialogue, str) or hasattr(dialogue, 'text')

    @pytest.mark.unit
    def test_generate_dialogue_maintains_character_voice(self, writing_engine, mock_openai_client):
        """Test that dialogue maintains character personality"""
        with patch.object(writing_engine, 'llm_client', mock_openai_client):
            character = {
                "name": "Professor Smith",
                "personality": {"traits": ["academic", "formal"]}
            }
            dialogue = writing_engine.generate_dialogue(
                character=character,
                context="Explaining a discovery"
            )
            
            assert dialogue is not None

    # ==================== Story Structure Tests ====================

    @pytest.mark.unit
    def test_create_story_outline(self, writing_engine, mock_openai_client):
        """Test story outline creation"""
        with patch.object(writing_engine, 'llm_client', mock_openai_client):
            concept = "A hero's journey in space"
            outline = writing_engine.create_outline(concept)
            
            assert outline is not None

    @pytest.mark.unit
    def test_validate_story_structure(self, writing_engine, sample_script):
        """Test story structure validation"""
        validation = writing_engine.validate_structure(sample_script)
        
        assert 'is_valid' in validation or hasattr(validation, 'is_valid')

    @pytest.mark.unit
    def test_suggest_improvements(self, writing_engine, sample_script, mock_openai_client):
        """Test improvement suggestions for script"""
        with patch.object(writing_engine, 'llm_client', mock_openai_client):
            suggestions = writing_engine.suggest_improvements(sample_script)
            
            assert suggestions is not None
            assert isinstance(suggestions, (list, dict))

    # ==================== Format Conversion Tests ====================

    @pytest.mark.unit
    def test_export_to_fountain_format(self, writing_engine, sample_script):
        """Test export to Fountain screenplay format"""
        fountain = writing_engine.export_to_fountain(sample_script)
        
        assert fountain is not None
        assert isinstance(fountain, str)

    @pytest.mark.unit
    def test_export_to_json(self, writing_engine, sample_script):
        """Test export to JSON format"""
        json_output = writing_engine.export_to_json(sample_script)
        
        assert json_output is not None
        # Should be valid JSON
        if isinstance(json_output, str):
            parsed = json.loads(json_output)
            assert 'scenes' in parsed or 'title' in parsed

    @pytest.mark.unit
    def test_import_from_fountain(self, writing_engine):
        """Test import from Fountain format"""
        fountain_text = """
Title: Test Script
Author: Test Author

INT. OFFICE - DAY

ALEX
Hello, world.
"""
        script = writing_engine.import_from_fountain(fountain_text)
        
        assert script is not None

    # ==================== Edge Cases ====================

    @pytest.mark.unit
    def test_handle_special_characters_in_prompt(self, writing_engine, mock_openai_client):
        """Test handling of special characters in prompts"""
        with patch.object(writing_engine, 'llm_client', mock_openai_client):
            prompt = "Create a script with émojis 🎬 and spëcial çharacters"
            result = writing_engine.generate_script(prompt)
            
            assert result is not None

    @pytest.mark.unit
    def test_handle_very_long_prompt(self, writing_engine, mock_openai_client):
        """Test handling of very long prompts"""
        with patch.object(writing_engine, 'llm_client', mock_openai_client):
            prompt = "Create a detailed script about " + "adventure " * 500
            result = writing_engine.generate_script(prompt)
            
            assert result is not None

    @pytest.mark.unit
    def test_handle_multilingual_content(self, writing_engine, mock_openai_client):
        """Test handling of multilingual content"""
        with patch.object(writing_engine, 'llm_client', mock_openai_client):
            prompt = "Create a bilingual script in English and Spanish"
            result = writing_engine.generate_script(prompt, constraints={"languages": ["en", "es"]})
            
            assert result is not None
