# AI/ML Processing - AI Film Studio

## Overview

The AI module contains all machine learning models and processing pipelines for generating AI-powered short films. It includes script analysis, image generation, voice synthesis, lip sync animation, music generation, and subtitle generation.

## Architecture

```
ai/
├── script-analysis/        # NLP & scene analysis
├── image-generation/       # Character & background generation
├── voice-synthesis/        # Text-to-Speech & voice cloning
├── lip-sync-animation/     # Facial animation
├── music-poems/            # Music & sloka generation
├── subtitles/              # Multi-language subtitle generation
└── common/                 # Shared AI utilities
```

## Technology Stack

- **Deep Learning Framework**: PyTorch 2.1+
- **Model Hub**: Hugging Face Transformers 4.36+
- **Image Generation**: Stable Diffusion XL (Diffusers 0.25+)
- **Video Processing**: FFmpeg, OpenCV
- **GPU**: CUDA 12.1, NVIDIA T4 (16GB)
- **Optimization**: xformers, Flash Attention, bitsandbytes

## AI Processing Pipelines

### 1. Script Analysis
**Purpose**: Parse and analyze input scripts for scene breakdown

**Models**:
- GPT-3.5-turbo / Claude API for text understanding
- Custom NLP models for cultural context analysis
- Scene detection and dialogue extraction

**Input**: Text script (plain text or JSON)
**Output**: Structured scene graph with metadata

```python
from script_analysis import ScriptAnalyzer

analyzer = ScriptAnalyzer()
scenes = analyzer.analyze_script(script_text)
# Output: List of scenes with characters, dialogue, actions
```

### 2. Image Generation
**Purpose**: Generate character images and backgrounds

**Models**:
- **Stable Diffusion XL** (SDXL) for high-quality images
- **ControlNet** for pose and depth control
- **Custom LoRA** models for specific artistic styles

**Input**: Text prompt, style parameters
**Output**: 1024x1024 PNG images

```python
from image_generation import ImageGenerator

generator = ImageGenerator(model="sdxl_base")
image = generator.generate(
    prompt="A young warrior standing in a forest",
    negative_prompt="blurry, low quality",
    num_steps=30,
    guidance_scale=7.5
)
```

**Supported Styles**:
- Realistic
- Anime
- Cartoon
- Oil Painting
- Watercolor

### 3. Voice Synthesis
**Purpose**: Convert text to speech with emotion and tone control

**Models**:
- TTS models (Tacotron 2, FastSpeech 2)
- Voice cloning (YourTTS, Coqui TTS)
- Emotion control layers

**Input**: Text, voice ID, language
**Output**: WAV audio file

```python
from voice_synthesis import VoiceSynthesizer

synthesizer = VoiceSynthesizer()
audio = synthesizer.synthesize(
    text="Welcome to AI Film Studio",
    voice_id="male_1",
    language="en",
    emotion="neutral",
    speed=1.0
)
```

**Supported Languages**:
- English, Hindi, Spanish, French, German, Japanese, Chinese

**Supported Emotions**:
- Neutral, Happy, Sad, Angry, Surprised, Fearful

### 4. Lip Sync Animation
**Purpose**: Generate facial animation synchronized with audio

**Models**:
- Wav2Lip for lip synchronization
- Facial landmark detection
- Blendshape generation

**Input**: Character image, audio file
**Output**: Animated video with lip-synced character

```python
from lip_sync import LipSyncAnimator

animator = LipSyncAnimator()
video = animator.animate(
    character_image="character.png",
    audio_file="dialogue.wav",
    fps=24
)
```

### 5. Music & Poems
**Purpose**: Generate background music and slokas

**Models**:
- **AudioCraft** (Facebook) for music generation
- **MusicGen** for custom compositions
- Sloka database for cultural content

**Input**: Mood, tempo, duration
**Output**: MP3 audio file

```python
from music_poems import MusicGenerator

generator = MusicGenerator()
music = generator.generate(
    mood="epic",
    tempo=120,
    duration=30
)
```

**Supported Moods**:
- Epic, Calm, Tense, Joyful, Melancholic

### 6. Subtitle Generation
**Purpose**: Generate multi-language subtitles with timing

**Models**:
- Speech recognition (Whisper)
- Translation models (MarianMT)
- Subtitle synchronization

**Input**: Video file, target languages
**Output**: SRT subtitle files

```python
from subtitles import SubtitleGenerator

generator = SubtitleGenerator()
subtitles = generator.generate(
    video_file="output.mp4",
    languages=["en", "es", "hi", "fr"]
)
```

## GPU Workers

### Instance Configuration

**Instance Type**: g4dn.xlarge (AWS EC2)
- **GPU**: NVIDIA T4 (16GB)
- **vCPUs**: 4
- **Memory**: 16GB
- **Storage**: 125GB NVMe SSD

### Auto-Scaling

Workers scale based on SQS queue depth:
- **Scale Up**: Queue depth > 10 messages
- **Scale Down**: Queue depth < 2 messages
- **Min Instances**: 0 (dev), 1 (prod)
- **Max Instances**: 5 (dev), 20 (prod)

### Cost Optimization

- **On-Demand**: $0.526/hour
- **Spot Instances**: ~$0.158/hour (70% savings)
- **Strategy**: 70% spot, 30% on-demand

## Job Processing Flow

1. **Job Received**: Worker polls SQS queue
2. **Model Loading**: Load required AI model (if not cached)
3. **Processing**: Execute generation task
4. **Upload Results**: Upload to S3
5. **Status Update**: Update job status in RDS
6. **Cleanup**: Delete SQS message

```python
import boto3
from ai_worker import AIWorker

# Initialize worker
sqs = boto3.client('sqs')
worker = AIWorker()

while True:
    # Poll SQS queue
    messages = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )
    
    if 'Messages' in messages:
        for message in messages['Messages']:
            # Process job
            job = parse_message(message['Body'])
            result = worker.process(job)
            
            # Upload result to S3
            upload_to_s3(result)
            
            # Update job status
            update_job_status(job.id, 'completed')
            
            # Delete message
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )
```

## Model Management

### Model Storage

Models are stored in:
- **S3**: Long-term storage of model weights
- **Local Cache**: `/models/` directory on GPU worker

### Model Loading

```python
from common.model_loader import ModelLoader

loader = ModelLoader()

# Load model (downloads from S3 if not cached)
model = loader.load("sdxl_base", device="cuda")

# Model is cached for subsequent requests
```

### Model Versions

| Model | Version | Size | Purpose |
|-------|---------|------|---------|
| SDXL Base | 1.0 | 6.9GB | Image generation |
| Custom LoRA | 1.2 | 500MB | Style transfer |
| TTS Model | 2.0 | 1.2GB | Voice synthesis |
| Wav2Lip | 1.0 | 250MB | Lip sync |
| MusicGen | 1.0 | 3.3GB | Music generation |

## Environment Setup

### Prerequisites

- Python 3.11+
- CUDA 12.1+
- NVIDIA Driver 525+
- 16GB+ GPU memory

### Installation

```bash
# Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install AI dependencies
pip install -r requirements.txt

# Download models
python scripts/download_models.py
```

### Environment Variables

```bash
# AWS Configuration
AWS_REGION=us-east-1
S3_BUCKET_NAME=ai-film-studio-media-prod
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/123456789/ai-film-studio-jobs

# Model Configuration
MODEL_CACHE_DIR=/models
MODEL_DEVICE=cuda
MODEL_PRECISION=fp16  # fp16, fp32

# API Keys
OPENAI_API_KEY=sk-xxxxx
HUGGINGFACE_TOKEN=hf_xxxxx
```

## Performance Optimization

### Memory Optimization

```python
# Use FP16 precision
model.half()

# Enable gradient checkpointing
model.enable_gradient_checkpointing()

# Clear CUDA cache
import torch
torch.cuda.empty_cache()
```

### Inference Optimization

```python
# Use Flash Attention
from xformers.ops import memory_efficient_attention

# Compile model with torch.compile
model = torch.compile(model, mode="reduce-overhead")

# Use batch processing
batch_images = generator.generate_batch(prompts)
```

## Monitoring

### GPU Metrics

```python
import nvidia_smi

nvidia_smi.nvmlInit()
handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)

# Get GPU utilization
utilization = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
print(f"GPU: {utilization.gpu}%")
print(f"Memory: {utilization.memory}%")
```

### Job Metrics

- **Processing Time**: Average time per job
- **Success Rate**: Successful jobs / total jobs
- **Queue Depth**: Number of pending jobs
- **GPU Utilization**: Average GPU usage
- **Cost per Job**: Average cost per generation

## Testing

### Unit Tests

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_image_generation.py

# Run with GPU
pytest tests/ --gpu
```

### Model Tests

```bash
# Test image generation
python tests/test_models.py --model sdxl

# Test voice synthesis
python tests/test_models.py --model tts

# Test all models
python tests/test_models.py --all
```

## Troubleshooting

### Common Issues

**Out of Memory (OOM)**:
```python
# Reduce batch size
generator.batch_size = 1

# Use FP16
model.half()

# Clear cache
torch.cuda.empty_cache()
```

**Slow Generation**:
```python
# Use xformers
pip install xformers

# Enable Flash Attention
model.enable_xformers_memory_efficient_attention()
```

**Model Loading Errors**:
```bash
# Download models manually
python scripts/download_models.py --force

# Check model cache
ls -lh /models/
```

## Contributing

Please read the [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](../LICENSE)

---

For more details, see the [System Design Documentation](../docs/architecture/system-design.md).
