#!/bin/bash
# Deployment script for AWS CDK infrastructure

set -e

ENVIRONMENT=${1:-dev}
REGION=${2:-us-east-1}

echo "🚀 Deploying AI Film Studio Infrastructure"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
fi

# Install AWS CDK if not present
if ! command -v cdk &> /dev/null; then
    echo "Installing AWS CDK..."
    npm install -g aws-cdk
fi

# Bootstrap CDK (if needed)
echo "Checking CDK bootstrap..."
cdk bootstrap aws://$(aws sts get-caller-identity --query Account --output text)/$REGION || true

# Synthesize
echo "Synthesizing CDK stack..."
cdk synth --context environment=$ENVIRONMENT --context region=$REGION

# Deploy
echo "Deploying stack..."
cdk deploy --context environment=$ENVIRONMENT --context region=$REGION --require-approval never

echo "✅ Deployment complete!"
echo "Check outputs above for service URLs and endpoints."
