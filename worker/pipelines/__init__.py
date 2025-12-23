"""Pipelines module initialization"""
from pipelines.image_generation import image_pipeline
from pipelines.video_generation import video_pipeline
from pipelines.audio_generation import audio_pipeline
from pipelines.ffmpeg_composer import ffmpeg_composer

__all__ = ["image_pipeline", "video_pipeline", "audio_pipeline", "ffmpeg_composer"]
