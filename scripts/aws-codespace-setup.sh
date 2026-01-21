#!/bin/bash
# Quick AWS Setup for Codespace CLI
# Run this script to configure AWS credentials and deploy Amplify

set -e

echo "================================================"
echo "AWS Amplify Setup via Codespace CLI"
echo "================================================"
echo ""

# Check if AWS CLI is available
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Installing..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip -q awscliv2.zip
    sudo ./aws/install
    rm -rf aws awscliv2.zip
    echo "✅ AWS CLI installed"
fi

echo "AWS CLI version: $(aws --version)"
echo ""

# Check authentication
echo "Checking AWS authentication..."
if aws sts get-caller-identity &> /dev/null; then
    echo "✅ Already authenticated with AWS"
    aws sts get-caller-identity
else
    echo "❌ Not authenticated with AWS"
    echo ""
    echo "To authenticate, you have two options:"
    echo ""
    echo "Option 1: Configure AWS credentials manually"
    echo "  aws configure"
    echo "  Then enter your Access Key ID, Secret Access Key, and region"
    echo ""
    echo "Option 2: Use AWS IAM Identity Center (SSO)"
    echo "  aws configure sso"
    echo "  Follow the prompts to authenticate via browser"
    echo ""
    read -p "Press Enter to run 'aws configure' or Ctrl+C to exit..."
    aws configure
fi

echo ""
echo "================================================"
echo "Verifying AWS credentials..."
echo "================================================"

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_USER=$(aws sts get-caller-identity --query Arn --output text)

echo "✅ Authenticated as: $AWS_USER"
echo "✅ Account ID: $AWS_ACCOUNT_ID"

echo ""
echo "================================================"
echo "Next steps:"
echo "================================================"
echo ""
echo "1. Run the Amplify setup script:"
echo "   ./scripts/amplify-cloudshell-setup.sh"
echo ""
echo "2. Or use manual Amplify commands from:"
echo "   scripts/amplify-cloudshell-commands.md"
echo ""
