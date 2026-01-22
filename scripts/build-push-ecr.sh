#!/bin/bash
# Bash script to build and push Docker images to ECR
# Usage: ./scripts/build-push-ecr.sh -e dev -t backend

set -e

ENVIRONMENT="dev"
IMAGE_TYPE="all"
TAG="latest"
REGION="us-east-1"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -t|--type)
            IMAGE_TYPE="$2"
            shift 2
            ;;
        --tag)
            TAG="$2"
            shift 2
            ;;
        -r|--region)
            REGION="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "=== Building and Pushing Docker Images to ECR ==="
echo "Environment: $ENVIRONMENT"
echo "Image Type: $IMAGE_TYPE"
echo "Tag: $TAG"
echo "Region: $REGION"
echo ""

# Get AWS account ID
echo "Getting AWS account ID..."
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
if [ -z "$ACCOUNT_ID" ]; then
    echo "Error: Failed to get AWS account ID. Make sure AWS CLI is configured."
    exit 1
fi
echo "Account ID: $ACCOUNT_ID"
echo ""

# ECR base URI
ECR_BASE="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

# Login to ECR
echo "Logging in to ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_BASE
echo "Successfully logged in to ECR"
echo ""

# Function to create ECR repository if it doesn't exist
create_ecr_repo() {
    local REPO_NAME=$1
    echo "Checking if repository '$REPO_NAME' exists..."
    
    if aws ecr describe-repositories --repository-names $REPO_NAME --region $REGION > /dev/null 2>&1; then
        echo "Repository '$REPO_NAME' already exists"
    else
        echo "Repository doesn't exist. Creating..."
        aws ecr create-repository \
            --repository-name $REPO_NAME \
            --region $REGION \
            --image-scanning-configuration scanOnPush=true \
            --image-tag-mutability MUTABLE
        echo "Repository '$REPO_NAME' created successfully"
    fi
}

# Function to build and push image
build_and_push() {
    local IMAGE_NAME=$1
    local DOCKERFILE=$2
    local CONTEXT=${3:-.}
    
    local REPO_NAME="ai-film-studio-$IMAGE_NAME-$ENVIRONMENT"
    local ECR_URI="$ECR_BASE/$REPO_NAME"
    
    echo "=== Processing $IMAGE_NAME ==="
    echo "Repository: $REPO_NAME"
    echo "ECR URI: $ECR_URI"
    echo ""
    
    # Create repository if needed
    create_ecr_repo $REPO_NAME
    echo ""
    
    # Build image
    echo "Building Docker image..."
    docker build -t "$IMAGE_NAME:$TAG" -f $DOCKERFILE $CONTEXT
    echo "Image built successfully"
    echo ""
    
    # Tag image
    echo "Tagging image..."
    docker tag "$IMAGE_NAME:$TAG" "$ECR_URI:$TAG"
    docker tag "$IMAGE_NAME:$TAG" "$ECR_URI:latest"
    echo "Image tagged successfully"
    echo ""
    
    # Push image
    echo "Pushing image to ECR..."
    docker push "$ECR_URI:$TAG"
    docker push "$ECR_URI:latest"
    echo "Image pushed successfully"
    echo ""
    
    echo "=== $IMAGE_NAME Complete ==="
    echo "ECR URI: $ECR_URI"
    echo "Tags: $TAG, latest"
    echo ""
}

# Build and push images
if [ "$IMAGE_TYPE" == "all" ] || [ "$IMAGE_TYPE" == "backend" ]; then
    build_and_push "backend" "Dockerfile" "."
fi

if [ "$IMAGE_TYPE" == "all" ] || [ "$IMAGE_TYPE" == "worker" ]; then
    build_and_push "worker" "Dockerfile.worker" "."
fi

echo "=== All Images Built and Pushed Successfully ==="
echo ""
echo "Next steps:"
echo "1. Update ECS service to use new image"
echo "2. Verify deployment in AWS Console"
echo ""
