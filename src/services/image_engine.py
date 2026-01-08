"""Main Image Creation Engine orchestrator"""
from typing import Dict, Any, Optional, List
from src.models.shot import Shot
from src.models.character import Character
from src.models.location import Location
from src.models.asset import Asset
from src.services.prompt_builder import PromptBuilder
from src.services.model_router import ModelRouter, ModelProvider
from src.services.character_consistency import CharacterConsistency
from src.services.location_consistency import LocationConsistency
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageEngine:
    """Main orchestrator for image generation pipeline"""
    
    def __init__(self):
        self.prompt_builder = PromptBuilder()
        self.model_router = ModelRouter()
        self.character_consistency = CharacterConsistency()
        self.location_consistency = LocationConsistency()
    
    def generate_shot_image(
        self,
        shot: Shot,
        characters: Optional[List[Character]] = None,
        location: Optional[Location] = None,
        preferred_provider: Optional[ModelProvider] = None
    ) -> Dict[str, Any]:
        """Generate image for a shot"""
        logger.info(f"Generating image for shot {shot.shot_number}")
        
        # Step 1: Build prompt
        prompt_data = self.prompt_builder.build_prompt(
            shot=shot,
            characters=characters,
            location=location
        )
        base_prompt = prompt_data["prompt"]
        negative_prompt = prompt_data["negative_prompt"]
        
        logger.info(f"Generated prompt: {base_prompt}")
        
        # Step 2: Apply character consistency
        enhanced_prompt = base_prompt
        generation_params = {}
        
        if characters:
            for character in characters:
                self.character_consistency.register_character(character)
                enhanced_prompt, generation_params = \
                    self.character_consistency.apply_consistency(
                        enhanced_prompt, character, generation_params
                    )
        
        # Step 3: Apply location consistency
        if location:
            self.location_consistency.register_location(location)
            enhanced_prompt, generation_params = \
                self.location_consistency.apply_consistency(
                    enhanced_prompt, location, generation_params
                )
        
        # Step 4: Select model
        requires_lora = any(
            char.embedding_id is not None for char in (characters or [])
        )
        
        model_config = self.model_router.select_model(
            style=shot.style,
            resolution=(1024, 576),  # Default cinematic aspect ratio
            requires_lora=requires_lora,
            preferred_provider=preferred_provider
        )
        
        logger.info(f"Selected model: {model_config['provider']}")
        
        # Step 5: Merge generation parameters
        final_params = model_config["default_params"].copy()
        final_params.update(generation_params)
        final_params["prompt"] = enhanced_prompt
        final_params["negative_prompt"] = negative_prompt
        
        # Step 6: Create generation request
        generation_request = {
            "shot_id": shot.id,
            "shot_number": shot.shot_number,
            "model_config": model_config,
            "parameters": final_params,
            "metadata": {
                "style": shot.style,
                "camera": shot.shot_type,
                "lighting": shot.lighting,
                "characters": [char.id for char in (characters or [])],
                "location_id": location.id if location else None,
            }
        }
        
        logger.info("Image generation request prepared")
        
        return generation_request
    
    def process_shot_batch(
        self,
        shots: List[Shot],
        characters_map: Dict[str, Character],
        locations_map: Dict[str, Location]
    ) -> List[Dict[str, Any]]:
        """Process multiple shots for batch generation"""
        logger.info(f"Processing batch of {len(shots)} shots")
        
        requests = []
        for shot in shots:
            # Get characters for this shot
            shot_characters = [
                characters_map[char_id]
                for char_id in shot.characters
                if char_id in characters_map
            ]
            
            # Get location for this shot
            location = locations_map.get(shot.location_id) if shot.location_id else None
            
            # Generate request
            request = self.generate_shot_image(
                shot=shot,
                characters=shot_characters,
                location=location
            )
            requests.append(request)
        
        logger.info(f"Generated {len(requests)} image generation requests")
        
        return requests
    
    def create_asset_from_generation(
        self,
        generation_result: Dict[str, Any],
        shot_id: str
    ) -> Asset:
        """Create Asset model from generation result"""
        asset = Asset(
            asset_type="image",
            url=generation_result.get("url", ""),
            filename=generation_result.get("filename", ""),
            prompt=generation_result.get("prompt"),
            model=generation_result.get("model"),
            generation_params=generation_result.get("parameters", {}),
            width=generation_result.get("width"),
            height=generation_result.get("height"),
            shot_id=shot_id,
            status="generated"
        )
        
        logger.info(f"Created asset for shot {shot_id}")
        
        return asset
    
    def validate_generation(
        self,
        asset: Asset,
        shot: Shot,
        characters: Optional[List[Character]] = None,
        location: Optional[Location] = None
    ) -> Dict[str, Any]:
        """Validate generated image against requirements"""
        validation_results = {
            "asset_id": asset.id,
            "shot_id": shot.id,
            "valid": True,
            "issues": []
        }
        
        # Validate character consistency
        if characters:
            for character in characters:
                char_validation = self.character_consistency.validate_character_consistency(
                    character.id, asset.url
                )
                if not char_validation.get("consistent"):
                    validation_results["valid"] = False
                    validation_results["issues"].append(
                        f"Character {character.name} consistency check failed"
                    )
        
        # Validate location consistency
        if location:
            loc_validation = self.location_consistency.validate_location_consistency(
                location.id, asset.url
            )
            if not loc_validation.get("consistent"):
                validation_results["valid"] = False
                validation_results["issues"].append(
                    f"Location {location.name} consistency check failed"
                )
        
        logger.info(f"Validation result: {validation_results['valid']}")
        
        return validation_results
