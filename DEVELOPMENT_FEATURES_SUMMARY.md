# Development Features Summary

## Overview
This document summarizes the new features implemented: **Podcast Mode** and **Subtitle Generation Improvements**.

## 1. Podcast Mode

### Backend API Endpoints (`src/api/routes/podcast.py`)

#### POST `/api/v1/podcast/generate`
- **Purpose**: Generate podcast-style videos with multiple characters
- **Request Body**:
  - `title`: Podcast episode title (required)
  - `characters`: List of 2-4 character configurations (required)
    - `character_id`: Unique identifier
    - `image_url`: S3 URL of character image
    - `voice_id`: Voice model ID
    - `name`: Character name for lower thirds
    - `role`: Role (Host, Guest, Speaker)
  - `dialogue`: List of dialogue lines (required)
    - `character_id`: Character speaking
    - `text`: Dialogue text
    - `emotion`: Emotion (neutral, happy, sad, etc.)
    - `timestamp`: Optional timestamp
  - `layout`: Video layout type (default: split_screen_50_50)
  - `background_style`: Background style (studio, room, etc.)
  - `add_lower_thirds`: Add character name overlays (default: true)
  - `add_background_music`: Add background music (default: false)
  - `duration`: Target duration in seconds (optional)
- **Response**: `{ job_id, status }`
- **Status Code**: 202 (Accepted)

#### GET `/api/v1/podcast/status/{job_id}`
- **Purpose**: Get the status of a podcast video generation job
- **Response**: Job status with video_url, thumbnail_url, duration, etc.
- **Status Codes**: 200 (Success), 404 (Not Found)

#### GET `/api/v1/podcast/layouts`
- **Purpose**: Get list of supported podcast video layouts
- **Response**: Array of layouts with descriptions and max character counts
- **Status Code**: 200 (Success)

#### GET `/api/v1/podcast/job/{job_id}/result`
- **Purpose**: Get the final result of a completed podcast video generation
- **Response**: Full job result with video URL, thumbnail, duration, etc.
- **Status Codes**: 200 (Success), 400 (Not Completed), 404 (Not Found)

### Frontend Component (`frontend/src/app/podcast/page.tsx`)

**Features**:
- Character management (add/remove up to 4 characters)
- Dialogue editor with character assignment
- Layout selection (6 supported layouts)
- Background style selection
- Lower thirds and background music options
- Real-time job status polling
- Result display with video and thumbnail URLs

**Supported Layouts**:
1. Split Screen 50/50 - Equal split between two characters
2. Split Screen 60/40 - Emphasis on host (60%) with guest (40%)
3. Split Screen 70/30 - Strong emphasis on main speaker
4. Over-the-Shoulder - Alternating over-shoulder shots
5. Picture-in-Picture - Main speaker with others in corner
6. Round Table - Four-person grid layout

## 2. Subtitle Generation Improvements

### Backend API Endpoints (`src/api/routes/subtitles.py`)

#### POST `/api/v1/subtitles/generate`
- **Purpose**: Generate subtitles from audio using ASR
- **Request Body**:
  - `audio_url`: S3 URL of audio file (required)
  - `model_name`: ASR model (default: whisper-large-v3)
  - `source_language`: Source language code (default: en)
  - `output_format`: Subtitle format - srt, vtt, or ass (default: srt)
  - `speaker_diarization`: Identify different speakers (default: false)
  - `max_line_length`: Max characters per line (default: 42, range: 20-80)
  - `languages`: Optional list for multi-language generation
- **Response**: `{ job_id, status }`
- **Status Code**: 202 (Accepted)

#### POST `/api/v1/subtitles/translate`
- **Purpose**: Translate subtitles to multiple languages
- **Request Body**:
  - `subtitle_url`: S3 URL of source subtitle file (required)
  - `target_languages`: List of target language codes (required)
  - `translation_service`: Translation service (default: google-translate)
  - `preserve_timing`: Preserve original timestamps (default: true)
- **Response**: `{ job_id, status }`
- **Status Code**: 202 (Accepted)

#### POST `/api/v1/subtitles/burn`
- **Purpose**: Burn subtitles into video (hardcoded)
- **Request Body**:
  - `video_url`: S3 URL of video file (required)
  - `subtitle_url`: S3 URL of subtitle file (required)
  - `font_name`: Font name (default: Arial)
  - `font_size`: Font size (default: 24, range: 12-72)
  - `font_color`: Font color (default: white)
  - `background_color`: Background color (default: black)
  - `position`: Subtitle position - top, bottom, or center (default: bottom)
- **Response**: `{ job_id, status }`
- **Status Code**: 202 (Accepted)

#### GET `/api/v1/subtitles/status/{job_id}`
- **Purpose**: Get the status of a subtitle job
- **Response**: Job status with subtitle_urls, video_url, languages, etc.
- **Status Codes**: 200 (Success), 404 (Not Found)

#### GET `/api/v1/subtitles/languages?model_name={model_name}`
- **Purpose**: Get list of supported languages for ASR
- **Query Parameters**: `model_name` (optional, default: whisper-large-v3)
- **Response**: List of supported language codes
- **Status Code**: 200 (Success)

#### GET `/api/v1/subtitles/formats`
- **Purpose**: Get list of supported subtitle formats
- **Response**: List of formats (srt, vtt, ass)
- **Status Code**: 200 (Success)

#### GET `/api/v1/subtitles/translation-services`
- **Purpose**: Get list of available translation services
- **Response**: List of services with provider and supported languages
- **Status Code**: 200 (Success)

### Frontend Component (`frontend/src/app/subtitles/page.tsx`)

**Features**:
- **Generate Tab**: 
  - Audio URL input
  - ASR model selection
  - Source language selection
  - Output format selection (SRT, VTT, ASS)
  - Speaker diarization toggle
  - Max line length configuration
  - Multi-language generation support
- **Translate Tab**:
  - Subtitle URL input
  - Translation service selection
  - Multiple target language selection
  - Preserve timing option
- **Burn Tab**:
  - Video and subtitle URL inputs
  - Font customization (name, size, color)
  - Background color configuration
  - Position selection (top, bottom, center)
- Real-time job status polling
- Result display with subtitle URLs and video URL

## API Client Updates (`frontend/src/lib/api.ts`)

Added methods for:
- `generatePodcast()` - Start podcast video generation
- `getPodcastStatus()` - Check podcast job status
- `getPodcastLayouts()` - Get supported layouts
- `generateSubtitles()` - Start subtitle generation
- `translateSubtitles()` - Start subtitle translation
- `burnSubtitles()` - Start subtitle burning
- `getSubtitleStatus()` - Check subtitle job status
- `getSupportedLanguages()` - Get supported languages
- `getSupportedFormats()` - Get supported formats
- `getTranslationServices()` - Get translation services

## Integration

### Backend Integration
- Routes registered in `src/api/main.py`
- Routes exported in `src/api/routes/__init__.py`
- Services use existing `PodcastVideoService` and `SubtitleMultilangService`

### Frontend Integration
- Pages created at `/podcast` and `/subtitles`
- API client methods added to `api.ts`
- Tabs component created for subtitle page UI

## Next Steps

1. **UI Components**: Create or install shadcn/ui components (Button, Card, Input, Select, etc.) if not already available
2. **Navigation**: Add links to podcast and subtitles pages in the main navigation
3. **Error Handling**: Enhance error handling and user feedback
4. **Testing**: Add unit and integration tests for new endpoints
5. **Documentation**: Update API documentation with new endpoints

## Notes

- All endpoints use background tasks for long-running operations
- Job status polling implemented in frontend components
- Services support both typed (Pydantic) and dict inputs for flexibility
- Multi-language subtitle generation supported
- All operations are asynchronous and return job IDs for status tracking
