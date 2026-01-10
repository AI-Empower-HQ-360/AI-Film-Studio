variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets (backend)"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "worker_subnet_cidrs" {
  description = "CIDR blocks for worker subnets (GPU instances)"
  type        = list(string)
  default     = ["10.0.20.0/24", "10.0.21.0/24"]
}

variable "database_subnet_cidrs" {
  description = "CIDR blocks for database subnets"
  type        = list(string)
  default     = ["10.0.30.0/24", "10.0.31.0/24"]
}

# RDS Configuration
variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.medium"
}

variable "db_allocated_storage" {
  description = "Allocated storage for RDS in GB"
  type        = number
  default     = 20
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "aifilmstudio"
}

variable "db_username" {
  description = "Master username for database"
  type        = string
  default     = "admin"
  sensitive   = true
}

variable "db_password" {
  description = "Master password for database"
  type        = string
  sensitive   = true
}

# ECS Configuration
variable "worker_instance_type" {
  description = "EC2 instance type for GPU workers"
  type        = string
  default     = "g4dn.xlarge"
}

# Container Repositories
variable "ecr_backend_repository" {
  description = "ECR repository for backend container"
  type        = string
  default     = "ai-film-studio-backend"
}

variable "ecr_worker_repository" {
  description = "ECR repository for worker container"
  type        = string
  default     = "ai-film-studio-worker"
}

# SSL Certificates
variable "alb_certificate_arn" {
  description = "ACM certificate ARN for ALB HTTPS"
  type        = string
  default     = ""
}

variable "cloudfront_certificate_arn" {
  description = "ACM certificate ARN for CloudFront (must be in us-east-1)"
  type        = string
  default     = ""
}

variable "cloudfront_aliases" {
  description = "Custom domain aliases for CloudFront"
  type        = list(string)
  default     = []
}

# Secrets
variable "jwt_secret" {
  description = "JWT signing secret"
  type        = string
  sensitive   = true
}

# Alerts
variable "alert_email" {
  description = "Email for CloudWatch alerts"
  type        = string
  default     = "alerts@ai-empower-hq.com"
}
