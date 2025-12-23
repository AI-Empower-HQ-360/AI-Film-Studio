"""
Main pipeline orchestrator for job processing.
"""
from typing import Dict
from celery import chain, group
from tasks.image_generation import generate_images
from tasks.video_generation import generate_video
from tasks.voice_synthesis import synthesize_voice
from tasks.music_synthesis import synthesize_music
from tasks.ffmpeg_composition import compose_final_video


def process_job(job_id: int, script: str, config: Dict) -> None:
    """
    Main pipeline to process a complete job.
    
    Args:
        job_id: Job identifier
        script: Script text
        config: Job configuration
    
    Pipeline stages:
        1. Generate images from script
        2. Generate video from images
        3. Synthesize voice narration (parallel)
        4. Synthesize background music (parallel)
        5. Compose final video with all audio tracks
    """
    print(f"[Job {job_id}] Starting job processing pipeline")
    
    # Extract prompts from script (simplified)
    prompts = [line.strip() for line in script.split('\n') if line.strip()]
    
    # Build Celery pipeline
    # Stage 1: Generate images
    image_task = generate_images.si(job_id, prompts, config)
    
    # Stage 2: Generate video from images
    # Note: In production, pass image paths from previous task
    video_task = generate_video.si(job_id, [], config)
    
    # Stage 3 & 4: Generate audio (parallel)
    audio_group = group(
        synthesize_voice.si(job_id, script, config),
        synthesize_music.si(job_id, config)
    )
    
    # Stage 5: Compose final video
    compose_task = compose_final_video.si(
        job_id,
        f"/tmp/job_{job_id}/video/video_raw.mp4",
        {
            'voice': f"/tmp/job_{job_id}/audio/narration.mp3",
            'music': f"/tmp/job_{job_id}/audio/background_music.mp3"
        },
        config
    )
    
    # Execute pipeline
    # Sequential: images -> video -> (voice + music in parallel) -> compose
    pipeline = chain(
        image_task,
        video_task,
        audio_group,
        compose_task
    )
    
    # Run pipeline asynchronously
    result = pipeline.apply_async()
    
    print(f"[Job {job_id}] Pipeline started with task ID: {result.id}")
    
    return result.id
