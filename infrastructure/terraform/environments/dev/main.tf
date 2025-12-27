# AI Film Studio - Development Environment
# Terraform Configuration

terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Backend configuration for state management
  backend "s3" {
    bucket         = "ai-film-studio-terraform-state"
    key            = "dev/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "ai-film-studio-terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = "dev"
      Project     = "ai-film-studio"
      ManagedBy   = "terraform"
      Owner       = "AI-Empower-HQ-360"
    }
  }
}

# Local variables
locals {
  environment = "dev"
  project_name = "ai-film-studio"
  common_tags = {
    Environment = local.environment
    Project     = local.project_name
  }
}

# VPC Module
module "vpc" {
  source = "../../modules/vpc"

  environment  = local.environment
  project_name = local.project_name
  vpc_cidr     = var.vpc_cidr
  azs          = var.availability_zones
  
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  worker_subnet_cidrs  = var.worker_subnet_cidrs
  database_subnet_cidrs = var.database_subnet_cidrs
  
  enable_nat_gateway = true
  single_nat_gateway = true  # Cost optimization for dev
  enable_dns_hostnames = true
  enable_dns_support = true

  tags = local.common_tags
}

# RDS PostgreSQL Module
module "rds" {
  source = "../../modules/rds"

  environment  = local.environment
  project_name = local.project_name
  
  vpc_id               = module.vpc.vpc_id
  database_subnet_ids  = module.vpc.database_subnet_ids
  allowed_security_groups = [
    module.ecs_backend.backend_security_group_id,
    module.ecs_worker.worker_security_group_id
  ]
  
  instance_class       = var.rds_instance_class
  allocated_storage    = var.rds_allocated_storage
  engine_version       = "15.4"
  multi_az             = false  # Single AZ for dev
  
  database_name        = var.rds_database_name
  master_username      = var.db_username
  master_password      = var.db_password  # Use AWS Secrets Manager in prod
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"
  
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  
  tags = local.common_tags
}

# S3 Buckets Module
module "s3" {
  source = "../../modules/s3"

  environment  = local.environment
  project_name = local.project_name
  
  # Frontend bucket
  create_frontend_bucket = true
  frontend_bucket_name   = "${local.project_name}-frontend-${local.environment}"
  
  # Assets bucket
  create_assets_bucket = true
  assets_bucket_name   = "${local.project_name}-assets-${local.environment}"
  assets_lifecycle_rules = {
    expire_old_versions = {
      enabled = true
      days    = 30
    }
    delete_old_objects = {
      enabled = true
      days    = 30
    }
  }
  
  enable_versioning = true
  enable_encryption = true
  
  tags = local.common_tags
}

# SQS Queue Module
module "sqs" {
  source = "../../modules/sqs"

  environment  = local.environment
  project_name = local.project_name
  
  queue_name              = "${local.project_name}-jobs-${local.environment}"
  visibility_timeout      = 600  # 10 minutes for job processing
  message_retention       = 14 * 24 * 60 * 60  # 14 days
  max_message_size        = 256 * 1024  # 256 KB
  receive_wait_time       = 20  # Long polling
  
  # Dead Letter Queue
  create_dlq              = true
  dlq_max_receive_count   = 3
  
  tags = local.common_tags
}

# ECS Cluster for Backend
module "ecs_backend" {
  source = "../../modules/ecs"

  environment  = local.environment
  project_name = local.project_name
  service_name = "backend"
  
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  public_subnet_ids  = module.vpc.public_subnet_ids
  
  # ALB Configuration
  create_alb         = true
  alb_internal       = false
  certificate_arn    = var.alb_certificate_arn  # Optional for HTTPS
  
  # ECS Service Configuration
  task_cpu           = 512
  task_memory        = 1024
  desired_count      = 2
  container_port     = 8000
  
  # Auto Scaling
  enable_autoscaling = true
  min_capacity       = 2
  max_capacity       = 5
  cpu_threshold      = 70
  memory_threshold   = 75
  
  # Environment Variables
  environment_variables = {
    ENVIRONMENT       = local.environment
    DATABASE_HOST     = module.rds.db_endpoint
    DATABASE_PORT     = "5432"
    DATABASE_NAME     = var.db_name
    SQS_QUEUE_URL     = module.sqs.queue_url
    S3_ASSETS_BUCKET  = module.s3.assets_bucket_name
    AWS_REGION        = var.aws_region
  }
  
  # Secrets from AWS Secrets Manager
  secrets = {
    DATABASE_PASSWORD = module.rds.db_secret_arn
    JWT_SECRET        = aws_secretsmanager_secret.jwt_secret.arn
  }
  
  # Container Image
  container_image = "${var.ecr_backend_repository}:latest"
  
  # Health Check
  health_check_path = "/health"
  
  tags = local.common_tags
}

# ECS Cluster for GPU Workers
module "ecs_worker" {
  source = "../../modules/ecs"

  environment  = local.environment
  project_name = local.project_name
  service_name = "worker"
  
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.worker_subnet_ids
  
  # No ALB needed for workers
  create_alb = false
  
  # Use EC2 launch type for GPU instances
  launch_type    = "EC2"
  instance_type  = var.worker_gpu_instance_type  # g4dn.xlarge
  
  # ECS Service Configuration
  task_cpu           = 4096
  task_memory        = 16384
  desired_count      = 1
  
  # Auto Scaling based on SQS queue depth
  enable_autoscaling = true
  min_capacity       = 1
  max_capacity       = 10
  scaling_metric     = "sqs"
  sqs_queue_name     = module.sqs.queue_name
  target_queue_depth = 5  # 5 messages per worker
  
  # Environment Variables
  environment_variables = {
    ENVIRONMENT       = local.environment
    DATABASE_HOST     = module.rds.db_endpoint
    DATABASE_PORT     = "5432"
    DATABASE_NAME     = var.db_name
    SQS_QUEUE_URL     = module.sqs.queue_url
    S3_ASSETS_BUCKET  = module.s3.assets_bucket_name
    AWS_REGION        = var.aws_region
    NVIDIA_VISIBLE_DEVICES = "all"
  }
  
  # Secrets
  secrets = {
    DATABASE_PASSWORD = module.rds.db_secret_arn
  }
  
  # Container Image
  container_image = "${var.ecr_worker_repository}:latest"
  
  # GPU Resource Requirements
  resource_requirements = [{
    type  = "GPU"
    value = "1"
  }]
  
  tags = local.common_tags
}

# CloudFront Distribution for Frontend
module "cloudfront" {
  source = "../../modules/cloudfront"

  environment  = local.environment
  project_name = local.project_name
  
  frontend_bucket_id              = module.s3.frontend_bucket_id
  frontend_bucket_regional_domain = module.s3.frontend_bucket_regional_domain_name
  
  aliases             = var.cloudfront_aliases
  acm_certificate_arn = var.cloudfront_certificate_arn
  
  price_class = "PriceClass_100"  # US, Canada, Europe
  
  default_root_object = "index.html"
  
  # Custom error responses for SPA
  custom_error_responses = [
    {
      error_code         = 404
      response_code      = 200
      response_page_path = "/index.html"
    },
    {
      error_code         = 403
      response_code      = 200
      response_page_path = "/index.html"
    }
  ]
  
  tags = local.common_tags
}

# Secrets Manager for sensitive data
resource "aws_secretsmanager_secret" "jwt_secret" {
  name        = "${local.project_name}-jwt-secret-${local.environment}"
  description = "JWT signing secret for authentication"
  
  tags = local.common_tags
}

resource "aws_secretsmanager_secret_version" "jwt_secret" {
  secret_id     = aws_secretsmanager_secret.jwt_secret.id
  secret_string = var.jwt_secret
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "backend" {
  name              = "/ecs/${local.project_name}-backend-${local.environment}"
  retention_in_days = 7
  
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "worker" {
  name              = "/ecs/${local.project_name}-worker-${local.environment}"
  retention_in_days = 7
  
  tags = local.common_tags
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "backend_cpu_high" {
  alarm_name          = "${local.project_name}-backend-cpu-high-${local.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "Backend CPU utilization is too high"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  
  dimensions = {
    ClusterName = module.ecs_backend.cluster_name
    ServiceName = module.ecs_backend.service_name
  }
}

resource "aws_cloudwatch_metric_alarm" "queue_depth_high" {
  alarm_name          = "${local.project_name}-queue-depth-high-${local.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = 300
  statistic           = "Average"
  threshold           = 50
  alarm_description   = "SQS queue depth is too high"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  
  dimensions = {
    QueueName = module.sqs.queue_name
  }
}

# SNS Topic for Alerts
resource "aws_sns_topic" "alerts" {
  name = "${local.project_name}-alerts-${local.environment}"
  
  tags = local.common_tags
}

resource "aws_sns_topic_subscription" "alerts_email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# Outputs
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "backend_alb_dns" {
  description = "Backend ALB DNS name"
  value       = module.ecs_backend.alb_dns_name
}

output "cloudfront_domain" {
  description = "CloudFront distribution domain"
  value       = module.cloudfront.cloudfront_domain_name
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.db_endpoint
  sensitive   = true
}

output "sqs_queue_url" {
  description = "SQS queue URL"
  value       = module.sqs.queue_url
}

output "assets_bucket" {
  description = "S3 assets bucket name"
  value       = module.s3.assets_bucket_name
}
