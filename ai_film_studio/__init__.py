"""
AI Film Studio - End-to-end AI Film Production Pipeline

This package provides tools for creating films from script to final MP4 output.
Pipeline: script → scenes → shots → video → MP4
"""

__version__ = "0.1.0"
__author__ = "AI-Empower-HQ-360"

from ai_film_studio.pipeline import FilmPipeline

__all__ = ["FilmPipeline", "__version__"]
