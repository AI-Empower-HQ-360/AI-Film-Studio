"""Prompt templates for different shot types and styles"""

# Shot type templates
SHOT_TYPE_TEMPLATES = {
    "wide": "Wide establishing shot of {subject} {action} in {location}, {style}",
    "medium": "Medium shot of {subject} {action}, {style}",
    "close-up": "Close-up shot of {subject}, {expression}, {style}",
    "extreme-close-up": "Extreme close-up of {subject}, detailed view, {style}",
    "over-the-shoulder": "Over the shoulder shot from {pov_character} looking at {subject}, {style}",
}

# Style templates
STYLE_TEMPLATES = {
    "cinematic": "cinematic lighting, film grain, professional cinematography, depth of field, {camera_work}",
    "anime": "anime style, cel shaded, vibrant colors, detailed illustration, {mood}",
    "noir": "noir style, high contrast, dramatic shadows, black and white, moody atmosphere",
    "realistic": "photorealistic, ultra detailed, 8k resolution, sharp focus, professional photography",
    "painterly": "oil painting style, artistic, visible brushstrokes, impressionist",
}

# Lighting templates
LIGHTING_TEMPLATES = {
    "golden-hour": "golden hour lighting, warm sunset glow, soft shadows, magic hour",
    "blue-hour": "blue hour lighting, cool twilight atmosphere, deep blue sky",
    "natural": "natural lighting, soft ambient light, realistic shadows",
    "dramatic": "dramatic lighting, high contrast, strong directional light, deep shadows",
    "soft": "soft diffused lighting, gentle illumination, even lighting",
    "rim": "rim lighting, backlit, silhouette effect, edge lighting",
}

# Camera angle templates
CAMERA_ANGLE_TEMPLATES = {
    "eye-level": "eye-level angle, natural perspective",
    "high-angle": "high angle shot, looking down, elevated perspective",
    "low-angle": "low angle shot, looking up, dramatic perspective",
    "bird's-eye": "bird's eye view, top-down perspective, aerial shot",
    "worm's-eye": "worm's eye view, extreme low angle, looking up from ground",
}

# Mood templates
MOOD_TEMPLATES = {
    "romantic": "romantic atmosphere, intimate, warm tones, dreamy",
    "tense": "tense atmosphere, suspenseful, dramatic, intense",
    "peaceful": "peaceful atmosphere, serene, calm, tranquil",
    "mysterious": "mysterious atmosphere, enigmatic, shadowy, intriguing",
    "joyful": "joyful atmosphere, bright, cheerful, happy",
    "melancholic": "melancholic atmosphere, somber, reflective, emotional",
}

# Character action templates
CHARACTER_ACTION_TEMPLATES = {
    "walking": "walking through {location}, natural movement, {mood}",
    "standing": "standing in {location}, confident pose, {mood}",
    "sitting": "sitting in {location}, relaxed pose, {mood}",
    "running": "running through {location}, dynamic movement, {mood}",
    "talking": "engaged in conversation, expressive, {mood}",
    "looking": "looking at {target}, focused expression, {mood}",
}

# Location type templates
LOCATION_TEMPLATES = {
    "forest": "lush forest environment, trees, natural foliage, {time_of_day}",
    "city": "urban cityscape, buildings, streets, {time_of_day}",
    "interior": "interior space, {atmosphere}, detailed environment",
    "beach": "beach setting, sand, ocean, {time_of_day}",
    "mountain": "mountain landscape, peaks, dramatic scenery, {time_of_day}",
    "field": "open field, expansive landscape, {time_of_day}",
}

# Negative prompts by style
NEGATIVE_PROMPTS = {
    "cinematic": "low quality, blurry, distorted, deformed, ugly, bad anatomy, extra limbs, amateur, overexposed, underexposed",
    "anime": "low quality, blurry, distorted, deformed, ugly, bad anatomy, extra limbs, realistic, photograph, 3d render",
    "realistic": "low quality, blurry, distorted, deformed, ugly, bad anatomy, extra limbs, cartoon, anime, painting, illustration",
    "noir": "low quality, blurry, distorted, deformed, ugly, bad anatomy, extra limbs, color, colorful, bright",
    "painterly": "low quality, blurry, distorted, deformed, ugly, bad anatomy, extra limbs, photograph, digital art, 3d render",
}

# Default quality enhancers
QUALITY_ENHANCERS = [
    "professional quality",
    "highly detailed",
    "masterpiece",
    "best quality",
]


def get_template(template_type: str, key: str) -> str:
    """Get a template by type and key"""
    templates = {
        "shot_type": SHOT_TYPE_TEMPLATES,
        "style": STYLE_TEMPLATES,
        "lighting": LIGHTING_TEMPLATES,
        "camera_angle": CAMERA_ANGLE_TEMPLATES,
        "mood": MOOD_TEMPLATES,
        "character_action": CHARACTER_ACTION_TEMPLATES,
        "location": LOCATION_TEMPLATES,
    }
    return templates.get(template_type, {}).get(key, "")


def get_negative_prompt(style: str) -> str:
    """Get negative prompt for a style"""
    return NEGATIVE_PROMPTS.get(style, NEGATIVE_PROMPTS["cinematic"])
