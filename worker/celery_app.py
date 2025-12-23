"""
Celery configuration for the worker.
"""
from celery import Celery

# Create Celery instance
celery_app = Celery(
    'ai_film_studio_worker',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=[
        'tasks.image_generation',
        'tasks.video_generation',
        'tasks.voice_synthesis',
        'tasks.music_synthesis',
        'tasks.ffmpeg_composition'
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3300,  # 55 minutes
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_reject_on_worker_lost=True,
    task_default_retry_delay=60,  # 1 minute
    task_max_retries=3,
)

if __name__ == '__main__':
    celery_app.start()
