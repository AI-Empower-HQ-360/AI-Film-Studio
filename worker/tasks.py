import os
import asyncio
from celery_app import app
from config import settings
from pipelines import (
    image_pipeline,
    video_pipeline,
    audio_pipeline,
    ffmpeg_composer
)
from utils.api_client import api_client


@app.task(bind=True, name='process_film_job')
def process_film_job(self, job_data: dict):
    """
    Main task for processing a film generation job
    
    Args:
        job_data: Job configuration including:
            - job_id: Job ID
            - project_id: Project ID
            - script: Film script or description
            - scenes: List of scene descriptions
            - config: Additional configuration
    """
    job_id = job_data.get('job_id')
    script = job_data.get('script', '')
    scenes = job_data.get('scenes', [])
    config = job_data.get('config', {})
    
    print(f"Processing job {job_id}")
    
    # Create temp directory for this job
    job_dir = os.path.join(settings.TEMP_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)
    
    try:
        # Update status to processing
        asyncio.run(update_job_status(job_id, "processing", 0))
        
        # Step 1: Generate images for each scene
        asyncio.run(update_job_status(job_id, "generating_images", 10))
        image_paths = generate_scene_images(job_id, scenes, job_dir)
        
        # Step 2: Generate video from images
        asyncio.run(update_job_status(job_id, "generating_video", 40))
        video_path = generate_video(job_id, image_paths, job_dir)
        
        # Step 3: Generate audio
        asyncio.run(update_job_status(job_id, "generating_audio", 70))
        audio_path = generate_audio(job_id, script, job_dir, config)
        
        # Step 4: Compose final video
        asyncio.run(update_job_status(job_id, "composing", 85))
        final_video_path = compose_final_video(
            job_id, video_path, audio_path, job_dir, config
        )
        
        # Step 5: Generate thumbnail
        thumbnail_path = generate_thumbnail(job_id, final_video_path, job_dir)
        
        # Step 6: Upload to storage (placeholder)
        video_url = upload_to_storage(final_video_path, f"jobs/{job_id}/output.mp4")
        thumbnail_url = upload_to_storage(thumbnail_path, f"jobs/{job_id}/thumbnail.jpg")
        
        # Update job as completed
        asyncio.run(update_job_status(job_id, "completed", 100))
        
        print(f"Job {job_id} completed successfully")
        
        return {
            "status": "completed",
            "video_url": video_url,
            "thumbnail_url": thumbnail_url
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"Job {job_id} failed: {error_msg}")
        asyncio.run(update_job_status(job_id, "failed", error_message=error_msg))
        raise


async def update_job_status(job_id: str, status: str, progress: int = None, error_message: str = None):
    """Update job status via API"""
    await api_client.update_job_status(
        job_id=job_id,
        status=status,
        progress=progress,
        error_message=error_message
    )


def generate_scene_images(job_id: str, scenes: list, job_dir: str) -> list:
    """Generate images for each scene"""
    if not scenes:
        # Generate default scene if no scenes provided
        scenes = ["A cinematic scene from an AI-generated film"]
    
    images_dir = os.path.join(job_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    print(f"Generating {len(scenes)} scene images...")
    image_paths = image_pipeline.generate_scene_images(scenes, images_dir)
    
    return image_paths


def generate_video(job_id: str, image_paths: list, job_dir: str) -> str:
    """Generate video from images"""
    videos_dir = os.path.join(job_dir, "videos")
    os.makedirs(videos_dir, exist_ok=True)
    
    video_path = os.path.join(videos_dir, "sequence.mp4")
    
    print("Creating video sequence...")
    video_pipeline.create_video_sequence(image_paths, video_path)
    
    return video_path


def generate_audio(job_id: str, script: str, job_dir: str, config: dict) -> str:
    """Generate audio/music"""
    audio_dir = os.path.join(job_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    
    music_path = os.path.join(audio_dir, "background.wav")
    
    # Generate background music
    music_prompt = config.get('music_prompt', 'Cinematic background music')
    duration = config.get('video_duration', 10)
    
    print("Generating audio...")
    audio_pipeline.generate_background_music(music_prompt, duration, music_path)
    
    return music_path


def compose_final_video(
    job_id: str,
    video_path: str,
    audio_path: str,
    job_dir: str,
    config: dict
) -> str:
    """Compose final video with audio"""
    output_dir = os.path.join(job_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    final_path = os.path.join(output_dir, "final.mp4")
    
    print("Composing final video...")
    ffmpeg_composer.compose_video_with_audio(
        video_path,
        audio_path,
        final_path,
        audio_volume=config.get('audio_volume', 0.5)
    )
    
    # Add text overlay if specified
    if config.get('title'):
        with_title_path = os.path.join(output_dir, "final_with_title.mp4")
        ffmpeg_composer.add_text_overlay(
            final_path,
            with_title_path,
            config['title'],
            position="top"
        )
        final_path = with_title_path
    
    return final_path


def generate_thumbnail(job_id: str, video_path: str, job_dir: str) -> str:
    """Generate thumbnail from video"""
    output_dir = os.path.join(job_dir, "output")
    thumbnail_path = os.path.join(output_dir, "thumbnail.jpg")
    
    print("Generating thumbnail...")
    ffmpeg_composer.create_thumbnail(video_path, thumbnail_path, timestamp=1.0)
    
    return thumbnail_path


def upload_to_storage(file_path: str, object_key: str) -> str:
    """
    Upload file to storage (S3 or local)
    
    Returns:
        URL to the uploaded file
    """
    # Placeholder for actual upload implementation
    # In production, this would upload to S3 or other storage
    
    print(f"Uploading {file_path} to {object_key}")
    
    # For now, return a mock URL
    return f"https://storage.example.com/{object_key}"


@app.task(name='test_task')
def test_task():
    """Simple test task"""
    return "Worker is running!"
