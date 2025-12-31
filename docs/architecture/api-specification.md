# API Specification - AI Film Studio Backend

**Version:** 1.0  
**Last Updated:** 2025-12-31  
**Document Owner:** AI-Empower-HQ-360

---

## Overview

This document provides detailed API specifications for all microservices in the AI Film Studio backend.

**Base URLs:**
- User Service: `http://localhost:3001/api`
- Project Service: `http://localhost:3002/api`
- Credit Service: `http://localhost:3003/api`
- AI Job Service: `http://localhost:3004/api`
- YouTube Service: `http://localhost:3005/api`
- Admin Service: `http://localhost:3006/api`

---

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

---

## User Service APIs

### POST /users/register

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "tier": "free",
    "credits": 3
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### POST /users/login

Login with email and password.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "tier": "free",
    "credits": 3
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### GET /users/profile

Get current user profile (requires authentication).

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "tier": "free",
  "credits": 3,
  "createdAt": "2025-12-31T17:00:00Z"
}
```

---

### PUT /users/profile

Update user profile (requires authentication).

**Request Body:**
```json
{
  "name": "Jane Doe"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Jane Doe",
  "tier": "free"
}
```

---

## Project Service APIs

### POST /projects/create

Create a new project (requires authentication).

**Request Body:**
```json
{
  "name": "My First Film",
  "description": "A short film about AI",
  "videoType": "story",
  "language": "en"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "userId": "uuid",
  "name": "My First Film",
  "description": "A short film about AI",
  "status": "draft",
  "videoType": "story",
  "language": "en",
  "createdAt": "2025-12-31T17:00:00Z"
}
```

---

### GET /projects

List user's projects (requires authentication).

**Query Parameters:**
- `status` (optional): Filter by status (draft, processing, completed, failed)
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20)

**Response (200 OK):**
```json
{
  "projects": [
    {
      "id": "uuid",
      "name": "My First Film",
      "status": "completed",
      "createdAt": "2025-12-31T17:00:00Z"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 1
}
```

---

### GET /projects/:id

Get project details (requires authentication).

**Response (200 OK):**
```json
{
  "id": "uuid",
  "userId": "uuid",
  "name": "My First Film",
  "description": "A short film about AI",
  "status": "completed",
  "videoType": "story",
  "language": "en",
  "outputUrl": "s3://bucket/path/video.mp4",
  "createdAt": "2025-12-31T17:00:00Z",
  "updatedAt": "2025-12-31T18:00:00Z"
}
```

---

### POST /projects/:id/regenerate

Regenerate project with new parameters (requires authentication).

**Request Body:**
```json
{
  "style": "anime",
  "duration": 60
}
```

**Response (202 Accepted):**
```json
{
  "jobId": "uuid",
  "status": "queued",
  "message": "Regeneration started"
}
```

---

### DELETE /projects/:id

Delete a project (requires authentication).

**Response (200 OK):**
```json
{
  "message": "Project deleted successfully"
}
```

---

## Credit Service APIs

### GET /credits/balance

Get user's credit balance (requires authentication).

**Response (200 OK):**
```json
{
  "balance": 15,
  "tier": "pro",
  "history": [
    {
      "type": "deduction",
      "amount": -1,
      "description": "Video generation",
      "createdAt": "2025-12-31T17:00:00Z"
    }
  ]
}
```

---

### POST /credits/topup

Purchase additional credits (requires authentication).

**Request Body:**
```json
{
  "quantity": 10
}
```

**Response (200 OK):**
```json
{
  "stripeSessionId": "cs_test_...",
  "redirectUrl": "https://checkout.stripe.com/..."
}
```

---

### GET /plans

Get available subscription plans.

**Response (200 OK):**
```json
{
  "plans": [
    {
      "id": "free",
      "name": "Free",
      "price": 0,
      "credits": 3,
      "features": ["Watermarked videos", "3 videos/month"]
    },
    {
      "id": "pro",
      "name": "Pro",
      "price": 29,
      "credits": 30,
      "features": ["No watermark", "30 videos/month", "Priority support"]
    }
  ]
}
```

---

## AI Job Service APIs

### POST /ai/video-generate

Generate video from text prompt (requires authentication).

**Request Body:**
```json
{
  "projectId": "uuid",
  "prompt": "A cinematic scene of a sunset over mountains",
  "style": "cinematic",
  "duration": 30
}
```

**Response (202 Accepted):**
```json
{
  "jobId": "uuid",
  "status": "queued",
  "estimatedTime": "3-5 minutes"
}
```

---

### POST /ai/audio-generate

Generate audio/voice from text (requires authentication).

**Request Body:**
```json
{
  "projectId": "uuid",
  "text": "Welcome to AI Film Studio",
  "voiceId": "male-young-energetic",
  "language": "en"
}
```

**Response (202 Accepted):**
```json
{
  "jobId": "uuid",
  "status": "queued",
  "estimatedTime": "1-2 minutes"
}
```

---

### POST /ai/lip-sync

Apply lip-sync to video (requires authentication).

**Request Body:**
```json
{
  "projectId": "uuid",
  "videoPath": "s3://bucket/video.mp4",
  "audioPath": "s3://bucket/audio.mp3"
}
```

**Response (202 Accepted):**
```json
{
  "jobId": "uuid",
  "status": "queued",
  "estimatedTime": "2-4 minutes"
}
```

---

### POST /ai/music-generate

Generate background music (requires authentication).

**Request Body:**
```json
{
  "projectId": "uuid",
  "prompt": "Upbeat electronic music",
  "duration": 30,
  "genre": "electronic"
}
```

**Response (202 Accepted):**
```json
{
  "jobId": "uuid",
  "status": "queued",
  "estimatedTime": "1-3 minutes"
}
```

---

### GET /ai/jobs/:id/status

Get job status (requires authentication).

**Response (200 OK):**
```json
{
  "id": "uuid",
  "projectId": "uuid",
  "type": "video_generation",
  "status": "processing",
  "progress": 65,
  "createdAt": "2025-12-31T17:00:00Z",
  "startedAt": "2025-12-31T17:01:00Z"
}
```

---

## YouTube Service APIs

### POST /youtube/upload

Upload video to YouTube (requires authentication + YouTube OAuth).

**Request Body:**
```json
{
  "projectId": "uuid",
  "title": "My AI Generated Film",
  "description": "Created with AI Film Studio",
  "tags": ["AI", "Film", "Generated"],
  "privacy": "public"
}
```

**Response (200 OK):**
```json
{
  "videoId": "dQw4w9WgXcQ",
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "status": "uploaded"
}
```

---

### POST /youtube/playlist

Create YouTube playlist (requires authentication + YouTube OAuth).

**Request Body:**
```json
{
  "title": "My AI Films",
  "description": "Collection of AI-generated films",
  "privacy": "public"
}
```

**Response (201 Created):**
```json
{
  "playlistId": "PLxxxxxxxxxxxxxx",
  "title": "My AI Films",
  "url": "https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxx"
}
```

---

### GET /youtube/videos

Get user's uploaded YouTube videos (requires authentication).

**Response (200 OK):**
```json
{
  "videos": [
    {
      "id": "dQw4w9WgXcQ",
      "title": "My AI Generated Film",
      "views": 1250,
      "uploadedAt": "2025-12-31T17:00:00Z"
    }
  ]
}
```

---

## Admin Service APIs

### GET /admin/users

List all users (requires admin authentication).

**Query Parameters:**
- `search` (optional): Search by email or name
- `tier` (optional): Filter by tier
- `page` (optional): Page number
- `limit` (optional): Items per page

**Response (200 OK):**
```json
{
  "users": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "name": "John Doe",
      "tier": "pro",
      "credits": 15,
      "createdAt": "2025-12-31T17:00:00Z"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 150
}
```

---

### GET /admin/analytics

Get platform analytics (requires admin authentication).

**Response (200 OK):**
```json
{
  "totalUsers": 1500,
  "activeUsers": 450,
  "totalProjects": 3200,
  "totalVideosGenerated": 2800,
  "avgGenerationTime": "4.2 minutes",
  "systemLoad": {
    "cpuUsage": 65,
    "memoryUsage": 72,
    "queueDepth": 12
  }
}
```

---

### POST /admin/users/:id/grant-credits

Grant credits to a user (requires admin authentication).

**Request Body:**
```json
{
  "amount": 10,
  "reason": "Customer support compensation"
}
```

**Response (200 OK):**
```json
{
  "userId": "uuid",
  "newBalance": 25,
  "message": "Credits granted successfully"
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Invalid request parameters",
  "details": {
    "field": "email",
    "message": "Invalid email format"
  }
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "error": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "retryAfter": 60
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-31  
**Status:** Approved
