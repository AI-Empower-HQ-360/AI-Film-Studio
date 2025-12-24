# Automated Film Production Workflow

## Overview

This document describes the fully automated end-to-end workflow implementation for the AI Film Studio. The system takes a script as input and produces a final MP4 film without any human intervention.

## Architecture

```
User → Script → Backend → Workflow Engine → Queue → Workers → Storage → Final MP4 → User
```

## Components

### 1. Workflow Engine (`src/services/orchestrator.py`)

The brain of the automation system. Responsibilities:

- ✅ Validates and moderates scripts
- ✅ Breaks scripts into scenes
- ✅ Breaks scenes into shots
- ✅ Estimates costs and reserves credits
- ✅ Creates task dependency graph
- ✅ Pushes tasks to queue
- ✅ Tracks job progress
- ✅ Triggers composition when ready
- ✅ Handles job completion/failure

### 2. Queue System (`src/services/queue.py`)

In-memory queue with Redis-compatible interface. Features:

- ✅ Holds all shot-level tasks
- ✅ Automatic retry logic
- ✅ Dead-letter queue (DLQ) for failed tasks
- ✅ Task priority support
- ✅ Worker task distribution

### 3. Worker System (`src/services/worker.py`)

Autonomous workers that process tasks. Each worker:

- ✅ Pulls tasks from queue automatically
- ✅ Loads shot and consistency context
- ✅ Calls appropriate AI models (image/video/voice/music)
- ✅ Uploads outputs to storage
- ✅ Updates backend with results
- ✅ Requests next task
- ✅ Handles failures and retries

### 4. Storage Layer (`src/services/storage.py`)

In-memory storage for jobs, scenes, and shots:

- ✅ Job lifecycle management
- ✅ Scene and shot tracking
- ✅ Status updates
- ✅ Asset URL storage

### 5. Script Parser (`src/services/script_parser.py`)

Parses film scripts into structured data:

- ✅ Extracts scenes from script
- ✅ Extracts shots from each scene
- ✅ Parses metadata (location, time, duration)
- ✅ Handles both structured and unstructured scripts

### 6. API Endpoints (`src/api/routes.py`)

RESTful API for workflow control:

- ✅ `POST /api/v1/jobs` - Submit script and create job
- ✅ `GET /api/v1/jobs/{job_id}` - Get job status
- ✅ `GET /api/v1/jobs/{job_id}/state` - Get detailed workflow state
- ✅ `GET /api/v1/jobs/{job_id}/download` - Get final video download URL
- ✅ `GET /api/v1/jobs` - List all jobs
- ✅ `POST /api/v1/jobs/{job_id}/cancel` - Cancel job

## Complete Automation Flow

```
1. User submits script via POST /api/v1/jobs
2. Backend validates + moderates script
3. Backend creates job record
4. Script parser breaks script into scenes → shots
5. Orchestrator estimates cost
6. Orchestrator builds task graph
7. Tasks pushed to queue
8. Background workers automatically start
9. Workers pull tasks from queue
10. Workers generate videos/images/audio per shot
11. Workers upload assets to storage
12. Workers update shot status in backend
13. Orchestrator tracks progress
14. When all shots complete, orchestrator triggers composition
15. Worker composes final MP4 with FFmpeg
16. Backend marks job as completed
17. User gets download URL
18. User downloads final film
```

## Data Models (`src/models/workflow.py`)

### JobStatus
- `PENDING` - Job created, not yet validated
- `VALIDATING` - Script being validated
- `QUEUED` - Tasks queued for processing
- `PROCESSING` - Workers processing tasks
- `COMPOSING` - Final composition in progress
- `COMPLETED` - Film ready for download
- `FAILED` - Job failed
- `CANCELLED` - Job cancelled by user

### TaskStatus
- `PENDING` - Task created
- `QUEUED` - In queue
- `RUNNING` - Being processed
- `COMPLETED` - Successfully completed
- `FAILED` - Failed and in DLQ
- `RETRYING` - Being retried

### TaskType
- `VIDEO_GENERATION` - Generate video for shot
- `VOICE_GENERATION` - Generate audio/voice for shot
- `IMAGE_GENERATION` - Generate image
- `MUSIC_GENERATION` - Generate background music
- `COMPOSITION` - Final video composition

## Script Format

The system supports both structured and unstructured scripts.

### Structured Format (Recommended)

```
SCENE 1: INT. OFFICE - DAY
Description of the scene

SHOT 1: Wide shot - 5s
Camera pans across the busy office

SHOT 2: Close up - 3s
Focus on protagonist at desk

SCENE 2: EXT. PARK - AFTERNOON
Beautiful park setting

SHOT 1: Medium shot - 4s
Walking through the park
```

### Unstructured Format

The system will automatically create a default scene and shot:

```
A hero's journey through an enchanted forest...
```

## Usage Example

### 1. Create a Job

```bash
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "script": "SCENE 1: INT. ROOM - DAY\nSHOT 1: Wide - 5s\nA person enters",
    "title": "My First Film"
  }'
```

### 2. Check Job Status

```bash
curl http://localhost:8000/api/v1/jobs/job-abc123
```

### 3. Download Final Film

```bash
curl http://localhost:8000/api/v1/jobs/job-abc123/download
```

## Testing

Run the test suite:

```bash
pytest tests/
```

## License

See LICENSE file for details.
