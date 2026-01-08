# Operational Runbooks

**Version**: 1.0  
**Last Updated**: 2025-12-27  
**Owner**: DevOps Team

---

## Table of Contents

1. [Deployment Procedures](#deployment-procedures)
2. [Rollback Procedures](#rollback-procedures)
3. [Scaling Operations](#scaling-operations)
4. [Database Operations](#database-operations)
5. [Monitoring and Alerting](#monitoring-and-alerting)
6. [Security Operations](#security-operations)
7. [Backup and Recovery](#backup-and-recovery)
8. [Troubleshooting Guide](#troubleshooting-guide)

---

## Deployment Procedures

### Standard Deployment (Blue/Green)

**Frequency**: Multiple times per week  
**Duration**: ~30 minutes  
**Risk Level**: Low

#### Pre-Deployment Checklist
- [ ] All tests pass in CI/CD pipeline
- [ ] Code review approved by 2+ engineers
- [ ] Database migrations tested in staging
- [ ] Rollback plan documented
- [ ] Stakeholders notified (if major release)
- [ ] Backup created
- [ ] On-call engineer available

#### Deployment Steps

**1. Verify Staging Environment**
```bash
# SSH into staging bastion or use AWS Systems Manager
aws ecs describe-services --cluster staging-cluster --services backend-service

# Check health
curl https://staging-api.aifilmstudio.com/health

# Validate critical flows
# - User login
# - Film generation
# - File download
```

**2. Deploy to Production (Blue Environment)**
```bash
# Navigate to GitHub Actions or use AWS Console
# Trigger production deployment workflow

# Monitor deployment logs
aws ecs describe-tasks --cluster prod-cluster --tasks <task-arns>

# Check deployment progress
aws ecs describe-services --cluster prod-cluster --services backend-service
```

**3. Smoke Testing**
```bash
# Test critical endpoints
curl -X POST https://api.aifilmstudio.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Check health endpoint
curl https://api.aifilmstudio.com/health

# Test film generation (optional, can be expensive)
# Use test account with test flag
```

**4. Traffic Switchover**
```bash
# Update load balancer target group weights
# Blue (new): 100%, Green (old): 0%

aws elbv2 modify-listener --listener-arn <listener-arn> \
  --default-actions Type=forward,TargetGroupArn=<blue-tg-arn>,Weight=100

# Monitor CloudWatch metrics for 10 minutes
# - Error rate
# - Response time
# - CPU/Memory utilization
```

**5. Post-Deployment Validation**
```bash
# Check error logs
aws logs tail /aws/ecs/prod/backend --follow --since 10m

# Verify database connections
aws rds describe-db-instances --db-instance-identifier prod-db

# Check queue depth
aws sqs get-queue-attributes \
  --queue-url https://sqs.us-east-1.amazonaws.com/xxx/prod-jobs \
  --attribute-names ApproximateNumberOfMessages
```

**6. Monitor for 30 Minutes**
- Watch CloudWatch dashboard
- Monitor Slack #ops-alerts channel
- Check error rates (should be <1%)
- Verify user-reported issues (if any)

#### Post-Deployment Checklist
- [ ] All health checks passing
- [ ] Error rate within acceptable range (<1%)
- [ ] Response times normal (<200ms p95)
- [ ] Database queries performing well
- [ ] No critical alerts triggered
- [ ] Status page updated (if applicable)
- [ ] Deployment logged in change log

---

## Rollback Procedures

### When to Rollback

**Automatic Rollback Triggers**:
- Error rate >5% for 5 minutes
- Response time >500ms for 5 minutes
- Health check failures >50%
- Database connection failures

**Manual Rollback Triggers**:
- Critical feature broken
- Data corruption detected
- Security vulnerability introduced
- Customer escalations

### Quick Rollback (5-10 minutes)

**1. Assess the Situation**
```bash
# Check current error rate
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name HTTPCode_Target_5XX_Count \
  --dimensions Name=LoadBalancer,Value=<lb-name> \
  --start-time <ISO-timestamp> \
  --end-time <ISO-timestamp> \
  --period 60 \
  --statistics Sum

# Check deployment timeline
git log --oneline --since="1 hour ago"
```

**2. Execute Rollback**
```bash
# Revert load balancer to previous version (Green environment)
aws elbv2 modify-listener --listener-arn <listener-arn> \
  --default-actions Type=forward,TargetGroupArn=<green-tg-arn>,Weight=100

# Alternatively, use GitHub Actions workflow
# Navigate to: Actions > Production Deployment > Run workflow
# Select "Rollback to previous version"
```

**3. Verify Rollback**
```bash
# Check service version
curl https://api.aifilmstudio.com/version

# Verify health
curl https://api.aifilmstudio.com/health

# Monitor metrics
aws cloudwatch get-metric-statistics --metric-name HTTPCode_Target_5XX_Count ...
```

**4. Database Rollback (if needed)**
```bash
# WARNING: Only if database migration caused issues
# This is rare and should be carefully considered

# Connect to RDS
aws rds describe-db-instances --db-instance-identifier prod-db

# Restore from backup (if necessary)
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier prod-db-restored \
  --db-snapshot-identifier prod-db-snapshot-2025-12-27

# Run reverse migration
cd /path/to/backend
alembic downgrade -1  # Rollback one migration
```

**5. Post-Rollback Actions**
- Update status page
- Notify team in Slack #engineering
- Create incident report
- Schedule post-mortem meeting
- Document root cause

---

## Scaling Operations

### Manual Scaling

#### Scale Backend Services

**Scale Up (Increase Capacity)**
```bash
# Update ECS service desired count
aws ecs update-service \
  --cluster prod-cluster \
  --service backend-service \
  --desired-count 8

# Monitor scaling progress
aws ecs describe-services --cluster prod-cluster --services backend-service

# Verify new tasks are healthy
aws ecs list-tasks --cluster prod-cluster --service-name backend-service
```

**Scale Down (Reduce Capacity)**
```bash
# Reduce desired count
aws ecs update-service \
  --cluster prod-cluster \
  --service backend-service \
  --desired-count 3

# Monitor graceful shutdown
aws logs tail /aws/ecs/prod/backend --follow --since 5m
```

#### Scale GPU Workers

**Scale Up GPU Instances**
```bash
# Update Auto Scaling Group
aws autoscaling set-desired-capacity \
  --auto-scaling-group-name prod-gpu-workers \
  --desired-capacity 5

# Monitor instance launch
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=gpu-worker" \
  --query 'Reservations[*].Instances[*].[InstanceId,State.Name,LaunchTime]'

# Verify workers are processing jobs
aws sqs get-queue-attributes \
  --queue-url https://sqs.us-east-1.amazonaws.com/xxx/prod-jobs \
  --attribute-names ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible
```

#### Scale Database

**Vertical Scaling (Increase Instance Size)**
```bash
# Modify RDS instance class
aws rds modify-db-instance \
  --db-instance-identifier prod-db \
  --db-instance-class db.r6g.2xlarge \
  --apply-immediately

# WARNING: This causes brief downtime (1-2 minutes)
# Schedule during maintenance window if possible

# Monitor modification progress
aws rds describe-db-instances --db-instance-identifier prod-db
```

**Read Replica Scaling**
```bash
# Add read replica
aws rds create-db-instance-read-replica \
  --db-instance-identifier prod-db-read-replica-3 \
  --source-db-instance-identifier prod-db \
  --db-instance-class db.r6g.large \
  --availability-zone us-east-1c

# Update application to use read replicas
# (Requires code deployment)
```

### Auto-Scaling Configuration

#### Verify Auto-Scaling Policies

**Backend ECS Service**
```bash
# Check current auto-scaling policies
aws application-autoscaling describe-scaling-policies \
  --service-namespace ecs \
  --resource-id service/prod-cluster/backend-service

# Check target tracking
aws application-autoscaling describe-scalable-targets \
  --service-namespace ecs \
  --resource-ids service/prod-cluster/backend-service
```

**GPU Workers Auto Scaling Group**
```bash
# Check ASG configuration
aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names prod-gpu-workers

# Check scaling policies
aws autoscaling describe-policies \
  --auto-scaling-group-name prod-gpu-workers
```

---

## Database Operations

### Daily Database Maintenance

**Check Database Performance**
```bash
# Connect to database (read-only for checks)
psql -h prod-db.xxxxx.us-east-1.rds.amazonaws.com -U admin -d aifilmstudio

# Check active connections
SELECT count(*) as connections, state 
FROM pg_stat_activity 
GROUP BY state;

# Check slow queries
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

# Check database size
SELECT pg_size_pretty(pg_database_size('aifilmstudio'));

# Check table sizes
SELECT schemaname, tablename, 
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC 
LIMIT 10;
```

### Database Backup and Restore

**Manual Backup**
```bash
# Create manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier prod-db \
  --db-snapshot-identifier prod-db-manual-$(date +%Y%m%d-%H%M%S)

# Verify snapshot
aws rds describe-db-snapshots \
  --db-instance-identifier prod-db \
  --snapshot-type manual
```

**Restore from Backup**
```bash
# List available snapshots
aws rds describe-db-snapshots \
  --db-instance-identifier prod-db

# Restore to new instance (safer than in-place restore)
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier prod-db-restored \
  --db-snapshot-identifier prod-db-snapshot-2025-12-27

# After verification, can update application config or promote restored instance
```

### Database Migration

**Apply Migration**
```bash
# Run migrations using Alembic (from backend container)
cd /path/to/backend
source venv/bin/activate

# Check current migration version
alembic current

# Run pending migrations
alembic upgrade head

# Verify migration
alembic current
psql -h prod-db.xxx.rds.amazonaws.com -U admin -d aifilmstudio -c "\d"
```

**Rollback Migration**
```bash
# Downgrade one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>

# Check status
alembic current
```

---

## Monitoring and Alerting

### CloudWatch Dashboards

**Access Dashboards**
1. Navigate to AWS Console > CloudWatch > Dashboards
2. Select "AI-Film-Studio-Production" dashboard

**Key Widgets**:
- API Response Time (p50, p95, p99)
- Error Rate (4xx, 5xx)
- ECS Service CPU/Memory
- RDS Connections and CPU
- SQS Queue Depth
- Film Generation Success Rate

### Alert Response

**P1 - Critical Alert Response**

**Example: Service Down**
```bash
# 1. Acknowledge alert in PagerDuty (within 5 minutes)

# 2. Check service status
aws ecs describe-services --cluster prod-cluster --services backend-service

# 3. Check recent deployments
git log --oneline --since="2 hours ago"

# 4. Review error logs
aws logs tail /aws/ecs/prod/backend --follow --since 30m | grep ERROR

# 5. Check health endpoint
curl https://api.aifilmstudio.com/health

# 6. Execute recovery action (rollback or restart)
# See Rollback Procedures section

# 7. Update status page
# Navigate to status page admin

# 8. Communicate in #ops-alerts Slack channel
```

**Example: High Error Rate**
```bash
# 1. Identify error pattern
aws logs filter-pattern "[error] OR [ERROR] OR [exception]" \
  --log-group-name /aws/ecs/prod/backend \
  --start-time <timestamp>

# 2. Check recent changes
git log --oneline --since="1 hour ago"

# 3. Check specific error endpoint
curl -v https://api.aifilmstudio.com/api/v1/problematic-endpoint

# 4. Review CloudWatch metrics for affected service

# 5. Decide: rollback, hotfix, or scale

# 6. Execute chosen action
```

### Custom Metrics

**Publish Custom Metrics**
```bash
# From application or CLI
aws cloudwatch put-metric-data \
  --namespace AIFilmStudio/Production \
  --metric-name FilmsGenerated \
  --value 42 \
  --timestamp $(date -u +"%Y-%m-%dT%H:%M:%S")

# Query custom metrics
aws cloudwatch get-metric-statistics \
  --namespace AIFilmStudio/Production \
  --metric-name FilmsGenerated \
  --start-time 2025-12-27T00:00:00Z \
  --end-time 2025-12-27T23:59:59Z \
  --period 3600 \
  --statistics Sum
```

---

## Security Operations

### Security Incident Response

**Suspected Security Breach**

**1. Immediate Actions (0-15 minutes)**
```bash
# Isolate affected resources
# Update security group to block all inbound traffic
aws ec2 modify-security-group-rules \
  --group-id sg-xxxxx \
  --security-group-rules IpPermissions=[...]

# Terminate suspicious EC2 instances
aws ec2 terminate-instances --instance-ids i-xxxxx

# Disable compromised IAM credentials
aws iam update-access-key \
  --access-key-id AKIA... \
  --status Inactive \
  --user-name suspicious-user

# Change database passwords (if compromised)
aws rds modify-db-instance \
  --db-instance-identifier prod-db \
  --master-user-password <new-strong-password> \
  --apply-immediately
```

**2. Investigation (15-60 minutes)**
```bash
# Review CloudTrail logs
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRole \
  --start-time <timestamp>

# Check for unauthorized access
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=GetObject \
  --max-results 100

# Review GuardDuty findings
aws guardduty list-findings --detector-id <detector-id>

# Check access logs
aws s3 cp s3://prod-logs-bucket/cloudfront/ . --recursive
grep "404\|403\|500" *.gz | less
```

**3. Remediation**
- Rotate all secrets and credentials
- Apply security patches
- Update security groups
- Enable additional monitoring
- Document incident

**4. Post-Incident**
- Conduct security review
- Update security policies
- Implement preventive measures
- Notify affected users (if required by law)

### Certificate Renewal

**Check Certificate Expiration**
```bash
# List ACM certificates
aws acm list-certificates

# Get certificate details
aws acm describe-certificate --certificate-arn <cert-arn>

# Certificates should auto-renew via ACM
# If manual renewal needed, create new certificate and update listeners
```

---

## Backup and Recovery

### Verify Backup Status

**Database Backups**
```bash
# List automated backups
aws rds describe-db-snapshots \
  --db-instance-identifier prod-db \
  --snapshot-type automated

# Verify latest backup timestamp
# Should be within last 24 hours
```

**S3 Cross-Region Replication**
```bash
# Check replication status
aws s3api get-bucket-replication \
  --bucket ai-film-studio-media-prod

# Verify objects in DR bucket
aws s3 ls s3://ai-film-studio-media-dr-usw2/ --recursive | wc -l
```

### Test Restore Procedure

**Quarterly DR Test**
```bash
# 1. Restore database to test instance
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier test-restore \
  --db-snapshot-identifier <latest-snapshot>

# 2. Verify data integrity
psql -h test-restore.xxx.rds.amazonaws.com -U admin -d aifilmstudio
# Run validation queries

# 3. Test application connectivity
# Update test environment to use restored database

# 4. Document results

# 5. Clean up test resources
aws rds delete-db-instance \
  --db-instance-identifier test-restore \
  --skip-final-snapshot
```

---

## Troubleshooting Guide

### Common Issues

#### Issue: High API Response Time

**Symptoms**:
- p95 response time >500ms
- Users reporting slow performance
- CloudWatch alerts triggered

**Investigation**:
```bash
# 1. Check database query performance
psql -h prod-db.xxx.rds.amazonaws.com -U admin -d aifilmstudio
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;

# 2. Check ECS task CPU/Memory
aws ecs describe-services --cluster prod-cluster --services backend-service

# 3. Check Redis cache hit rate
aws elasticache describe-cache-clusters --cache-cluster-id prod-cache

# 4. Review application logs
aws logs tail /aws/ecs/prod/backend --follow | grep "slow query"
```

**Resolution**:
- Scale up ECS service if CPU >70%
- Optimize slow database queries
- Add database indexes
- Increase cache TTL
- Add read replicas

#### Issue: Film Generation Failures

**Symptoms**:
- Jobs stuck in "processing" state
- High failure rate (>5%)
- SQS DLQ messages increasing

**Investigation**:
```bash
# 1. Check SQS queue depth
aws sqs get-queue-attributes \
  --queue-url https://sqs.us-east-1.amazonaws.com/xxx/prod-jobs \
  --attribute-names All

# 2. Check GPU worker logs
aws logs tail /aws/ec2/gpu-worker --follow --since 30m

# 3. Check worker instance status
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=gpu-worker" \
  --query 'Reservations[*].Instances[*].[InstanceId,State.Name]'

# 4. Check DLQ messages
aws sqs receive-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/xxx/prod-jobs-dlq \
  --max-number-of-messages 10
```

**Resolution**:
- Scale up GPU workers if queue depth >50
- Restart stuck workers
- Investigate error messages in logs
- Requeue failed jobs
- Check GPU resource availability

#### Issue: S3 Access Denied Errors

**Investigation**:
```bash
# 1. Check IAM role permissions
aws iam get-role --role-name ecs-task-role
aws iam list-attached-role-policies --role-name ecs-task-role

# 2. Check bucket policy
aws s3api get-bucket-policy --bucket ai-film-studio-media-prod

# 3. Test access from ECS task
aws ecs execute-command \
  --cluster prod-cluster \
  --task <task-id> \
  --interactive \
  --command "/bin/bash"

# Inside container:
aws s3 ls s3://ai-film-studio-media-prod/
```

**Resolution**:
- Update IAM role permissions
- Fix bucket policy
- Verify CORS configuration
- Check for bucket versioning issues

---

## Emergency Contacts

### Escalation Path

**Level 1**: On-call engineer (PagerDuty)  
**Level 2**: Engineering lead (if no response in 15 min)  
**Level 3**: CTO (if no response in 30 min)  

### External Support

**AWS Enterprise Support**: Available 24/7  
**Phone**: 1-800-XXX-XXXX  
**Critical Issue Response**: 15 minutes

---

## Appendix: Command Reference

### Useful AWS CLI Commands

```bash
# ECS
aws ecs list-clusters
aws ecs list-services --cluster <cluster-name>
aws ecs describe-services --cluster <cluster> --services <service>
aws ecs list-tasks --cluster <cluster> --service-name <service>
aws ecs describe-tasks --cluster <cluster> --tasks <task-id>

# RDS
aws rds describe-db-instances
aws rds describe-db-snapshots
aws rds create-db-snapshot
aws rds restore-db-instance-from-db-snapshot

# S3
aws s3 ls s3://bucket-name/
aws s3 sync s3://source/ s3://destination/
aws s3api get-bucket-versioning --bucket <bucket>

# CloudWatch
aws logs tail <log-group> --follow
aws logs filter-pattern <pattern> --log-group-name <group>
aws cloudwatch get-metric-statistics --namespace <ns> --metric-name <metric>

# Auto Scaling
aws autoscaling describe-auto-scaling-groups
aws autoscaling set-desired-capacity --auto-scaling-group-name <name> --desired-capacity <num>

# Load Balancer
aws elbv2 describe-load-balancers
aws elbv2 describe-target-groups
aws elbv2 describe-target-health --target-group-arn <arn>
```

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-27  
**Next Review**: 2026-03-27
