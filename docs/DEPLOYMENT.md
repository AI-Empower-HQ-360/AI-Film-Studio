# Deployment Guide

This guide covers deploying AI Film Studio to production environments.

## Quick Start with Docker Compose

The easiest way to deploy the entire stack:

### Prerequisites
- Docker and Docker Compose installed
- AWS account (for S3 storage)
- API keys for AI services

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Verify services**
```bash
docker-compose ps
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

5. **View logs**
```bash
docker-compose logs -f backend
docker-compose logs -f worker
```

6. **Stop services**
```bash
docker-compose down
```

## Production Deployment

### Backend Deployment

#### Option 1: AWS ECS

1. **Build and push Docker image**
```bash
cd backend
docker build -t ai-film-studio-backend .
docker tag ai-film-studio-backend:latest YOUR_ECR_REPO/backend:latest
docker push YOUR_ECR_REPO/backend:latest
```

2. **Create ECS Task Definition**
```json
{
  "family": "ai-film-studio-backend",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "YOUR_ECR_REPO/backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "DATABASE_URL", "value": "postgresql://..."},
        {"name": "REDIS_URL", "value": "redis://..."}
      ],
      "secrets": [
        {"name": "SECRET_KEY", "valueFrom": "arn:aws:secretsmanager:..."},
        {"name": "AWS_ACCESS_KEY_ID", "valueFrom": "arn:aws:secretsmanager:..."}
      ]
    }
  ]
}
```

3. **Create ECS Service** with Application Load Balancer

#### Option 2: Google Cloud Run

```bash
cd backend
gcloud builds submit --tag gcr.io/PROJECT_ID/backend
gcloud run deploy backend \
  --image gcr.io/PROJECT_ID/backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=... \
  --set-secrets SECRET_KEY=...
```

#### Option 3: Heroku

```bash
cd backend
heroku create ai-film-studio-backend
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
heroku config:set SECRET_KEY=...
git push heroku main
```

### Worker Deployment

#### Option 1: AWS ECS

Same as backend, but with different task definition:

```json
{
  "family": "ai-film-studio-worker",
  "containerDefinitions": [
    {
      "name": "worker",
      "image": "YOUR_ECR_REPO/worker:latest",
      "environment": [
        {"name": "REDIS_URL", "value": "redis://..."}
      ],
      "secrets": [
        {"name": "OPENAI_API_KEY", "valueFrom": "arn:aws:secretsmanager:..."}
      ]
    }
  ]
}
```

#### Option 2: Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: celery-worker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: celery-worker
  template:
    metadata:
      labels:
        app: celery-worker
    spec:
      containers:
      - name: worker
        image: YOUR_REGISTRY/worker:latest
        env:
        - name: REDIS_URL
          value: "redis://redis:6379/0"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai
```

### Frontend Deployment

#### Option 1: Vercel (Recommended)

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy**
```bash
cd frontend
vercel
```

3. **Set environment variables in Vercel dashboard**
- `NEXT_PUBLIC_API_URL`: Your backend URL

#### Option 2: Netlify

1. **Build the project**
```bash
cd frontend
npm run build
```

2. **Deploy via Netlify CLI**
```bash
npm i -g netlify-cli
netlify deploy --prod --dir=.next
```

#### Option 3: AWS S3 + CloudFront

1. **Build static export** (modify next.config.ts first)
```bash
npm run build
```

2. **Upload to S3**
```bash
aws s3 sync .next s3://your-bucket/
```

3. **Configure CloudFront** distribution

### Database Setup

#### AWS RDS PostgreSQL

1. **Create RDS instance**
```bash
aws rds create-db-instance \
  --db-instance-identifier ai-film-studio-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20
```

2. **Run migrations**
```bash
# Connect to RDS and create tables
psql -h YOUR_RDS_ENDPOINT -U admin -d postgres -f schema.sql
```

#### Managed PostgreSQL (Digital Ocean, Supabase, etc.)

Follow provider's setup instructions and use connection string in `DATABASE_URL`.

### Redis Setup

#### AWS ElastiCache

```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id ai-film-studio-redis \
  --engine redis \
  --cache-node-type cache.t3.micro \
  --num-cache-nodes 1
```

#### Managed Redis (Redis Labs, Upstash, etc.)

Use provider's connection URL in `REDIS_URL`.

### S3 Setup

1. **Create S3 bucket**
```bash
aws s3 mb s3://ai-film-studio-outputs
```

2. **Configure CORS**
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["https://your-frontend-domain.com"],
      "AllowedMethods": ["GET", "HEAD"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

3. **Set lifecycle policy** (optional, to auto-delete old files)
```json
{
  "Rules": [
    {
      "Id": "DeleteOldFiles",
      "Status": "Enabled",
      "Expiration": {
        "Days": 30
      },
      "Prefix": "outputs/"
    }
  ]
}
```

## Environment Variables

### Backend
```env
# Required
SECRET_KEY=your-secret-key-min-32-chars
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://host:6379/0
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET_NAME=your-bucket

# Optional
MAX_COST_PER_JOB=100.0
MAX_COST_PER_USER_DAILY=500.0
ENABLE_CONTENT_MODERATION=true
```

### Worker
```env
# Required
REDIS_URL=redis://host:6379/0
OPENAI_API_KEY=sk-...
STABILITY_API_KEY=sk-...
ELEVENLABS_API_KEY=...

# Optional
WORKER_CONCURRENCY=4
```

### Frontend
```env
NEXT_PUBLIC_API_URL=https://api.your-domain.com
```

## Monitoring

### Application Monitoring

#### Sentry (Error Tracking)

1. **Install Sentry SDK**
```bash
pip install sentry-sdk[fastapi]
```

2. **Initialize in main.py**
```python
import sentry_sdk
sentry_sdk.init(dsn="YOUR_DSN")
```

#### DataDog (APM)

1. **Install DataDog agent**
2. **Add tracing to FastAPI**
```python
from ddtrace import patch_all
patch_all()
```

### Infrastructure Monitoring

#### Prometheus + Grafana

1. **Expose metrics endpoint**
```python
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
```

2. **Configure Prometheus to scrape**
3. **Create Grafana dashboards**

## Scaling

### Horizontal Scaling

#### Backend
- Deploy multiple instances behind load balancer
- Use session affinity if needed
- Scale based on CPU/memory metrics

#### Worker
- Scale based on queue length
- Use auto-scaling groups
- Monitor task completion time

### Vertical Scaling

- Increase instance size for compute-heavy tasks
- Use GPU instances for AI model inference

### Database Scaling

- Enable read replicas
- Use connection pooling (pgbouncer)
- Optimize queries and indexes

## Security Checklist

- [ ] Change all default passwords
- [ ] Use secrets manager for sensitive data
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up VPC/network isolation
- [ ] Enable database encryption at rest
- [ ] Implement rate limiting
- [ ] Set up WAF rules
- [ ] Enable audit logging
- [ ] Regular security updates

## Backup and Recovery

### Database Backups

```bash
# Automated daily backups
pg_dump -h HOST -U USER -d DATABASE > backup.sql

# Upload to S3
aws s3 cp backup.sql s3://backups/$(date +%Y%m%d).sql
```

### Restore Procedure

```bash
# Download backup
aws s3 cp s3://backups/YYYYMMDD.sql backup.sql

# Restore
psql -h HOST -U USER -d DATABASE < backup.sql
```

## Troubleshooting

### Backend Issues

**Can't connect to database**
- Check DATABASE_URL format
- Verify network connectivity
- Check database is running

**High memory usage**
- Reduce worker count
- Check for memory leaks
- Enable connection pooling

### Worker Issues

**Tasks not processing**
- Check Redis connection
- Verify worker is running
- Check queue has tasks

**Tasks timing out**
- Increase TASK_TIMEOUT
- Optimize AI API calls
- Use task result expiry

### Frontend Issues

**API calls failing**
- Check CORS configuration
- Verify API_URL is correct
- Check authentication tokens

## Cost Optimization

1. **Use spot instances** for workers (70% cost savings)
2. **Implement caching** to reduce API calls
3. **Set S3 lifecycle policies** to delete old files
4. **Use reserved instances** for predictable workload
5. **Monitor AI API costs** and set alerts
6. **Compress videos** to reduce storage costs

## Performance Optimization

1. **Enable CDN** for frontend assets
2. **Use database indexes** on frequently queried fields
3. **Implement Redis caching** for expensive queries
4. **Optimize image/video sizes**
5. **Use async I/O** throughout
6. **Batch AI API calls** where possible

## Maintenance

### Regular Tasks

- Monitor error rates and logs
- Check disk space usage
- Review cost reports
- Update dependencies
- Test backup/restore
- Security patches
- Performance tuning

### Upgrade Procedure

1. Test in staging environment
2. Announce maintenance window
3. Create database backup
4. Deploy new version
5. Run smoke tests
6. Monitor for issues
7. Rollback if needed

## Support

For deployment issues:
- Check GitHub Issues
- Review logs and metrics
- Contact support team
