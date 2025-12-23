# AI Film Studio Hub - Worker

GPU-accelerated worker service for processing AI film generation jobs including image generation, video creation, audio synthesis, and FFmpeg composition.

## Features

- **Image Generation**: Stable Diffusion XL for high-quality scene images
- **Video Generation**: Video synthesis from images with motion
- **Audio Generation**: Background music and narration (placeholder)
- **FFmpeg Composition**: Professional video composition and encoding
- **Celery Task Queue**: Distributed job processing with Redis
- **GPU Support**: CUDA, MPS, or CPU execution

## Installation

1. Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg libsm6 libxext6

# macOS
brew install ffmpeg
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running

### Start Celery Worker
```bash
celery -A celery_app worker --loglevel=info
```

### With GPU Support
```bash
# CUDA (NVIDIA)
celery -A celery_app worker --loglevel=info --concurrency=1

# MPS (Apple Silicon)
DEVICE=mps celery -A celery_app worker --loglevel=info --concurrency=1
```

### Monitor with Flower
```bash
pip install flower
celery -A celery_app flower
# Visit http://localhost:5555
```

## Architecture

```
worker/
├── pipelines/
│   ├── image_generation.py   # Stable Diffusion image gen
│   ├── video_generation.py   # Video synthesis
│   ├── audio_generation.py   # Audio/music generation
│   └── ffmpeg_composer.py    # FFmpeg composition
├── utils/
│   └── api_client.py          # Backend API client
├── celery_app.py              # Celery configuration
├── tasks.py                   # Job processing tasks
├── config.py                  # Worker settings
└── requirements.txt
```

## Job Processing Pipeline

1. **Image Generation**: Generate images for each scene using Stable Diffusion XL
2. **Video Generation**: Convert images to video sequences with motion
3. **Audio Generation**: Create background music and narration
4. **Composition**: Combine video and audio with FFmpeg
5. **Upload**: Upload final video to storage

## Tasks

### Main Task: `process_film_job`

Processes a complete film generation job with the following steps:
- Generate scene images from prompts
- Create video sequences
- Generate background audio
- Compose final video with audio
- Generate thumbnail
- Upload to storage

Example job data:
```python
{
    "job_id": "123e4567-e89b-12d3-a456-426614174000",
    "project_id": "abc123",
    "script": "A cinematic journey through space",
    "scenes": [
        "A spaceship launching from Earth",
        "Flying through an asteroid field",
        "Landing on a distant planet"
    ],
    "config": {
        "music_prompt": "Epic space adventure music",
        "video_duration": 9,
        "audio_volume": 0.5,
        "title": "Space Journey"
    }
}
```

### Test Task: `test_task`

Simple test task to verify worker is running:
```bash
celery -A celery_app call tasks.test_task
```

## Configuration

See `.env.example` for all configuration options.

Key settings:
- `DEVICE`: GPU device (cuda/mps/cpu)
- `IMAGE_MODEL`: Stable Diffusion model ID
- `VIDEO_MODEL`: Video generation model ID
- `CELERY_BROKER_URL`: Redis connection for Celery
- `AWS_*`: AWS credentials for S3 storage

## GPU Requirements

### Recommended
- NVIDIA GPU with 8GB+ VRAM (for SDXL)
- CUDA 11.8+
- 16GB+ system RAM

### Minimum
- NVIDIA GPU with 6GB VRAM (with attention slicing)
- Or CPU execution (slower)

### Apple Silicon
- M1/M2/M3 with MPS support
- 16GB+ unified memory

## Performance

- Image generation: ~10-30s per image (GPU)
- Video generation: ~30-60s per video (GPU)
- Audio generation: ~5-10s (CPU)
- FFmpeg composition: ~10-20s

Total job time: 2-5 minutes for a 3-scene video

## Troubleshooting

### Out of Memory
- Reduce `IMAGE_WIDTH` and `IMAGE_HEIGHT`
- Enable `enable_attention_slicing()` (already enabled)
- Use CPU instead of GPU

### FFmpeg Not Found
- Install FFmpeg: `apt-get install ffmpeg` or `brew install ffmpeg`
- Worker will use moviepy fallback (slower)

### Model Download Slow
- Models are downloaded from HuggingFace on first use
- Pre-download: `huggingface-cli download stabilityai/stable-diffusion-xl-base-1.0`
