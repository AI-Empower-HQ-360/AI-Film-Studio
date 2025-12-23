# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Refresh Token
```http
POST /auth/refresh
```

**Request Body:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```

## Projects

### Create Project
```http
POST /projects/
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "My First Film",
  "description": "A short film about AI"
}
```

### List Projects
```http
GET /projects/
Authorization: Bearer <token>
```

### Get Project
```http
GET /projects/{project_id}
Authorization: Bearer <token>
```

### Update Project
```http
PUT /projects/{project_id}
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "Updated Film Name",
  "description": "Updated description"
}
```

### Delete Project
```http
DELETE /projects/{project_id}
Authorization: Bearer <token>
```

## Jobs

### Create Job
```http
POST /jobs/
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "project_id": 1,
  "script": "A beautiful sunrise over mountains\nBirds flying in the sky\nA peaceful lake",
  "config": {
    "num_images": 10,
    "video_duration": 30,
    "include_voice": true,
    "include_music": true,
    "fps": 30,
    "quality": "high",
    "voice": "default",
    "genre": "cinematic",
    "mood": "inspiring"
  }
}
```

**Response:**
```json
{
  "id": 1,
  "project_id": 1,
  "user_id": 1,
  "script": "...",
  "status": "pending",
  "progress": 0.0,
  "estimated_cost": 2.45,
  "actual_cost": 0.0,
  "moderation_status": "approved",
  "moderation_score": 0.1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### List Jobs
```http
GET /jobs/
Authorization: Bearer <token>
```

### Get Job
```http
GET /jobs/{job_id}
Authorization: Bearer <token>
```

### Update Job
```http
PATCH /jobs/{job_id}
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "status": "processing",
  "progress": 50.0
}
```

### Cancel Job
```http
POST /jobs/{job_id}/cancel
Authorization: Bearer <token>
```

### Estimate Cost
```http
POST /jobs/estimate-cost
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "num_images": 10,
  "video_duration": 30,
  "include_voice": true,
  "include_music": true
}
```

**Response:**
```json
{
  "estimated_cost": 2.45,
  "breakdown": {
    "image_generation": 0.20,
    "video_generation": 1.50,
    "voice_synthesis": 0.45,
    "music_synthesis": 0.30,
    "ffmpeg_processing": 0.03
  }
}
```

### Get Signed Download URL
```http
POST /jobs/signed-url
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "job_id": 1
}
```

**Response:**
```json
{
  "url": "https://s3.amazonaws.com/...",
  "expires_at": "2024-01-01T01:00:00"
}
```

## Job States

Jobs progress through the following states:

1. **pending** - Job created, waiting to be queued
2. **queued** - Job added to worker queue
3. **moderating** - Content being moderated
4. **moderation_failed** - Content failed moderation
5. **processing** - AI generation in progress
6. **completed** - Job finished successfully
7. **failed** - Job failed during processing
8. **cancelled** - Job cancelled by user

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

Common HTTP status codes:
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (missing or invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

## Rate Limiting

- Maximum 100 requests per minute per user
- Maximum 1000 requests per hour per user

## Cost Limits

- Maximum $100 per job
- Maximum $500 per user per day
