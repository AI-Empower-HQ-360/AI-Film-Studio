# 🔌 AI Film Studio - API Reference

**Version**: 1.0  
**Base URL**: `https://api.aifilmstudio.com/api/v1`  
**Last Updated**: December 31, 2025

---

## Overview

The AI Film Studio API provides programmatic access to our video generation platform. Use the API to integrate AI video creation into your applications, workflows, and services.

### Key Features

- RESTful API design
- JSON request/response format
- JWT authentication
- Rate limiting
- Comprehensive error handling
- Webhook notifications
- Batch operations support

---

## Authentication

### API Key

All API requests require authentication using an API key.

**Header**:
```http
Authorization: Bearer YOUR_API_KEY
```

### Getting Your API Key

1. Log in to your AI Film Studio account
2. Navigate to Settings → API Keys
3. Click "Generate New API Key"
4. Copy and securely store your key

**Security Best Practices**:
- Never share your API key publicly
- Rotate keys regularly (every 90 days)
- Use environment variables
- Restrict key permissions by IP if possible

---

## Rate Limits

| Plan | Requests/Minute | Requests/Day |
|------|----------------|--------------|
| Free | 10 | 100 |
| Standard | 60 | 5,000 |
| Pro | 120 | 20,000 |
| Enterprise | Custom | Custom |

**Rate Limit Headers**:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1704038400
```

---

## Endpoints

### Projects

#### Create Project

```http
POST /projects
```

**Request Body**:
```json
{
  "title": "My Video Project",
  "script": "A compelling story about innovation...",
  "settings": {
    "duration": 60,
    "style": "cinematic",
    "language": "en",
    "subtitle_languages": ["en", "es"]
  }
}
```

**Response**: `201 Created`
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "My Video Project",
  "status": "draft",
  "estimated_credits": 3,
  "created_at": "2025-12-31T10:00:00Z"
}
```

#### Get Project

```http
GET /projects/{project_id}
```

**Response**: `200 OK`
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "My Video Project",
  "script": "A compelling story about innovation...",
  "status": "completed",
  "assets": {
    "video_url": "https://cdn.aifilmstudio.com/videos/...",
    "thumbnail_url": "https://cdn.aifilmstudio.com/thumbnails/..."
  },
  "created_at": "2025-12-31T10:00:00Z",
  "completed_at": "2025-12-31T10:05:00Z"
}
```

#### List Projects

```http
GET /projects?page=1&per_page=20&status=completed
```

**Query Parameters**:
- `page` (integer): Page number (default: 1)
- `per_page` (integer): Items per page (default: 20, max: 100)
- `status` (string): Filter by status (draft, processing, completed, failed)
- `sort` (string): Sort field (created_at, updated_at)
- `order` (string): Sort order (asc, desc)

**Response**: `200 OK`
```json
{
  "projects": [...],
  "total_count": 42,
  "page": 1,
  "per_page": 20,
  "total_pages": 3
}
```

---

### Video Generation

#### Generate Video

```http
POST /projects/{project_id}/generate
```

**Request Body**:
```json
{
  "settings": {
    "duration": 60,
    "style": "cinematic",
    "characters": [
      {
        "name": "narrator",
        "age": "adult",
        "gender": "male",
        "voice": "deep"
      }
    ],
    "music_genre": "epic",
    "include_subtitles": true,
    "subtitle_languages": ["en", "es"],
    "youtube_upload": false
  }
}
```

**Response**: `202 Accepted`
```json
{
  "job_id": "660e9511-f39c-52e5-b827-557766551111",
  "status": "queued",
  "estimated_time": "3-5 minutes",
  "credits_deducted": 3
}
```

#### Get Job Status

```http
GET /jobs/{job_id}
```

**Response**: `200 OK`
```json
{
  "job_id": "660e9511-f39c-52e5-b827-557766551111",
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 65,
  "current_step": "voice_synthesis",
  "estimated_time_remaining": "90 seconds",
  "started_at": "2025-12-31T10:00:00Z"
}
```

---

### Webhooks

#### Register Webhook

```http
POST /webhooks
```

**Request Body**:
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["job.completed", "job.failed"],
  "secret": "your_webhook_secret"
}
```

**Response**: `201 Created`
```json
{
  "webhook_id": "770f0622-g40d-63f6-c938-668877662222",
  "url": "https://your-app.com/webhook",
  "events": ["job.completed", "job.failed"],
  "created_at": "2025-12-31T10:00:00Z"
}
```

#### Webhook Payload

```json
{
  "event": "job.completed",
  "timestamp": "2025-12-31T10:05:00Z",
  "data": {
    "job_id": "660e9511-f39c-52e5-b827-557766551111",
    "project_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "output_url": "https://cdn.aifilmstudio.com/videos/..."
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing or invalid API key |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |
| 503 | Service Unavailable - Temporary outage |

**Error Response Format**:
```json
{
  "error": {
    "code": "INSUFFICIENT_CREDITS",
    "message": "You don't have enough credits to generate this video.",
    "details": {
      "required": 3,
      "available": 0
    }
  }
}
```

---

## Code Examples

### Python

```python
import requests

API_KEY = "your_api_key"
BASE_URL = "https://api.aifilmstudio.com/api/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Create project
project_data = {
    "title": "My Video",
    "script": "An amazing story...",
    "settings": {"duration": 60}
}

response = requests.post(
    f"{BASE_URL}/projects",
    json=project_data,
    headers=headers
)

project = response.json()
print(f"Project created: {project['project_id']}")

# Generate video
job_response = requests.post(
    f"{BASE_URL}/projects/{project['project_id']}/generate",
    json={"settings": {"duration": 60}},
    headers=headers
)

job = job_response.json()
print(f"Job started: {job['job_id']}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_KEY = 'your_api_key';
const BASE_URL = 'https://api.aifilmstudio.com/api/v1';

const headers = {
  'Authorization': `Bearer ${API_KEY}`,
  'Content-Type': 'application/json'
};

// Create project
async function createProject() {
  const response = await axios.post(
    `${BASE_URL}/projects`,
    {
      title: 'My Video',
      script: 'An amazing story...',
      settings: { duration: 60 }
    },
    { headers }
  );
  
  return response.data;
}

// Generate video
async function generateVideo(projectId) {
  const response = await axios.post(
    `${BASE_URL}/projects/${projectId}/generate`,
    {
      settings: { duration: 60 }
    },
    { headers }
  );
  
  return response.data;
}

createProject().then(project => {
  console.log(`Project created: ${project.project_id}`);
  return generateVideo(project.project_id);
}).then(job => {
  console.log(`Job started: ${job.job_id}`);
});
```

---

## Support

**Documentation**: https://docs.aifilmstudio.com  
**Support Email**: api-support@aifilmstudio.com  
**Community Forum**: https://community.aifilmstudio.com  
**Status Page**: https://status.aifilmstudio.com

---

*For complete API documentation, visit https://docs.aifilmstudio.com/api*
