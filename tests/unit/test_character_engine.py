"""
Unit Tests for Character Engine
Tests character creation, management, and AI-driven character features
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime
import json


class TestCharacterEngine:
    """Test suite for Character Engine functionality"""

    @pytest.fixture
    def character_engine(self):
        """Create a character engine instance for testing"""
        from src.engines.character_engine import CharacterEngine
        return CharacterEngine()

    @pytest.fixture
    def mock_image_generator(self):
        """Mock image generation service"""
        generator = MagicMock()
        generator.generate = AsyncMock(return_value={
            "url": "https://example.com/character.png",
            "width": 1024,
            "height": 1024
        })
        return generator

    # ==================== Character Creation Tests ====================

    @pytest.mark.unit
    def test_create_character(self, character_engine, sample_character):
        """Test basic character creation"""
        character = character_engine.create_character(
            name=sample_character['name'],
            description=sample_character['description'],
            appearance=sample_character['appearance']
        )
        
        assert character is not None
        assert character.name == sample_character['name']

    @pytest.mark.unit
    def test_create_character_with_minimal_info(self, character_engine):
        """Test character creation with minimal information"""
        character = character_engine.create_character(
            name="Minimal Character"
        )
        
        assert character is not None
        assert character.name == "Minimal Character"

    @pytest.mark.unit
    def test_create_character_validates_name(self, character_engine):
        """Test that character name is validated"""
        with pytest.raises((ValueError, TypeError)):
            character_engine.create_character(name="")

    @pytest.mark.unit
    def test_create_character_generates_id(self, character_engine):
        """Test that character gets a unique ID"""
        char1 = character_engine.create_character(name="Character 1")
        char2 = character_engine.create_character(name="Character 2")
        
        assert char1.id != char2.id

    # ==================== Character Appearance Tests ====================

    @pytest.mark.unit
    async def test_generate_character_portrait(self, character_engine, sample_character, mock_image_generator):
        """Test character portrait generation"""
        with patch.object(character_engine, 'image_generator', mock_image_generator):
            portrait = await character_engine.generate_portrait(sample_character)
            
            assert portrait is not None
            assert 'url' in portrait
            mock_image_generator.generate.assert_called_once()

    @pytest.mark.unit
    async def test_generate_character_variations(self, character_engine, sample_character, mock_image_generator):
        """Test generating multiple character variations"""
        with patch.object(character_engine, 'image_generator', mock_image_generator):
            variations = await character_engine.generate_variations(
                sample_character,
                num_variations=3
            )
            
            assert len(variations) == 3

    @pytest.mark.unit
    def test_update_character_appearance(self, character_engine, sample_character):
        """Test updating character appearance"""
        character = character_engine.create_character(**sample_character)
        
        new_appearance = {
            "hair_color": "blonde",
            "eye_color": "green"
        }
        updated = character_engine.update_appearance(character.id, new_appearance)
        
        assert updated.appearance['hair_color'] == "blonde"
        assert updated.appearance['eye_color'] == "green"

    # ==================== Character Personality Tests ====================

    @pytest.mark.unit
    def test_set_character_personality(self, character_engine, sample_character):
        """Test setting character personality traits"""
        character = character_engine.create_character(**sample_character)
        
        personality = {
            "traits": ["brave", "witty", "loyal"],
            "motivation": "protect the innocent",
            "fear": "failure"
        }
        updated = character_engine.set_personality(character.id, personality)
        
        assert "brave" in updated.personality['traits']

    @pytest.mark.unit
    def test_analyze_character_personality(self, character_engine, sample_character, mock_openai_client):
        """Test AI-driven personality analysis"""
        with patch.object(character_engine, 'llm_client', mock_openai_client):
            character = character_engine.create_character(**sample_character)
            analysis = character_engine.analyze_personality(character)
            
            assert analysis is not None

    @pytest.mark.unit
    def test_generate_character_backstory(self, character_engine, sample_character, mock_openai_client):
        """Test AI-generated backstory"""
        with patch.object(character_engine, 'llm_client', mock_openai_client):
            character = character_engine.create_character(**sample_character)
            backstory = character_engine.generate_backstory(character)
            
            assert backstory is not None
            assert isinstance(backstory, str)

    # ==================== Character Voice Tests ====================

    @pytest.mark.unit
    def test_assign_voice_to_character(self, character_engine, sample_character):
        """Test voice assignment to character"""
        character = character_engine.create_character(**sample_character)
        
        updated = character_engine.assign_voice(character.id, "voice_001")
        
        assert updated.voice_id == "voice_001"

    @pytest.mark.unit
    def test_get_available_voices(self, character_engine, mock_elevenlabs_client):
        """Test retrieving available voices"""
        with patch.object(character_engine, 'voice_client', mock_elevenlabs_client):
            voices = character_engine.get_available_voices()
            
            assert isinstance(voices, list)
            assert len(voices) > 0

    @pytest.mark.unit
    def test_voice_preview(self, character_engine, sample_character, mock_elevenlabs_client):
        """Test voice preview generation"""
        with patch.object(character_engine, 'voice_client', mock_elevenlabs_client):
            character = character_engine.create_character(**sample_character)
            preview = character_engine.generate_voice_preview(
                character.id,
                text="Hello, this is a voice test."
            )
            
            assert preview is not None

    # ==================== Character Relationship Tests ====================

    @pytest.mark.unit
    def test_create_character_relationship(self, character_engine):
        """Test creating relationships between characters"""
        char1 = character_engine.create_character(name="Character 1")
        char2 = character_engine.create_character(name="Character 2")
        
        relationship = character_engine.create_relationship(
            char1.id,
            char2.id,
            relationship_type="ally"
        )
        
        assert relationship is not None
        assert relationship.type == "ally"

    @pytest.mark.unit
    def test_get_character_relationships(self, character_engine):
        """Test retrieving character relationships"""
        char1 = character_engine.create_character(name="Character 1")
        char2 = character_engine.create_character(name="Character 2")
        char3 = character_engine.create_character(name="Character 3")
        
        character_engine.create_relationship(char1.id, char2.id, "friend")
        character_engine.create_relationship(char1.id, char3.id, "enemy")
        
        relationships = character_engine.get_relationships(char1.id)
        
        assert len(relationships) == 2

    # ==================== Character Animation Tests ====================

    @pytest.mark.unit
    def test_set_character_pose(self, character_engine, sample_character):
        """Test setting character pose"""
        character = character_engine.create_character(**sample_character)
        
        pose = character_engine.set_pose(character.id, "standing_confident")
        
        assert pose is not None

    @pytest.mark.unit
    def test_set_character_expression(self, character_engine, sample_character):
        """Test setting character facial expression"""
        character = character_engine.create_character(**sample_character)
        
        expression = character_engine.set_expression(character.id, "happy")
        
        assert expression is not None

    @pytest.mark.unit
    async def test_generate_animation_frames(self, character_engine, sample_character, mock_image_generator):
        """Test generating animation frames"""
        with patch.object(character_engine, 'image_generator', mock_image_generator):
            character = character_engine.create_character(**sample_character)
            frames = await character_engine.generate_animation(
                character.id,
                animation_type="walk",
                num_frames=8
            )
            
            assert len(frames) == 8

    # ==================== Character Persistence Tests ====================

    @pytest.mark.unit
    def test_save_character(self, character_engine, sample_character, mock_database):
        """Test saving character to database"""
        with patch.object(character_engine, 'db', mock_database):
            character = character_engine.create_character(**sample_character)
            saved = character_engine.save(character)
            
            assert saved is True
            mock_database.execute.assert_called()

    @pytest.mark.unit
    def test_load_character(self, character_engine, mock_database):
        """Test loading character from database"""
        # Create a sync mock for the load operation
        mock_result = MagicMock()
        mock_result.fetchone.return_value = {
            "id": "char_001",
            "name": "Test Character",
            "description": "A test character"
        }
        sync_db = MagicMock()
        sync_db.execute.return_value = mock_result
        
        with patch.object(character_engine, 'db', sync_db):
            character = character_engine.load("char_001")
            
            assert character is not None
            assert character.id == "char_001"

    @pytest.mark.unit
    def test_delete_character(self, character_engine, sample_character, mock_database):
        """Test deleting character"""
        with patch.object(character_engine, 'db', mock_database):
            character = character_engine.create_character(**sample_character)
            deleted = character_engine.delete(character.id)
            
            assert deleted is True

    # ==================== Edge Cases ====================

    @pytest.mark.unit
    def test_handle_duplicate_character_name(self, character_engine):
        """Test handling duplicate character names"""
        char1 = character_engine.create_character(name="Same Name")
        char2 = character_engine.create_character(name="Same Name")
        
        # Should allow same names but different IDs
        assert char1.id != char2.id
        assert char1.name == char2.name

    @pytest.mark.unit
    def test_handle_special_characters_in_name(self, character_engine):
        """Test handling special characters in names"""
        character = character_engine.create_character(
            name="José María O'Brien-石田"
        )
        
        assert character is not None
        assert character.name == "José María O'Brien-石田"

    @pytest.mark.unit
    def test_character_serialization(self, character_engine, sample_character):
        """Test character serialization to dict/JSON"""
        character = character_engine.create_character(**sample_character)
        
        serialized = character_engine.to_dict(character)
        
        assert isinstance(serialized, dict)
        assert 'name' in serialized
        assert 'id' in serialized

    @pytest.mark.unit
    def test_character_cloning(self, character_engine, sample_character):
        """Test cloning a character"""
        original = character_engine.create_character(**sample_character)
        clone = character_engine.clone(original.id, new_name="Clone Character")
        
        assert clone.id != original.id
        assert clone.name == "Clone Character"
        assert clone.appearance == original.appearance
