# Development Environment (dev branch)

## 🎯 Purpose
Active feature development and rapid iteration.

## 🌍 Environment Details

| Property | Value |
|----------|-------|
| Branch | `dev` |
| AWS Account | Dev Account |
| Environment URL | https://dev.aifilmstudio.com |
| Database | Dev RDS (Single AZ) |
| Cache | Dev ElastiCache |
| Salesforce | Developer Sandbox |

## 🚀 Deployment

- **Trigger**: Automatic on push to `dev` branch
- **Method**: GitHub Actions workflow
- **Approval**: Not required
- **Rollback**: Automatic via previous deployment

## ✅ Testing Requirements

- Unit tests must pass
- Code coverage > 70%
- Linting checks pass

## 🔐 Access Control

- Developers: Full read/write access
- QA: Read access
- DevOps: Full access

## 📊 Monitoring

- CloudWatch Logs: `dev-ai-film-studio-*`
- CloudWatch Metrics: `dev/ai-film-studio/*`
- Alarms: Critical errors only

## 🔧 Configuration

### Environment Variables
```bash
ENVIRONMENT=dev
AWS_REGION=us-east-1
DATABASE_URL=dev-db.aifilmstudio.com
REDIS_URL=dev-redis.aifilmstudio.com
API_BASE_URL=https://dev-api.aifilmstudio.com
```

### Feature Flags
- All features enabled for testing
- Experimental features allowed

## 📝 Development Workflow

1. Create feature branch from `dev`:
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/your-feature-name
   ```

2. Make changes and commit:
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

3. Push and create PR:
   ```bash
   git push origin feature/your-feature-name
   # Create PR to dev branch on GitHub
   ```

4. After PR approval and merge:
   ```bash
   # Automatic deployment to Dev environment
   ```

## 🐛 Debugging

- Access logs: `aws logs tail dev-ai-film-studio --follow`
- SSH access: Available for developers
- Port forwarding: Enabled for local debugging

## 📞 Support

- Contact: dev-team@aifilmstudio.com
- Slack: #dev-environment
- On-call: Not applicable (Dev environment)

---

**Last Updated**: 2025-12-31
