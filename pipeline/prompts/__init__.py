"""Prompt templates package"""
from pipeline.prompts.templates import (
    SHOT_TYPE_TEMPLATES,
    STYLE_TEMPLATES,
    LIGHTING_TEMPLATES,
    CAMERA_ANGLE_TEMPLATES,
    MOOD_TEMPLATES,
    CHARACTER_ACTION_TEMPLATES,
    LOCATION_TEMPLATES,
    NEGATIVE_PROMPTS,
    QUALITY_ENHANCERS,
    get_template,
    get_negative_prompt,
)

__all__ = [
    "SHOT_TYPE_TEMPLATES",
    "STYLE_TEMPLATES",
    "LIGHTING_TEMPLATES",
    "CAMERA_ANGLE_TEMPLATES",
    "MOOD_TEMPLATES",
    "CHARACTER_ACTION_TEMPLATES",
    "LOCATION_TEMPLATES",
    "NEGATIVE_PROMPTS",
    "QUALITY_ENHANCERS",
    "get_template",
    "get_negative_prompt",
]
