# Production Environment (main branch)

## 🎯 Purpose
Live production deployment serving real users.

## 🌍 Environment Details

| Property | Value |
|----------|-------|
| Branch | `main` (or `production`) |
| AWS Account | Production Account |
| Environment URL | https://aifilmstudio.com |
| Database | Production RDS (Multi-AZ with read replicas) |
| Cache | Production ElastiCache (Cluster mode, multi-AZ) |
| Salesforce | Production Org |

## 🚀 Deployment

- **Trigger**: Manual deployment only
- **Method**: GitHub Actions workflow with blue-green deployment
- **Approval**: 3+ approvers (including 1 code owner)
- **Rollback**: Automated rollback with one-click capability
- **Strategy**: Blue-green or Canary deployment
- **Deployment Window**: Scheduled during low-traffic periods

## ✅ Testing Requirements

- All tests from all environments must pass
- Full regression test suite (100% pass rate)
- Production smoke tests post-deployment
- Zero critical or high-severity security vulnerabilities
- Performance tests exceed SLA requirements
- Disaster recovery test passed
- Final sign-off from Product and Engineering leads

## 🔐 Access Control

- Developers: No direct access (read-only via monitoring tools)
- QA Engineers: No direct access
- DevOps Engineers: Limited read access
- Release Managers: Full deployment access
- Site Reliability Engineers: Full access for incidents
- Administrators: Full access (emergency only)

## 📊 Monitoring

- CloudWatch Logs: `prod-ai-film-studio-*`
- CloudWatch Metrics: `prod/ai-film-studio/*`
- Alarms: Comprehensive alerting for all services
- X-Ray tracing: Enabled with sampling
- APM: Full application performance monitoring
- Real User Monitoring (RUM): Enabled
- Synthetic monitoring: 24/7 health checks
- PagerDuty integration: Critical alerts

## 🔧 Configuration

### Environment Variables
```bash
ENVIRONMENT=production
AWS_REGION=us-east-1
DATABASE_URL=prod-db.aifilmstudio.com
DATABASE_REPLICA_URL=prod-db-replica.aifilmstudio.com
REDIS_URL=prod-redis.aifilmstudio.com
API_BASE_URL=https://api.aifilmstudio.com
```

### Feature Flags
- Production features only
- Experimental features: Disabled
- Beta features: Enabled for specific user segments
- Kill switches: Available for emergency feature disable

## 📝 Deployment Workflow

### Pre-Deployment

1. **Change Request**:
   - Create change management ticket
   - Document changes and rollback plan
   - Schedule deployment window
   - Notify all stakeholders

2. **Pre-Deployment Checklist**:
   - [ ] All tests passing in Staging for 48+ hours
   - [ ] No critical bugs reported
   - [ ] Security audit completed
   - [ ] Performance validated
   - [ ] Database migrations tested
   - [ ] Rollback plan documented
   - [ ] On-call team briefed
   - [ ] Customer communication prepared (if needed)
   - [ ] Monitoring dashboards reviewed
   - [ ] Backup completed

### Deployment

1. Create PR from `staging` to `main`:
   ```bash
   git checkout main
   git pull origin main
   # Create PR from staging branch
   ```

2. PR Review Requirements:
   - 3+ approvals (including 1 code owner)
   - All automated checks pass
   - Security team sign-off
   - Product team sign-off
   - Engineering lead sign-off

3. Deployment execution:
   ```bash
   # After all approvals
   git merge staging
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin main --tags
   # Manual trigger of production deployment
   ```

4. Blue-Green Deployment:
   - New version deployed to "Green" environment
   - Health checks and smoke tests run
   - Traffic gradually shifted (0% → 25% → 50% → 100%)
   - Monitor metrics at each stage
   - Rollback immediately if issues detected

### Post-Deployment

1. **Immediate Verification** (0-15 minutes):
   - Run automated smoke tests
   - Verify critical user flows
   - Check error rates and latency
   - Monitor logs for anomalies

2. **Short-Term Monitoring** (1-4 hours):
   - Continuous metrics monitoring
   - User feedback review
   - Performance benchmarking
   - Security monitoring

3. **Documentation**:
   - Update release notes
   - Document any issues encountered
   - Update runbooks if needed
   - Close change management ticket

## 🎯 Production Checklist

### Before Deployment
- [ ] Change request approved
- [ ] Deployment window scheduled
- [ ] All stakeholders notified
- [ ] On-call team briefed
- [ ] Rollback plan ready
- [ ] Database backup completed
- [ ] Monitoring dashboards prepared

### During Deployment
- [ ] Blue environment health verified
- [ ] Green environment deployed successfully
- [ ] Smoke tests passed
- [ ] Gradual traffic shift (25% → 50% → 100%)
- [ ] Metrics within acceptable ranges
- [ ] No critical errors in logs

### After Deployment
- [ ] Full smoke test suite passed
- [ ] Performance metrics baseline met
- [ ] Error rates within normal range
- [ ] User feedback monitored
- [ ] Release notes published
- [ ] Post-deployment report completed

## 🧪 Production Testing

- **Smoke Tests**: Automated critical path testing
- **Synthetic Monitoring**: 24/7 health checks from multiple regions
- **Canary Deployments**: Gradual rollout to subset of users
- **Feature Flags**: Progressive feature enablement

## 🚨 Incident Response

### Severity Levels

| Severity | Description | Response Time |
|----------|-------------|---------------|
| P0 - Critical | Service down, data loss | Immediate (< 5 min) |
| P1 - High | Major feature broken | < 15 minutes |
| P2 - Medium | Non-critical feature broken | < 1 hour |
| P3 - Low | Minor issue, workaround available | < 24 hours |

### Rollback Procedure

For immediate rollback:

1. **Automatic Rollback**:
   ```bash
   # If automated checks fail, system auto-rolls back
   # No manual intervention needed
   ```

2. **Manual Rollback**:
   ```bash
   # Switch traffic back to Blue (previous version)
   # Via AWS Console or CLI command
   aws elbv2 modify-target-group --target-group-arn <blue-tg> --weight 100
   ```

3. **Code Revert**:
   ```bash
   git revert <commit-hash>
   git push origin main
   # Trigger emergency deployment
   ```

4. **Post-Incident**:
   - Declare incident in PagerDuty
   - Notify stakeholders immediately
   - Document timeline and actions taken
   - Conduct post-mortem within 48 hours
   - Create action items for prevention

## 🔐 Security

- All commits must be signed
- MFA required for all production access
- Audit logging enabled for all operations
- Regular security scans and penetration testing
- Compliance: SOC 2, GDPR, HIPAA (if applicable)
- Data encryption: At rest and in transit
- Secrets management: AWS Secrets Manager
- DDoS protection: AWS Shield + CloudFlare

## 📊 SLA Targets

| Metric | Target |
|--------|--------|
| Uptime | 99.9% |
| API Response Time (p95) | < 500ms |
| API Response Time (p99) | < 1000ms |
| Error Rate | < 0.1% |
| Time to Detect (TTD) | < 5 minutes |
| Time to Resolve (TTR) | < 1 hour (P1) |

## 🐛 Debugging

- Access logs: Restricted, audit logged
- SSH access: Emergency only, MFA required
- Database access: Read-only replicas only
- Bastion hosts: MFA and IP-restricted
- Log aggregation: CloudWatch + third-party SIEM

## 📞 Support

- **Email**: ops@aifilmstudio.com
- **Slack**: #production-alerts, #incidents
- **PagerDuty**: 24/7 on-call rotation
- **Escalation**: Defined escalation matrix
- **Status Page**: https://status.aifilmstudio.com

## 🏷️ Release Versioning

All production releases are tagged with semantic versioning:

```bash
v1.0.0 - Major.Minor.Patch
```

- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes (backward compatible)

Example:
```bash
git tag -a v1.2.3 -m "Release v1.2.3: Bug fixes and performance improvements"
git push origin v1.2.3
```

## 📈 Capacity Planning

- Review usage metrics weekly
- Plan for 2x current load
- Auto-scaling configured for all services
- Regular load testing (monthly)
- Cost optimization reviews (quarterly)

## 🔄 Disaster Recovery

- **RTO (Recovery Time Objective)**: 4 hours
- **RPO (Recovery Point Objective)**: 1 hour
- **Backup Frequency**: Continuous (transaction log) + Daily snapshots
- **Backup Retention**: 30 days
- **DR Testing**: Quarterly drills
- **Multi-Region**: Standby region (us-west-2) ready for failover

---

**Last Updated**: 2025-12-31

**⚠️ IMPORTANT**: Production is a controlled environment. All changes must follow the documented process. Unauthorized access or changes may result in disciplinary action.
