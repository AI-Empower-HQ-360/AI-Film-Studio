# AWS Backend Infrastructure Setup

## Overview

Complete guide for deploying the AI Film Studio backend API to AWS using ECS Fargate, with RDS, S3, and SQS.

---

## 🏗️ Architecture Components

```
┌─────────────────────────────────────────────────────────────┐
│                     AWS Cloud Infrastructure                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐                     │
│  │   Route 53   │─────▶│     ALB      │                     │
│  │  (DNS)       │      │(Load Balancer)│                    │
│  └──────────────┘      └───────┬──────┘                     │
│                                 │                            │
│                        ┌────────▼────────┐                   │
│                        │   ECS Fargate   │                   │
│                        │  FastAPI Tasks  │                   │
│                        │  (Auto-scaling) │                   │
│                        └────────┬────────┘                   │
│                                 │                            │
│         ┌───────────────────────┼───────────────────┐       │
│         │                       │                   │       │
│    ┌────▼────┐           ┌─────▼─────┐      ┌─────▼─────┐ │
│    │   RDS   │           │    S3     │      │    SQS    │ │
│    │Postgres │           │  Bucket   │      │   Queue   │ │
│    └─────────┘           └───────────┘      └───────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Secrets Manager (API Keys, Credentials)       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

1. **AWS CLI Installed**
   ```bash
   aws --version
   # AWS CLI 2.x required
   ```

2. **Docker Installed** (for local testing)
   ```bash
   docker --version
   ```

3. **AWS Account with Permissions**
   - ECS, ECR, RDS, S3, SQS, IAM, VPC, Secrets Manager

---

## 🚀 Quick Start (AWS CloudShell)

### Step 1: Create S3 Bucket

```bash
# Set variables
export AWS_REGION=us-east-1
export BUCKET_NAME=ai-film-studio-assets-prod
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create S3 bucket
aws s3 mb s3://${BUCKET_NAME} --region ${AWS_REGION}

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket ${BUCKET_NAME} \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket ${BUCKET_NAME} \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Set CORS for frontend access
aws s3api put-bucket-cors \
  --bucket ${BUCKET_NAME} \
  --cors-configuration file://s3-cors.json

# Set lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket ${BUCKET_NAME} \
  --lifecycle-configuration file://s3-lifecycle.json
```

**Create `s3-cors.json`:**
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["https://www.aifilmstudio.com", "https://staging.aifilmstudio.com"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
      "AllowedHeaders": ["*"],
      "ExposeHeaders": ["ETag"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

**Create `s3-lifecycle.json`:**
```json
{
  "Rules": [
    {
      "Id": "DeleteTempFilesAfter7Days",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "temp/"
      },
      "Expiration": {
        "Days": 7
      }
    },
    {
      "Id": "TransitionOldVideosToGlacier",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "videos/"
      },
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ]
    }
  ]
}
```

### Step 2: Create SQS Queue

```bash
# Create job queue
aws sqs create-queue \
  --queue-name ai-film-studio-queue-prod \
  --attributes '{
    "DelaySeconds": "0",
    "MessageRetentionPeriod": "1209600",
    "ReceiveMessageWaitTimeSeconds": "20",
    "VisibilityTimeout": "3600"
  }'

# Create dead letter queue
aws sqs create-queue \
  --queue-name ai-film-studio-dlq-prod \
  --attributes MessageRetentionPeriod=1209600

# Get queue URLs
export QUEUE_URL=$(aws sqs get-queue-url --queue-name ai-film-studio-queue-prod --query QueueUrl --output text)
export DLQ_URL=$(aws sqs get-queue-url --queue-name ai-film-studio-dlq-prod --query QueueUrl --output text)

echo "Queue URL: $QUEUE_URL"
echo "DLQ URL: $DLQ_URL"
```

### Step 3: Create RDS Database

```bash
# Create DB subnet group
aws rds create-db-subnet-group \
  --db-subnet-group-name ai-film-studio-db-subnet \
  --db-subnet-group-description "AI Film Studio DB Subnets" \
  --subnet-ids subnet-xxxxx subnet-yyyyy

# Create RDS instance (PostgreSQL)
aws rds create-db-instance \
  --db-instance-identifier ai-film-studio-db-prod \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.4 \
  --master-username aifilmadmin \
  --master-user-password 'YourSecurePassword123!' \
  --allocated-storage 20 \
  --storage-type gp3 \
  --storage-encrypted \
  --db-subnet-group-name ai-film-studio-db-subnet \
  --vpc-security-group-ids sg-xxxxx \
  --backup-retention-period 7 \
  --preferred-backup-window "03:00-04:00" \
  --preferred-maintenance-window "sun:04:00-sun:05:00" \
  --multi-az \
  --publicly-accessible false

# Wait for DB to be available
aws rds wait db-instance-available \
  --db-instance-identifier ai-film-studio-db-prod

# Get DB endpoint
export DB_ENDPOINT=$(aws rds describe-db-instances \
  --db-instance-identifier ai-film-studio-db-prod \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text)

echo "Database Endpoint: $DB_ENDPOINT"
```

### Step 4: Store Secrets in Secrets Manager

```bash
# Store database credentials
aws secretsmanager create-secret \
  --name ai-film-studio/db/prod \
  --secret-string '{
    "username": "aifilmadmin",
    "password": "YourSecurePassword123!",
    "host": "'$DB_ENDPOINT'",
    "port": "5432",
    "database": "aifilmstudio"
  }'

# Store API keys
aws secretsmanager create-secret \
  --name ai-film-studio/api-keys/prod \
  --secret-string '{
    "STABILITY_AI_API_KEY": "your_key_here",
    "ELEVENLABS_API_KEY": "your_key_here",
    "OPENAI_API_KEY": "your_key_here",
    "RUNWAYML_API_KEY": "your_key_here"
  }'

# Store JWT secret
aws secretsmanager create-secret \
  --name ai-film-studio/jwt/prod \
  --secret-string '{
    "JWT_SECRET": "'$(openssl rand -base64 32)'",
    "JWT_ALGORITHM": "HS256"
  }'
```

### Step 5: Create ECR Repository

```bash
# Create ECR repository for backend
aws ecr create-repository \
  --repository-name ai-film-studio/backend \
  --image-scanning-configuration scanOnPush=true \
  --encryption-configuration encryptionType=AES256

# Get repository URI
export ECR_URI=$(aws ecr describe-repositories \
  --repository-names ai-film-studio/backend \
  --query 'repositories[0].repositoryUri' \
  --output text)

echo "ECR Repository: $ECR_URI"
```

### Step 6: Build and Push Docker Image

```bash
# Login to ECR
aws ecr get-login-password --region ${AWS_REGION} | \
  docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Build Docker image
cd /workspaces/AI-Film-Studio
docker build -t ai-film-studio-backend .

# Tag image
docker tag ai-film-studio-backend:latest ${ECR_URI}:latest
docker tag ai-film-studio-backend:latest ${ECR_URI}:v0.1.0

# Push to ECR
docker push ${ECR_URI}:latest
docker push ${ECR_URI}:v0.1.0
```

### Step 7: Create ECS Cluster

```bash
# Create ECS cluster
aws ecs create-cluster \
  --cluster-name ai-film-studio-prod \
  --capacity-providers FARGATE FARGATE_SPOT \
  --default-capacity-provider-strategy \
    capacityProvider=FARGATE,weight=1,base=1 \
    capacityProvider=FARGATE_SPOT,weight=4

echo "ECS Cluster created: ai-film-studio-prod"
```

### Step 8: Create Task Definition

**Create `ecs-task-definition.json`:**
```json
{
  "family": "ai-film-studio-backend-prod",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ai-film-studio-task-role",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ai-film-studio/backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "environment": [
        {
          "name": "AWS_REGION",
          "value": "us-east-1"
        },
        {
          "name": "AWS_S3_BUCKET",
          "value": "ai-film-studio-assets-prod"
        },
        {
          "name": "API_HOST",
          "value": "0.0.0.0"
        },
        {
          "name": "API_PORT",
          "value": "8000"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:ai-film-studio/db/prod"
        },
        {
          "name": "STABILITY_AI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:ai-film-studio/api-keys/prod:STABILITY_AI_API_KEY::"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ai-film-studio-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "backend"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/api/v1/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

```bash
# Register task definition
aws ecs register-task-definition \
  --cli-input-json file://ecs-task-definition.json
```

### Step 9: Create Application Load Balancer

```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name ai-film-studio-alb-prod \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx \
  --scheme internet-facing \
  --type application \
  --ip-address-type ipv4

# Create target group
aws elbv2 create-target-group \
  --name ai-film-studio-tg-prod \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxxxx \
  --target-type ip \
  --health-check-enabled \
  --health-check-path /api/v1/health \
  --health-check-interval-seconds 30 \
  --health-check-timeout-seconds 5 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:ACCOUNT_ID:loadbalancer/app/ai-film-studio-alb-prod/xxxxx \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:ACCOUNT_ID:targetgroup/ai-film-studio-tg-prod/xxxxx
```

### Step 10: Create ECS Service

```bash
# Create ECS service
aws ecs create-service \
  --cluster ai-film-studio-prod \
  --service-name backend-api \
  --task-definition ai-film-studio-backend-prod:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --platform-version LATEST \
  --network-configuration "awsvpcConfiguration={
    subnets=[subnet-xxxxx,subnet-yyyyy],
    securityGroups=[sg-xxxxx],
    assignPublicIp=ENABLED
  }" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:ACCOUNT_ID:targetgroup/ai-film-studio-tg-prod/xxxxx,containerName=backend,containerPort=8000" \
  --health-check-grace-period-seconds 60

echo "ECS Service created successfully!"
```

---

## ✅ Verification

```bash
# Get ALB DNS name
export ALB_DNS=$(aws elbv2 describe-load-balancers \
  --names ai-film-studio-alb-prod \
  --query 'LoadBalancers[0].DNSName' \
  --output text)

# Test health endpoint
curl http://${ALB_DNS}/api/v1/health

# Expected response:
# {"status":"healthy","version":"0.1.0","service":"AI Film Studio"}
```

---

## 📊 Cost Estimate

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| ECS Fargate | 2 tasks × 1 vCPU, 2 GB | $60 |
| RDS PostgreSQL | db.t3.micro, Multi-AZ | $30 |
| S3 | 100 GB storage + transfer | $15 |
| ALB | 1 load balancer | $16 |
| SQS | 1M requests | $0.40 |
| Secrets Manager | 3 secrets | $1.20 |
| CloudWatch Logs | 10 GB logs | $5 |
| **Total** | | **~$127/month** |

---

## 🔐 Security Best Practices

1. ✅ Use Secrets Manager for credentials
2. ✅ Enable encryption at rest (S3, RDS, SQS)
3. ✅ Use security groups to restrict access
4. ✅ Enable VPC Flow Logs
5. ✅ Use IAM roles instead of access keys
6. ✅ Enable CloudTrail for audit logging
7. ✅ Use WAF on ALB (optional)

---

## 📚 Next Steps

1. Set up auto-scaling for ECS service
2. Configure CloudWatch alarms
3. Set up CI/CD pipeline (GitHub Actions)
4. Add custom domain with Route 53
5. Enable SSL/TLS with ACM
6. Deploy GPU worker nodes for AI processing
