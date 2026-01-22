"""
API Routes Module
FastAPI route handlers for the AI Film Studio API.
"""

__version__ = "0.1.0"

# Import route modules for easy access
from . import projects
from . import characters
from . import video
from . import voice
from . import export
from . import delivery
from . import auth

__all__ = [
    "projects",
    "characters", 
    "video",
    "voice",
    "export",
    "delivery",
    "auth",
]
