# AI Film Studio - Technical Implementation

## Database Schema

### 1. Users Table

Stores user account information, credentials, and subscription details.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | VARCHAR(255) | User full name |
| email | VARCHAR(255) | Unique email, login credential |
| password_hash | VARCHAR(255) | Encrypted password (bcrypt) |
| role | ENUM (creator/admin) | User permissions level |
| credits | INTEGER | Current credits balance |
| plan_type | ENUM (Free/Standard/Pro/Enterprise) | Subscription plan |
| created_at | TIMESTAMP | Account creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### 2. Projects Table

Stores user projects with scripts, images, and video generation details.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key → Users.id |
| title | VARCHAR(255) | Project name |
| script | TEXT | User-provided script |
| images | JSON | Uploaded character images |
| voice | ENUM | Selected voice option |
| duration | INTEGER | Video length in minutes |
| music | VARCHAR(255) | Music/sloka selection |
| status | ENUM (pending/processing/complete/failed) | Video generation status |
| video_url | VARCHAR(500) | S3 URL of generated video |
| subtitles_url | VARCHAR(500) | S3 URL of generated subtitles |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### 3. Credits / Plans Table

Stores user credit balance and subscription information.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key → Users.id |
| plan_type | ENUM | Subscription plan |
| credits_balance | INTEGER | Current credit count |
| subscription_start | TIMESTAMP | Plan start date |
| subscription_end | TIMESTAMP | Plan end date |

### 4. YouTube Integration Table

Stores information about YouTube uploads and integrations.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key → Users.id |
| project_id | UUID | Foreign key → Projects.id |
| channel_id | VARCHAR(255) | YouTube channel ID |
| video_id | VARCHAR(255) | Uploaded video ID |
| playlist_id | VARCHAR(255) | Playlist ID |
| upload_status | ENUM (pending/processing/complete/failed) | Upload status |

### 5. Logs Table

Stores system logs and user actions for audit trail.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| project_id | UUID | Foreign key → Projects.id |
| user_id | UUID | Foreign key → Users.id |
| action | VARCHAR(255) | Action description |
| message | TEXT | Additional details |
| timestamp | TIMESTAMP | Action time |

---

## API Contracts

### User Service

#### POST /api/users/register
Register a new user

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "plan_type": "Free",
  "credits": 3,
  "role": "creator",
  "created_at": "2025-12-31T00:00:00Z"
}
```

#### POST /api/users/login
User authentication

**Request:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "access_token": "jwt-token-here",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### GET /api/users/profile
Get user profile (requires authentication)

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "plan_type": "Free",
  "credits": 3,
  "role": "creator",
  "created_at": "2025-12-31T00:00:00Z",
  "updated_at": "2025-12-31T00:00:00Z"
}
```

---

### Project Service

#### POST /api/projects/create
Create a new project

**Request:**
```json
{
  "title": "My First Film",
  "script": "Once upon a time...",
  "images": ["image1.jpg", "image2.jpg"],
  "voice": "male",
  "duration": 2,
  "music": "cinematic"
}
```

**Response:**
```json
{
  "id": "project-uuid",
  "user_id": "user-uuid",
  "title": "My First Film",
  "status": "pending",
  "created_at": "2025-12-31T00:00:00Z"
}
```

#### GET /api/projects/{id}
Get project details

**Response:**
```json
{
  "id": "project-uuid",
  "title": "My First Film",
  "status": "complete",
  "video_url": "https://s3.amazonaws.com/...",
  "subtitles_url": "https://s3.amazonaws.com/..."
}
```

#### POST /api/projects/{id}/regenerate
Regenerate project video

**Response:**
```json
{
  "id": "project-uuid",
  "status": "pending"
}
```

---

### Credit / Subscription

#### GET /api/credits/balance
Get user's credit balance

**Response:**
```json
{
  "balance": 15,
  "plan_type": "Pro",
  "credits_per_minute": 3
}
```

#### POST /api/credits/topup
Top up credits / upgrade plan

**Request:**
```json
{
  "plan_type": "Pro"
}
```

**Response:**
```json
{
  "credits_balance": 60,
  "plan_type": "Pro",
  "message": "Credits topped up successfully"
}
```

#### GET /api/credits/plans
Get all available plans

**Response:**
```json
[
  {
    "plan_type": "Free",
    "price": 0,
    "credits_per_month": 3,
    "credits_per_minute": 3,
    "max_video_length": 1
  },
  {
    "plan_type": "Standard",
    "price": 39,
    "credits_per_month": 30,
    "credits_per_minute": 3,
    "max_video_length": 10
  }
]
```

---

### YouTube Service

#### POST /api/youtube/upload
Upload video to YouTube

**Request:**
```json
{
  "project_id": "project-uuid",
  "channel_id": "youtube-channel-id"
}
```

**Response:**
```json
{
  "id": "integration-uuid",
  "video_id": "youtube-video-id",
  "playlist_id": "youtube-playlist-id",
  "upload_status": "pending"
}
```

#### GET /api/youtube/videos
Get user's YouTube videos

**Response:**
```json
{
  "videos": [
    {
      "id": "integration-uuid",
      "video_id": "youtube-video-id",
      "upload_status": "complete"
    }
  ],
  "total": 1
}
```

---

### AI Job Service

#### POST /api/ai/video-generate
Generate video from project

**Request:**
```json
{
  "project_id": "project-uuid",
  "script": "Story script here...",
  "images": ["img1.jpg"],
  "voice": "female",
  "duration": 2,
  "music": "ambient"
}
```

**Response:**
```json
{
  "job_id": "job-uuid",
  "status": "queued",
  "estimated_time": "3-5 minutes"
}
```

#### POST /api/ai/audio-generate
Generate audio from text

**Request:**
```json
{
  "project_id": "project-uuid",
  "text": "Hello world",
  "voice": "neutral",
  "language": "en"
}
```

#### POST /api/ai/lip-sync
Perform lip sync

**Request:**
```json
{
  "project_id": "project-uuid",
  "video_url": "https://s3.../video.mp4",
  "audio_url": "https://s3.../audio.mp3"
}
```

#### POST /api/ai/music-generate
Generate background music

**Request:**
```json
{
  "project_id": "project-uuid",
  "prompt": "Cinematic orchestral music",
  "duration": 120,
  "style": "cinematic"
}
```

---

## Cost Per Video Calculation

### Assumptions
- **Credits System:** 3 credits = 1 minute of video
- **Compute Cost:** $0.50/minute GPU processing (EC2 G4/G5 instances)
- **Storage Cost:** $0.02/video (S3)
- **Network Cost:** $0.01/video (negligible for small videos)

### Pricing Plans

| Plan | Price (USD) | Credits | Max Video Length | Cost per Minute |
|------|-------------|---------|------------------|-----------------|
| **Free** | $0 | 3 credits | 1 minute | $0.53 |
| **Standard** | $39 | 30 credits | 10 minutes | $0.53 |
| **Pro** | $49 | 60 credits | 20 minutes | $0.53 |
| **Enterprise** | $99 | 120 credits | 40 minutes | $0.53 |

### Cost Breakdown

For a 1-minute video:
- AI Compute: $0.50 (dominant cost)
- Storage: $0.02
- Network: $0.01
- **Total:** $0.53 per minute

### Revenue Model

- **Free Tier:** Break-even or loss leader for user acquisition
- **Standard ($39):** 
  - Cost: 10 minutes × $0.53 = $5.30
  - Revenue: $39
  - Profit Margin: 86.4%
- **Pro ($49):**
  - Cost: 20 minutes × $0.53 = $10.60
  - Revenue: $49
  - Profit Margin: 78.4%
- **Enterprise ($99):**
  - Cost: 40 minutes × $0.53 = $21.20
  - Revenue: $99
  - Profit Margin: 78.6%

### Scaling Considerations

- AI compute dominates the cost structure
- Storage and network costs are relatively minor
- Spot instances can reduce GPU costs by 70%
- Caching and optimization can reduce generation time
- Higher usage tiers benefit from economies of scale

---

## Implementation Notes

### Database Setup

1. Install PostgreSQL
2. Create database: `ai_film_studio`
3. Run Alembic migrations (see next section)
4. Seed subscription plans

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database (if using Alembic)
alembic upgrade head

# Run the application
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

Once the server is running, access:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

---

## Security Considerations

1. **Authentication:** JWT tokens with 24-hour expiration
2. **Password Hashing:** bcrypt with salt
3. **HTTPS:** Required in production
4. **Rate Limiting:** Implement for authentication endpoints
5. **Input Validation:** All inputs validated using Pydantic
6. **SQL Injection:** Protected by SQLAlchemy ORM
7. **CORS:** Configure allowed origins in production

---

## Next Steps

1. Set up Alembic for database migrations
2. Implement actual AI processing pipeline
3. Integrate with AWS S3 for media storage
4. Integrate with AWS SQS for job queue
5. Implement YouTube Data API integration
6. Add payment processing (Stripe)
7. Implement comprehensive testing
8. Set up CI/CD pipeline
9. Deploy to production environment
10. Monitor and optimize performance
