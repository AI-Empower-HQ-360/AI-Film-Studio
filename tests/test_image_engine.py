"""Tests for image engine components"""
import pytest
from src.models.character import Character
from src.models.location import Location
from src.models.shot import Shot
from src.models.asset import Asset
from src.services.prompt_builder import PromptBuilder
from src.services.model_router import ModelRouter, ModelProvider
from src.services.character_consistency import CharacterConsistency
from src.services.location_consistency import LocationConsistency
from src.services.image_engine import ImageEngine


class TestModels:
    """Test data models"""
    
    def test_character_model(self):
        """Test Character model"""
        character = Character(
            name="Radha",
            description="Divine character",
            appearance={"hair": "long black hair", "eyes": "dark brown eyes"},
            attire={"style": "traditional Indian"},
            character_type="main"
        )
        assert character.name == "Radha"
        assert character.appearance["hair"] == "long black hair"
    
    def test_location_model(self):
        """Test Location model"""
        location = Location(
            name="Vrindavan Forest",
            description="Sacred forest",
            location_type="exterior",
            time_of_day="dusk",
            weather="clear"
        )
        assert location.name == "Vrindavan Forest"
        assert location.time_of_day == "dusk"
    
    def test_shot_model(self):
        """Test Shot model"""
        shot = Shot(
            scene_id="scene_001",
            shot_number=1,
            shot_type="close-up",
            description="Test shot",
            style="cinematic",
            lighting="golden-hour"
        )
        assert shot.shot_number == 1
        assert shot.shot_type == "close-up"
    
    def test_asset_model(self):
        """Test Asset model"""
        asset = Asset(
            asset_type="image",
            url="test.png",
            filename="test.png",
            width=1024,
            height=576,
            status="generated"
        )
        assert asset.asset_type == "image"
        assert asset.width == 1024


class TestPromptBuilder:
    """Test PromptBuilder service"""
    
    def test_build_prompt_basic(self):
        """Test basic prompt building"""
        builder = PromptBuilder()
        shot = Shot(
            scene_id="scene_001",
            shot_number=1,
            shot_type="close-up",
            description="Character in forest",
            style="cinematic",
            lighting="natural"
        )
        
        result = builder.build_prompt(shot)
        assert "prompt" in result
        assert "close-up" in result["prompt"]
        assert result["style"] == "cinematic"
    
    def test_build_prompt_with_character(self):
        """Test prompt building with character"""
        builder = PromptBuilder()
        shot = Shot(
            scene_id="scene_001",
            shot_number=1,
            shot_type="medium",
            description="Walking",
            style="cinematic",
            lighting="golden-hour"
        )
        character = Character(
            name="Radha",
            description="Divine character",
            appearance={"hair": "long black hair"}
        )
        
        result = builder.build_prompt(shot, characters=[character])
        assert "Radha" in result["prompt"]
    
    def test_build_prompt_with_location(self):
        """Test prompt building with location"""
        builder = PromptBuilder()
        shot = Shot(
            scene_id="scene_001",
            shot_number=1,
            shot_type="wide",
            description="Scene",
            style="cinematic",
            lighting="natural"
        )
        location = Location(
            name="Forest",
            description="Dense forest",
            location_type="exterior"
        )
        
        result = builder.build_prompt(shot, location=location)
        assert "forest" in result["prompt"].lower()


class TestModelRouter:
    """Test ModelRouter service"""
    
    def test_select_model_by_style(self):
        """Test model selection by style"""
        router = ModelRouter()
        config = router.select_model(style="cinematic")
        assert config["provider"] in ["sdxl", "leonardo"]
    
    def test_select_model_anime_style(self):
        """Test model selection for anime style"""
        router = ModelRouter()
        config = router.select_model(style="anime")
        assert config["provider"] in ["leonardo", "stable-diffusion"]
    
    def test_select_model_with_lora(self):
        """Test model selection requiring LoRA"""
        router = ModelRouter()
        config = router.select_model(
            style="cinematic",
            requires_lora=True
        )
        assert config["capabilities"]["supports_lora"]
    
    def test_fallback_provider(self):
        """Test fallback provider selection"""
        router = ModelRouter()
        fallback = router.get_fallback_provider(ModelProvider.SDXL)
        assert fallback in [ModelProvider.STABLE_DIFFUSION, ModelProvider.LEONARDO]


class TestCharacterConsistency:
    """Test CharacterConsistency service"""
    
    def test_register_character(self):
        """Test character registration"""
        consistency = CharacterConsistency()
        character = Character(
            id="char_001",
            name="Radha",
            description="Test"
        )
        consistency.register_character(character)
        retrieved = consistency.get_character("char_001")
        assert retrieved.name == "Radha"
    
    def test_get_consistency_params(self):
        """Test consistency parameters generation"""
        consistency = CharacterConsistency()
        character = Character(
            id="char_001",
            name="Radha",
            description="Test",
            appearance={"hair": "long black hair"},
            seed=42
        )
        
        params = consistency.get_consistency_params(character)
        assert params["character_name"] == "Radha"
        assert params["seed"] == 42
    
    def test_apply_consistency(self):
        """Test applying consistency to prompt"""
        consistency = CharacterConsistency()
        character = Character(
            id="char_001",
            name="Radha",
            description="Test",
            appearance={"hair": "long black hair"}
        )
        
        prompt = "Character walking"
        gen_params = {}
        
        enhanced_prompt, updated_params = consistency.apply_consistency(
            prompt, character, gen_params
        )
        
        assert "long black hair" in enhanced_prompt


class TestLocationConsistency:
    """Test LocationConsistency service"""
    
    def test_register_location(self):
        """Test location registration"""
        consistency = LocationConsistency()
        location = Location(
            id="loc_001",
            name="Forest",
            description="Test forest",
            location_type="exterior"
        )
        consistency.register_location(location)
        retrieved = consistency.get_location("loc_001")
        assert retrieved.name == "Forest"
    
    def test_get_consistency_params(self):
        """Test consistency parameters generation"""
        consistency = LocationConsistency()
        location = Location(
            id="loc_001",
            name="Forest",
            description="Dense forest",
            location_type="exterior",
            time_of_day="dusk"
        )
        
        params = consistency.get_consistency_params(location)
        assert params["location_name"] == "Forest"
        assert params["time_of_day"] == "dusk"
    
    def test_get_lighting_params(self):
        """Test lighting parameters"""
        consistency = LocationConsistency()
        location = Location(
            id="loc_001",
            name="Forest",
            description="Test",
            location_type="exterior"
        )
        
        params = consistency.get_lighting_params(location, "golden-hour", "clear")
        assert "color_temp" in params
        assert "intensity" in params


class TestImageEngine:
    """Test ImageEngine orchestrator"""
    
    def test_image_engine_initialization(self):
        """Test ImageEngine initialization"""
        engine = ImageEngine()
        assert engine.prompt_builder is not None
        assert engine.model_router is not None
        assert engine.character_consistency is not None
        assert engine.location_consistency is not None
    
    def test_generate_shot_image(self):
        """Test shot image generation"""
        engine = ImageEngine()
        shot = Shot(
            id="shot_001",
            scene_id="scene_001",
            shot_number=1,
            shot_type="close-up",
            description="Test shot",
            style="cinematic",
            lighting="natural"
        )
        
        request = engine.generate_shot_image(shot)
        assert "shot_id" in request
        assert "model_config" in request
        assert "parameters" in request
    
    def test_create_asset_from_generation(self):
        """Test asset creation from generation result"""
        engine = ImageEngine()
        result = {
            "url": "test.png",
            "filename": "test.png",
            "prompt": "test prompt",
            "model": "sdxl",
            "width": 1024,
            "height": 576
        }
        
        asset = engine.create_asset_from_generation(result, "shot_001")
        assert asset.asset_type == "image"
        assert asset.shot_id == "shot_001"
