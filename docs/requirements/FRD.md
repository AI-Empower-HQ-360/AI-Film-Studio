# Functional Requirements Document (FRD)
## AI Film Studio Platform

**Document Version**: 1.0  
**Date**: 2025-12-27  
**Author**: AI-Empower-HQ-360  
**Status**: Approved

---

## 1. Introduction

### 1.1 Purpose
This document specifies the **functional requirements** for the AI Film Studio platform, detailing what the system must do to meet business objectives.

### 1.2 Scope
Covers all user-facing features, system behaviors, data flows, and API specifications for the MVP release.

### 1.3 Audience
- Product managers
- Software engineers
- QA engineers
- UX/UI designers

---

## 2. System Overview

### 2.1 System Context
The AI Film Studio platform consists of:
- **Frontend** (Next.js): User interface
- **Backend API** (FastAPI): Business logic and orchestration
- **Worker Service** (Python): AI processing and video generation
- **Data Layer** (RDS, S3, SQS): Persistence and messaging

### 2.2 User Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| **Guest** | Non-authenticated visitor | View landing page, sign up |
| **User** | Authenticated creator | Create projects, submit jobs, download films |
| **Admin** | Platform administrator | All user permissions + moderation + system management |

---

## 3. Functional Requirements

## 3.1 User Authentication & Authorization

### FR-001: User Registration
**Priority**: High  
**Status**: Required

**Description**: Allow new users to create accounts.

**Input**:
- Email address
- Password (min 8 chars, 1 uppercase, 1 number, 1 special char)
- Display name

**Process**:
1. Validate email format
2. Check email uniqueness
3. Hash password (bcrypt)
4. Create user record
5. Send verification email
6. Assign welcome credits (e.g., 100 credits)

**Output**:
- Success: User account created, verification email sent
- Failure: Error message (email exists, invalid format, etc.)

**Business Rules**:
- Email must be unique
- Password complexity enforced
- New users receive 100 free credits

---

### FR-002: User Login
**Priority**: High  
**Status**: Required

**Description**: Authenticate users and issue JWT tokens.

**Input**:
- Email
- Password

**Process**:
1. Validate credentials
2. Generate JWT access token (expires in 1 hour)
3. Generate refresh token (expires in 7 days)
4. Return tokens

**Output**:
- Success: JWT access token, refresh token, user profile
- Failure: 401 Unauthorized

**Business Rules**:
- Max 5 failed attempts → account locked for 15 minutes
- JWT includes user_id, role, email

---

### FR-003: Password Reset
**Priority**: Medium  
**Status**: Required

**Description**: Allow users to reset forgotten passwords.

**Input**:
- Email address (for reset request)
- Reset token + new password (for reset confirmation)

**Process**:
1. User requests reset → system sends email with token
2. Token valid for 1 hour
3. User submits token + new password → password updated

**Output**:
- Success: Password updated
- Failure: Invalid/expired token

---

## 3.2 Project Management

### FR-004: Create Project
**Priority**: High  
**Status**: Required

**Description**: Users can create new film projects.

**Input**:
- Project name (required, max 100 chars)
- Description (optional, max 500 chars)

**Process**:
1. Validate inputs
2. Create project record
3. Associate with user_id
4. Generate unique project_id

**Output**:
- Success: Project object with project_id
- Failure: Validation error

**Business Rules**:
- Users can create unlimited projects
- Project names must be unique per user

---

### FR-005: View Projects
**Priority**: High  
**Status**: Required

**Description**: Users can view all their projects.

**Input**:
- user_id (from JWT)
- Pagination params (page, limit)

**Process**:
1. Query projects table filtered by user_id
2. Include job counts and statuses
3. Sort by created_at desc

**Output**:
- List of project objects
- Total count, pagination metadata

---

### FR-006: Delete Project
**Priority**: Medium  
**Status**: Required

**Description**: Users can delete their projects.

**Input**:
- project_id

**Process**:
1. Verify ownership
2. Soft delete project record
3. Mark associated jobs as deleted
4. Schedule S3 asset cleanup (async)

**Output**:
- Success: 204 No Content
- Failure: 404 Not Found, 403 Forbidden

---

## 3.3 Film Generation Workflow

### FR-007: Submit Script for Film Generation
**Priority**: High  
**Status**: Required

**Description**: Users submit scripts to generate films.

**Input**:
- project_id
- script_text (required, 50-5000 chars)
- style (optional: "cinematic", "documentary", "anime")
- duration_target (optional: 30, 60, 90 seconds)

**Process**:
1. Validate script length
2. Check user credit balance (min 10 credits required)
3. Content moderation check
4. Create job record (status: QUEUED)
5. Deduct credits (10 per job)
6. Publish job to SQS queue
7. Return job_id

**Output**:
- Success: Job object with job_id, status
- Failure: Insufficient credits, inappropriate content, validation error

**Business Rules**:
- Cost: 10 credits per job
- Content moderation must pass
- Scripts with banned keywords rejected

---

### FR-008: Job Processing (Worker)
**Priority**: High  
**Status**: Required

**Description**: Worker consumes jobs and generates films.

**Process**:
1. Poll SQS queue
2. Update job status → PROCESSING
3. **Scene Breakdown**:
   - Parse script with NLP
   - Identify scenes, actions, characters
4. **Shot Generation**:
   - Generate AI prompts per scene
   - Call SDXL/AI models
   - Generate images/video clips
   - Upload to S3
5. **Composition**:
   - Use FFmpeg to stitch clips
   - Add transitions, effects
   - Render final MP4
   - Upload to S3
6. Update job status → COMPLETED
7. Store output_url

**Output**:
- Job status updated
- Final MP4 in S3
- Thumbnail generated

**Error Handling**:
- If failure → status: FAILED, error_message stored
- Retry logic: 3 attempts with exponential backoff

---

### FR-009: View Job Status
**Priority**: High  
**Status**: Required

**Description**: Users can check job progress.

**Input**:
- job_id

**Process**:
1. Query job record
2. Return status, progress percentage, error message

**Output**:
```json
{
  "job_id": "j_abc123",
  "status": "PROCESSING",
  "progress": 65,
  "created_at": "2025-12-27T10:00:00Z",
  "estimated_completion": "2025-12-27T10:04:00Z",
  "output_url": null
}
```

**Job States**:
- **QUEUED** → Job submitted, waiting for worker
- **PROCESSING** → Worker actively generating film
- **COMPLETED** → Film ready, output_url available
- **FAILED** → Error occurred, see error_message

---

### FR-010: Download Film
**Priority**: High  
**Status**: Required

**Description**: Users can download completed films.

**Input**:
- job_id

**Process**:
1. Verify job ownership
2. Check status = COMPLETED
3. Generate S3 presigned URL (valid 1 hour)
4. Return URL

**Output**:
- Success: Presigned download URL
- Failure: 404 (job not found), 403 (not owner), 400 (not completed)

---

## 3.4 Credit Management

### FR-011: View Credit Balance
**Priority**: High  
**Status**: Required

**Description**: Users can view their credit balance.

**Input**:
- user_id (from JWT)

**Process**:
1. Query user credits from database

**Output**:
```json
{
  "user_id": "u_xyz789",
  "credits": 150,
  "last_updated": "2025-12-27T09:30:00Z"
}
```

---

### FR-012: Purchase Credits
**Priority**: Medium  
**Status**: Phase 2

**Description**: Users can buy credits via payment integration.

**Input**:
- package_id (e.g., "100_credits", "500_credits")
- payment_method

**Process**:
1. Create payment intent (Stripe)
2. Process payment
3. Add credits to user account
4. Create transaction record

**Output**:
- Success: Updated credit balance
- Failure: Payment error

---

### FR-013: Credit Transaction History
**Priority**: Low  
**Status**: Phase 2

**Description**: Users can view credit transaction history.

**Input**:
- user_id

**Output**:
- List of transactions (purchases, deductions, refunds)

---

## 3.5 Content Moderation

### FR-014: Script Content Filtering
**Priority**: High  
**Status**: Required

**Description**: Prevent inappropriate content generation.

**Process**:
1. Check script against banned keyword list
2. Use AI classifier for violence, hate speech, NSFW content
3. If flagged → reject job submission
4. Log flagged content for admin review

**Banned Categories**:
- Violence/gore
- Hate speech
- Explicit sexual content
- Self-harm
- Illegal activities

**Output**:
- Pass: Job proceeds
- Fail: 400 Bad Request with reason

---

### FR-015: Admin Content Review
**Priority**: Medium  
**Status**: Required

**Description**: Admins can review flagged content.

**Interface**:
- List of flagged jobs
- View script, reason for flag
- Actions: Approve, Reject, Ban User

---

## 3.6 Admin Features

### FR-016: User Management
**Priority**: Medium  
**Status**: Required

**Actions**:
- View all users
- Search users by email/name
- Suspend/unsuspend accounts
- View user activity (jobs, credits)

---

### FR-017: System Metrics Dashboard
**Priority**: Medium  
**Status**: Required

**Metrics**:
- Total users
- Active users (last 30 days)
- Total jobs (queued, processing, completed, failed)
- Average job duration
- Credit consumption rate
- System health (API latency, worker queue depth)

---

## 4. API Specifications

### 4.1 Authentication Endpoints

**POST /api/v1/auth/register**  
**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "display_name": "John Doe"
}
```
**Response (201)**:
```json
{
  "user_id": "u_abc123",
  "email": "user@example.com",
  "display_name": "John Doe",
  "credits": 100,
  "created_at": "2025-12-27T10:00:00Z"
}
```

**POST /api/v1/auth/login**  
**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```
**Response (200)**:
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "user_id": "u_abc123",
    "email": "user@example.com",
    "display_name": "John Doe"
  }
}
```

### 4.2 Project Endpoints

**POST /api/v1/projects**  
Headers: Authorization: Bearer <token>

**Request**:
```json
{
  "name": "My First Film",
  "description": "A short sci-fi trailer"
}
```
**Response (201)**:
```json
{
  "project_id": "p_xyz789",
  "name": "My First Film",
  "description": "A short sci-fi trailer",
  "created_at": "2025-12-27T10:05:00Z",
  "job_count": 0
}
```

**GET /api/v1/projects**  
Headers: Authorization: Bearer <token>

Query Params: `page=1&limit=20`

**Response (200)**:
```json
{
  "projects": [
    {
      "project_id": "p_xyz789",
      "name": "My First Film",
      "job_count": 3,
      "last_updated": "2025-12-27T10:10:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 20
}
```

### 4.3 Job Endpoints

**POST /api/v1/jobs**  
Headers: Authorization: Bearer <token>

**Request**:
```json
{
  "project_id": "p_xyz789",
  "script": "INT. SPACESHIP - A lone astronaut gazes at Earth through the window...",
  "style": "cinematic",
  "duration_target": 60
}
```
**Response (201)**:
```json
{
  "job_id": "j_abc123",
  "status": "QUEUED",
  "created_at": "2025-12-27T10:15:00Z",
  "credits_deducted": 10
}
```

**GET /api/v1/jobs/{job_id}**  
Headers: Authorization: Bearer <token>

**Response (200)**:
```json
{
  "job_id": "j_abc123",
  "status": "COMPLETED",
  "progress": 100,
  "output_url": "https://s3.../film_abc123.mp4",
  "thumbnail_url": "https://s3.../thumb_abc123.jpg",
  "duration": 62,
  "created_at": "2025-12-27T10:15:00Z",
  "completed_at": "2025-12-27T10:19:30Z"
}
```

---

## 5. Data Models

### User
```typescript
{
  user_id: string (PK)
  email: string (unique)
  password_hash: string
  display_name: string
  role: "user" | "admin"
  credits: integer
  is_active: boolean
  created_at: timestamp
  updated_at: timestamp
}
```

### Project
```typescript
{
  project_id: string (PK)
  user_id: string (FK)
  name: string
  description: string
  created_at: timestamp
  updated_at: timestamp
}
```

### Job
```typescript
{
  job_id: string (PK)
  project_id: string (FK)
  user_id: string (FK)
  script: text
  style: string
  duration_target: integer
  status: "QUEUED" | "PROCESSING" | "COMPLETED" | "FAILED"
  progress: integer (0-100)
  output_url: string (nullable)
  thumbnail_url: string (nullable)
  error_message: string (nullable)
  credits_used: integer
  created_at: timestamp
  updated_at: timestamp
  completed_at: timestamp (nullable)
}
```

---

## 6. Business Rules Summary
- Credits: 10 credits per job
- Welcome Credits: 100 credits for new users
- Script Length: 50-5000 characters
- Film Duration: 30, 60, or 90 seconds
- Content Moderation: Automatic filtering + admin review
- Rate Limiting: 10 job submissions per hour per user
- Job Retention: Completed jobs stored for 30 days
- File Formats: MP4 (H.264, 1080p)

---

## 7. Error Handling

| Error Code | Description | Example |
|------------|-------------|---------|
| 400 | Bad Request | Invalid script format |
| 401 | Unauthorized | Invalid JWT token |
| 403 | Forbidden | Insufficient credits |
| 404 | Not Found | Job not found |
| 409 | Conflict | Email already exists |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected error |

---

## 8. Acceptance Criteria

Each functional requirement must:

✅ Pass unit tests (>80% coverage)  
✅ Pass integration tests  
✅ Be documented with API specs  
✅ Be validated in QA environment  
✅ Meet performance benchmarks

---

## 9. Dependencies
- External Services: AWS S3, SQS, RDS, CloudFront
- AI Models: SDXL, custom video generation models
- Third-Party Libraries: FFmpeg, Pydantic, SQLAlchemy

---

## 10. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | AI-Empower-HQ-360 | ✅ Approved | 2025-12-27 |
| Technical Lead | TBD | ✅ Approved | 2025-12-27 |

---

**Document Control**  
Version: 1.0  
Next Review: 2026-01-27
