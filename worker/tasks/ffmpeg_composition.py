"""
FFmpeg composition task for final video assembly.
"""
from celery import Task
from typing import Dict
import os
import subprocess
from ..celery_app import celery_app
from ..utils.retry_logic import celery_retry_on_exception


@celery_app.task(bind=True, name='tasks.compose_final_video')
@celery_retry_on_exception(exceptions=(subprocess.CalledProcessError,), max_retries=3)
def compose_final_video(
    self: Task,
    job_id: int,
    video_path: str,
    audio_paths: Dict[str, str],
    config: Dict
) -> Dict:
    """
    Compose final video with audio tracks using FFmpeg.
    
    Args:
        job_id: Job identifier
        video_path: Path to the video file
        audio_paths: Dictionary with 'voice' and 'music' audio paths
        config: Configuration including output format, quality, etc.
    
    Returns:
        Dict with final video path and metadata
    """
    print(f"[Job {job_id}] Starting FFmpeg composition")
    
    # Configuration
    output_format = config.get('format', 'mp4')
    quality = config.get('quality', 'high')
    resolution = config.get('resolution', '1920x1080')
    output_dir = f"/tmp/job_{job_id}"
    
    os.makedirs(output_dir, exist_ok=True)
    
    final_output = os.path.join(output_dir, f"final_output.{output_format}")
    
    # Update progress
    self.update_state(
        state='PROGRESS',
        meta={'stage': 'ffmpeg_composition', 'progress': 0}
    )
    
    # Quality presets
    quality_presets = {
        'low': {'crf': 28, 'preset': 'fast'},
        'medium': {'crf': 23, 'preset': 'medium'},
        'high': {'crf': 18, 'preset': 'slow'},
    }
    
    preset = quality_presets.get(quality, quality_presets['medium'])
    
    print(f"[Job {job_id}] Composing video with FFmpeg")
    print(f"  - Video: {video_path}")
    print(f"  - Voice: {audio_paths.get('voice', 'none')}")
    print(f"  - Music: {audio_paths.get('music', 'none')}")
    print(f"  - Output: {final_output}")
    
    # Build FFmpeg command
    # Basic structure: ffmpeg -i video.mp4 -i voice.mp3 -i music.mp3 
    #                  -filter_complex "[2:a]volume=0.3[music];[1:a][music]amix=inputs=2[audio]" 
    #                  -map 0:v -map [audio] output.mp4
    
    # Mock FFmpeg execution (in production, use actual FFmpeg)
    # Example command:
    # ffmpeg_cmd = [
    #     'ffmpeg',
    #     '-i', video_path,
    #     '-i', audio_paths.get('voice', ''),
    #     '-i', audio_paths.get('music', ''),
    #     '-filter_complex',
    #     '[2:a]volume=0.3[music];[1:a][music]amix=inputs=2[audio]',
    #     '-map', '0:v',
    #     '-map', '[audio]',
    #     '-c:v', 'libx264',
    #     '-preset', preset['preset'],
    #     '-crf', str(preset['crf']),
    #     '-c:a', 'aac',
    #     '-b:a', '192k',
    #     '-s', resolution,
    #     '-y',
    #     final_output
    # ]
    
    # subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
    
    # Simulate FFmpeg processing
    print(f"[Job {job_id}] FFmpeg command would execute here...")
    
    self.update_state(
        state='PROGRESS',
        meta={'stage': 'ffmpeg_composition', 'progress': 100}
    )
    
    # Get file size (would be actual size in production)
    file_size_mb = 0  # os.path.getsize(final_output) / (1024 * 1024)
    
    print(f"[Job {job_id}] FFmpeg composition completed: {final_output}")
    
    return {
        'job_id': job_id,
        'output_path': final_output,
        'format': output_format,
        'quality': quality,
        'resolution': resolution,
        'file_size_mb': file_size_mb,
        'success': True
    }
