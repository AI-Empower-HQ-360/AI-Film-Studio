variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "ai-film-studio"
}

variable "aws_region" {
  description = "AWS region for resource deployment"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "rds_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "rds_allocated_storage" {
  description = "Allocated storage for RDS instance in GB"
  type        = number
  default     = 20
}

variable "rds_database_name" {
  description = "Name of the RDS database"
  type        = string
  default     = "filmstudio"
}

variable "backend_container_port" {
  description = "Port for backend container"
  type        = number
  default     = 8000
}

variable "worker_gpu_instance_type" {
  description = "EC2 instance type for GPU workers"
  type        = string
  default     = "g4dn.xlarge"
}

variable "cloudwatch_retention_days" {
  description = "CloudWatch logs retention period in days"
  type        = number
  default     = 7
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.11.0/24", "10.0.12.0/24"]
}

variable "worker_subnet_cidrs" {
  description = "CIDR blocks for worker subnets"
  type        = list(string)
  default     = ["10.0.21.0/24", "10.0.22.0/24"]
}

variable "database_subnet_cidrs" {
  description = "CIDR blocks for database subnets"
  type        = list(string)
  default     = ["10.0.31.0/24", "10.0.32.0/24"]
}

variable "db_username" {
  description = "Master database username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Master database password"
  type        = string
  sensitive   = true
}

variable "alb_certificate_arn" {
  description = "ACM certificate ARN for ALB HTTPS listener (optional)"
  type        = string
  default     = ""
}

variable "ecr_backend_repository" {
  description = "ECR repository URI for backend service image"
  type        = string
}

variable "ecr_worker_repository" {
  description = "ECR repository URI for worker service image"
  type        = string
}

variable "cloudfront_aliases" {
  description = "Optional domain aliases for CloudFront distribution"
  type        = list(string)
  default     = []
}

variable "cloudfront_certificate_arn" {
  description = "ACM certificate ARN for CloudFront aliases (optional)"
  type        = string
  default     = ""
}

variable "jwt_secret" {
  description = "JWT signing secret"
  type        = string
  sensitive   = true
}

variable "alert_email" {
  description = "Email address for SNS alert subscriptions"
  type        = string
}
