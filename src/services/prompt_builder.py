"""Prompt builder for image generation"""
from typing import Dict, Any, List, Optional
from src.models.shot import Shot
from src.models.character import Character
from src.models.location import Location


class PromptBuilder:
    """Builds rich prompts for image generation"""
    
    def __init__(self):
        self.style_modifiers = {
            "cinematic": "cinematic lighting, film grain, professional cinematography, depth of field",
            "anime": "anime style, cel shaded, vibrant colors, detailed illustration",
            "noir": "noir style, high contrast, dramatic shadows, black and white",
            "realistic": "photorealistic, ultra detailed, 8k resolution, sharp focus",
            "painterly": "oil painting style, artistic, brushstrokes visible",
        }
        
        self.camera_modifiers = {
            "wide": "wide shot, full scene visible",
            "medium": "medium shot, waist up",
            "close-up": "close-up shot, face and shoulders",
            "extreme-close-up": "extreme close-up, detailed facial features",
            "over-the-shoulder": "over the shoulder shot, perspective view",
        }
        
        self.lighting_modifiers = {
            "natural": "natural lighting, soft ambient light",
            "golden-hour": "golden hour lighting, warm sunset glow",
            "blue-hour": "blue hour lighting, cool twilight atmosphere",
            "dramatic": "dramatic lighting, high contrast, strong shadows",
            "soft": "soft diffused lighting, gentle illumination",
            "rim": "rim lighting, backlit, silhouette effect",
        }
    
    def build_prompt(
        self,
        shot: Shot,
        characters: Optional[List[Character]] = None,
        location: Optional[Location] = None
    ) -> Dict[str, Any]:
        """Build a complete prompt from shot metadata"""
        
        # Build character descriptions
        character_desc = ""
        if characters:
            char_descs = []
            for char in characters:
                desc = f"{char.name}"
                if char.appearance:
                    appearance_parts = [
                        f"{v}" for k, v in char.appearance.items()
                    ]
                    desc += f" ({', '.join(appearance_parts)})"
                if char.attire:
                    attire_parts = [
                        f"{v}" for k, v in char.attire.items() if isinstance(v, str)
                    ]
                    if attire_parts:
                        desc += f", wearing {', '.join(attire_parts)}"
                char_descs.append(desc)
            
            if len(char_descs) == 1:
                character_desc = char_descs[0]
            elif len(char_descs) == 2:
                character_desc = f"{char_descs[0]} and {char_descs[1]}"
            else:
                character_desc = ", ".join(char_descs[:-1]) + f", and {char_descs[-1]}"
        
        # Build location description
        location_desc = ""
        if location:
            location_desc = location.description
            if location.environment:
                env_parts = [
                    f"{v}" for k, v in location.environment.items() if isinstance(v, str)
                ]
                if env_parts:
                    location_desc += f", {', '.join(env_parts)}"
            if location.atmosphere:
                atm_parts = [
                    f"{v}" for k, v in location.atmosphere.items() if isinstance(v, str)
                ]
                if atm_parts:
                    location_desc += f", {', '.join(atm_parts)}"
        
        # Build main prompt
        prompt_parts = []
        
        # Camera shot type
        if shot.shot_type in self.camera_modifiers:
            prompt_parts.append(self.camera_modifiers[shot.shot_type])
        
        # Subject (characters)
        if character_desc:
            prompt_parts.append(f"of {character_desc}")
        
        # Action
        if shot.action:
            prompt_parts.append(shot.action)
        elif shot.description:
            prompt_parts.append(shot.description)
        
        # Location
        if location_desc:
            prompt_parts.append(f"in {location_desc}")
        
        # Lighting
        if shot.lighting in self.lighting_modifiers:
            prompt_parts.append(self.lighting_modifiers[shot.lighting])
        
        # Style
        if shot.style in self.style_modifiers:
            prompt_parts.append(self.style_modifiers[shot.style])
        
        # Mood
        if shot.mood and shot.mood != "neutral":
            prompt_parts.append(f"{shot.mood} atmosphere")
        
        # Combine into final prompt
        prompt = ", ".join(prompt_parts)
        
        # Build result dictionary
        result = {
            "prompt": prompt,
            "style": shot.style,
            "camera": shot.shot_type,
            "camera_angle": shot.camera_angle,
            "camera_movement": shot.camera_movement,
            "lighting": shot.lighting,
            "mood": shot.mood,
            "negative_prompt": self._build_negative_prompt(shot.style),
        }
        
        return result
    
    def _build_negative_prompt(self, style: str) -> str:
        """Build negative prompt based on style"""
        base_negative = "low quality, blurry, distorted, deformed, ugly, bad anatomy, extra limbs"
        
        style_negatives = {
            "cinematic": base_negative + ", amateur, overexposed, underexposed",
            "anime": base_negative + ", realistic, photograph, 3d render",
            "realistic": base_negative + ", cartoon, anime, painting, illustration",
            "painterly": base_negative + ", photograph, digital art, 3d render",
        }
        
        return style_negatives.get(style, base_negative)
    
    def build_prompt_from_template(
        self,
        template: str,
        variables: Dict[str, Any]
    ) -> str:
        """Build prompt from a template string with variables"""
        return template.format(**variables)
