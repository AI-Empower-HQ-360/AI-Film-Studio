#!/bin/bash
# Build and push Docker images to ECR

set -e

ENVIRONMENT=${1:-dev}
REGION=${2:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "🔨 Building and pushing Docker images"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"
echo "Account ID: $ACCOUNT_ID"

# Backend repository
BACKEND_REPO="ai-film-studio-backend-$ENVIRONMENT"
BACKEND_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$BACKEND_REPO"

# Worker repository
WORKER_REPO="ai-film-studio-worker-$ENVIRONMENT"
WORKER_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$WORKER_REPO"

# Login to ECR
echo "Logging in to ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# Build and push backend
echo "Building backend image..."
cd ../..
docker build -f infrastructure/aws-cdk/Dockerfile.backend -t $BACKEND_REPO:latest .
docker tag $BACKEND_REPO:latest $BACKEND_URI:latest
docker push $BACKEND_URI:latest

# Build and push worker
echo "Building worker image..."
docker build -f infrastructure/aws-cdk/Dockerfile.worker -t $WORKER_REPO:latest .
docker tag $WORKER_REPO:latest $WORKER_URI:latest
docker push $WORKER_URI:latest

echo "✅ Images built and pushed successfully!"
echo "Backend: $BACKEND_URI:latest"
echo "Worker: $WORKER_URI:latest"
