# Environment Configuration Guide

This guide explains how to set up environment-specific configuration files for the AI Film Studio platform.

## Quick Start

1. **Choose your environment** (Dev, Sandbox, Staging, or Production)
2. **Copy the appropriate template** to create your environment file
3. **Fill in the values** with your actual credentials and configuration
4. **Never commit** real credentials to version control

## Environment Files

### Development
```bash
cp .env.dev.example .env
# Edit .env with your local development credentials
```

### Sandbox
```bash
cp .env.sandbox.example .env.sandbox
# Edit .env.sandbox with your sandbox environment credentials
```

### Staging
```bash
cp .env.staging.example .env.staging
# Edit .env.staging with your staging environment credentials
```

### Production
```bash
cp .env.prod.example .env.prod
# Edit .env.prod with your production environment credentials
```

## Important Security Notes

⚠️ **Never commit actual environment files to Git!**

The `.gitignore` file is configured to ignore:
- `.env`
- `.env.local`
- `.env.dev`
- `.env.sandbox`
- `.env.staging`
- `.env.prod`
- `*.env`

✅ **Use AWS Secrets Manager for sensitive data in production**

For production and staging environments, it's recommended to:
1. Store sensitive credentials in AWS Secrets Manager
2. Reference them in your application code
3. Use IAM roles instead of access keys where possible

## Environment Variables Explained

### Database Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Full database connection string | `postgresql://user:pass@host:5432/dbname` |
| `DATABASE_HOST` | Database hostname | `localhost` or RDS endpoint |
| `DATABASE_PORT` | Database port | `5432` |
| `DATABASE_NAME` | Database name | `ai_film_studio_dev` |
| `DATABASE_USER` | Database user | `postgres` |
| `DATABASE_PASSWORD` | Database password | Store in Secrets Manager |

### AWS Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `AWS_REGION` | AWS region | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | AWS access key (use IAM roles in production) | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Store in Secrets Manager |
| `S3_BUCKET_NAME` | S3 bucket for media storage | `ai-film-studio-dev-media` |
| `SQS_QUEUE_URL` | SQS queue URL for job processing | Full SQS URL |

### Salesforce Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `SALESFORCE_CLIENT_ID` | OAuth Client ID from Connected App | Store in Secrets Manager |
| `SALESFORCE_CLIENT_SECRET` | OAuth Client Secret | Store in Secrets Manager |
| `SALESFORCE_USERNAME` | Salesforce username | `user@example.com` |
| `SALESFORCE_PASSWORD` | Salesforce password | Store in Secrets Manager |
| `SALESFORCE_SECURITY_TOKEN` | Salesforce security token | Store in Secrets Manager |
| `SALESFORCE_INSTANCE_URL` | Salesforce instance URL | `https://login.salesforce.com` |

### YouTube Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `YOUTUBE_API_KEY` | YouTube Data API key | Store in Secrets Manager |
| `YOUTUBE_CLIENT_ID` | OAuth Client ID | `xxx.apps.googleusercontent.com` |
| `YOUTUBE_CLIENT_SECRET` | OAuth Client Secret | Store in Secrets Manager |
| `YOUTUBE_REDIRECT_URI` | OAuth redirect URI | `https://yourdomain.com/api/auth/youtube/callback` |

### JWT Authentication

| Variable | Description | Example |
|----------|-------------|---------|
| `JWT_SECRET` | Secret key for signing JWTs | Generate strong random string |
| `JWT_EXPIRES_IN` | Token expiration time | `7d` (7 days) |
| `JWT_REFRESH_SECRET` | Secret for refresh tokens | Generate strong random string |
| `JWT_REFRESH_EXPIRES_IN` | Refresh token expiration | `30d` (30 days) |

### AI Services

| Variable | Description | Example |
|----------|-------------|---------|
| `ELEVENLABS_API_KEY` | ElevenLabs API key for TTS | Store in Secrets Manager |
| `RUNWAY_API_KEY` | Runway ML API key | Store in Secrets Manager |
| `DREAM_MACHINE_API_KEY` | Dream Machine API key | Store in Secrets Manager |

### Feature Flags

| Variable | Description | Values |
|----------|-------------|--------|
| `ENABLE_PODCAST_MODE` | Enable podcast generation | `true` or `false` |
| `ENABLE_SLOKAS_MODE` | Enable slokas/poems | `true` or `false` |
| `ENABLE_MULTI_LANGUAGE` | Enable multiple languages | `true` or `false` |
| `ENABLE_INDIAN_MUSIC` | Enable Indian music generation | `true` or `false` |
| `ENABLE_WESTERN_MUSIC` | Enable Western music generation | `true` or `false` |

## Environment-Specific Best Practices

### Development
- Use local database and Redis when possible
- Lower resource limits for cost savings
- Enable verbose logging (`LOG_LEVEL=DEBUG`)
- Use mock services for external APIs (optional)

### Sandbox
- Mirror dev configuration
- Use AWS services but keep costs low
- Test integrations with real services
- Enable moderate logging (`LOG_LEVEL=INFO`)

### Staging
- Mirror production configuration
- Use production-like data (anonymized)
- Full monitoring and alerting
- Test disaster recovery procedures

### Production
- Use AWS Secrets Manager for all sensitive data
- Enable all security features
- Use Multi-AZ databases and caching
- Enable enhanced monitoring
- Use IAM roles instead of access keys
- Set up automated backups
- Configure auto-scaling

## Terraform Variables

For infrastructure deployment, create corresponding `.tfvars` files:

```bash
# Dev environment
terraform/environments/dev/terraform.tfvars

# Sandbox environment
terraform/environments/sandbox/terraform.tfvars

# Staging environment
terraform/environments/staging/terraform.tfvars

# Production environment
terraform/environments/prod/terraform.tfvars
```

Example `terraform.tfvars`:
```hcl
environment = "dev"
aws_region = "us-east-1"
vpc_cidr = "10.0.0.0/16"
gpu_instance_type = "g4dn.xlarge"
rds_instance_class = "db.t3.micro"
```

## Troubleshooting

### Database Connection Issues
1. Check security group allows connections from your IP
2. Verify database credentials
3. Ensure VPC networking is configured correctly
4. Check database is running and accessible

### AWS Credentials Issues
1. Verify IAM user has required permissions
2. Check AWS CLI configuration: `aws configure list`
3. Test access: `aws s3 ls`
4. Use IAM roles in ECS/EKS instead of access keys

### Redis Connection Issues
1. Check ElastiCache security group settings
2. Verify Redis endpoint and port
3. Check if password is required
4. Ensure application is in the same VPC

### Salesforce API Issues
1. Verify Connected App is active
2. Check OAuth scopes
3. Verify security token (if using password flow)
4. Check API usage limits
5. Ensure IP restrictions allow your server

### YouTube API Issues
1. Verify API is enabled in Google Cloud Console
2. Check OAuth redirect URIs match exactly
3. Verify quota limits
4. Check API key restrictions

## Related Documentation

- [Environment Setup Master Checklist](./ENVIRONMENT_SETUP_CHECKLIST.md) - Complete setup guide
- [Main README](../README.md) - Project overview
- [Architecture Documentation](./architecture/) - System design

## Support

For issues with environment setup:
1. Check this documentation
2. Review the [Environment Setup Checklist](./ENVIRONMENT_SETUP_CHECKLIST.md)
3. Check AWS, Salesforce, and YouTube API documentation
4. Open an issue in the repository with details about your problem

---

**Remember:** Security is paramount. Never expose credentials in code or commits. Use AWS Secrets Manager and IAM roles wherever possible.
