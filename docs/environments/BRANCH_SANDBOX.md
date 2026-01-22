# Sandbox Environment (sandbox branch)

## 🎯 Purpose
Testing, QA, and integration validation.

## 🌍 Environment Details

| Property | Value |
|----------|-------|
| Branch | `sandbox` |
| AWS Account | Test Account |
| Environment URL | https://sandbox.aifilmstudio.com |
| Database | Test RDS (Single AZ) |
| Cache | Test ElastiCache |
| Salesforce | QA Sandbox |

## 🚀 Deployment

- **Trigger**: Automatic on push to `sandbox` branch
- **Method**: GitHub Actions workflow
- **Approval**: QA team approval required for PR
- **Rollback**: Manual via GitHub Actions

## ✅ Testing Requirements

- All unit tests must pass
- Integration tests must pass
- E2E tests must pass
- Code coverage > 80%
- Security scans pass
- Performance benchmarks met

## 🔐 Access Control

- Developers: Read access
- QA Engineers: Full read/write access
- DevOps: Full access

## 📊 Monitoring

- CloudWatch Logs: `sandbox-ai-film-studio-*`
- CloudWatch Metrics: `sandbox/ai-film-studio/*`
- Alarms: All errors and warnings

## 🔧 Configuration

### Environment Variables
```bash
ENVIRONMENT=sandbox
AWS_REGION=us-east-1
DATABASE_URL=sandbox-db.aifilmstudio.com
REDIS_URL=sandbox-redis.aifilmstudio.com
API_BASE_URL=https://sandbox-api.aifilmstudio.com
```

### Feature Flags
- Production-like feature flags
- Beta features enabled
- Experimental features: Case-by-case basis

## 📝 QA Workflow

1. Merge from `dev` to `sandbox`:
   ```bash
   git checkout sandbox
   git pull origin sandbox
   git merge dev
   git push origin sandbox
   ```

2. Wait for automatic deployment

3. Run QA test suite:
   ```bash
   npm run test:e2e
   npm run test:integration
   ```

4. If tests pass, proceed to staging:
   ```bash
   git checkout staging
   git merge sandbox
   # Create PR to staging
   ```

## 🧪 Testing Focus

- **Functional Testing**: All features work as expected
- **Integration Testing**: Services communicate properly
- **Regression Testing**: No existing features broken
- **Performance Testing**: Load and stress tests
- **Security Testing**: Penetration testing, vulnerability scans

## 🐛 Debugging

- Access logs: `aws logs tail sandbox-ai-film-studio --follow`
- SSH access: QA team only
- Database access: Read-only for QA, full access for DevOps

## 📞 Support

- Contact: qa-team@aifilmstudio.com
- Slack: #sandbox-environment
- On-call: QA team during business hours

---

**Last Updated**: 2025-12-31
