# Cloud Infrastructure - AI Film Studio

## Overview

This directory contains Infrastructure as Code (IaC) configurations for deploying AI Film Studio on AWS using Terraform and Kubernetes.

## Structure

```
cloud-infra/
├── terraform/          # Terraform configurations
│   ├── environments/   # Environment-specific configs (dev, test, staging, prod)
│   └── modules/        # Reusable Terraform modules
├── k8s/                # Kubernetes manifests
└── monitoring/         # CloudWatch, Prometheus, Grafana configs
```

## Terraform Modules

### Available Modules

1. **VPC Module** - Virtual Private Cloud setup
2. **ECS Module** - ECS cluster and services
3. **RDS Module** - PostgreSQL database
4. **S3 Module** - Object storage buckets
5. **ALB Module** - Application Load Balancer
6. **CloudFront Module** - CDN distribution
7. **ElastiCache Module** - Redis cache

## Environments

### Development
- **Purpose**: Rapid development and testing
- **Cost**: ~$335/month
- **Instances**: Small, single AZ

### Testing/QA
- **Purpose**: Integration testing
- **Infrastructure**: Mirrors production, scaled down

### Staging
- **Purpose**: Pre-production validation
- **Infrastructure**: Production-like

### Production
- **Purpose**: Live traffic
- **Cost**: ~$2,600/month
- **Instances**: Multi-AZ, auto-scaling

## Deployment

### Prerequisites
- AWS Account with appropriate permissions
- Terraform >= 1.5
- AWS CLI configured

### Initialize Terraform

```bash
cd terraform/environments/dev
terraform init
```

### Plan Changes

```bash
terraform plan -out=tfplan
```

### Apply Changes

```bash
terraform apply tfplan
```

## Kubernetes (EKS)

Alternative container orchestration using Kubernetes.

### Deploy to EKS

```bash
# Create EKS cluster
eksctl create cluster -f k8s/cluster.yaml

# Apply manifests
kubectl apply -f k8s/namespaces/
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
```

## Monitoring

### CloudWatch
- Logs aggregation
- Metrics collection
- Alarms and notifications
- Dashboards

### Prometheus (Optional)
- Advanced metrics collection
- Service discovery
- Alert rules

### Grafana (Optional)
- Custom dashboards
- Data visualization
- Multi-source monitoring

## Security

- VPC isolation
- Security groups
- IAM roles with least privilege
- Secrets Manager for credentials
- AWS WAF for web protection
- Encryption at rest and in transit

## Cost Optimization

- Spot instances for GPU workers (70% savings)
- Reserved instances for stable workloads
- S3 Intelligent-Tiering
- Auto-scaling based on demand
- CloudFront caching

## License

MIT License - see [LICENSE](../LICENSE)
