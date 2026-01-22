# ECR Repository Setup Guide

## Overview

This guide explains how to set up and use Amazon ECR (Elastic Container Registry) repositories for the AI Film Studio project.

## ECR Repositories

The CDK stack creates two ECR repositories:

1. **Backend Repository**: `ai-film-studio-backend-{environment}`
   - For backend API Docker images
   - Used by ECS Fargate service

2. **Worker Repository**: `ai-film-studio-worker-{environment}`
   - For GPU worker Docker images
   - Used by EC2 GPU instances

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured
3. **Docker** installed
4. **GitHub Actions** configured with AWS credentials

## Setup Methods

### Method 1: Via CDK (Recommended)

The ECR repositories are automatically created when you deploy the CDK stack:

```bash
cd infrastructure/aws-cdk
cdk deploy AIFilmStudio-dev
```

This creates:
- `ai-film-studio-backend-dev`
- `ai-film-studio-worker-dev`

### Method 2: Via AWS CLI

```bash
# Create backend repository
aws ecr create-repository \
  --repository-name ai-film-studio-backend-dev \
  --region us-east-1 \
  --image-scanning-configuration scanOnPush=true \
  --image-tag-mutability MUTABLE

# Create worker repository
aws ecr create-repository \
  --repository-name ai-film-studio-worker-dev \
  --region us-east-1 \
  --image-scanning-configuration scanOnPush=true \
  --image-tag-mutability MUTABLE
```

### Method 3: Via GitHub Actions (Automated)

The GitHub Actions workflow (`.github/workflows/ecr-build-push.yml`) automatically creates repositories if they don't exist when you push code.

## Manual Docker Build and Push

### 1. Authenticate Docker to ECR

```bash
# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1

# Login to ECR
aws ecr get-login-password --region $REGION | \
  docker login --username AWS --password-stdin \
  $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
```

**Windows PowerShell:**
```powershell
$accountId = (aws sts get-caller-identity --query Account --output text)
$region = "us-east-1"
aws ecr get-login-password --region $region | docker login --username AWS --password-stdin "$accountId.dkr.ecr.$region.amazonaws.com"
```

### 2. Build Docker Image

```bash
# Backend image
docker build -t ai-film-studio-backend:latest -f Dockerfile .

# Worker image
docker build -t ai-film-studio-worker:latest -f Dockerfile.worker .
```

### 3. Tag Image for ECR

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1
ENVIRONMENT=dev

# Backend
docker tag ai-film-studio-backend:latest \
  $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ai-film-studio-backend-$ENVIRONMENT:latest

# Worker
docker tag ai-film-studio-worker:latest \
  $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ai-film-studio-worker-$ENVIRONMENT:latest
```

### 4. Push to ECR

```bash
# Backend
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ai-film-studio-backend-$ENVIRONMENT:latest

# Worker
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ai-film-studio-worker-$ENVIRONMENT:latest
```

## GitHub Actions Workflow

The workflow (`.github/workflows/ecr-build-push.yml`) automatically:

1. **Builds** Docker images on code push
2. **Tags** images with multiple tags (latest, commit SHA, branch-run number)
3. **Pushes** to ECR repositories
4. **Updates** ECS services to use new images

### Triggering the Workflow

**Automatic triggers:**
- Push to `main` or `develop` branches
- Changes to `src/`, `Dockerfile`, or `requirements.txt`

**Manual trigger:**
```bash
# Via GitHub UI: Actions > Build and Push to ECR > Run workflow
# Or via GitHub CLI:
gh workflow run ecr-build-push.yml \
  -f environment=dev \
  -f image_type=backend \
  -f tag=v1.0.0
```

## ECR Repository Configuration

### Lifecycle Policies

The CDK stack configures lifecycle policies to:
- Keep last 10 images
- Automatically delete older images

### Image Scanning

- **Scan on Push**: Enabled
- Scans for vulnerabilities automatically
- Results available in ECR console

### Access Control

ECR repositories use IAM for access control:
- ECS tasks have read access
- GitHub Actions has push access (via IAM role)
- Developers need `ecr:GetAuthorizationToken` and `ecr:BatchGetImage` permissions

## Viewing ECR Repositories

### Via AWS Console

1. Go to **ECR** service in AWS Console
2. Navigate to **Repositories**
3. Find `ai-film-studio-backend-{env}` and `ai-film-studio-worker-{env}`

### Via AWS CLI

```bash
# List repositories
aws ecr describe-repositories --region us-east-1

# List images in a repository
aws ecr list-images \
  --repository-name ai-film-studio-backend-dev \
  --region us-east-1

# Get image details
aws ecr describe-images \
  --repository-name ai-film-studio-backend-dev \
  --region us-east-1
```

## Troubleshooting

### Error: Repository does not exist

```bash
# Create it manually or deploy CDK stack
cdk deploy AIFilmStudio-dev
```

### Error: Access denied

```bash
# Check IAM permissions
aws iam get-user
aws iam list-attached-user-policies --user-name YOUR_USERNAME

# Ensure you have:
# - ecr:GetAuthorizationToken
# - ecr:BatchGetImage
# - ecr:PutImage
# - ecr:InitiateLayerUpload
```

### Error: Docker login failed

```bash
# Verify AWS credentials
aws sts get-caller-identity

# Try login again
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com
```

### Error: Image push failed

```bash
# Check repository exists
aws ecr describe-repositories --repository-name ai-film-studio-backend-dev

# Check image tag
docker images | grep ai-film-studio

# Verify ECR URI matches
echo $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ai-film-studio-backend-dev
```

## Best Practices

1. **Use specific tags** for production (e.g., `v1.0.0`)
2. **Use `latest`** only for development
3. **Enable image scanning** for security
4. **Set lifecycle policies** to manage storage costs
5. **Use multi-stage builds** to reduce image size
6. **Tag images** with commit SHA for traceability

## Cost Optimization

- **Lifecycle policies**: Automatically delete old images
- **Image scanning**: Free for first 1 million scans/month
- **Storage**: Pay only for what you store
- **Data transfer**: Free within same region

## Security

- **Image scanning**: Enabled by default
- **IAM access control**: Use least privilege
- **Private repositories**: Not publicly accessible
- **Encryption**: At rest and in transit

## Next Steps

1. **Deploy CDK stack** to create repositories
2. **Configure GitHub Actions** with AWS credentials
3. **Build and push** your first image
4. **Update ECS service** to use new image

## Related Documentation

- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [CDK ECR Construct](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_ecr.html)
- [GitHub Actions ECR Login](https://github.com/aws-actions/amazon-ecr-login)
