# AI Film Studio - Environment Setup Quick Start Guide

This guide helps you quickly set up any environment for AI Film Studio.

---

## 📋 Table of Contents

1. [Development Environment](#development-environment)
2. [Testing/QA Environment](#testingqa-environment)
3. [Staging Environment](#staging-environment)
4. [Production Environment](#production-environment)
5. [Troubleshooting](#troubleshooting)

---

## Development Environment

### Prerequisites

- **Node.js**: 18+ (for frontend)
- **Python**: 3.11+ (for backend and workers)
- **Docker Desktop**: Latest version (for PostgreSQL, Redis)
- **Git**: Latest version

### Quick Setup (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/AI-Empower-HQ-360/AI-Film-Studio.git
cd AI-Film-Studio

# 2. Copy environment configuration
cp .env.dev.example .env.dev

# 3. Start local services with Docker
docker-compose up -d

# 4. Set up Python backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 5. Run database migrations
alembic upgrade head

# 6. Start backend server
uvicorn src.main:app --reload --port 5000

# 7. In a new terminal, set up frontend
cd frontend
npm install
npm run dev

# 8. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
# API Docs: http://localhost:5000/docs
```

### Configuration

Edit `.env.dev` to customize:

```bash
# Enable/disable AI features
USE_MOCK_AI=true          # Use mock responses for fast testing
# USE_MOCK_AI=false       # Use real AI models (requires GPU)

# Database
DATABASE_URL=postgresql://aifilm:dev_password@localhost:5432/aifilm_dev

# Redis
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=DEBUG           # Verbose logging for development
```

### Development Workflow

```bash
# Run tests
pytest                    # Backend tests
npm test                  # Frontend tests

# Lint code
ruff check .              # Python linting
npm run lint              # Frontend linting

# Format code
black .                   # Python formatting
npm run format            # Frontend formatting
```

---

## Testing/QA Environment

### Prerequisites

- **AWS Account**: With appropriate permissions
- **AWS CLI**: Configured with credentials
- **Terraform**: 1.5+ (optional, for infrastructure)

### Accessing Sandbox Environment

The sandbox environment is automatically deployed when code is merged to the `develop` branch.

```bash
# Environment URLs
Frontend: https://sandbox.ai-filmstudio.com
API: https://api-sandbox.ai-filmstudio.com
API Docs: https://api-sandbox.ai-filmstudio.com/docs

# Test user credentials (use for QA testing)
Email: test@ai-filmstudio.com
Password: TestUser123!
```

### Running Tests Against Sandbox

```bash
# Set sandbox API URL
export API_URL=https://api-sandbox.ai-filmstudio.com

# Run integration tests
pytest tests/integration/

# Run E2E tests
npm run test:e2e
```

### QA Testing Checklist

- [ ] User registration and login
- [ ] Script upload and parsing
- [ ] AI video generation (end-to-end)
- [ ] Video download and playback
- [ ] Payment flows (test mode)
- [ ] Email notifications
- [ ] API rate limiting
- [ ] Error handling

---

## Staging Environment

### Prerequisites

- **Staging Access**: VPN or IP whitelisting required
- **AWS SSO**: Multi-factor authentication enabled

### Accessing Staging Environment

```bash
# Environment URLs
Frontend: https://staging.ai-filmstudio.com
API: https://api-staging.ai-filmstudio.com

# Access requires VPN connection
# Contact DevOps team for VPN credentials
```

### Deployment to Staging

Staging deployments are triggered when code is merged to the `main` branch.

```bash
# Manual deployment (requires approval)
# 1. Merge your PR to 'main'
# 2. Go to GitHub Actions
# 3. Approve the staging deployment
# 4. Monitor deployment progress
```

### Staging Validation

```bash
# Run smoke tests
npm run test:smoke -- --env=staging

# Run performance tests
npm run test:performance -- --env=staging

# Check deployment status
curl https://api-staging.ai-filmstudio.com/health
```

---

## Production Environment

### Prerequisites

- **Production Access**: Restricted to DevOps team
- **AWS SSO**: Multi-factor authentication required
- **Change Approval**: Product owner sign-off required

### Production URLs

```bash
Frontend: https://www.ai-filmstudio.com
API: https://api.ai-filmstudio.com
```

### Deployment to Production

Production deployments require manual approval and follow a blue-green deployment strategy.

```bash
# Deployment Process (DevOps only)
# 1. Staging validation must be complete
# 2. Create production release tag
# 3. Schedule deployment window
# 4. Trigger GitHub Actions workflow
# 5. Approve production deployment
# 6. Monitor gradual traffic shift
#    - 10% → Monitor 10 min
#    - 50% → Monitor 10 min
#    - 100% → Complete
# 7. Verify metrics in CloudWatch
```

### Production Monitoring

```bash
# CloudWatch Dashboard
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=ai-film-studio-prod

# Key Metrics to Monitor
- API Error Rate (target: < 0.1%)
- API Latency (target: < 500ms p95)
- GPU Worker Utilization (target: 60-80%)
- SQS Queue Depth (target: < 50)
- Database CPU (target: < 70%)
```

---

## Troubleshooting

### Common Issues

#### Database Connection Failed

```bash
# Development
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart PostgreSQL
docker-compose restart postgres

# Verify connection
psql -h localhost -U aifilm -d aifilm_dev
```

#### Redis Connection Failed

```bash
# Check if Redis is running
docker ps | grep redis

# Restart Redis
docker-compose restart redis

# Test connection
redis-cli -h localhost ping
```

#### AI Model Loading Failed

```bash
# Development: Use mock AI
export USE_MOCK_AI=true

# Download models manually
python scripts/download_models.py

# Check model cache directory
ls -lh ./models/
```

#### Frontend Not Loading

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Next.js cache
rm -rf .next

# Restart dev server
npm run dev
```

#### Backend 500 Errors

```bash
# Check backend logs
docker-compose logs backend

# Check database migrations
alembic current
alembic upgrade head

# Verify environment variables
cat .env.dev
```

### Environment-Specific Troubleshooting

#### Sandbox/Staging/Production

```bash
# Check ECS service status
aws ecs describe-services \
  --cluster aifilm-sandbox \
  --services aifilm-backend

# View CloudWatch logs
aws logs tail /aws/ecs/aifilm-sandbox \
  --follow \
  --format short

# Check RDS status
aws rds describe-db-instances \
  --db-instance-identifier aifilm-sandbox-db

# Verify S3 bucket access
aws s3 ls s3://ai-film-studio-sandbox-us-east-1/
```

### Getting Help

- **Development Issues**: Slack #dev-support
- **QA/Testing Issues**: Slack #qa-team
- **Staging/Production Issues**: Slack #devops (urgent: PagerDuty)
- **Documentation**: See [environments.md](./docs/architecture/environments.md)

---

## Environment Comparison Reference

| Feature | Development | Testing/QA | Staging | Production |
|---------|-------------|------------|---------|------------|
| **Cost** | $0-100/mo | ~$335/mo | ~$1,000/mo | ~$2,600/mo |
| **Setup Time** | 5 minutes | Auto | Auto | Manual |
| **Database** | Local | db.t3.medium | db.r6g.large | db.r6g.xlarge |
| **GPU Workers** | Optional | 1x g4dn.xlarge | 1-3x | 3-20x |
| **Auto-scaling** | No | Limited | Yes | Yes |
| **Monitoring** | Logs only | CloudWatch | CloudWatch + Alarms | Full stack |
| **Backups** | None | Daily (7d) | Daily (14d) | Daily (30d) + DR |
| **Access** | Local only | Team | VPN required | Public |
| **SSL/TLS** | No | Yes | Yes | Yes + WAF |

---

## Next Steps

1. **Read the full documentation**: [environments.md](./docs/architecture/environments.md)
2. **View architecture diagrams**: [environment-diagram.md](./docs/architecture/environment-diagram.md)
3. **Review system design**: [system-design.md](./docs/architecture/system-design.md)
4. **Check infrastructure code**: [infrastructure/terraform/](./infrastructure/terraform/)

---

**Happy Coding! 🚀**
