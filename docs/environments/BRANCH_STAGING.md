# Staging Environment (staging branch)

## 🎯 Purpose
Pre-production validation and final verification before production deployment.

## 🌍 Environment Details

| Property | Value |
|----------|-------|
| Branch | `staging` |
| AWS Account | Production Account (Staging VPC) |
| Environment URL | https://staging.aifilmstudio.com |
| Database | Staging RDS (Multi-AZ) |
| Cache | Staging ElastiCache (Cluster mode) |
| Salesforce | Staging Sandbox |

## 🚀 Deployment

- **Trigger**: Manual deployment with approval
- **Method**: GitHub Actions workflow
- **Approval**: 2+ reviewers required (including DevOps)
- **Rollback**: Automated rollback capability
- **Strategy**: Blue-green deployment

## ✅ Testing Requirements

- All tests from Dev and Sandbox must pass
- Full test suite execution (100% coverage)
- Performance tests meet SLA requirements
- Security scans show no critical vulnerabilities
- Smoke tests pass
- UAT (User Acceptance Testing) completed

## 🔐 Access Control

- Developers: Read access only
- QA Engineers: Read access
- DevOps Engineers: Full access
- Release Managers: Full access
- Product Managers: Read access for UAT

## 📊 Monitoring

- CloudWatch Logs: `staging-ai-film-studio-*`
- CloudWatch Metrics: `staging/ai-film-studio/*`
- Alarms: Production-level monitoring
- X-Ray tracing: Enabled
- APM: Full application performance monitoring

## 🔧 Configuration

### Environment Variables
```bash
ENVIRONMENT=staging
AWS_REGION=us-east-1
DATABASE_URL=staging-db.aifilmstudio.com
REDIS_URL=staging-redis.aifilmstudio.com
API_BASE_URL=https://staging-api.aifilmstudio.com
```

### Feature Flags
- Exact mirror of production
- All production features enabled
- Experimental features: Disabled

## 📝 Deployment Workflow

1. Create PR from `sandbox` to `staging`:
   ```bash
   git checkout staging
   git pull origin staging
   # Create PR from sandbox branch
   ```

2. PR Review Requirements:
   - 2+ approvals from DevOps/Release Managers
   - All automated checks pass
   - Security scan approval
   - Performance test results reviewed

3. Merge and deploy:
   ```bash
   # After PR approval
   git merge sandbox
   git push origin staging
   # Manual trigger of deployment workflow
   ```

4. Post-deployment verification:
   - Smoke tests run automatically
   - Manual UAT by product team
   - Performance monitoring for 24-48 hours

## 🧪 Testing Focus

- **Smoke Testing**: Core functionality verified immediately
- **UAT**: Business stakeholders validate features
- **Performance Testing**: Load testing under production-like conditions
- **Security Testing**: Final security audit
- **Disaster Recovery**: Backup and restore procedures tested

## 🎯 Pre-Production Checklist

- [ ] All tests passing in Sandbox
- [ ] Security scan completed with no critical issues
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Rollback plan documented
- [ ] Monitoring and alerts configured
- [ ] Database migrations tested
- [ ] Third-party integrations verified
- [ ] UAT sign-off received
- [ ] Change management ticket created

## 🐛 Debugging

- Access logs: `aws logs tail staging-ai-film-studio --follow`
- SSH access: DevOps and Release Managers only
- Database access: Read-only, restricted IP access
- Production-like data: Anonymized production data

## 📞 Support

- Contact: devops-team@aifilmstudio.com
- Slack: #staging-environment
- On-call: DevOps team 24/7

## 🔄 Rollback Procedure

If issues are detected in staging:

1. Stop ongoing deployments
2. Revert to previous stable version:
   ```bash
   git revert <commit-hash>
   git push origin staging
   ```
3. Notify stakeholders
4. Investigate root cause
5. Fix in dev/sandbox and restart process

---

**Last Updated**: 2025-12-31
