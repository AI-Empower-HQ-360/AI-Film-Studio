# Cloud Infrastructure

Terraform & cloud setup for AI Film Studio.

## Directory Structure

- `terraform/` - Infrastructure as Code (IaC) scripts (EC2, ECS, S3, RDS, etc.)
- `k8s/` - Kubernetes manifests
- `monitoring/` - CloudWatch / Prometheus / Grafana configs

## Getting Started

```bash
cd terraform/environments/dev
terraform init
terraform plan
terraform apply
```
