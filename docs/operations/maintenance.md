# Maintenance Procedures

**Version**: 1.0  
**Last Updated**: 2025-12-27  
**Owner**: DevOps Team

---

## Table of Contents

1. [Scheduled Maintenance Windows](#scheduled-maintenance-windows)
2. [Database Maintenance](#database-maintenance)
3. [Infrastructure Updates](#infrastructure-updates)
4. [Security Updates](#security-updates)
5. [Certificate Management](#certificate-management)
6. [Backup Validation](#backup-validation)
7. [Capacity Planning](#capacity-planning)

---

## Scheduled Maintenance Windows

### Regular Maintenance Schedule

**Frequency**: Bi-weekly (2nd and 4th Sunday of each month)  
**Time**: 2:00 AM - 6:00 AM UTC (off-peak hours)  
**Duration**: Maximum 4 hours  
**Notification**: 7 days advance notice to users

### Pre-Maintenance Checklist

**7 Days Before**:
- [ ] Schedule maintenance window in calendar
- [ ] Notify users via email and status page
- [ ] Post notification in Slack #engineering
- [ ] Prepare maintenance tasks list
- [ ] Review and approve change requests
- [ ] Prepare rollback procedures

**24 Hours Before**:
- [ ] Create database backup
- [ ] Verify backup integrity
- [ ] Test rollback procedures in staging
- [ ] Brief on-call team
- [ ] Prepare status page updates
- [ ] Verify all required access and credentials

**1 Hour Before**:
- [ ] Post status page update: "Scheduled Maintenance Starting Soon"
- [ ] Join maintenance bridge/call
- [ ] Final verification of team readiness
- [ ] Snapshot current system state

### During Maintenance

**Communication**:
- Update status page every 30 minutes
- Post progress in Slack #ops-alerts
- Notify if extended time needed

**Execution**:
- Follow documented procedures
- Verify each step before proceeding
- Document any deviations from plan
- Capture logs and screenshots

### Post-Maintenance Checklist

- [ ] Verify all services healthy
- [ ] Run smoke tests
- [ ] Check monitoring dashboards (30 minutes)
- [ ] Update status page: "Maintenance Complete"
- [ ] Send completion email to stakeholders
- [ ] Document lessons learned
- [ ] Update maintenance runbook if needed

---

## Database Maintenance

### Weekly Database Tasks

#### Analyze and Vacuum (Every Sunday 3 AM UTC)

**Automated Script**:
```bash
#!/bin/bash
# Run as cron job: 0 3 * * 0 /path/to/db_maintenance.sh

export PGPASSWORD="<password>"
DBHOST="prod-db.xxxxx.us-east-1.rds.amazonaws.com"
DBNAME="aifilmstudio"
DBUSER="admin"

# Analyze tables
psql -h $DBHOST -U $DBUSER -d $DBNAME -c "ANALYZE VERBOSE;"

# Vacuum (analyze done automatically)
psql -h $DBHOST -U $DBUSER -d $DBNAME -c "VACUUM ANALYZE VERBOSE;"

# Update statistics
psql -h $DBHOST -U $DBUSER -d $DBNAME -c "
SELECT schemaname, tablename, n_live_tup, n_dead_tup, last_vacuum, last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;
"
```

**Manual Execution** (if script fails):
```sql
-- Connect to database
\connect aifilmstudio

-- Analyze all tables
ANALYZE VERBOSE;

-- Vacuum all tables
VACUUM ANALYZE VERBOSE;

-- Check table bloat
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
  n_dead_tup
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

---

### Monthly Database Tasks

#### Reindex Tables (First Sunday of Month)

**Purpose**: Improve query performance, reduce index bloat

```sql
-- Connect to database
\connect aifilmstudio

-- Reindex large tables (do during maintenance window)
REINDEX TABLE users;
REINDEX TABLE projects;
REINDEX TABLE jobs;
REINDEX TABLE assets;

-- Check index sizes
SELECT
  schemaname,
  tablename,
  indexname,
  pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Automated Approach** (PostgreSQL 12+):
```sql
-- Reindex concurrently (no downtime)
REINDEX INDEX CONCURRENTLY idx_users_email;
REINDEX INDEX CONCURRENTLY idx_projects_user_id;
```

---

#### Update Table Statistics

**Check Statistics Currency**:
```sql
SELECT
  schemaname,
  tablename,
  last_analyze,
  last_autoanalyze,
  n_mod_since_analyze
FROM pg_stat_user_tables
WHERE n_mod_since_analyze > 1000
ORDER BY n_mod_since_analyze DESC;
```

**Force Statistics Update**:
```sql
ANALYZE VERBOSE users;
ANALYZE VERBOSE projects;
ANALYZE VERBOSE jobs;
```

---

### Quarterly Database Tasks

#### Database Parameter Tuning

**Review Configuration**:
```sql
-- Check current settings
SHOW ALL;

-- Key parameters to review
SHOW shared_buffers;
SHOW effective_cache_size;
SHOW work_mem;
SHOW maintenance_work_mem;
SHOW max_connections;
```

**Recommended Settings for Production** (db.r6g.xlarge):
```
shared_buffers = 8GB
effective_cache_size = 24GB
work_mem = 50MB
maintenance_work_mem = 2GB
max_connections = 200
random_page_cost = 1.1 (SSD)
```

**Update Parameters**:
```bash
# Via AWS CLI
aws rds modify-db-parameter-group \
  --db-parameter-group-name prod-params \
  --parameters "ParameterName=shared_buffers,ParameterValue=8GB,ApplyMethod=pending-reboot"

# Requires instance reboot (schedule during maintenance window)
aws rds reboot-db-instance --db-instance-identifier prod-db
```

---

#### Disk Space Cleanup

**Identify Large Objects**:
```sql
-- Find largest tables
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
  pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
  pg_size_pretty(pg_indexes_size(schemaname||'.'||tablename)) as indexes_size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 20;

-- Find old data to archive/delete
SELECT 
  DATE(created_at) as date,
  COUNT(*) as count
FROM jobs
WHERE created_at < NOW() - INTERVAL '90 days'
  AND status = 'completed'
GROUP BY DATE(created_at)
ORDER BY date;
```

**Archive Old Data**:
```sql
-- Archive completed jobs older than 90 days to S3
-- (Use data export or custom script)

-- After archiving, delete old records
DELETE FROM jobs
WHERE created_at < NOW() - INTERVAL '90 days'
  AND status = 'completed'
  AND id IN (
    -- Select batch to avoid lock escalation
    SELECT id FROM jobs
    WHERE created_at < NOW() - INTERVAL '90 days'
      AND status = 'completed'
    LIMIT 1000
  );

-- Run VACUUM after large deletes
VACUUM ANALYZE VERBOSE jobs;
```

---

## Infrastructure Updates

### Operating System Patches

#### EC2 Instances (GPU Workers)

**Automated Patching with AWS Systems Manager**:
```bash
# Create patch baseline
aws ssm create-patch-baseline \
  --name "AI-Film-Studio-Baseline" \
  --operating-system "AMAZON_LINUX_2" \
  --approval-rules "PatchRules=[{PatchFilterGroup={PatchFilters=[{Key=CLASSIFICATION,Values=Security},{Key=SEVERITY,Values=Critical,Important}]},ApproveAfterDays=7}]"

# Create maintenance window
aws ssm create-maintenance-window \
  --name "AI-Film-Studio-Patching" \
  --schedule "cron(0 4 ? * SUN *)" \
  --duration 4 \
  --cutoff 1
```

**Manual Patching**:
```bash
# SSH into GPU worker instance
ssh ec2-user@<gpu-worker-ip>

# Update system packages
sudo yum update -y

# Reboot if kernel updated
sudo reboot

# Verify instance returns healthy
# Check CloudWatch metrics and logs
```

---

### Container Image Updates

#### Update Base Images

**Review for Security Vulnerabilities**:
```bash
# Scan Docker images
docker scan aifilmstudio/backend:latest
docker scan aifilmstudio/worker:latest

# Use Trivy for comprehensive scan
trivy image aifilmstudio/backend:latest
```

**Rebuild with Updated Base Images**:
```bash
# Update Dockerfile base image
# FROM python:3.11-slim → FROM python:3.11.8-slim

# Rebuild images
docker build -t aifilmstudio/backend:v1.2.0 -f backend/Dockerfile .
docker build -t aifilmstudio/worker:v1.2.0 -f worker/Dockerfile .

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/backend:v1.2.0
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/worker:v1.2.0

# Deploy via CI/CD or manual update
aws ecs update-service --cluster prod-cluster --service backend-service --force-new-deployment
```

---

### Terraform Infrastructure Updates

**Update Terraform Modules**:
```bash
# Review current versions
cd infrastructure/terraform/environments/prod
terraform version
terraform providers

# Update provider versions in versions.tf
# terraform {
#   required_version = ">= 1.6.0"
#   required_providers {
#     aws = {
#       source  = "hashicorp/aws"
#       version = "~> 5.0"  # Update to latest
#     }
#   }
# }

# Initialize with upgrade
terraform init -upgrade

# Review changes
terraform plan

# Apply during maintenance window
terraform apply
```

---

## Security Updates

### Dependency Updates

#### Backend Dependencies (Python)

**Check for Vulnerabilities**:
```bash
cd backend

# Check for outdated packages
pip list --outdated

# Security audit with Safety
safety check --json

# Update requirements
pip install --upgrade <package>
pip freeze > requirements.txt
```

**Automated Dependency Scanning**:
- Enable Dependabot in GitHub
- Configure Snyk integration
- Review security alerts weekly

---

#### Frontend Dependencies (Node.js)

**Check for Vulnerabilities**:
```bash
cd frontend

# NPM audit
npm audit

# Update packages
npm update
npm audit fix

# For major updates
npm install <package>@latest

# Commit updated package.json and package-lock.json
```

---

### SSL/TLS Certificate Updates

**Check Certificate Expiration**:
```bash
# List ACM certificates
aws acm list-certificates --region us-east-1

# Get certificate details
aws acm describe-certificate \
  --certificate-arn arn:aws:acm:us-east-1:xxx:certificate/xxx
```

**ACM Certificates Auto-Renew**, but verify:
- Certificate is in "ISSUED" status
- Domain validation is successful
- Certificate is attached to load balancer

**Manual Certificate Renewal** (if needed):
1. Request new certificate in ACM
2. Complete domain validation (DNS or email)
3. Update load balancer listener
4. Verify new certificate is active
5. Delete old certificate after 30 days

---

### Secrets Rotation

**Rotate Database Credentials** (Quarterly):
```bash
# Update database password
aws rds modify-db-instance \
  --db-instance-identifier prod-db \
  --master-user-password <new-strong-password> \
  --apply-immediately

# Update in Secrets Manager
aws secretsmanager update-secret \
  --secret-id ai-film-studio/prod/database-url \
  --secret-string "postgresql://admin:<new-password>@prod-db.xxx.rds.amazonaws.com/aifilmstudio"

# Restart services to pick up new secret
aws ecs update-service --cluster prod-cluster --service backend-service --force-new-deployment

# Verify connectivity
# Check application logs for database connection success
```

**Rotate API Keys** (As needed):
- OpenAI API key
- Stripe API key
- Third-party service keys

---

## Certificate Management

### CloudFront SSL Certificate

**Managed by ACM** (Auto-renewal enabled)

**Verification**:
```bash
# Check certificate status
aws acm describe-certificate --certificate-arn <arn> --region us-east-1

# Verify CloudFront distribution using correct certificate
aws cloudfront get-distribution --id <distribution-id>
```

---

### Application Load Balancer Certificate

**Verification**:
```bash
# Check listener certificates
aws elbv2 describe-listeners --load-balancer-arn <alb-arn>

# Verify certificate validity
aws elbv2 describe-listener-certificates --listener-arn <listener-arn>
```

---

## Backup Validation

### Monthly Backup Testing

**Test Database Restore** (First Saturday of month):
```bash
# Restore to test instance
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier test-restore-$(date +%Y%m) \
  --db-snapshot-identifier prod-db-automated-backup-latest

# Wait for restore to complete
aws rds wait db-instance-available --db-instance-identifier test-restore-$(date +%Y%m)

# Connect and verify data
psql -h test-restore-202601.xxx.rds.amazonaws.com -U admin -d aifilmstudio

# Run validation queries
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM projects;
SELECT MAX(created_at) FROM jobs;

# Document results in maintenance log

# Clean up test instance
aws rds delete-db-instance \
  --db-instance-identifier test-restore-$(date +%Y%m) \
  --skip-final-snapshot
```

---

### S3 Data Integrity Check

**Verify Cross-Region Replication**:
```bash
# Compare object counts
aws s3 ls s3://ai-film-studio-media-prod/ --recursive | wc -l
aws s3 ls s3://ai-film-studio-media-dr-usw2/ --recursive | wc -l

# Check replication status
aws s3api head-object \
  --bucket ai-film-studio-media-prod \
  --key <sample-key> \
  --query 'ReplicationStatus'

# Random sample validation
aws s3api get-object-metadata \
  --bucket ai-film-studio-media-prod \
  --key <random-key>

aws s3api get-object-metadata \
  --bucket ai-film-studio-media-dr-usw2 \
  --key <random-key>
```

---

## Capacity Planning

### Monthly Capacity Review

**Metrics to Review**:
- CPU utilization trend (ECS, RDS, EC2)
- Memory utilization trend
- Storage growth rate
- Network bandwidth usage
- Database connections usage
- Queue depth patterns

**Forecasting**:
```python
# Simple linear projection
current_users = 5000
monthly_growth_rate = 0.15  # 15% month-over-month
months_ahead = 6

projected_users = current_users * (1 + monthly_growth_rate) ** months_ahead
print(f"Projected users in 6 months: {projected_users:.0f}")

# Storage projection
current_storage_gb = 500
avg_storage_per_user_gb = 0.1
projected_storage = projected_users * avg_storage_per_user_gb
print(f"Projected storage needed: {projected_storage:.0f} GB")
```

**Action Items**:
- Order reserved instances if sustained growth
- Plan database upgrade if CPU consistently >60%
- Increase storage if projected to hit 80% in 3 months
- Review auto-scaling policies if frequent scaling events

---

### Quarterly Capacity Planning

**Deep Analysis**:
- Historical growth trends (6-12 months)
- Seasonal patterns
- Cost optimization opportunities
- Architecture scalability review

**Report Sections**:
1. Current resource utilization
2. Growth projections (3, 6, 12 months)
3. Bottleneck identification
4. Recommended capacity changes
5. Budget impact analysis

---

## Maintenance Log Template

```markdown
# Maintenance Log - [Date]

**Type**: Scheduled / Emergency  
**Duration**: [Start] - [End] UTC  
**Performed By**: [Name/Team]

## Tasks Completed
- [ ] Database maintenance (vacuum, analyze)
- [ ] Security patches applied
- [ ] Certificate verification
- [ ] Backup validation
- [ ] Capacity review

## Issues Encountered
- [None / List issues]

## Metrics Before/After
- API p95 response time: [Before] → [After]
- Database CPU: [Before] → [After]
- Storage usage: [Before] → [After]

## Next Maintenance
- Scheduled: [Date]
- Special tasks: [List any]
```

---

## Contact Information

**Maintenance Questions**: #devops-support on Slack  
**Maintenance Schedule**: Google Calendar "AI Film Studio Operations"  
**Emergency Maintenance**: On-call engineer via PagerDuty

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-27  
**Next Review**: 2026-03-27
