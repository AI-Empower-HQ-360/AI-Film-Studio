# Infrastructure Setup Guide

This document provides instructions for setting up and deploying the AI Film Studio infrastructure.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [AWS Infrastructure Deployment](#aws-infrastructure-deployment)
- [CI/CD Configuration](#cicd-configuration)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Tools

1. **Terraform** >= 1.5.0
   ```bash
   # Install via Homebrew (macOS)
   brew install terraform
   
   # Or download from https://www.terraform.io/downloads
   ```

2. **AWS CLI** >= 2.0
   ```bash
   # Install via Homebrew (macOS)
   brew install awscli
   
   # Configure AWS credentials
   aws configure
   ```

3. **Docker Desktop**
   - Download from https://www.docker.com/products/docker-desktop
   - Ensure Docker is running before starting local development

4. **Node.js** >= 18
   ```bash
   # Install via Homebrew (macOS)
   brew install node@18
   ```

5. **Python** >= 3.11
   ```bash
   # Install via Homebrew (macOS)
   brew install python@3.11
   ```

### AWS Account Setup

1. Create an AWS account if you don't have one
2. Set up IAM user with appropriate permissions:
   - AdministratorAccess (for initial setup)
   - Or specific permissions for EC2, ECS, RDS, S3, CloudFront, etc.
3. Generate Access Key and Secret Key
4. Configure AWS CLI:
   ```bash
   aws configure
   ```

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio
```

### 2. Start Local Services with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

### 3. Access Local Services

- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **PgAdmin**: http://localhost:5050 (admin@ai-film-studio.local / admin)
- **Redis Commander**: http://localhost:8081
- **LocalStack Dashboard**: http://localhost:4566

### 4. Initialize LocalStack Resources

```bash
# Create S3 bucket
aws --endpoint-url=http://localhost:4566 s3 mb s3://ai-film-studio-assets-dev

# Create SQS queue
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name ai-film-studio-queue

# List resources
aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 sqs list-queues
```

## AWS Infrastructure Deployment

### 1. Initialize Terraform State Backend

First, create the S3 bucket and DynamoDB table for Terraform state:

```bash
# Create S3 bucket for Terraform state
aws s3 mb s3://ai-film-studio-terraform-state-dev --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket ai-film-studio-terraform-state-dev \
  --versioning-configuration Status=Enabled

# Create DynamoDB table for state locking
aws dynamodb create-table \
  --table-name ai-film-studio-terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

### 2. Deploy Development Environment

```bash
cd infrastructure/terraform/environments/dev

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply the infrastructure
terraform apply

# Save the outputs
terraform output > outputs.txt
```

### 3. Deploy Sandbox/QA Environment

```bash
cd ../sandbox

# Create state bucket for sandbox
aws s3 mb s3://ai-film-studio-terraform-state-sandbox --region us-east-1

# Initialize and apply
terraform init
terraform plan
terraform apply
```

### 4. Deploy Staging Environment

```bash
cd ../staging

# Create state bucket for staging
aws s3 mb s3://ai-film-studio-terraform-state-staging --region us-east-1

# Initialize and apply
terraform init
terraform plan
terraform apply
```

### 5. Deploy Production Environment

```bash
cd ../production

# Create state bucket for production
aws s3 mb s3://ai-film-studio-terraform-state-production --region us-east-1

# Initialize and apply
terraform init
terraform plan
terraform apply
```

**Note**: Production deployments should require manual approval. Use the GitHub Actions workflow for production deployments.

## CI/CD Configuration

### 1. GitHub Secrets Setup

Add the following secrets to your GitHub repository:

#### Development Environment
- `AWS_ACCESS_KEY_ID` - AWS access key for dev environment
- `AWS_SECRET_ACCESS_KEY` - AWS secret key for dev environment

#### Staging Environment
- `AWS_ACCESS_KEY_ID_STAGING` - AWS access key for staging
- `AWS_SECRET_ACCESS_KEY_STAGING` - AWS secret key for staging

#### Production Environment
- `AWS_ACCESS_KEY_ID_PROD` - AWS access key for production
- `AWS_SECRET_ACCESS_KEY_PROD` - AWS secret key for production

#### Optional Secrets
- `SNYK_TOKEN` - Snyk API token for security scanning
- `NEXT_PUBLIC_API_URL` - API URL for frontend

### 2. GitHub Environments Configuration

Create the following environments in your GitHub repository settings:

1. **dev** - Auto-deploy on push to `develop` branch
2. **staging** - Auto-deploy on push to `main` branch
3. **production** - Requires manual approval before deployment

### 3. Workflow Triggers

The CI/CD workflows are triggered automatically:

- **Terraform**: On push/PR to `infrastructure/terraform/**`
- **Backend**: On push/PR to `backend/**`, `src/**`, `requirements.txt`
- **Worker**: On push/PR to `worker/**`
- **Frontend**: On push/PR to `frontend/**`

## Environment Variables

### Backend Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis
REDIS_URL=redis://:password@host:6379/0

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET=ai-film-studio-assets-dev
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/123456789/queue-name

# Security
JWT_SECRET=your_jwt_secret_here
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
API_VERSION=v1
```

### Worker Environment Variables

```bash
# Database and Redis (same as backend)
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://:password@host:6379/0

# AWS (same as backend)
AWS_REGION=us-east-1
S3_BUCKET=ai-film-studio-assets-dev
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/123456789/queue-name

# AI Models
DEVICE=cuda  # or 'cpu' for local development
MODEL_CACHE_DIR=/app/models
HUGGINGFACE_TOKEN=your_hf_token_here

# Processing
MAX_CONCURRENT_JOBS=2
JOB_TIMEOUT=300
```

### Frontend Environment Variables

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://api.ai-film-studio.com
NEXT_PUBLIC_ENVIRONMENT=production

# Optional
NEXT_PUBLIC_ANALYTICS_ID=your_analytics_id
```

## Monitoring and Observability

### CloudWatch Dashboards

Access CloudWatch dashboards in AWS Console:

1. Navigate to CloudWatch > Dashboards
2. View system health metrics
3. Monitor API performance
4. Track GPU utilization

### CloudWatch Alarms

Alarms are automatically configured for:

- RDS CPU utilization > 80%
- SQS queue depth > 100
- ECS task failures
- DLQ messages > 0

### Logs

Access logs in CloudWatch Logs:

```bash
# Backend logs
aws logs tail /ecs/ai-film-studio-backend-dev --follow

# Worker logs
aws logs tail /ecs/ai-film-studio-workers-dev --follow
```

## Cost Optimization

### Development Environment

- Auto-scale GPU workers to 0 when idle
- Use spot instances for GPU workers
- Stop RDS instance when not in use:
  ```bash
  aws rds stop-db-instance --db-instance-identifier ai-film-studio-postgres-dev
  ```

### Production Environment

- Use Reserved Instances for predictable workloads
- Enable S3 Intelligent-Tiering
- Use CloudFront for global content delivery
- Implement aggressive caching strategies

### Cost Monitoring

```bash
# View monthly costs
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

## Troubleshooting

### Terraform Issues

**Issue**: "Backend configuration changed"
```bash
# Re-initialize with the new backend
terraform init -reconfigure
```

**Issue**: "Resource already exists"
```bash
# Import the existing resource
terraform import aws_s3_bucket.frontend ai-film-studio-frontend-dev-123456789
```

### Docker Compose Issues

**Issue**: "Port already in use"
```bash
# Find and kill the process using the port
lsof -ti:8000 | xargs kill -9
```

**Issue**: "Cannot connect to database"
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres

# View PostgreSQL logs
docker-compose logs postgres
```

### ECS Deployment Issues

**Issue**: "Service failed to stabilize"
```bash
# Check task status
aws ecs describe-tasks \
  --cluster ai-film-studio-backend-dev \
  --tasks $(aws ecs list-tasks --cluster ai-film-studio-backend-dev --query 'taskArns[0]' --output text)

# Check logs
aws logs tail /ecs/ai-film-studio-backend-dev --follow
```

### GPU Worker Issues

**Issue**: "Out of memory"
- Reduce batch size
- Use smaller models
- Enable gradient checkpointing

**Issue**: "CUDA not available"
- Verify GPU instance type (g4dn/g5)
- Check NVIDIA drivers are installed
- Use AWS Deep Learning AMI

## Backup and Recovery

### Manual Backup

```bash
# Create RDS snapshot
aws rds create-db-snapshot \
  --db-instance-identifier ai-film-studio-postgres-prod \
  --db-snapshot-identifier manual-backup-$(date +%Y%m%d-%H%M%S)

# Export Terraform state
cd infrastructure/terraform/environments/production
terraform state pull > terraform-state-backup-$(date +%Y%m%d-%H%M%S).json
```

### Disaster Recovery

See [Disaster Recovery Plan](../../docs/architecture/cloud-infrastructure-stack.md#disaster-recovery) in the architecture documentation.

## Additional Resources

- [Cloud Infrastructure Stack Documentation](../../docs/architecture/cloud-infrastructure-stack.md)
- [System Design Document](../../docs/architecture/system-design.md)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

## Support

For issues or questions:
- Create an issue in the GitHub repository
- Contact the DevOps team: devops@ai-empower-hq.com
- Check the [Troubleshooting](#troubleshooting) section above

---

**Last Updated**: 2025-12-31  
**Maintained by**: AI-Empower-HQ-360 DevOps Team
