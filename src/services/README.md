# Backend Services

This directory contains all the microservices for the AI Film Studio platform.

## Service Overview

### 1. User Service (`user/`)
Handles user authentication, registration, and profile management.

**Key Features:**
- User registration with email/password
- JWT-based authentication
- OAuth 2.0 integration (Google, GitHub)
- Profile management
- Password reset functionality
- Token generation and validation

**Main Class:** `UserService`

**Methods:**
- `register_user()` - Register new user
- `login()` - Authenticate user and generate tokens
- `get_user_by_email()` - Fetch user by email
- `update_user_profile()` - Update user information
- `change_password()` - Change user password
- `verify_token()` - Validate JWT token

### 2. Project Service (`project/`)
Manages CRUD operations for film projects.

**Key Features:**
- Create, read, update, delete projects
- Project status management
- User project listing with pagination
- Project ownership validation
- Soft delete implementation

**Main Class:** `ProjectService`

**Methods:**
- `create_project()` - Create new film project
- `get_project()` - Get project by ID
- `get_user_projects()` - List user's projects
- `update_project()` - Update project details
- `delete_project()` - Soft delete project
- `update_project_status()` - Change project status

### 3. Credits Service (`credits/`)
Handles credit management and transaction tracking.

**Key Features:**
- Credit balance management
- Credit deduction and addition
- Transaction history
- Monthly credit reset
- Payment integration support

**Main Class:** `CreditsService`

**Methods:**
- `get_user_credits()` - Get current balance
- `deduct_credits()` - Deduct credits for usage
- `add_credits()` - Add credits (purchase/grant)
- `get_transaction_history()` - View credit history
- `check_sufficient_credits()` - Validate balance
- `reset_monthly_credits()` - Reset credits by tier

### 4. AI Job Service (`ai_job/`)
Manages AI processing job queue and status tracking.

**Key Features:**
- Job queue management (Redis/BullMQ)
- Job status and progress tracking
- Priority queue support
- Retry logic for failed jobs
- Queue statistics and monitoring

**Main Class:** `AIJobService`

**Job Types:**
- `script_analysis` - Analyze and break down script
- `image_generation` - Generate scene images
- `voice_synthesis` - Text-to-speech conversion
- `video_composition` - Combine elements into video
- `subtitle_generation` - Generate subtitles
- `thumbnail_generation` - Create video thumbnail
- `full_generation` - Complete end-to-end generation

**Methods:**
- `create_job()` - Create new processing job
- `get_job()` - Get job details
- `get_user_jobs()` - List user's jobs
- `update_job_status()` - Update job progress
- `update_job_result()` - Store job results
- `cancel_job()` - Cancel queued/processing job
- `retry_job()` - Retry failed job
- `get_queue_stats()` - Get queue metrics

### 5. YouTube Service (`youtube/`)
Handles YouTube API integration for video uploads.

**Key Features:**
- OAuth 2.0 YouTube account connection
- Video upload to YouTube
- Playlist creation and management
- Upload progress tracking
- Token refresh handling

**Main Class:** `YouTubeService`

**Methods:**
- `connect_youtube_account()` - Connect YouTube via OAuth
- `upload_video()` - Upload video with metadata
- `create_playlist()` - Create new playlist
- `get_upload_status()` - Check upload progress
- `disconnect_youtube_account()` - Remove connection

### 6. Admin Service (`admin/`)
Administrative operations and system management.

**Key Features:**
- System statistics and monitoring
- User management and search
- Credit granting (admin privilege)
- Failed job investigation
- Content moderation queue
- Audit logging

**Main Class:** `AdminService`

**Methods:**
- `get_system_stats()` - Comprehensive metrics
- `search_users()` - Find users
- `get_user_details()` - Detailed user info
- `suspend_user()` - Deactivate account
- `reactivate_user()` - Reactivate account
- `grant_credits()` - Admin credit grant
- `get_failed_jobs()` - View failed jobs
- `get_moderation_queue()` - Projects for review
- `approve_project()` - Approve content
- `reject_project()` - Reject content

## Architecture

### Service Pattern
Each service follows a consistent pattern:

```python
class ServiceName:
    def __init__(self, db_connection, *args):
        self.db = db_connection
        # Additional dependencies
    
    async def method_name(self, params) -> ReturnType:
        """
        Method description
        
        Args:
            param: Description
            
        Returns:
            Return value description
        """
        try:
            # Implementation
            logger.info(f"Action completed: {details}")
            return result
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise
```

### Database Interaction
Services use a database connection abstraction layer with methods:
- `query(sql, params)` - Execute SELECT queries
- `insert(table, data)` - Insert records
- `update(table, where, data)` - Update records
- `delete(table, where)` - Delete records

### Error Handling
All services implement comprehensive error handling:
- Log errors with context
- Raise exceptions for caller handling
- Validate input parameters
- Check authorization/ownership

### Logging
Structured logging throughout:
- Info level for successful operations
- Warning level for validation failures
- Error level for exceptions
- Debug level for detailed traces (development)

## Usage Examples

### User Service
```python
from src.services.user.user_service import UserService

# Initialize service
user_service = UserService(db, jwt_secret="secret_key")

# Register user
user = await user_service.register_user(
    email="user@example.com",
    password="SecurePass123!",
    first_name="John",
    last_name="Doe"
)

# Login
auth = await user_service.login(
    email="user@example.com",
    password="SecurePass123!"
)
access_token = auth["access_token"]
```

### Project Service
```python
from src.services.project.project_service import ProjectService

# Initialize service
project_service = ProjectService(db)

# Create project
project = await project_service.create_project(
    user_id=user_id,
    title="My First Film",
    script="A story about...",
    style="cinematic",
    target_duration=90
)

# List projects
projects = await project_service.get_user_projects(
    user_id=user_id,
    status="completed",
    limit=10
)
```

### AI Job Service
```python
from src.services.ai_job.ai_job_service import AIJobService

# Initialize service
job_service = AIJobService(db, queue_client)

# Create generation job
job = await job_service.create_job(
    project_id=project_id,
    user_id=user_id,
    job_type="full_generation",
    parameters={
        "style": "cinematic",
        "duration": 90,
        "voice": "male_narrator"
    },
    priority=2  # Normal priority
)

# Check status
status = await job_service.get_job(job_id)
print(f"Progress: {status['progress']}%")
```

## Testing

Each service should have corresponding unit tests:

```bash
pytest tests/services/test_user_service.py
pytest tests/services/test_project_service.py
pytest tests/services/test_credits_service.py
pytest tests/services/test_ai_job_service.py
pytest tests/services/test_youtube_service.py
pytest tests/services/test_admin_service.py
```

## Dependencies

Required Python packages:
```
fastapi==0.104.1
pydantic==2.5.0
jwt==2.8.0
passlib==1.7.4
google-api-python-client==2.108.0
google-auth-oauthlib==1.2.0
redis==5.0.1
```

## Environment Variables

Services require the following environment variables:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# JWT
JWT_SECRET=your-jwt-secret-key
JWT_ALGORITHM=HS256

# YouTube API
YOUTUBE_CLIENT_ID=your-client-id
YOUTUBE_CLIENT_SECRET=your-client-secret

# Redis
REDIS_URL=redis://localhost:6379

# AWS (for S3)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=ai-film-studio-prod
```

## Future Enhancements

- [ ] Implement WebSocket support for real-time updates
- [ ] Add caching layer (Redis) for frequently accessed data
- [ ] Implement rate limiting per service
- [ ] Add service health check endpoints
- [ ] Implement circuit breaker pattern
- [ ] Add distributed tracing (OpenTelemetry)
- [ ] Implement event sourcing for audit trail
- [ ] Add GraphQL API layer
- [ ] Implement saga pattern for distributed transactions

## License

Copyright © 2025 AI-Empower-HQ-360. All rights reserved.
