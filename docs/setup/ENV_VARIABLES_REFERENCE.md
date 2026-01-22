# 🔐 AI Film Studio - Environment Variables Reference

> **Complete reference guide for all environment variables across all services and environments**

📋 **Tags:** `#environment` `#configuration` `#variables` `#secrets` `#reference`

---

## 📑 Table of Contents

- [Overview](#overview)
- [Variable Categories](#variable-categories)
- [Security Best Practices](#security-best-practices)
- [Variable Reference by Service](#variable-reference-by-service)
- [Environment-Specific Overrides](#environment-specific-overrides)

---

## Overview

This document provides a comprehensive reference for all environment variables used across the AI Film Studio platform. Variables are organized by category and service, with detailed descriptions, allowed values, and environment-specific recommendations.

### File Locations

Environment variables should be defined in:
- **Application**: `.env.{environment}` files in project root
- **Terraform**: `terraform.tfvars` files in `infrastructure/terraform/environments/{environment}/`
- **Kubernetes**: ConfigMaps and Secrets in cluster
- **AWS**: Secrets Manager or Parameter Store

> ⚠️ **Important:** The Python services read configuration from `os.environ`. They do **not** automatically load `.env.{environment}` files. When running locally, you must explicitly load the appropriate `.env` file so that its values are present in the environment.
>
> Common options:
>
> - Using Uvicorn directly:
>   ```bash
>   uvicorn src.api.main:app --reload --env-file .env.dev
>   ```
> - Using `python-dotenv` CLI:
>   ```bash
>   dotenv -f .env.dev run -- uvicorn src.api.main:app --reload
>   ```
> - Using your shell to export variables:
>   ```bash
>   set -a
>   source .env.dev
>   set +a
>   uvicorn src.api.main:app --reload
>   ```

### Environment Key

- **Dev** = Development environment
- **Sandbox** = QA/Testing environment
- **Staging** = Pre-production environment
- **Prod** = Production environment

---

## Variable Categories

1. [General Settings](#1-general-settings)
2. [API Configuration](#2-api-configuration)
3. [Frontend Configuration](#3-frontend-configuration)
4. [Database Configuration](#4-database-configuration)
5. [Cache/Redis Configuration](#5-cacheredis-configuration)
6. [AWS Configuration](#6-aws-configuration)
7. [Salesforce Configuration](#7-salesforce-configuration)
8. [YouTube/Google API Configuration](#8-youtubegoogle-api-configuration)
9. [AI/ML Models Configuration](#9-aiml-models-configuration)
10. [Authentication & Security](#10-authentication--security)
11. [Feature Flags](#11-feature-flags)
12. [Monitoring & Logging](#12-monitoring--logging)
13. [Email/Notification Configuration](#13-emailnotification-configuration)
14. [Third-Party Services](#14-third-party-services)
15. [Job Processing](#15-job-processing)
16. [Credit System](#16-credit-system)
17. [Performance Tuning](#17-performance-tuning)
18. [Backup & Recovery](#18-backup--recovery)
19. [Security Headers](#19-security-headers)
20. [Auto-Scaling](#20-auto-scaling)

---

## Security Best Practices

### ⚠️ CRITICAL SECURITY RULES

1. **NEVER commit secrets to version control**
2. **Use AWS Secrets Manager or Parameter Store for production**
3. **Rotate secrets regularly (90 days recommended)**
4. **Use different secrets for each environment**
5. **Limit access to production secrets to ops team only**
6. **Enable CloudTrail to audit secret access**
7. **Use IAM roles instead of access keys when possible**

### Secret Storage Strategy

| Environment | Storage Method | Access Control |
|-------------|---------------|----------------|
| Dev | Local `.env.dev` file | All developers |
| Sandbox | AWS Secrets Manager | QA + DevOps |
| Staging | AWS Secrets Manager | Limited team |
| Production | AWS Secrets Manager | Ops team only |

### How to Use Secrets Manager

```python
# Example: Retrieve secret from AWS Secrets Manager
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
db_credentials = get_secret('/aifilmstudio/prod/database')
jwt_secret = get_secret('/aifilmstudio/prod/jwt-secret')
```

---

## Variable Reference by Service

## 1. General Settings

### APP_NAME
- **Description**: Application name for logging and monitoring
- **Type**: String
- **Default**: `AI Film Studio`
- **Required**: Yes
- **Example**: `AI Film Studio`

### ENVIRONMENT
- **Description**: Current environment identifier
- **Type**: String (enum)
- **Allowed Values**: `development`, `sandbox`, `staging`, `production`
- **Required**: Yes
- **Dev**: `development`
- **Sandbox**: `sandbox`
- **Staging**: `staging`
- **Prod**: `production`

### NODE_ENV
- **Description**: Node.js environment mode
- **Type**: String (enum)
- **Allowed Values**: `development`, `production`
- **Required**: Yes (for Node.js services)
- **Dev**: `development`
- **Prod**: `production`

### DEBUG
- **Description**: Enable debug mode
- **Type**: Boolean
- **Default**: `false`
- **Dev**: `true`
- **Prod**: `false`

### LOG_LEVEL
- **Description**: Logging verbosity level
- **Type**: String (enum)
- **Allowed Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Dev**: `DEBUG`
- **Sandbox**: `INFO`
- **Staging**: `INFO`
- **Prod**: `WARNING`

### TIMEZONE
- **Description**: Application timezone
- **Type**: String (IANA timezone)
- **Default**: `UTC`
- **Example**: `UTC`, `America/New_York`

---

## 2. API Configuration

### API_HOST
- **Description**: API server host address
- **Type**: String (IP address)
- **Default**: `0.0.0.0`
- **Required**: Yes

### API_PORT
- **Description**: API server port
- **Type**: Integer
- **Default**: `8000`
- **Range**: `1024-65535`
- **Required**: Yes

### API_BASE_URL
- **Description**: Full API base URL
- **Type**: String (URL)
- **Required**: Yes
- **Dev**: `http://localhost:8000`
- **Sandbox**: `https://api-sandbox.aifilmstudio.com`
- **Staging**: `https://api-staging.aifilmstudio.com`
- **Prod**: `https://api.aifilmstudio.com`

### API_VERSION
- **Description**: API version string
- **Type**: String
- **Default**: `v1`
- **Example**: `v1`, `v2`

### API_DOCS_ENABLED
- **Description**: Enable API documentation endpoint
- **Type**: Boolean
- **Dev**: `true`
- **Prod**: `false`

### CORS_ORIGINS
- **Description**: Allowed CORS origins (comma-separated)
- **Type**: String (comma-separated URLs)
- **Required**: Yes
- **Dev**: `http://localhost:3000,http://localhost:8000`
- **Prod**: `https://aifilmstudio.com,https://app.aifilmstudio.com`

### RATE_LIMIT_ENABLED
- **Description**: Enable API rate limiting
- **Type**: Boolean
- **Dev**: `false`
- **Prod**: `true`

### RATE_LIMIT_REQUESTS
- **Description**: Maximum requests per window
- **Type**: Integer
- **Dev**: `100`
- **Sandbox**: `200`
- **Staging**: `500`
- **Prod**: `1000`

### RATE_LIMIT_WINDOW
- **Description**: Rate limit window in seconds
- **Type**: Integer
- **Default**: `60`

---

## 3. Frontend Configuration

### FRONTEND_URL
- **Description**: Frontend application URL
- **Type**: String (URL)
- **Required**: Yes
- **Dev**: `http://localhost:3000`
- **Sandbox**: `https://sandbox.aifilmstudio.com`
- **Staging**: `https://staging.aifilmstudio.com`
- **Prod**: `https://app.aifilmstudio.com`

### NEXT_PUBLIC_API_URL
- **Description**: API URL accessible from browser (Next.js public variable)
- **Type**: String (URL)
- **Required**: Yes
- **Note**: Must start with `NEXT_PUBLIC_` to be exposed to browser

### NEXT_PUBLIC_APP_NAME
- **Description**: Application name for frontend display
- **Type**: String
- **Example**: `AI Film Studio`

### NEXT_PUBLIC_ENVIRONMENT
- **Description**: Environment name for frontend display
- **Type**: String
- **Example**: `development`, `production`

---

## 4. Database Configuration

### DATABASE_URL
- **Description**: Complete PostgreSQL connection string
- **Type**: String (PostgreSQL connection URL)
- **Format**: `postgresql://user:password@host:port/database`
- **Required**: Yes
- **Security**: 🔒 SECRET - Store in Secrets Manager

### DATABASE_HOST
- **Description**: Database server hostname
- **Type**: String (hostname or IP)
- **Required**: Yes

### DATABASE_PORT
- **Description**: Database server port
- **Type**: Integer
- **Default**: `5432`

### DATABASE_NAME
- **Description**: Database name
- **Type**: String
- **Required**: Yes
- **Dev**: `aifilmstudio_dev`
- **Prod**: `aifilmstudio_prod`

### DATABASE_USER
- **Description**: Database username
- **Type**: String
- **Required**: Yes
- **Security**: 🔒 SECRET

### DATABASE_PASSWORD
- **Description**: Database password
- **Type**: String
- **Required**: Yes
- **Security**: 🔒 SECRET - Store in Secrets Manager

### DATABASE_POOL_SIZE
- **Description**: Connection pool size
- **Type**: Integer
- **Dev**: `5`
- **Sandbox**: `10`
- **Staging**: `30`
- **Prod**: `50-100`

### DATABASE_MAX_OVERFLOW
- **Description**: Maximum overflow connections
- **Type**: Integer
- **Dev**: `10`
- **Prod**: `100`

### DATABASE_ECHO
- **Description**: Echo SQL queries to console (debugging)
- **Type**: Boolean
- **Dev**: `true`
- **Prod**: `false`

### DATABASE_SSL_MODE
- **Description**: SSL mode for database connection
- **Type**: String (enum)
- **Allowed Values**: `disable`, `require`, `verify-ca`, `verify-full`
- **Dev**: `disable`
- **Prod**: `require`

### DATABASE_REPLICA_URL
- **Description**: Read replica connection string (optional)
- **Type**: String (PostgreSQL connection URL)
- **Required**: No (recommended for Staging/Prod)
- **Security**: 🔒 SECRET

---

## 5. Cache/Redis Configuration

### REDIS_URL
- **Description**: Complete Redis connection string
- **Type**: String (Redis connection URL)
- **Format**: `redis://host:port/db` or `rediss://` for SSL
- **Required**: Yes
- **Security**: 🔒 SECRET if password-protected

### REDIS_HOST
- **Description**: Redis server hostname
- **Type**: String

### REDIS_PORT
- **Description**: Redis server port
- **Type**: Integer
- **Default**: `6379`

### REDIS_DB
- **Description**: Redis database number
- **Type**: Integer
- **Default**: `0`
- **Range**: `0-15`

### REDIS_PASSWORD
- **Description**: Redis authentication password
- **Type**: String
- **Security**: 🔒 SECRET
- **Dev**: Empty (no password)
- **Prod**: Required

### REDIS_SSL
- **Description**: Enable SSL/TLS for Redis connection
- **Type**: Boolean
- **Dev**: `false`
- **Prod**: `true`

### CACHE_DEFAULT_TTL
- **Description**: Default cache TTL in seconds
- **Type**: Integer
- **Dev**: `300` (5 minutes)
- **Prod**: `1800` (30 minutes)

### CACHE_USER_SESSION_TTL
- **Description**: User session cache TTL in seconds
- **Type**: Integer
- **Dev**: `3600` (1 hour)
- **Prod**: `21600` (6 hours)

---

## 6. AWS Configuration

### AWS_REGION
- **Description**: Primary AWS region
- **Type**: String (AWS region code)
- **Default**: `us-east-1`
- **Example**: `us-east-1`, `eu-west-1`

### AWS_ACCESS_KEY_ID
- **Description**: AWS access key ID
- **Type**: String
- **Security**: 🔒 SECRET
- **Note**: Prefer IAM roles over access keys in production

### AWS_SECRET_ACCESS_KEY
- **Description**: AWS secret access key
- **Type**: String
- **Security**: 🔒 SECRET
- **Note**: Prefer IAM roles over access keys in production

### AWS_ACCOUNT_ID
- **Description**: AWS account number
- **Type**: String (12-digit number)
- **Required**: Yes

### S3_BUCKET_MEDIA
- **Description**: S3 bucket name for media storage
- **Type**: String (S3 bucket name)
- **Required**: Yes
- **Dev**: `aifilmstudio-dev-media`
- **Prod**: `aifilmstudio-prod-media`

### S3_BUCKET_VIDEOS
- **Description**: S3 bucket name for video storage
- **Type**: String
- **Required**: Yes

### S3_BUCKET_MODELS
- **Description**: S3 bucket name for AI model storage
- **Type**: String
- **Required**: Yes

### S3_PRESIGNED_URL_EXPIRY
- **Description**: Presigned URL expiration time in seconds
- **Type**: Integer
- **Default**: `3600` (1 hour)

### CLOUDFRONT_DOMAIN
- **Description**: CloudFront distribution domain name
- **Type**: String (domain name)
- **Required**: No (optional for Dev)
- **Example**: `d123prod.cloudfront.net`

### SQS_QUEUE_URL
- **Description**: SQS queue URL for job processing
- **Type**: String (SQS queue URL)
- **Required**: Yes
- **Format**: `https://sqs.{region}.amazonaws.com/{account-id}/{queue-name}`

### SQS_VISIBILITY_TIMEOUT
- **Description**: SQS message visibility timeout in seconds
- **Type**: Integer
- **Default**: `300` (5 minutes)

### SECRETS_MANAGER_PREFIX
- **Description**: Prefix for secrets in AWS Secrets Manager
- **Type**: String
- **Example**: `/aifilmstudio/prod/`

---

## 7. Salesforce Configuration

### SALESFORCE_INSTANCE_URL
- **Description**: Salesforce instance URL
- **Type**: String (URL)
- **Required**: Yes
- **Dev**: `https://your-dev-instance.develop.my.salesforce.com`
- **Prod**: `https://your-production.my.salesforce.com`

### SALESFORCE_CLIENT_ID
- **Description**: Salesforce connected app client ID
- **Type**: String
- **Security**: 🔒 SECRET
- **Required**: Yes

### SALESFORCE_CLIENT_SECRET
- **Description**: Salesforce connected app client secret
- **Type**: String
- **Security**: 🔒 SECRET
- **Required**: Yes

### SALESFORCE_USERNAME
- **Description**: Salesforce API user username
- **Type**: String (email format)
- **Required**: Yes
- **Security**: 🔒 SECRET

### SALESFORCE_PASSWORD
- **Description**: Salesforce API user password
- **Type**: String
- **Security**: 🔒 SECRET
- **Required**: Yes

### SALESFORCE_SECURITY_TOKEN
- **Description**: Salesforce security token
- **Type**: String
- **Security**: 🔒 SECRET
- **Required**: Yes

### SALESFORCE_ENABLE_SYNC
- **Description**: Enable synchronization with Salesforce
- **Type**: Boolean
- **Default**: `true`

### SALESFORCE_SYNC_INTERVAL
- **Description**: Sync interval in seconds
- **Type**: Integer
- **Dev**: `300` (5 minutes)
- **Prod**: `120` (2 minutes)

---

## 8. YouTube/Google API Configuration

### GOOGLE_CLIENT_ID
- **Description**: Google OAuth client ID
- **Type**: String
- **Security**: 🔒 SECRET
- **Required**: Yes
- **Format**: `{id}.apps.googleusercontent.com`

### GOOGLE_CLIENT_SECRET
- **Description**: Google OAuth client secret
- **Type**: String
- **Security**: 🔒 SECRET
- **Required**: Yes

### GOOGLE_REDIRECT_URI
- **Description**: OAuth redirect URI
- **Type**: String (URL)
- **Required**: Yes
- **Dev**: `http://localhost:3000/api/auth/youtube/callback`
- **Prod**: `https://app.aifilmstudio.com/api/auth/youtube/callback`

### GOOGLE_API_KEY
- **Description**: Google API key for read-only operations
- **Type**: String
- **Security**: 🔒 SECRET
- **Required**: No (optional)

### YOUTUBE_API_QUOTA_LIMIT
- **Description**: Daily API quota limit
- **Type**: Integer
- **Default**: `10000`
- **Note**: Request increase from Google if needed

### YOUTUBE_UPLOAD_RETRY
- **Description**: Number of upload retries on failure
- **Type**: Integer
- **Default**: `3`
- **Prod**: `5`

### YOUTUBE_DEFAULT_PRIVACY
- **Description**: Default video privacy setting
- **Type**: String (enum)
- **Allowed Values**: `public`, `private`, `unlisted`
- **Dev**: `private`
- **Prod**: `public`

---

## 9. AI/ML Models Configuration

### MODEL_CACHE_DIR
- **Description**: Local directory for model caching
- **Type**: String (filesystem path)
- **Dev**: `./data/model_cache`
- **Prod**: `/mnt/efs/models`

### CUDA_VISIBLE_DEVICES
- **Description**: GPU devices to use (comma-separated)
- **Type**: String
- **Dev**: `0`
- **Prod**: `0,1,2,3`

### SD_MODEL_NAME
- **Description**: Stable Diffusion model identifier
- **Type**: String (HuggingFace model ID)
- **Default**: `stabilityai/stable-diffusion-xl-base-1.0`

### SD_INFERENCE_STEPS
- **Description**: Number of inference steps for SD
- **Type**: Integer
- **Range**: `20-50`
- **Dev**: `30`
- **Prod**: `40`

### SD_BATCH_SIZE
- **Description**: Batch size for SD inference
- **Type**: Integer
- **Dev**: `1`
- **Prod**: `4`

### TTS_PROVIDER
- **Description**: Text-to-speech provider
- **Type**: String (enum)
- **Allowed Values**: `elevenlabs`, `coqui`, `openai`
- **Default**: `elevenlabs`

### ELEVENLABS_API_KEY
- **Description**: ElevenLabs API key
- **Type**: String
- **Security**: 🔒 SECRET
- **Required**: If using ElevenLabs

### FFMPEG_THREADS
- **Description**: Number of FFmpeg threads
- **Type**: Integer
- **Dev**: `4`
- **Prod**: `32`

### FFMPEG_CRF
- **Description**: Constant Rate Factor for video quality
- **Type**: Integer
- **Range**: `0-51` (lower = better quality)
- **Dev**: `23`
- **Prod**: `18`

---

## 10. Authentication & Security

### JWT_SECRET_KEY
- **Description**: Secret key for JWT token signing
- **Type**: String (minimum 32 characters)
- **Security**: 🔒 SECRET - Critical
- **Required**: Yes
- **Note**: Generate with `openssl rand -hex 32`

### JWT_ALGORITHM
- **Description**: JWT signing algorithm
- **Type**: String
- **Default**: `HS256`
- **Allowed Values**: `HS256`, `HS384`, `HS512`, `RS256`

### JWT_ACCESS_TOKEN_EXPIRE_MINUTES
- **Description**: Access token expiration time in minutes
- **Type**: Integer
- **Dev**: `60`
- **Prod**: `30`

### JWT_REFRESH_TOKEN_EXPIRE_DAYS
- **Description**: Refresh token expiration time in days
- **Type**: Integer
- **Dev**: `30`
- **Prod**: `7`

### PASSWORD_HASH_ROUNDS
- **Description**: Bcrypt hashing rounds
- **Type**: Integer
- **Dev**: `12`
- **Prod**: `14`
- **Note**: Higher = more secure but slower

### SESSION_SECRET
- **Description**: Secret for session encryption
- **Type**: String (minimum 32 characters)
- **Security**: 🔒 SECRET - Critical
- **Required**: Yes

### SESSION_COOKIE_SECURE
- **Description**: Require HTTPS for session cookies
- **Type**: Boolean
- **Dev**: `false`
- **Prod**: `true`

---

## 11. Feature Flags

### FEATURE_USER_REGISTRATION
- **Description**: Enable user registration
- **Type**: Boolean
- **Default**: `true`

### FEATURE_YOUTUBE_UPLOAD
- **Description**: Enable YouTube upload feature
- **Type**: Boolean
- **Default**: `true`

### FEATURE_SALESFORCE_SYNC
- **Description**: Enable Salesforce synchronization
- **Type**: Boolean
- **Default**: `true`

### FEATURE_PODCAST_MODE
- **Description**: Enable podcast generation mode
- **Type**: Boolean
- **Default**: `true`

### FEATURE_CREDITS_SYSTEM
- **Description**: Enable credit system
- **Type**: Boolean
- **Default**: `true`

### FEATURE_SUBSCRIPTIONS
- **Description**: Enable subscription plans
- **Type**: Boolean
- **Dev**: `false`
- **Prod**: `true`

---

## 12. Monitoring & Logging

### CLOUDWATCH_ENABLED
- **Description**: Enable CloudWatch logging
- **Type**: Boolean
- **Dev**: `false`
- **Prod**: `true`

### CLOUDWATCH_LOG_GROUP
- **Description**: CloudWatch log group name
- **Type**: String
- **Example**: `/aws/aifilmstudio/prod`

### SENTRY_DSN
- **Description**: Sentry DSN for error tracking
- **Type**: String (URL)
- **Security**: 🔒 SECRET
- **Required**: No (recommended for Prod)

### SENTRY_ENVIRONMENT
- **Description**: Environment name for Sentry
- **Type**: String
- **Example**: `production`

### METRICS_ENABLED
- **Description**: Enable Prometheus metrics
- **Type**: Boolean
- **Dev**: `false`
- **Prod**: `true`

---

## 13. Email/Notification Configuration

### EMAIL_PROVIDER
- **Description**: Email service provider
- **Type**: String (enum)
- **Allowed Values**: `smtp`, `sendgrid`, `ses`
- **Default**: `sendgrid`

### SENDGRID_API_KEY
- **Description**: SendGrid API key
- **Type**: String
- **Security**: 🔒 SECRET
- **Required**: If using SendGrid

### SENDGRID_FROM_EMAIL
- **Description**: Default sender email address
- **Type**: String (email format)
- **Example**: `noreply@aifilmstudio.com`

### TWILIO_ACCOUNT_SID
- **Description**: Twilio account SID for SMS
- **Type**: String
- **Security**: 🔒 SECRET

### TWILIO_AUTH_TOKEN
- **Description**: Twilio authentication token
- **Type**: String
- **Security**: 🔒 SECRET

---

## 14. Third-Party Services

### STRIPE_PUBLIC_KEY
- **Description**: Stripe publishable key
- **Type**: String
- **Security**: Public (but environment-specific)

### STRIPE_SECRET_KEY
- **Description**: Stripe secret key
- **Type**: String
- **Security**: 🔒 SECRET - Critical

### STRIPE_WEBHOOK_SECRET
- **Description**: Stripe webhook signing secret
- **Type**: String
- **Security**: 🔒 SECRET

### GOOGLE_ANALYTICS_ID
- **Description**: Google Analytics measurement ID
- **Type**: String
- **Format**: `G-XXXXXXXXXX`

---

## 15. Job Processing

### WORKER_CONCURRENCY
- **Description**: Number of concurrent worker processes
- **Type**: Integer
- **Dev**: `2`
- **Prod**: `16`

### WORKER_MAX_RETRIES
- **Description**: Maximum job retry attempts
- **Type**: Integer
- **Default**: `3`
- **Prod**: `5`

### JOB_TIMEOUT_IMAGE_GEN
- **Description**: Timeout for image generation in seconds
- **Type**: Integer
- **Default**: `300` (5 minutes)

### JOB_TIMEOUT_VIDEO_GEN
- **Description**: Timeout for video generation in seconds
- **Type**: Integer
- **Default**: `600` (10 minutes)

---

## 16. Credit System

### CREDITS_ENABLED
- **Description**: Enable credit system
- **Type**: Boolean
- **Default**: `true`

### CREDITS_DEFAULT_BALANCE
- **Description**: Default credit balance for new users
- **Type**: Integer
- **Dev**: `100`
- **Prod**: `0`

### CREDITS_IMAGE_GENERATION
- **Description**: Credits cost for image generation
- **Type**: Integer
- **Default**: `5`

### CREDITS_VIDEO_GENERATION
- **Description**: Credits cost for video generation
- **Type**: Integer
- **Default**: `20`

---

## 17. Performance Tuning

### DB_POOL_SIZE
- **Description**: Database connection pool size
- **Type**: Integer
- **Dev**: `10`
- **Prod**: `100`

### WORKER_THREADS
- **Description**: Number of worker threads
- **Type**: Integer
- **Dev**: `4`
- **Prod**: `32`

### REQUEST_TIMEOUT
- **Description**: API request timeout in seconds
- **Type**: Integer
- **Default**: `30`

---

## 18. Backup & Recovery

### BACKUP_ENABLED
- **Description**: Enable automated backups
- **Type**: Boolean
- **Dev**: `false`
- **Prod**: `true`

### BACKUP_SCHEDULE
- **Description**: Backup schedule (cron format)
- **Type**: String (cron expression)
- **Default**: `0 2 * * *` (2 AM daily)

### BACKUP_RETENTION_DAYS
- **Description**: Backup retention period in days
- **Type**: Integer
- **Dev**: `7`
- **Prod**: `90`

---

## 19. Security Headers

### HSTS_ENABLED
- **Description**: Enable HTTP Strict Transport Security
- **Type**: Boolean
- **Dev**: `false`
- **Prod**: `true`

### CSP_ENABLED
- **Description**: Enable Content Security Policy
- **Type**: Boolean
- **Dev**: `false`
- **Prod**: `true`

---

## 20. Auto-Scaling

### AUTO_SCALING_ENABLED
- **Description**: Enable auto-scaling
- **Type**: Boolean
- **Staging**: `true`
- **Prod**: `true`

### AUTO_SCALING_MIN_INSTANCES
- **Description**: Minimum number of instances
- **Type**: Integer
- **Staging**: `2`
- **Prod**: `4`

### AUTO_SCALING_MAX_INSTANCES
- **Description**: Maximum number of instances
- **Type**: Integer
- **Staging**: `8`
- **Prod**: `50`

### AUTO_SCALING_TARGET_CPU
- **Description**: Target CPU utilization percentage
- **Type**: Integer
- **Range**: `0-100`
- **Default**: `70`

---

## Environment-Specific Overrides

### Quick Reference Matrix

| Variable | Dev | Sandbox | Staging | Production |
|----------|-----|---------|---------|------------|
| DEBUG | true | true | false | false |
| LOG_LEVEL | DEBUG | INFO | INFO | WARNING |
| DATABASE_POOL_SIZE | 5 | 10 | 30 | 100 |
| WORKER_CONCURRENCY | 2 | 4 | 8 | 16 |
| RATE_LIMIT_REQUESTS | 100 | 200 | 500 | 1000 |
| JWT_ACCESS_TOKEN_EXPIRE | 60 min | 60 min | 60 min | 30 min |
| BACKUP_ENABLED | false | true | true | true |
| AUTO_SCALING_ENABLED | false | false | true | true |

---

## 📝 Summary

This reference document provides:

✅ **Complete variable catalog** - All environment variables documented  
✅ **Security guidelines** - Clear marking of secrets and sensitive data  
✅ **Environment recommendations** - Specific values for each environment  
✅ **Type validation** - Data types and allowed values  
✅ **Cross-references** - Links to related documentation  

---

**🔒 Remember: Always use AWS Secrets Manager for production secrets!**

---

_Last Updated: 2025-01-01_  
_Version: 1.0.0_  
_Maintained by: AI-Empower-HQ-360_
