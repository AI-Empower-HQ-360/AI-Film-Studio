"""Location consistency module for visual continuity"""
from typing import Dict, Any, Optional, List
from src.models.location import Location


class LocationConsistency:
    """Manages location visual consistency across shots"""
    
    def __init__(self):
        self.location_cache: Dict[str, Location] = {}
        self.template_cache: Dict[str, Any] = {}
    
    def register_location(self, location: Location) -> None:
        """Register a location for consistency tracking"""
        if location.id:
            self.location_cache[location.id] = location
    
    def get_location(self, location_id: str) -> Optional[Location]:
        """Retrieve location by ID"""
        return self.location_cache.get(location_id)
    
    def get_consistency_params(
        self,
        location: Location,
        shot_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get parameters to maintain location consistency"""
        params = {
            "location_id": location.id,
            "location_name": location.name,
            "location_type": location.location_type,
        }
        
        # Add reference images if available
        if location.reference_images:
            params["reference_images"] = location.reference_images
            params["use_reference"] = True
        
        # Add template ID for location embeddings
        if location.template_id:
            params["template_id"] = location.template_id
        
        # Build environment prompt additions
        environment_tokens = []
        if location.environment:
            for key, value in location.environment.items():
                if isinstance(value, str):
                    environment_tokens.append(value)
                elif isinstance(value, list):
                    environment_tokens.extend(value)
        
        if environment_tokens:
            params["environment_prompt"] = ", ".join(environment_tokens)
        
        # Build atmosphere prompt additions
        atmosphere_tokens = []
        if location.atmosphere:
            for key, value in location.atmosphere.items():
                if isinstance(value, str):
                    atmosphere_tokens.append(value)
                elif isinstance(value, list):
                    atmosphere_tokens.extend(value)
        
        if atmosphere_tokens:
            params["atmosphere_prompt"] = ", ".join(atmosphere_tokens)
        
        # Time of day
        params["time_of_day"] = location.time_of_day
        
        # Weather
        params["weather"] = location.weather
        
        # Season
        params["season"] = location.season
        
        # Override with shot context if provided
        if shot_context:
            if "time_of_day" in shot_context:
                params["time_of_day"] = shot_context["time_of_day"]
            if "weather" in shot_context:
                params["weather"] = shot_context["weather"]
        
        return params
    
    def apply_consistency(
        self,
        prompt: str,
        location: Location,
        generation_params: Dict[str, Any],
        shot_context: Optional[Dict[str, Any]] = None
    ) -> tuple[str, Dict[str, Any]]:
        """Apply consistency parameters to prompt and generation params"""
        consistency_params = self.get_consistency_params(location, shot_context)
        
        # Enhance prompt with location details
        enhanced_prompt = prompt
        
        # Add environment details to prompt
        if "environment_prompt" in consistency_params:
            enhanced_prompt = f"{enhanced_prompt}, {consistency_params['environment_prompt']}"
        
        # Add atmosphere details to prompt
        if "atmosphere_prompt" in consistency_params:
            enhanced_prompt = f"{enhanced_prompt}, {consistency_params['atmosphere_prompt']}"
        
        # Add time of day
        time_of_day = consistency_params.get("time_of_day", "day")
        if time_of_day != "day":
            enhanced_prompt = f"{enhanced_prompt}, {time_of_day} time"
        
        # Add weather
        weather = consistency_params.get("weather", "clear")
        if weather != "clear":
            enhanced_prompt = f"{enhanced_prompt}, {weather} weather"
        
        # Update generation parameters
        updated_params = generation_params.copy()
        
        # Apply template/embedding
        if "template_id" in consistency_params:
            updated_params["location_template"] = {
                "id": consistency_params["template_id"],
                "weight": 0.7
            }
        
        # Apply reference images (for img2img or ControlNet)
        if consistency_params.get("use_reference"):
            updated_params["reference_images"] = consistency_params["reference_images"]
            updated_params["reference_strength"] = 0.5  # Slightly lower for locations
        
        return enhanced_prompt, updated_params
    
    def create_location_template(
        self,
        location: Location,
        reference_images: List[str]
    ) -> str:
        """Create location template/embedding from reference images"""
        # This would integrate with actual embedding training services
        # For now, return a placeholder
        template_id = f"loc_template_{location.id}_{len(reference_images)}"
        
        # Store in cache
        self.template_cache[template_id] = {
            "location_id": location.id,
            "reference_images": reference_images,
            "status": "pending"
        }
        
        return template_id
    
    def get_lighting_params(
        self,
        location: Location,
        time_of_day: str,
        weather: str
    ) -> Dict[str, Any]:
        """Get lighting parameters based on time and weather"""
        lighting_presets = {
            "dawn": {"color_temp": "cool", "intensity": "soft", "direction": "low"},
            "day": {"color_temp": "neutral", "intensity": "bright", "direction": "high"},
            "dusk": {"color_temp": "warm", "intensity": "soft", "direction": "low"},
            "night": {"color_temp": "cool", "intensity": "dim", "direction": "varied"},
        }
        
        weather_modifiers = {
            "clear": {"contrast": "high", "saturation": "normal"},
            "cloudy": {"contrast": "low", "saturation": "muted"},
            "rainy": {"contrast": "low", "saturation": "desaturated"},
            "foggy": {"contrast": "very_low", "saturation": "muted"},
            "snowy": {"contrast": "high", "saturation": "muted"},
        }
        
        params = lighting_presets.get(time_of_day, lighting_presets["day"]).copy()
        params.update(weather_modifiers.get(weather, weather_modifiers["clear"]))
        
        return params
    
    def validate_location_consistency(
        self,
        location_id: str,
        generated_image: str
    ) -> Dict[str, Any]:
        """Validate if generated image maintains location consistency"""
        # This would use computer vision/ML to validate consistency
        # For now, return a placeholder
        return {
            "location_id": location_id,
            "consistent": True,
            "confidence": 0.80,
            "issues": []
        }
