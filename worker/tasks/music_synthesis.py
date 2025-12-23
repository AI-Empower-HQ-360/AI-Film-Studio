"""
Music synthesis task for background music.
"""
from celery import Task
from typing import Dict
import os
from ..celery_app import celery_app
from ..utils.retry_logic import celery_retry_on_exception


@celery_app.task(bind=True, name='tasks.synthesize_music')
@celery_retry_on_exception(exceptions=(ConnectionError, TimeoutError), max_retries=3)
def synthesize_music(self: Task, job_id: int, config: Dict) -> Dict:
    """
    Generate background music for the video.
    
    Args:
        job_id: Job identifier
        config: Configuration including genre, mood, duration, etc.
    
    Returns:
        Dict with generated music path and metadata
    """
    print(f"[Job {job_id}] Starting music synthesis")
    
    # Configuration
    genre = config.get('genre', 'cinematic')
    mood = config.get('mood', 'inspiring')
    duration = config.get('duration', 60)
    output_dir = f"/tmp/job_{job_id}/audio"
    
    os.makedirs(output_dir, exist_ok=True)
    
    music_path = os.path.join(output_dir, "background_music.mp3")
    
    # Update progress
    self.update_state(
        state='PROGRESS',
        meta={'stage': 'music_synthesis', 'progress': 0}
    )
    
    # Mock music synthesis (replace with actual music generation API)
    # Example integrations:
    # - MusicGen: musicgen.generate()
    # - Mubert: mubert_api.generate()
    # - Soundraw: soundraw.create()
    # - AIVA: aiva.compose()
    
    print(f"[Job {job_id}] Generating {genre} music with {mood} mood for {duration}s")
    
    # Simulate music generation
    # In production:
    # music_data = musicgen.generate(
    #     genre=genre,
    #     mood=mood,
    #     duration=duration
    # )
    # with open(music_path, 'wb') as f:
    #     f.write(music_data)
    
    self.update_state(
        state='PROGRESS',
        meta={'stage': 'music_synthesis', 'progress': 100}
    )
    
    print(f"[Job {job_id}] Music synthesis completed: {music_path}")
    
    return {
        'job_id': job_id,
        'music_path': music_path,
        'duration': duration,
        'genre': genre,
        'mood': mood
    }
