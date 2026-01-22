# Monitoring Guide

**Version**: 1.0  
**Last Updated**: 2025-12-27  
**Owner**: DevOps Team

---

## Overview

This guide provides comprehensive information on monitoring the AI Film Studio platform, including dashboards, key metrics, alerting configuration, and troubleshooting procedures.

---

## CloudWatch Dashboards

### Production Dashboard

**Access**: AWS Console > CloudWatch > Dashboards > `AIFilmStudio-Production`

**Sections**:
1. API Performance
2. Film Generation Pipeline
3. Infrastructure Health
4. Database Performance
5. Business Metrics

---

### Dashboard Widgets

#### API Performance Section

**Response Time (Line Graph)**
- **Metrics**: p50, p95, p99 response time
- **Target**: p95 < 200ms
- **Alert Threshold**: p95 > 500ms for 5 minutes

**Error Rate (Stacked Area)**
- **Metrics**: 4xx errors, 5xx errors
- **Target**: < 1% total error rate
- **Alert Threshold**: > 5% for 5 minutes

**Request Rate (Line Graph)**
- **Metrics**: Requests per minute
- **Typical Range**: 100-500 rpm (normal), 1000+ rpm (peak)

**Top Endpoints by Traffic (Bar Chart)**
- Shows most-used API endpoints
- Helps identify usage patterns

#### Film Generation Section

**Queue Depth (Line Graph)**
- **Metric**: SQS ApproximateNumberOfMessages
- **Target**: < 50 messages
- **Alert Threshold**: > 100 messages for 10 minutes

**Generation Success Rate (Number)**
- **Metric**: Successful / Total generations
- **Target**: > 95%
- **Alert Threshold**: < 90% for 15 minutes

**Average Generation Time (Line Graph)**
- **Metric**: Time from job start to completion
- **Target**: < 5 minutes
- **Alert Threshold**: > 8 minutes for 10 minutes

**Active GPU Workers (Number)**
- **Metric**: Count of running GPU instances
- **Typical Range**: 1-5 (normal), 10-20 (peak)

#### Infrastructure Section

**ECS Service Health (Multi-stat)**
- **Metrics**: Running tasks, desired tasks, pending tasks
- **Alert**: Running < Desired for 5 minutes

**CPU Utilization (Line Graph)**
- **Metrics**: Backend CPU, Worker CPU
- **Target**: < 70% average
- **Alert Threshold**: > 85% for 10 minutes

**Memory Utilization (Line Graph)**
- **Metrics**: Backend memory, Worker memory
- **Target**: < 80% average
- **Alert Threshold**: > 90% for 5 minutes

**Load Balancer Health (Number)**
- **Metrics**: Healthy targets, unhealthy targets
- **Alert**: Unhealthy > 0

#### Database Section

**Database CPU (Line Graph)**
- **Metric**: RDS CPUUtilization
- **Target**: < 70% average
- **Alert Threshold**: > 85% for 10 minutes

**Database Connections (Line Graph)**
- **Metric**: DatabaseConnections
- **Target**: < 80% of max
- **Alert Threshold**: > 90% of max for 5 minutes

**Read/Write Latency (Line Graph)**
- **Metrics**: ReadLatency, WriteLatency
- **Target**: < 10ms
- **Alert Threshold**: > 50ms for 5 minutes

**Slow Queries (Log Insights Widget)**
- Queries taking > 1 second
- Refresh every 5 minutes

#### Business Metrics

**Active Users (Number)**
- **Metric**: Concurrent active sessions
- **Tracked via**: Redis session count

**Films Generated Today (Number)**
- **Metric**: Successful film generations count
- **Typical Range**: 1000-5000 per day

**Conversion Funnel (Bar Chart)**
- Signups → Activated → Generated Film → Paid
- Helps track user journey

**Revenue (Number)**
- **Metric**: Daily revenue (if integrated)
- **Source**: Stripe webhooks

---

## Key Metrics Reference

### Application Metrics

| Metric | Type | Target | Critical Threshold |
|--------|------|--------|-------------------|
| API Response Time (p95) | Latency | < 200ms | > 500ms |
| API Error Rate | Percentage | < 1% | > 5% |
| Film Generation Success | Percentage | > 95% | < 85% |
| Film Generation Time | Duration | < 5 min | > 10 min |
| Queue Depth | Count | < 50 | > 200 |

### Infrastructure Metrics

| Metric | Type | Target | Critical Threshold |
|--------|------|--------|-------------------|
| Backend CPU | Percentage | < 70% | > 85% |
| Backend Memory | Percentage | < 80% | > 90% |
| Worker CPU | Percentage | < 75% | > 90% |
| Worker Memory | Percentage | < 80% | > 90% |
| Disk Space | Percentage | > 30% free | < 10% free |

### Database Metrics

| Metric | Type | Target | Critical Threshold |
|--------|------|--------|-------------------|
| RDS CPU | Percentage | < 70% | > 85% |
| DB Connections | Count | < 80 | > 95 |
| Read Latency | Milliseconds | < 10ms | > 50ms |
| Write Latency | Milliseconds | < 20ms | > 100ms |
| Storage Space | Percentage | > 20% free | < 10% free |

---

## Alerting Configuration

### Alert Routing

**Critical Alerts (P1)** → PagerDuty + Slack #ops-alerts + SMS  
**High Priority (P2)** → PagerDuty + Slack #ops-alerts  
**Medium (P3)** → Slack #ops-alerts  
**Low (P4)** → Email

---

### Critical Alerts (P1)

#### API Unavailable
```json
{
  "AlarmName": "API-Unavailable-Prod",
  "MetricName": "HealthyHostCount",
  "Namespace": "AWS/ApplicationELB",
  "Threshold": 0,
  "ComparisonOperator": "LessThanOrEqualToThreshold",
  "EvaluationPeriods": 2,
  "Period": 60,
  "Statistic": "Average"
}
```

#### Database Connection Failure
```json
{
  "AlarmName": "Database-Connection-Failure",
  "MetricName": "DatabaseConnections",
  "Namespace": "AWS/RDS",
  "Threshold": 0,
  "ComparisonOperator": "LessThanOrEqualToThreshold",
  "EvaluationPeriods": 2,
  "Period": 60
}
```

#### High Error Rate
```json
{
  "AlarmName": "API-High-Error-Rate",
  "MetricName": "HTTPCode_Target_5XX_Count",
  "Namespace": "AWS/ApplicationELB",
  "Threshold": 100,
  "ComparisonOperator": "GreaterThanThreshold",
  "EvaluationPeriods": 5,
  "Period": 60,
  "Statistic": "Sum"
}
```

---

### High Priority Alerts (P2)

#### Elevated Response Time
```json
{
  "AlarmName": "API-Slow-Response",
  "MetricName": "TargetResponseTime",
  "Namespace": "AWS/ApplicationELB",
  "ExtendedStatistic": "p95",
  "Threshold": 500,
  "ComparisonOperator": "GreaterThanThreshold",
  "EvaluationPeriods": 5,
  "Period": 60
}
```

#### Queue Backing Up
```json
{
  "AlarmName": "SQS-Queue-Backing-Up",
  "MetricName": "ApproximateNumberOfMessagesVisible",
  "Namespace": "AWS/SQS",
  "Threshold": 100,
  "ComparisonOperator": "GreaterThanThreshold",
  "EvaluationPeriods": 2,
  "Period": 300
}
```

#### High CPU Utilization
```json
{
  "AlarmName": "Backend-High-CPU",
  "MetricName": "CPUUtilization",
  "Namespace": "AWS/ECS",
  "Threshold": 85,
  "ComparisonOperator": "GreaterThanThreshold",
  "EvaluationPeriods": 3,
  "Period": 300
}
```

---

### Medium Priority Alerts (P3)

#### Database Connections High
- Threshold: > 80% of max connections
- Period: 10 minutes
- Action: Investigate connection leaks

#### SSL Certificate Expiring
- Threshold: 30 days before expiration
- Frequency: Daily check
- Action: Renew certificate

#### Backup Failures
- Threshold: Backup older than 25 hours
- Frequency: Daily check
- Action: Investigate backup process

---

## Log Monitoring

### CloudWatch Logs Insights

#### Find Errors in Last Hour
```sql
fields @timestamp, @message
| filter @message like /ERROR/ or @message like /Exception/
| sort @timestamp desc
| limit 100
```

#### Slow API Requests
```sql
fields @timestamp, @message
| filter @message like /duration/
| parse @message /duration: (?<duration>\d+)ms/
| filter duration > 1000
| sort duration desc
| limit 50
```

#### Failed Film Generations
```sql
fields @timestamp, @message, job_id, error_message
| filter @message like /generation failed/
| stats count() by error_message
```

#### Top Error Messages
```sql
fields @timestamp, @message
| filter @message like /ERROR/
| parse @message /ERROR: (?<error_msg>[^;]+)/
| stats count() by error_msg
| sort count desc
| limit 20
```

---

## Monitoring Best Practices

### Dashboard Usage

**Daily Review** (5 minutes):
- Check all green/red status indicators
- Review overnight alerts
- Verify backup status
- Check cost trends

**Weekly Deep Dive** (30 minutes):
- Analyze performance trends
- Review capacity planning
- Identify optimization opportunities
- Update alerting thresholds if needed

**Monthly Review** (1 hour):
- Comprehensive metrics analysis
- Cost optimization review
- SLO compliance check
- Monitoring coverage gaps

---

### Alert Hygiene

**Tune Alerts**:
- Review alerts monthly for false positives
- Adjust thresholds based on actual patterns
- Remove alerts that don't require action
- Add alerts for new critical metrics

**Alert Fatigue Prevention**:
- Use appropriate evaluation periods
- Implement composite alarms
- Set realistic thresholds
- Group related alerts

**Alert Response**:
- Acknowledge within 5 minutes
- Investigate within response time SLA
- Document resolution
- Update runbooks if new issue

---

## Custom Metrics

### Publishing Custom Metrics

**From Application Code (Python)**:
```python
import boto3

cloudwatch = boto3.client('cloudwatch')

def publish_metric(metric_name, value, unit='Count'):
    cloudwatch.put_metric_data(
        Namespace='AIFilmStudio/Production',
        MetricData=[
            {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': datetime.utcnow()
            }
        ]
    )

# Example usage
publish_metric('FilmGenerated', 1, 'Count')
publish_metric('GenerationDuration', 245, 'Seconds')
```

**From CLI**:
```bash
aws cloudwatch put-metric-data \
  --namespace AIFilmStudio/Production \
  --metric-name FilmsGenerated \
  --value 1 \
  --unit Count
```

### Useful Custom Metrics

- **FilmsGenerated**: Count of successful film generations
- **GenerationDuration**: Time to generate each film
- **UserSignups**: New user registrations
- **SubscriptionConversions**: Free to paid conversions
- **CreditsUsed**: Credit consumption rate
- **CacheHitRatio**: Redis cache effectiveness

---

## Distributed Tracing

### AWS X-Ray Setup

**Enable X-Ray in Application**:
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

app = Flask(__name__)
XRayMiddleware(app, xray_recorder)
```

**Trace Analysis**:
1. Navigate to AWS X-Ray Console
2. Select "Service Map" to visualize dependencies
3. Select "Traces" to view individual request traces
4. Filter by response time, status code, or URL
5. Identify bottlenecks and optimization opportunities

**Common Trace Patterns**:
- Slow database queries
- External API calls taking too long
- High number of database round trips
- Missing cache layers

---

## SLO Tracking

### Service Level Objectives

**API Availability**: 99.9% (43.2 minutes downtime/month)
**API Response Time**: p95 < 200ms
**Film Generation Success**: 95%
**Film Generation Time**: p95 < 5 minutes

### SLO Compliance Queries

**API Availability (Monthly)**:
```sql
fields @timestamp
| filter @message like /health_check/
| stats count() as total, 
        sum(status = 200) as success,
        (success / total) * 100 as uptime_percentage
```

**Response Time Compliance**:
```sql
fields @timestamp, duration
| filter duration is not null
| stats percentile(duration, 95) as p95_duration,
        count() as total_requests
```

### Error Budget

**Monthly Error Budget**: 0.1% (99.9% availability)
- Total requests: 10,000,000
- Allowed errors: 10,000
- Current errors: [Track via dashboard]
- Remaining budget: [Calculate daily]

---

## Synthetic Monitoring

### Uptime Monitoring

**External Service**: Use Pingdom, UptimeRobot, or similar

**Endpoints to Monitor**:
- https://api.aifilmstudio.com/health (every 1 minute)
- https://app.aifilmstudio.com (every 1 minute)
- https://api.aifilmstudio.com/api/v1/auth/login (every 5 minutes)

**Alert Configuration**:
- Alert if down for 2 consecutive checks
- Check from multiple global locations
- Include SSL certificate monitoring

---

### End-to-End Tests

**Critical User Journeys** (Run every 15 minutes):
1. User signup
2. User login
3. Create project
4. Generate film (test account, fast mode)
5. Download film

**Implementation**: Lambda function with Playwright/Selenium

---

## Performance Optimization

### Identifying Bottlenecks

**High Database CPU**:
- Check pg_stat_statements for slow queries
- Add indexes for frequent queries
- Implement query result caching
- Consider read replicas

**High API Response Time**:
- Use X-Ray to identify slow operations
- Implement caching layers
- Optimize N+1 queries
- Add database connection pooling

**High Queue Depth**:
- Scale up GPU workers
- Optimize generation pipeline
- Implement job prioritization
- Add job timeout handling

---

## Troubleshooting with Monitoring

### Scenario: API is Slow

**Investigation Steps**:
1. Check API response time dashboard (which endpoints?)
2. Check database metrics (CPU, connections, latency)
3. Review X-Ray traces for slow requests
4. Check error logs for exceptions
5. Verify cache hit ratio
6. Check external API dependencies

**Common Causes**:
- Database query not optimized
- Cache miss rate high
- External API slow
- Resource exhaustion (CPU/memory)

---

### Scenario: Film Generation Failing

**Investigation Steps**:
1. Check queue depth (growing = workers not processing)
2. Check GPU worker logs for errors
3. Check DLQ for failed job details
4. Verify GPU worker instance health
5. Check S3 permissions for output uploads
6. Review generation success rate trend

**Common Causes**:
- GPU workers crashed
- Model loading failures
- S3 permissions issues
- Insufficient GPU memory
- Worker auto-scaling not keeping up

---

## Appendix: Metric Namespaces

### AWS Standard Namespaces
- `AWS/ApplicationELB` - Load balancer metrics
- `AWS/ECS` - Container service metrics
- `AWS/RDS` - Database metrics
- `AWS/S3` - Storage metrics
- `AWS/SQS` - Queue metrics
- `AWS/EC2` - Virtual machine metrics

### Custom Namespaces
- `AIFilmStudio/Production` - Application metrics
- `AIFilmStudio/Business` - Business KPIs

---

## Contact Information

**Questions about monitoring**: #devops-support on Slack  
**Dashboard access issues**: DevOps team  
**New metric requests**: Submit ticket in Jira  

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-27  
**Next Review**: 2026-03-27
