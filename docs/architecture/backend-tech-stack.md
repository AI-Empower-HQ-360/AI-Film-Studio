# Backend Tech Stack - AI Film Studio

**Version:** 1.0  
**Last Updated:** 2025-12-31  
**Document Owner:** AI-Empower-HQ-360

---

## Table of Contents

1. [Overview](#overview)
2. [Framework / Runtime](#1-framework--runtime)
3. [Database Layer](#2-database-layer)
4. [Microservices Architecture](#3-microservices-architecture)
5. [Authentication & Security](#4-authentication--security)
6. [AI / ML Integration](#5-ai--ml-integration)
7. [File & Media Handling](#6-file--media-handling)
8. [Queue / Job Management](#7-queue--job-management)
9. [Monitoring & Logging](#8-monitoring--logging)
10. [API Endpoints](#9-api-endpoints)
11. [Technology Stack Summary](#10-technology-stack-summary)

---

## Overview

This document provides a comprehensive overview of the backend technology stack for AI Film Studio. The platform utilizes a microservices architecture built on Node.js, enabling scalable AI-powered video generation, voice synthesis, lip-sync, and YouTube integration.

### Key Design Principles

- **Microservices Architecture**: Independent, scalable services
- **Asynchronous Processing**: Queue-based job processing for AI tasks
- **API-First Design**: RESTful APIs with optional GraphQL support
- **Scalability**: Horizontal scaling for each microservice
- **Reliability**: Fault tolerance and graceful degradation

---

## 1. Framework / Runtime

### Runtime Environment

| Layer | Technology | Notes |
|-------|------------|-------|
| **Runtime** | Node.js 18.x LTS | Fast, asynchronous, suitable for microservices and AI API calls |
| **Framework** | Express.js / NestJS | Express: lightweight & flexible; NestJS: structured, scalable, dependency injection |
| **API Type** | REST (MVP) / GraphQL (optional) | REST for core endpoints, GraphQL for complex data queries |

### Framework Selection

#### Express.js (Recommended for MVP)
```javascript
// Lightweight and flexible
const express = require('express');
const app = express();

app.use(express.json());
app.use('/api/users', userRoutes);
app.use('/api/projects', projectRoutes);
app.use('/api/ai', aiRoutes);

app.listen(3000, () => {
  console.log('AI Film Studio API running on port 3000');
});
```

**Advantages:**
- Minimal overhead, maximum flexibility
- Large ecosystem of middleware
- Easy to learn and implement
- Perfect for MVP and rapid development

#### NestJS (Recommended for Production Scale)
```typescript
// Structured, scalable architecture
import { Module } from '@nestjs/common';
import { UserModule } from './user/user.module';
import { ProjectModule } from './project/project.module';
import { AIModule } from './ai/ai.module';

@Module({
  imports: [UserModule, ProjectModule, AIModule],
})
export class AppModule {}
```

**Advantages:**
- Built-in dependency injection
- TypeScript first
- Modular architecture
- Built-in support for microservices
- Enterprise-ready patterns

---

## 2. Database Layer

### Relational Database

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Primary DB** | PostgreSQL 15 / MySQL 8 | Store users, projects, credits, subscription data |
| **Caching** | Redis 7.x | Fast project status updates, AI job queue, credits balance |
| **File Storage** | AWS S3 / GCP Storage | Store uploaded images, generated videos, thumbnails |

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    oauth_provider VARCHAR(50),
    oauth_id VARCHAR(255),
    tier VARCHAR(20) DEFAULT 'free',
    credits INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_oauth ON users(oauth_provider, oauth_id);
```

#### Projects Table
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    video_type VARCHAR(50),
    language VARCHAR(10) DEFAULT 'en',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
```

#### Jobs Table
```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'queued',
    progress INT DEFAULT 0,
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_jobs_project_id ON jobs(project_id);
CREATE INDEX idx_jobs_status ON jobs(status);
```

---

## 3. Microservices Architecture

### Service Breakdown

| Service | Port | Responsibilities |
|---------|------|------------------|
| **User Service** | 3001 | Registration, login, profile, OAuth integration |
| **Project Service** | 3002 | Create project, track status, generate AI videos, store metadata |
| **Credit / Subscription Service** | 3003 | Manage plans, credits deduction, top-ups |
| **AI Job Service** | 3004 | Handle video generation, voice synthesis, lip-sync, podcast overlay, music integration |
| **YouTube Service** | 3005 | Upload videos, manage playlists, generate thumbnails |
| **Admin Service** | 3006 | Analytics, user/project management, logs, moderation |

---

## 4. Authentication & Security

### JWT Authentication

| Layer | Technology | Notes |
|-------|------------|-------|
| **Auth Method** | JWT (JSON Web Tokens) | For API authentication |
| **OAuth 2.0** | Google / YouTube | Login & channel integration |
| **Encryption** | bcrypt / AES | Store passwords, sensitive info securely |
| **API Security** | Rate limiting, input validation, HTTPS | Protect endpoints from abuse |

---

## 5. AI / ML Integration

### AI Service Providers

| Layer | Technology | Notes |
|-------|------------|-------|
| **Video Generation** | Stable Diffusion Video (SD-V), Gen-2, CogVideo, LTX-2, Dream Machine | Pre-trained models or API endpoints |
| **Voice Synthesis** | ElevenLabs, Coqui TTS, OpenAI TTS | Multi-age & gender voices |
| **Lip-sync / Animation** | Wav2Lip, First Order Motion Model | Character animation & podcast overlays |
| **Music & Slokas** | OpenAI Jukebox, MIDI-based generation | Background music, slokas, poems |

---

## 6. File & Media Handling

### File Upload Flow

1. **Uploaded Images**: Stored in S3 → linked to project metadata
2. **Generated Videos**: Stored in S3 → video URLs returned to frontend
3. **Thumbnails**: Auto-generated via AI → stored in S3
4. **Subtitles**: Stored as .vtt / .srt → linked to project

---

## 7. Queue / Job Management

### Queue Technologies

| Layer | Technology | Notes |
|-------|------------|-------|
| **Job Queue** | BullMQ / RabbitMQ / AWS SQS | Manage AI video generation jobs asynchronously |
| **Worker Services** | Node.js / Python microservices | Process AI tasks (video, audio, animation) |

---

## 8. Monitoring & Logging

### Monitoring Stack

| Layer | Technology | Notes |
|-------|------------|-------|
| **Logs** | CloudWatch / ELK Stack | Track errors, video generation status, user actions |
| **Metrics** | Prometheus + Grafana | CPU/GPU usage, queue length, job duration |
| **Alerts** | CloudWatch Alarms | Notify on failed jobs, high latency, or downtime |

---

## 9. API Endpoints

### User Service

```
POST /api/users/register
POST /api/users/login
GET  /api/users/profile
PUT  /api/users/profile
```

### Project Service

```
POST   /api/projects/create
GET    /api/projects/:id
POST   /api/projects/:id/regenerate
DELETE /api/projects/:id
```

### Credit / Subscription

```
GET  /api/credits/balance
POST /api/credits/topup
GET  /api/plans
```

### YouTube Service

```
POST /api/youtube/upload
POST /api/youtube/playlist
GET  /api/youtube/videos
```

### AI Job Service

```
POST /api/ai/video-generate
POST /api/ai/audio-generate
POST /api/ai/lip-sync
POST /api/ai/music-generate
```

---

## 10. Technology Stack Summary

### Complete Technology Stack

```yaml
Backend Framework:
  Runtime: Node.js 18.x LTS
  Framework: Express.js / NestJS
  Language: JavaScript / TypeScript
  API: REST / GraphQL (optional)

Database:
  Primary: PostgreSQL 15 / MySQL 8
  Cache: Redis 7.x
  Storage: AWS S3 / Google Cloud Storage

Microservices:
  - User Service (Port 3001)
  - Project Service (Port 3002)
  - Credit Service (Port 3003)
  - AI Job Service (Port 3004)
  - YouTube Service (Port 3005)
  - Admin Service (Port 3006)

Authentication:
  Method: JWT (JSON Web Tokens)
  OAuth: Google OAuth 2.0, YouTube API
  Password Hashing: bcrypt
  Encryption: AES-256

AI Integration:
  Video: Stable Diffusion Video, Gen-2, CogVideo, LTX-2
  Voice: ElevenLabs, Coqui TTS, OpenAI TTS
  Lip-sync: Wav2Lip, First Order Motion Model
  Music: OpenAI Jukebox, MIDI generation

Queue Management:
  Primary: BullMQ (Redis-based)
  Alternative: RabbitMQ, AWS SQS
  Workers: Node.js / Python

Monitoring:
  Logs: Winston + CloudWatch / ELK Stack
  Metrics: Prometheus + Grafana
  Alerts: CloudWatch Alarms
  Error Tracking: Sentry

DevOps:
  Containerization: Docker
  Orchestration: Kubernetes / AWS ECS
  CI/CD: GitHub Actions
  Infrastructure: Terraform
```

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-31  
**Status:** Approved  
**Next Review:** 2026-01-31
