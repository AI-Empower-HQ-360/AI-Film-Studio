#!/bin/bash
# LocalStack initialization script
# Creates S3 buckets, SQS queues, and SNS topics for local development

set -e

echo "Initializing LocalStack AWS services..."

# Wait for LocalStack to be ready
sleep 5

# Create S3 buckets
awslocal s3 mb s3://ai-film-studio-assets
awslocal s3 mb s3://ai-film-studio-characters
awslocal s3 mb s3://ai-film-studio-marketing

echo "✓ S3 buckets created"

# Create SQS queues
awslocal sqs create-queue --queue-name ai-film-studio-jobs
awslocal sqs create-queue --queue-name ai-film-studio-video-jobs
awslocal sqs create-queue --queue-name ai-film-studio-voice-jobs
awslocal sqs create-queue --queue-name ai-film-studio-jobs-dlq

echo "✓ SQS queues created"

# Create SNS topics
awslocal sns create-topic --name ai-film-studio-job-completion
awslocal sns create-topic --name ai-film-studio-errors
awslocal sns create-topic --name ai-film-studio-system-alerts

echo "✓ SNS topics created"

# Create Secrets Manager secrets
awslocal secretsmanager create-secret \
    --name ai-film-studio/database \
    --secret-string '{"username":"aifilmstudio","password":"aifilmstudio","host":"postgres","port":"5432","dbname":"aifilmstudio"}'

awslocal secretsmanager create-secret \
    --name ai-film-studio/api-keys \
    --secret-string '{"openai":"test-key","elevenlabs":"test-key","stability":"test-key"}'

echo "✓ Secrets Manager secrets created"

echo "LocalStack initialization complete!"
