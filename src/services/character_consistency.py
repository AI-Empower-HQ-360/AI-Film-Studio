"""Character consistency module for visual continuity"""
from typing import Dict, Any, Optional, List
from src.models.character import Character


class CharacterConsistency:
    """Manages character visual consistency across shots"""
    
    def __init__(self):
        self.character_cache: Dict[str, Character] = {}
        self.embedding_cache: Dict[str, Any] = {}
    
    def register_character(self, character: Character) -> None:
        """Register a character for consistency tracking"""
        if character.id:
            self.character_cache[character.id] = character
    
    def get_character(self, character_id: str) -> Optional[Character]:
        """Retrieve character by ID"""
        return self.character_cache.get(character_id)
    
    def get_consistency_params(
        self,
        character: Character,
        shot_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get parameters to maintain character consistency"""
        params = {
            "character_id": character.id,
            "character_name": character.name,
        }
        
        # Add reference images if available
        if character.reference_images:
            params["reference_images"] = character.reference_images
            params["use_reference"] = True
        
        # Add embedding ID for LoRA or custom models
        if character.embedding_id:
            params["embedding_id"] = character.embedding_id
            params["lora_weight"] = 0.8  # Default weight
        
        # Add seed locking for consistency
        if character.seed is not None:
            params["seed"] = character.seed
            params["seed_locked"] = True
        
        # Build appearance prompt additions
        appearance_tokens = []
        if character.appearance:
            for key, value in character.appearance.items():
                if isinstance(value, str):
                    appearance_tokens.append(value)
                elif isinstance(value, list):
                    appearance_tokens.extend(value)
        
        if appearance_tokens:
            params["appearance_prompt"] = ", ".join(appearance_tokens)
        
        # Build attire prompt additions
        attire_tokens = []
        if character.attire:
            for key, value in character.attire.items():
                if isinstance(value, str):
                    attire_tokens.append(value)
                elif isinstance(value, list):
                    attire_tokens.extend(value)
        
        if attire_tokens:
            params["attire_prompt"] = ", ".join(attire_tokens)
        
        return params
    
    def apply_consistency(
        self,
        prompt: str,
        character: Character,
        generation_params: Dict[str, Any]
    ) -> tuple[str, Dict[str, Any]]:
        """Apply consistency parameters to prompt and generation params"""
        consistency_params = self.get_consistency_params(character)
        
        # Enhance prompt with character details
        enhanced_prompt = prompt
        
        # Add appearance details to prompt
        if "appearance_prompt" in consistency_params:
            enhanced_prompt = f"{enhanced_prompt}, {consistency_params['appearance_prompt']}"
        
        # Add attire details to prompt
        if "attire_prompt" in consistency_params:
            enhanced_prompt = f"{enhanced_prompt}, {consistency_params['attire_prompt']}"
        
        # Update generation parameters
        updated_params = generation_params.copy()
        
        # Apply seed locking
        if consistency_params.get("seed_locked"):
            updated_params["seed"] = consistency_params["seed"]
        
        # Apply LoRA/embedding
        if "embedding_id" in consistency_params:
            updated_params["lora"] = {
                "id": consistency_params["embedding_id"],
                "weight": consistency_params.get("lora_weight", 0.8)
            }
        
        # Apply reference images (for img2img or ControlNet)
        if consistency_params.get("use_reference"):
            updated_params["reference_images"] = consistency_params["reference_images"]
            updated_params["reference_strength"] = 0.6  # Default strength
        
        return enhanced_prompt, updated_params
    
    def create_character_embedding(
        self,
        character: Character,
        reference_images: List[str]
    ) -> str:
        """Create character embedding/LoRA from reference images"""
        # This would integrate with actual embedding training services
        # For now, return a placeholder
        embedding_id = f"emb_{character.id}_{len(reference_images)}"
        
        # Store in cache
        self.embedding_cache[embedding_id] = {
            "character_id": character.id,
            "reference_images": reference_images,
            "status": "pending"
        }
        
        return embedding_id
    
    def get_pose_controlnet_params(
        self,
        character: Character,
        pose_type: str = "standing"
    ) -> Dict[str, Any]:
        """Get ControlNet parameters for pose consistency"""
        return {
            "controlnet_type": "openpose",
            "pose_type": pose_type,
            "character_id": character.id,
            "strength": 0.7
        }
    
    def validate_character_consistency(
        self,
        character_id: str,
        generated_image: str
    ) -> Dict[str, Any]:
        """Validate if generated image maintains character consistency"""
        # This would use computer vision/ML to validate consistency
        # For now, return a placeholder
        return {
            "character_id": character_id,
            "consistent": True,
            "confidence": 0.85,
            "issues": []
        }
