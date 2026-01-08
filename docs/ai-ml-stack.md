# 🌐 AI FILM STUDIO – AI / ML TECH STACK

**Version:** 1.0  
**Last Updated:** 2025-12-31  
**Document Owner:** AI-Empower-HQ-360

---

## Table of Contents

1. [Overview](#overview)
2. [Video Generation](#1-video-generation)
3. [Voice Synthesis](#2-voice-synthesis)
4. [Lip-Sync & Face Animation](#3-lip-sync--face-animation)
5. [Music & Audio](#4-music--audio)
6. [Podcast-Style Videos](#5-podcast-style-videos)
7. [Subtitles & Multi-Language](#6-subtitles--multi-language)
8. [AI Job Management](#7-ai-job-management)
9. [AI Model Hosting](#8-ai-model-hosting)
10. [Summary](#summary)

---

## Overview

This document provides a comprehensive overview of the AI/ML technology stack for **AI Film Studio**, covering all components required for video generation, voice synthesis, animation, music, podcasts, and multi-language support.

The platform leverages state-of-the-art AI models and cloud infrastructure to deliver high-quality, automated content creation at scale.

---

## 1️⃣ Video Generation

### Core Models

| Function            | Recommendation                                     | Notes                                                  |
| ------------------- | -------------------------------------------------- | ------------------------------------------------------ |
| Core Models         | **Stable Diffusion Video (SD-V), Gen-2, CogVideo** | Pre-trained AI models for high-quality video synthesis |
| Open-Source Options | **LTX‑2, Dream Machine**                           | Full control, customizable pipelines, self-hosted      |
| Input               | Script + Images + Duration                         | Generate character-based videos                        |
| Output              | MP4 video                                          | Stored in S3, previewable on frontend                  |

### Implementation Details

**Primary Models:**
- **Stable Diffusion Video (SD-V)**: Text-to-video and image-to-video generation
- **Gen-2 (RunwayML)**: High-quality video synthesis via API
- **CogVideo**: Open-source Chinese video generation model
- **LTX-2**: Lightweight transformer-based video generation
- **Dream Machine**: Custom video generation pipeline

**Technical Stack:**
```yaml
Frameworks:
  - PyTorch: 2.1+
  - Diffusers: 0.25+ (Hugging Face)
  - CUDA: 12.1 (GPU acceleration)
  - xformers: 0.0.23 (memory efficient attention)

Models:
  - Stable Video Diffusion: stabilityai/stable-video-diffusion-img2vid-xt
  - AnimateDiff: guoyww/animatediff
  - ControlNet: lllyasviel/ControlNet
  
Processing:
  - FFmpeg: Video encoding and post-processing
  - OpenCV: Frame manipulation
  - MoviePy: Video composition
```

**Workflow:**
1. Parse script and extract scene descriptions
2. Generate character images using Stable Diffusion XL
3. Convert images to video using Stable Video Diffusion
4. Apply motion and transitions using AnimateDiff
5. Encode final video to MP4 format
6. Upload to S3 with metadata

---

## 2️⃣ Voice Synthesis

### TTS Models and Voice Options

| Function      | Recommendation                                             | Notes                         |
| ------------- | ---------------------------------------------------------- | ----------------------------- |
| TTS Models    | **ElevenLabs**, **Coqui TTS**, **OpenAI TTS**              | Multi-age & gender voices     |
| Voice Options | Baby, Toddler, 6yrs, 10yrs, Adult, Young Adult, Mature 25+ | Male & Female voices          |
| Features      | Voice cloning, text-to-speech, voice modulation            | Lip-sync compatible           |
| Input         | Script text + selected voice                               | Outputs audio track for video |

### Implementation Details

**Primary Services:**
- **ElevenLabs API**: Premium voice synthesis with emotion control
- **Coqui TTS**: Open-source, self-hosted TTS engine
- **OpenAI TTS**: GPT-4 powered voice generation
- **Azure Speech Services**: Enterprise-grade TTS with SSML support

**Voice Categories:**

```yaml
Age Groups:
  Baby (0-1 year):
    - Male: baby_boy_1, baby_boy_2
    - Female: baby_girl_1, baby_girl_2
  
  Toddler (2-5 years):
    - Male: toddler_boy_1, toddler_boy_2
    - Female: toddler_girl_1, toddler_girl_2
  
  Child (6-9 years):
    - Male: child_boy_1, child_boy_2
    - Female: child_girl_1, child_girl_2
  
  Pre-teen (10-12 years):
    - Male: preteen_boy_1, preteen_boy_2
    - Female: preteen_girl_1, preteen_girl_2
  
  Teen (13-17 years):
    - Male: teen_boy_1, teen_boy_2
    - Female: teen_girl_1, teen_girl_2
  
  Young Adult (18-24 years):
    - Male: young_adult_male_1, young_adult_male_2
    - Female: young_adult_female_1, young_adult_female_2
  
  Adult (25-45 years):
    - Male: adult_male_1, adult_male_2, adult_male_3
    - Female: adult_female_1, adult_female_2, adult_female_3
  
  Mature (45+ years):
    - Male: mature_male_1, mature_male_2
    - Female: mature_female_1, mature_female_2

Features:
  - Voice cloning from audio samples
  - Emotion control (happy, sad, angry, neutral)
  - Pitch and speed modulation
  - Multi-language support (English, Hindi, Spanish, etc.)
  - SSML support for advanced control
```

**Technical Stack:**
```yaml
APIs:
  - ElevenLabs API: Premium voices
  - OpenAI TTS API: gpt-4-audio
  - Coqui TTS: Self-hosted engine
  
Libraries:
  - pydub: Audio manipulation
  - librosa: Audio analysis
  - soundfile: Audio I/O
  - scipy: Signal processing
```

---

## 3️⃣ Lip-Sync & Face Animation

### Models and Capabilities

| Function | Recommendation                            | Notes                                    |
| -------- | ----------------------------------------- | ---------------------------------------- |
| Models   | **Wav2Lip**, **First Order Motion Model** | AI-driven face animation and lip-sync    |
| Input    | Character images + audio                  | Generates realistic mouth/head movements |
| Output   | Animated character video clip             | Integrated with generated video sequence |

### Implementation Details

**Primary Models:**
- **Wav2Lip**: State-of-the-art lip-sync model from IISc Bangalore
- **First Order Motion Model**: Face animation from keypoints
- **SadTalker**: 3D-aware face animation
- **FaceForensics**: Face manipulation detection (for quality control)

**Technical Stack:**
```yaml
Models:
  - Wav2Lip: rudrabha/Wav2Lip
  - FOMM: AliaksandrSiarohin/first-order-model
  - SadTalker: OpenTalker/SadTalker
  
Libraries:
  - face-alignment: Facial landmark detection
  - mediapipe: Real-time face tracking
  - dlib: Face detection and alignment
  - opencv-python: Image processing
  
GPU Requirements:
  - VRAM: 8GB+ recommended
  - CUDA compute capability: 7.0+
```

**Workflow:**
1. Detect face landmarks in character image
2. Extract audio features (mel-spectrograms)
3. Generate lip movements synchronized with audio
4. Apply facial animation using FOMM
5. Blend with original video frames
6. Post-process for quality enhancement

---

## 4️⃣ Music & Audio

### Audio Generation Capabilities

| Function                      | Recommendation                        | Notes                         |
| ----------------------------- | ------------------------------------- | ----------------------------- |
| Indian / Western Music        | OpenAI Jukebox, MIDI-based generation | Background tracks for videos  |
| Slokas / Sahasranamas / Poems | AI TTS or pre-recorded                | Multi-language support        |
| Audio Mixing                  | FFMPEG / Python libraries             | Merge voice + music + effects |

### Implementation Details

**Primary Services:**
- **OpenAI Jukebox**: Neural music generation
- **MusicGen (Meta)**: Text-to-music generation
- **AudioCraft**: Meta's audio generation toolkit
- **MIDI Generation**: Traditional music synthesis

**Technical Stack:**
```yaml
Music Generation:
  - audiocraft: Meta's audio generation
  - musicgen: facebook/musicgen-small
  - jukebox: openai/jukebox-1b-lyrics
  
Audio Processing:
  - FFmpeg: Audio mixing and encoding
  - pydub: Python audio manipulation
  - pedalboard: Spotify's audio effects library
  - soundfile: Audio I/O
  - librosa: Audio analysis
  
Effects & Mixing:
  - Reverb, Echo, Equalization
  - Compression and normalization
  - Multi-track mixing
  - Audio ducking (voice over music)

Indian Classical Support:
  - Carnatic raga patterns
  - Hindustani classical styles
  - Devotional sloka recitation
  - Vedic chanting synthesis
```

**Content Types:**
```yaml
Music Genres:
  - Indian Classical (Carnatic, Hindustani)
  - Bollywood
  - Western Classical
  - Pop, Rock, Jazz
  - Electronic, Ambient
  - Devotional (Bhajans, Kirtans)

Sacred Content:
  - Vedic Slokas
  - Vishnu Sahasranama
  - Lalita Sahasranama
  - Hanuman Chalisa
  - Sanskrit hymns
  - Multi-language devotional songs
```

---

## 5️⃣ Podcast-Style Videos

### Dual-Character Video Generation

| Function               | Recommendation                                     | Notes                                              |
| ---------------------- | -------------------------------------------------- | -------------------------------------------------- |
| Dual-character overlay | Custom AI pipeline using Wav2Lip + video synthesis | Both characters discussing / singing               |
| Input                  | Two images + script                                | Generates split-screen or conversation-style video |
| Output                 | MP4 video                                          | Stored and previewed in dashboard                  |

### Implementation Details

**Features:**
- Split-screen layouts (50/50, 60/40, 70/30)
- Over-the-shoulder shots
- Picture-in-picture mode
- Reaction shots
- Animated backgrounds
- Lower thirds with character names

**Technical Stack:**
```yaml
Pipeline:
  1. Generate voices for both characters (alternating dialogue)
  2. Create lip-sync animation for each character
  3. Composite characters side-by-side or in conversation layout
  4. Add background and visual effects
  5. Encode final podcast video

Layouts:
  - Split Screen: 50/50 vertical split
  - Host + Guest: 70/30 layout with main speaker prominent
  - Round Table: 4-person grid layout
  - Interview Style: Over-the-shoulder alternating shots
  
Technologies:
  - FFmpeg: Video composition
  - Pillow: Background generation
  - MoviePy: Scene composition
  - OpenCV: Frame manipulation
```

---

## 6️⃣ Subtitles & Multi-Language

### ASR and Translation Services

| Function            | Recommendation                             | Notes                                        |
| ------------------- | ------------------------------------------ | -------------------------------------------- |
| Subtitle Generation | Whisper ASR / OpenAI ASR                   | Converts audio to text                       |
| Multi-language      | Translation API (Google Translate, OpenAI) | Generates multilingual subtitles (.srt/.vtt) |

### Implementation Details

**Primary Services:**
- **OpenAI Whisper**: State-of-the-art speech recognition
- **Google Cloud Speech-to-Text**: Enterprise ASR
- **Azure Speech Services**: Multi-language support
- **Google Translate API**: Translation service
- **DeepL API**: High-quality translation

**Technical Stack:**
```yaml
Speech Recognition:
  - openai-whisper: Open-source ASR model
  - whisper-large-v3: Latest Whisper model
  - faster-whisper: Optimized Whisper inference
  
Translation:
  - googletrans: Google Translate Python API
  - deepl-python: DeepL API client
  - openai: GPT-4 translation
  
Subtitle Formats:
  - SRT: SubRip text format
  - VTT: WebVTT format
  - ASS/SSA: Advanced SubStation Alpha
  
Libraries:
  - pysrt: SRT file manipulation
  - webvtt-py: VTT file handling
  - ass: ASS/SSA subtitle support
```

**Supported Languages:**
```yaml
Primary Languages:
  - English (US, UK, AU)
  - Hindi
  - Spanish (ES, LA)
  - French
  - German
  - Portuguese (BR, PT)
  - Italian
  - Japanese
  - Korean
  - Chinese (Simplified, Traditional)
  - Arabic
  - Russian

Indian Languages:
  - Hindi
  - Tamil
  - Telugu
  - Malayalam
  - Kannada
  - Bengali
  - Marathi
  - Gujarati
  - Punjabi
  - Urdu
  - Sanskrit
```

**Features:**
- Auto-generated timestamps
- Speaker diarization (who said what)
- Punctuation restoration
- Formatting and styling
- Burn-in subtitles option
- Multi-language subtitle tracks

---

## 7️⃣ AI Job Management

### Queue and Worker Architecture

| Layer             | Recommendation                  | Notes                                                               |
| ----------------- | ------------------------------- | ------------------------------------------------------------------- |
| Queue / Scheduler | **BullMQ / RabbitMQ / AWS SQS** | Handle asynchronous AI video/audio processing                       |
| Worker Nodes      | Node.js / Python                | Process jobs for video generation, voice synthesis, lip-sync, music |
| GPU Compute       | AWS EC2 G4/G5 or Lambda GPU     | Required for video & animation rendering                            |
| Storage           | AWS S3                          | Store generated video, audio, thumbnails, subtitles                 |

### Implementation Details

**Queue Systems:**
- **AWS SQS**: Primary message queue (serverless, scalable)
- **BullMQ**: Redis-based job queue (for complex workflows)
- **RabbitMQ**: Alternative message broker (self-hosted)
- **Celery**: Python distributed task queue

**Technical Stack:**
```yaml
Job Queue:
  - AWS SQS: Standard and FIFO queues
  - BullMQ: Redis-backed job queue
  - Celery: Python task queue
  - Redis: In-memory data store
  
Worker Management:
  - AWS ECS/EKS: Container orchestration
  - Kubernetes: Worker pod management
  - Docker: Worker containerization
  - Spot Instances: Cost-optimized GPU compute
  
GPU Instances:
  - g4dn.xlarge: Entry-level GPU (T4, 16GB VRAM)
  - g4dn.2xlarge: Mid-range GPU (T4, 16GB VRAM, more CPU)
  - g5.xlarge: High-performance GPU (A10G, 24GB VRAM)
  - p3.2xlarge: Training/large models (V100, 16GB VRAM)
  
Storage:
  - S3: Object storage for assets
  - EFS: Shared file system for workers
  - EBS: Block storage for worker instances
```

**Job Types and Priorities:**
```yaml
Job Types:
  1. video_generation:
      priority: high
      timeout: 600s
      retry: 3
      
  2. voice_synthesis:
      priority: high
      timeout: 120s
      retry: 3
      
  3. lipsync_animation:
      priority: medium
      timeout: 300s
      retry: 2
      
  4. music_generation:
      priority: medium
      timeout: 240s
      retry: 2
      
  5. podcast_video:
      priority: medium
      timeout: 900s
      retry: 2
      
  6. subtitle_generation:
      priority: low
      timeout: 180s
      retry: 3

Priority Levels:
  - critical: Enterprise users, <30s queue time
  - high: Pro users, <2min queue time
  - medium: Free users, <5min queue time
  - low: Background jobs, <15min queue time
```

**Workflow Management:**
```yaml
Job Lifecycle:
  1. submitted: Job received and validated
  2. queued: Job added to priority queue
  3. processing: Worker picked up job
  4. rendering: AI model generating content
  5. post_processing: Encoding and optimization
  6. uploading: Uploading to S3
  7. completed: Job finished successfully
  8. failed: Job failed (with retry logic)
  
Monitoring:
  - CloudWatch: Job metrics and logs
  - Prometheus: Custom metrics
  - Grafana: Visualization dashboards
  - X-Ray: Distributed tracing
  
Auto-Scaling:
  - Scale workers based on queue depth
  - Spot instance fallback for cost optimization
  - GPU pool management
  - Priority-based resource allocation
```

---

## 8️⃣ AI Model Hosting

### Hosting Options

| Option                                 | Notes                                                         |
| -------------------------------------- | ------------------------------------------------------------- |
| API / SaaS (RunwayML, HuggingFace)     | Quick integration, less maintenance                           |
| Self-hosted (GCP/AWS GPU + Docker/K8s) | Full control, scalable, customizable, higher setup complexity |

### Implementation Details

**SaaS/API Services:**
```yaml
Video Generation:
  - RunwayML Gen-2: https://api.runwayml.com
  - Stability AI: https://api.stability.ai
  - Pika Labs: https://pika.art/api
  
Voice/TTS:
  - ElevenLabs: https://api.elevenlabs.io
  - OpenAI TTS: https://api.openai.com/v1/audio
  - Azure Speech: https://api.cognitive.microsoft.com
  
Translation:
  - Google Translate: https://translation.googleapis.com
  - DeepL: https://api-free.deepl.com
  
Pricing Considerations:
  - Pay-per-use model
  - API rate limits
  - Concurrent request limits
  - Storage costs
```

**Self-Hosted Infrastructure:**
```yaml
Model Serving:
  - TorchServe: PyTorch model serving
  - TensorFlow Serving: TF model serving
  - Triton Inference Server: NVIDIA's multi-framework serving
  - FastAPI: Custom model API
  
Container Orchestration:
  - Kubernetes (EKS): Production workloads
  - Docker Swarm: Simpler deployments
  - ECS Fargate: Serverless containers
  
Model Storage:
  - S3: Model artifacts storage
  - ECR: Container image registry
  - Model Registry: MLflow, DVC
  
Optimization:
  - ONNX Runtime: Cross-platform inference
  - TensorRT: NVIDIA GPU optimization
  - Quantization: INT8, FP16 precision
  - Model distillation: Smaller models
  
Cost Optimization:
  - Spot instances: Up to 90% savings
  - GPU sharing: Multiple models per GPU
  - Model caching: Reduce cold starts
  - Auto-scaling: Scale down idle resources
```

**Hybrid Approach (Recommended):**
```yaml
Production Strategy:
  Critical Services (SaaS):
    - High-quality voice synthesis (ElevenLabs)
    - Premium video generation (RunwayML)
    - Enterprise translation (DeepL)
    
  Self-Hosted Services:
    - Batch video generation (Stable Diffusion)
    - Lip-sync animation (Wav2Lip)
    - Music generation (MusicGen)
    - Subtitle generation (Whisper)
    
Benefits:
  - Reliability: SaaS backup for critical features
  - Cost: Self-hosted for high-volume tasks
  - Performance: Low-latency for local models
  - Flexibility: Custom models and workflows
```

---

## Summary

### 🔹 Complete AI / ML Stack Overview

```yaml
Video Models:
  - Stable Diffusion Video (SD-V)
  - Gen-2 (RunwayML)
  - CogVideo
  - LTX-2
  - Dream Machine
  - AnimateDiff
  
Voice / TTS:
  - ElevenLabs API
  - Coqui TTS
  - OpenAI TTS
  - Azure Speech Services
  - Multi-age voice support (Baby to Mature 45+)
  - Multi-gender support (Male/Female)
  
Lip-sync / Animation:
  - Wav2Lip
  - First Order Motion Model (FOMM)
  - SadTalker
  - MediaPipe Face Mesh
  
Music / Audio:
  - OpenAI Jukebox
  - MusicGen (Meta)
  - AudioCraft
  - MIDI generation
  - Indian classical music support
  - Slokas, sahasranamas, devotional content
  
Subtitles / Translation:
  - OpenAI Whisper ASR
  - Google Cloud Speech-to-Text
  - Google Translate API
  - DeepL API
  - 20+ language support
  - SRT/VTT/ASS formats
  
Podcast Video:
  - Dual-character AI overlay
  - Split-screen layouts
  - Conversation-style videos
  - Wav2Lip integration
  
Job Management:
  - AWS SQS (primary)
  - BullMQ (Redis-based)
  - RabbitMQ (alternative)
  - Celery (Python)
  - Priority queuing
  - Auto-scaling workers
  
GPU Compute:
  - AWS EC2 G4/G5 instances
  - Spot instances for cost optimization
  - EKS for container orchestration
  - Auto-scaling based on queue depth
  
Storage:
  - AWS S3 for all assets
  - Versioned and encrypted
  - CloudFront CDN for delivery
  - EFS for shared worker storage
```

### Key Features Supported

✅ **Video generation** with custom characters  
✅ **Multi-age, multi-gender** voice synthesis (Baby to Mature 45+)  
✅ **Lip-sync animation** with realistic mouth movements  
✅ **Music generation** (Indian classical, Western, devotional)  
✅ **Slokas, sahasranamas, and poems** (multi-language)  
✅ **Podcast-style conversation videos** (dual-character overlay)  
✅ **Multi-language subtitles** (20+ languages)  
✅ **Asynchronous job processing** with GPU workers  
✅ **Scalable infrastructure** on AWS  
✅ **Hybrid model hosting** (SaaS + self-hosted)

---

## Additional Resources

### Documentation
- [System Design Document](./architecture/system-design.md)
- [Functional Requirements](./requirements/FRD.md)
- [Non-Functional Requirements](./requirements/NFR.md)

### External Links
- [Stable Diffusion Video](https://stability.ai/stable-video)
- [ElevenLabs Documentation](https://docs.elevenlabs.io/)
- [Wav2Lip GitHub](https://github.com/Rudrabha/Wav2Lip)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Meta AudioCraft](https://github.com/facebookresearch/audiocraft)
- [AWS SQS Documentation](https://docs.aws.amazon.com/sqs/)

---

**Document Status:** ✅ Approved  
**Last Review Date:** 2025-12-31  
**Next Review Date:** 2026-03-31

---

*This document is maintained by the AI-Empower-HQ-360 team and is subject to updates as new AI technologies and models become available.*
