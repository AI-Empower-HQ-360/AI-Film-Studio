# 📚 Detailed Deployment Guide - AI Film Studio

This guide explains **every step** of deploying the AI Film Studio infrastructure to AWS, with real examples from this project.

---

## 📋 Table of Contents

1. [Understanding What We're Deploying](#understanding-what-were-deploying)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [Deployment Method 1: CI/CD (GitHub Actions)](#deployment-method-1-cicd-github-actions)
4. [Deployment Method 2: Manual (Local)](#deployment-method-2-manual-local)
5. [What Happens During Deployment](#what-happens-during-deployment)
6. [Verifying Deployment](#verifying-deployment)
7. [Post-Deployment Configuration](#post-deployment-configuration)
8. [Troubleshooting](#troubleshooting)

---

## 🏗️ Understanding What We're Deploying

### Our Infrastructure Stack

The AI Film Studio uses **AWS CDK (Cloud Development Kit)** to define infrastructure as code. When we deploy, we're creating:

#### 1. **Networking Layer (VPC)**
```
VPC: 10.0.0.0/16
├── Public Subnets (2 AZs)
│   ├── us-east-1a: 10.0.1.0/24
│   └── us-east-1b: 10.0.2.0/24
├── Private Subnets (2 AZs)
│   ├── us-east-1a: 10.0.11.0/24
│   └── us-east-1b: 10.0.12.0/24
├── Database Subnets (2 AZs)
│   ├── us-east-1a: 10.0.21.0/24
│   └── us-east-1b: 10.0.22.0/24
├── Internet Gateway
├── NAT Gateway (for private subnet internet access)
└── Route Tables
```

**Why:** Isolates our resources, provides security, enables private resources to access internet.

#### 2. **Database (RDS PostgreSQL)**
```
Database Instance:
├── Engine: PostgreSQL 16.1
├── Instance Type: db.t3.small (dev) / db.t3.medium (prod)
├── Storage: 100 GB (auto-scales to 500 GB)
├── Multi-AZ: Yes (production) / No (dev)
├── Backup Retention: 7 days (prod) / 1 day (dev)
└── Database Name: aifilmstudio
```

**Why:** Stores all application data (users, projects, films, etc.)

#### 3. **Compute (ECS Fargate)**
```
ECS Cluster: ai-film-studio-dev
└── Fargate Service: backend-service
    ├── Task Definition: Backend API
    ├── Desired Count: 1 (dev) / 2+ (prod)
    ├── CPU: 0.5 vCPU (512 units)
    ├── Memory: 1 GB (1024 MB)
    └── Container Image: Backend Docker image
```

**Why:** Runs our backend API without managing servers.

#### 4. **Load Balancer (ALB)**
```
Application Load Balancer:
├── Type: Internet-facing
├── Scheme: Public
├── Listeners:
│   └── Port 80 → Port 3000 (HTTP)
└── Target Group: Backend service
```

**Why:** Distributes traffic, provides health checks, enables SSL termination.

#### 5. **Storage (S3 Buckets)**
```
S3 Buckets:
├── ai-film-studio-assets-dev-{account-id}
│   └── Stores: Video files, images, media assets
├── ai-film-studio-characters-dev-{account-id}
│   └── Stores: Character models, animations
└── ai-film-studio-marketing-dev-{account-id}
    └── Stores: Marketing materials, trailers, posters
```

**Why:** Scalable object storage for large files.

#### 6. **Content Delivery (CloudFront)**
```
CloudFront Distribution:
├── Origin: S3 buckets
├── Behaviors:
│   ├── /assets/* → Assets bucket
│   ├── /characters/* → Characters bucket
│   └── /marketing/* → Marketing bucket
└── Caching: Optimized
```

**Why:** Fast global content delivery, reduces latency.

#### 7. **Message Queues (SQS)**
```
SQS Queues:
├── ai-film-studio-jobs-dev
│   └── Visibility Timeout: 15 minutes
├── ai-film-studio-video-jobs-dev
│   └── Visibility Timeout: 30 minutes
└── ai-film-studio-voice-jobs-dev
    └── Visibility Timeout: 10 minutes
```

**Why:** Asynchronous job processing (video generation, voice synthesis).

#### 8. **Caching (ElastiCache Redis)**
```
Redis Cluster:
├── Engine: Redis 7.0
├── Node Type: cache.t3.micro (dev) / cache.t3.small (prod)
└── Subnet Group: Private subnets
```

**Why:** Fast caching for sessions, API responses, temporary data.

#### 9. **Notifications (SNS)**
```
SNS Topics:
├── Job Completion Notifications
├── Error Alerts
└── System Alerts
```

**Why:** Real-time notifications for job completion, errors, system events.

#### 10. **Monitoring (CloudWatch)**
```
CloudWatch Alarms:
├── ECS CPU Utilization > 80%
├── ECS Memory Utilization > 80%
├── RDS CPU Utilization > 80%
└── SQS Queue Depth > 1000
```

**Why:** Proactive monitoring and alerting.

---

## ✅ Pre-Deployment Checklist

### Step 1: Verify GitHub Secrets

**Location:** GitHub Repository → Settings → Secrets and variables → Actions

**Required Secrets:**
```
✅ AWS_ACCESS_KEY_ID
   Example: AKIAIOSFODNN7EXAMPLE
   
✅ AWS_SECRET_ACCESS_KEY
   Example: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   
✅ AWS_ACCOUNT_ID
   Example: 123456789012
```

**How to verify:**
1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Verify all three secrets exist
4. If missing, click **"New repository secret"** and add them

### Step 2: Verify AWS IAM User

**Check if IAM user exists:**
```bash
aws iam get-user --user-name github-actions-cdk
```

**Expected output:**
```json
{
    "User": {
        "UserName": "github-actions-cdk",
        "UserId": "AIDAIOSFODNN7EXAMPLE",
        "Arn": "arn:aws:iam::123456789012:user/github-actions-cdk",
        "CreateDate": "2026-01-22T10:00:00Z"
    }
}
```

**If user doesn't exist, create it:**
```bash
# Create user
aws iam create-user --user-name github-actions-cdk

# Attach policy
aws iam attach-user-policy \
  --user-name github-actions-cdk \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess

# Create access key
aws iam create-access-key --user-name github-actions-cdk
```

**Expected output:**
```json
{
    "AccessKey": {
        "UserName": "github-actions-cdk",
        "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
        "Status": "Active",
        "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "CreateDate": "2026-01-22T10:00:00Z"
    }
}
```

**⚠️ Important:** Copy the `SecretAccessKey` immediately - it's only shown once!

### Step 3: Verify Local Setup (for manual deployment)

```bash
# Check Python version
python --version
# Expected: Python 3.12.0

# Check CDK version
cdk --version
# Expected: 2.1101.0 (build xxxxxx)

# Check AWS CLI
aws --version
# Expected: aws-cli/2.x.x

# Check AWS credentials
aws sts get-caller-identity
# Expected: Your AWS account details
```

---

## 🚀 Deployment Method 1: CI/CD (GitHub Actions)

This is the **recommended** method. It's automated, repeatable, and includes testing.

### Step-by-Step Process

#### Step 1: Trigger Deployment

**Option A: Automatic (Push to Branch)**

```bash
# Make a small change to trigger deployment
cd C:\Users\ctrpr\Projects\AI-Film-Studio
git checkout develop
echo "# Deployment trigger" >> infrastructure/aws-cdk/DEPLOYMENT_LOG.md
git add infrastructure/aws-cdk/DEPLOYMENT_LOG.md
git commit -m "Trigger infrastructure deployment"
git push origin develop
```

**What happens:**
- GitHub detects push to `develop` branch
- Checks if files in `infrastructure/aws-cdk/**` changed
- Triggers "AWS CDK Deploy" workflow

**Option B: Manual Trigger**

1. Go to **GitHub Repository**
2. Click **"Actions"** tab
3. Select **"AWS CDK Deploy"** workflow (left sidebar)
4. Click **"Run workflow"** button (top right)
5. Select:
   - **Environment:** `dev` (for first deployment)
   - **Action:** `deploy`
6. Click **"Run workflow"**

**Visual Example:**
```
GitHub Repository
└── Actions Tab
    └── AWS CDK Deploy (left sidebar)
        └── Run workflow (button, top right)
            └── Environment: dev
            └── Action: deploy
            └── [Run workflow]
```

#### Step 2: Workflow Execution

The workflow runs these jobs **in order**:

**Job 1: Test Infrastructure** (5-10 minutes)

```yaml
Name: Test Infrastructure
Runs on: ubuntu-latest
Working directory: infrastructure/aws-cdk
```

**What it does:**
1. **Checkout code**
   ```bash
   git checkout develop
   cd infrastructure/aws-cdk
   ```

2. **Set up Python 3.12**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install CDK CLI**
   ```bash
   npm install -g aws-cdk
   # Installs: aws-cdk@latest
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # Installs: aws-cdk-lib, constructs, boto3, python-dotenv
   
   pip install -r requirements-test.txt
   # Installs: pytest, pytest-cov
   ```

5. **Run infrastructure tests**
   ```bash
   pytest tests/ -v --tb=short
   ```
   
   **Expected output:**
   ```
   tests/test_stack.py::TestVPC::test_vpc_created PASSED
   tests/test_stack.py::TestVPC::test_public_subnets_created PASSED
   tests/test_stack.py::TestRDS::test_rds_instance_created PASSED
   ... (25 tests total)
   ============================ 25 passed in 38.10s ============================
   ```

6. **Synthesize CDK stack**
   ```bash
   cdk synth --quiet
   ```
   
   **What this does:**
   - Converts CDK code to CloudFormation template
   - Validates all resources
   - Generates `cdk.out/AIFilmStudio.template.json`
   
   **Expected output:**
   ```
   Successfully synthesized to cdk.out
   Supply a stack id (did you mean AIFilmStudio?)
   ```

**Job 2: Deploy to Development** (15-30 minutes)

This job only runs if:
- Push to `develop` branch, OR
- Manual trigger with `environment: dev`

```yaml
Name: Deploy to Development
Needs: test (must pass first)
Runs on: ubuntu-latest
Environment: development
```

**What it does:**

1. **Checkout code**
   ```bash
   git checkout develop
   cd infrastructure/aws-cdk
   ```

2. **Configure AWS credentials**
   ```bash
   # Uses GitHub secrets:
   export AWS_ACCESS_KEY_ID=${{ secrets.AWS_ACCESS_KEY_ID }}
   export AWS_SECRET_ACCESS_KEY=${{ secrets.AWS_SECRET_ACCESS_KEY }}
   export AWS_DEFAULT_REGION=us-east-1
   ```

3. **Set up Python and CDK**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   npm install -g aws-cdk
   ```

4. **Bootstrap CDK (if needed)**
   ```bash
   cdk bootstrap aws://123456789012/us-east-1
   ```
   
   **What this does:**
   - Creates S3 bucket for CDK assets: `cdk-hnb659fds-assets-123456789012-us-east-1`
   - Creates IAM roles for CDK deployment
   - Only needed once per account/region
   
   **Expected output:**
   ```
   ⏳  Bootstrapping environment aws://123456789012/us-east-1...
   CDKToolkit: creating CloudFormation changeset...
   ✅  Environment aws://123456789012/us-east-1 bootstrapped
   ```
   
   **Or if already bootstrapped:**
   ```
   ✅  Environment aws://123456789012/us-east-1 already bootstrapped
   ```

5. **CDK Diff (Preview Changes)**
   ```bash
   cdk diff
   ```
   
   **What this does:**
   - Compares current stack with what's in AWS
   - Shows what will be created, modified, or deleted
   - **First deployment:** Shows all resources to be created
   
   **Expected output (first deployment):**
   ```
   Stack AIFilmStudio
   Resources
   [~] AWS::EC2::VPC AIFilmStudio/VPC VPC123456789012
        └─ [~] CidrBlock
            └─ [~] .CidrBlock: "10.0.0.0/16"
   [+] AWS::RDS::DBInstance AIFilmStudio/Database DatabaseB269D8BB
   [+] AWS::ECS::Cluster AIFilmStudio/Cluster Cluster123456789012
   ... (many more resources)
   
   Stack AIFilmStudio
    └─ Parameters
        └─ BootstrapVersion: 12
   ```

6. **CDK Deploy**
   ```bash
   cdk deploy --require-approval never --all
   ```
   
   **What this does:**
   - Uploads CDK assets to S3
   - Creates CloudFormation stack
   - Provisions all AWS resources
   - Waits for stack creation to complete
   
   **Expected output:**
   ```
   AIFilmStudio: deploying...
   AIFilmStudio: creating CloudFormation changeset...
   
   ✅  AIFilmStudio
   
   Outputs:
   AIFilmStudio.BackendURL = http://ai-film-studio-alb-1234567890.us-east-1.elb.amazonaws.com
   AIFilmStudio.DatabaseEndpoint = ai-film-studio-db-dev.xxxxx.us-east-1.rds.amazonaws.com:5432
   AIFilmStudio.AssetsBucketName = ai-film-studio-assets-dev-123456789012
   AIFilmStudio.CloudFrontURL = https://d1234567890.cloudfront.net
   ...
   
   Stack ARN:
   arn:aws:cloudformation:us-east-1:123456789012:stack/AIFilmStudio/abc123...
   ```

**What's happening in AWS (behind the scenes):**

1. **CloudFormation Stack Creation** (5-10 min)
   ```
   Status: CREATE_IN_PROGRESS
   ├── VPC creation (2-3 min)
   ├── Subnet creation (1 min)
   ├── Internet Gateway (30 sec)
   ├── NAT Gateway (3-5 min) ⚠️ Slowest
   └── Route Tables (1 min)
   ```

2. **RDS Database Creation** (10-15 min)
   ```
   Status: CREATE_IN_PROGRESS
   ├── Subnet group creation (1 min)
   ├── Security group creation (30 sec)
   ├── Database instance creation (10-15 min) ⚠️ Slowest
   └── Initial backup (2-3 min)
   ```

3. **ECS Cluster & Service** (5-10 min)
   ```
   Status: CREATE_IN_PROGRESS
   ├── ECS Cluster creation (1 min)
   ├── Task definition creation (1 min)
   ├── ALB creation (2-3 min)
   ├── Target group creation (1 min)
   ├── ECS Service creation (3-5 min)
   └── Container startup (2-3 min)
   ```

4. **S3 Buckets** (2-3 min)
   ```
   Status: CREATE_IN_PROGRESS
   ├── Assets bucket (1 min)
   ├── Characters bucket (1 min)
   └── Marketing bucket (1 min)
   ```

5. **CloudFront Distribution** (10-15 min)
   ```
   Status: CREATE_IN_PROGRESS
   ├── Distribution creation (5-10 min) ⚠️ Slowest
   └── DNS propagation (5-10 min)
   ```

6. **Other Resources** (5-10 min)
   ```
   ├── ElastiCache Redis (5-7 min)
   ├── SQS Queues (1-2 min)
   ├── SNS Topics (1 min)
   └── CloudWatch Alarms (1 min)
   ```

**Total Time:** ~30-45 minutes for first deployment

7. **Get Stack Outputs**
   ```bash
   aws cloudformation describe-stacks \
     --stack-name AIFilmStudio \
     --query 'Stacks[0].Outputs' \
     --output table
   ```
   
   **Expected output:**
   ```
   ---------------------------------------------------------------------------
   |                            DescribeStacks                               |
   +------------------+------------------------------------------------------+
   |  OutputKey       |  OutputValue                                         |
   +------------------+------------------------------------------------------+
   |  BackendURL      |  http://ai-film-studio-alb-1234567890.us-east-1...  |
   |  DatabaseEndpoint|  ai-film-studio-db-dev.xxxxx.us-east-1.rds...     |
   |  AssetsBucketName|  ai-film-studio-assets-dev-123456789012             |
   |  CloudFrontURL   |  https://d1234567890.cloudfront.net                 |
   |  RedisEndpoint   |  ai-film-studio-redis-dev.xxxxx.cache.amazonaws... |
   +------------------+------------------------------------------------------+
   ```

#### Step 3: Monitor Deployment

**In GitHub Actions:**
1. Go to **Actions** tab
2. Click on the running workflow
3. Watch real-time logs
4. See each step execute

**In AWS Console:**
1. Go to **CloudFormation** service
2. Find stack: **AIFilmStudio**
3. Click **"Events"** tab
4. Watch resource creation progress

**Example Events:**
```
Time                    Status              Resource
10:00:00  CREATE_IN_PROGRESS  AIFilmStudio
10:00:30  CREATE_IN_PROGRESS  VPC
10:01:00  CREATE_COMPLETE      VPC
10:01:30  CREATE_IN_PROGRESS  Database
10:15:00  CREATE_COMPLETE      Database
10:15:30  CREATE_IN_PROGRESS  Cluster
10:20:00  CREATE_COMPLETE      Cluster
...
10:30:00  CREATE_COMPLETE      AIFilmStudio
```

---

## 💻 Deployment Method 2: Manual (Local)

Deploy from your local machine using AWS CLI and CDK.

### Prerequisites

```bash
# Verify you're in the right directory
cd C:\Users\ctrpr\Projects\AI-Film-Studio\infrastructure\aws-cdk

# Activate virtual environment
.venv-cdk\Scripts\activate
# You should see: (.venv-cdk) in your prompt

# Verify AWS credentials
aws sts get-caller-identity
# Should show your AWS account details
```

### Step-by-Step Manual Deployment

#### Step 1: Run Tests (Optional but Recommended)

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run tests
pytest tests/ -v

# Expected: 25 passed
```

#### Step 2: Synthesize Stack

```bash
cdk synth
```

**What this does:**
- Validates CDK code
- Generates CloudFormation template
- Saves to `cdk.out/AIFilmStudio.template.json`

**Expected output:**
```
Successfully synthesized to cdk.out
Supply a stack id (did you mean AIFilmStudio?)
```

**Check generated template:**
```bash
# View template size
ls -lh cdk.out/AIFilmStudio.template.json

# View first 50 lines
head -n 50 cdk.out/AIFilmStudio.template.json
```

#### Step 3: Preview Changes (CDK Diff)

```bash
cdk diff
```

**What this shows:**
- Resources to be created (marked with `[+]`)
- Resources to be modified (marked with `[~]`)
- Resources to be deleted (marked with `[-]`)

**First deployment example:**
```
Stack AIFilmStudio
Resources
[+] AWS::EC2::VPC VPC VPC123456789012
[+] AWS::EC2::Subnet PublicSubnet1 Subnet123456789012
[+] AWS::EC2::Subnet PublicSubnet2 Subnet234567890123
[+] AWS::EC2::Subnet PrivateSubnet1 Subnet345678901234
[+] AWS::EC2::Subnet PrivateSubnet2 Subnet456789012345
[+] AWS::EC2::Subnet DatabaseSubnet1 Subnet567890123456
[+] AWS::EC2::Subnet DatabaseSubnet2 Subnet678901234567
[+] AWS::EC2::InternetGateway InternetGateway InternetGateway123456789012
[+] AWS::EC2::NatGateway NatGateway NatGateway123456789012
[+] AWS::RDS::DBInstance Database DatabaseB269D8BB
[+] AWS::ECS::Cluster Cluster Cluster123456789012
... (many more)
```

#### Step 4: Bootstrap CDK (First Time Only)

```bash
# Get your AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "Account ID: $ACCOUNT_ID"

# Bootstrap
cdk bootstrap aws://$ACCOUNT_ID/us-east-1
```

**Expected output:**
```
⏳  Bootstrapping environment aws://123456789012/us-east-1...
CDKToolkit: creating CloudFormation changeset...
[████████████████████████████████████████████████████] (3/3)

 ✅  Environment aws://123456789012/us-east-1 bootstrapped
```

#### Step 5: Deploy Stack

```bash
# Deploy with approval prompt
cdk deploy

# OR deploy without prompts (faster)
cdk deploy --require-approval never
```

**What happens:**

1. **CDK uploads assets to S3**
   ```
   AIFilmStudio: deploying...
   AIFilmStudio: uploading assets...
   [████████████████████████████████████████████████████] (1/1)
   ```

2. **Creates CloudFormation changeset**
   ```
   AIFilmStudio: creating CloudFormation changeset...
   [████████████████████████████████████████████████████] (1/1)
   ```

3. **Deploys stack**
   ```
   0/50 | 11:00:00 | CREATE_IN_PROGRESS   | AWS::CloudFormation::Stack | AIFilmStudio
   1/50 | 11:00:30 | CREATE_IN_PROGRESS   | AWS::EC2::VPC | VPC
   2/50 | 11:01:00 | CREATE_COMPLETE      | AWS::EC2::VPC | VPC
   3/50 | 11:01:30 | CREATE_IN_PROGRESS   | AWS::EC2::Subnet | PublicSubnet1
   ...
   50/50 | 11:30:00 | CREATE_COMPLETE      | AWS::CloudFormation::Stack | AIFilmStudio
   ```

4. **Shows outputs**
   ```
   ✅  AIFilmStudio
   
   Outputs:
   AIFilmStudio.BackendURL = http://ai-film-studio-alb-1234567890.us-east-1.elb.amazonaws.com
   AIFilmStudio.DatabaseEndpoint = ai-film-studio-db-dev.xxxxx.us-east-1.rds.amazonaws.com:5432
   AIFilmStudio.AssetsBucketName = ai-film-studio-assets-dev-123456789012
   AIFilmStudio.CloudFrontURL = https://d1234567890.cloudfront.net
   AIFilmStudio.RedisEndpoint = ai-film-studio-redis-dev.xxxxx.cache.amazonaws.com:6379
   
   Stack ARN:
   arn:aws:cloudformation:us-east-1:123456789012:stack/AIFilmStudio/abc123...
   ```

**Total time:** ~30-45 minutes

#### Step 6: Verify Deployment

```bash
# Check stack status
aws cloudformation describe-stacks \
  --stack-name AIFilmStudio \
  --query 'Stacks[0].StackStatus' \
  --output text
# Expected: CREATE_COMPLETE

# List all resources
aws cloudformation list-stack-resources \
  --stack-name AIFilmStudio \
  --output table
```

---

## 🔍 What Happens During Deployment

### Phase 1: Preparation (1-2 minutes)

1. **CDK reads your code**
   - Parses `app.py`
   - Loads `stacks/ai_film_studio_stack.py`
   - Validates syntax and dependencies

2. **Synthesizes CloudFormation template**
   - Converts CDK constructs to CloudFormation resources
   - Generates ~500-1000 lines of JSON/YAML
   - Validates resource properties

3. **Uploads assets to S3**
   - Docker images (if any)
   - Lambda code (if any)
   - Other deployment artifacts

### Phase 2: Stack Creation (25-40 minutes)

CloudFormation creates resources **in dependency order**:

**Order 1: Networking (5-10 min)**
```
1. VPC (1 min)
2. Internet Gateway (30 sec)
3. Subnets (2 min)
4. Route Tables (1 min)
5. NAT Gateway (5-7 min) ⚠️ Slowest
```

**Order 2: Security (2-3 min)**
```
1. Security Groups (1 min)
2. IAM Roles (1 min)
3. Secrets Manager (1 min)
```

**Order 3: Storage (5-10 min)**
```
1. S3 Buckets (2 min)
2. RDS Subnet Group (1 min)
3. RDS Database (10-15 min) ⚠️ Slowest
4. ElastiCache Subnet Group (1 min)
5. ElastiCache Redis (5-7 min)
```

**Order 4: Compute (10-15 min)**
```
1. ECS Cluster (1 min)
2. ECR Repositories (2 min)
3. Task Definitions (1 min)
4. Application Load Balancer (3-5 min)
5. Target Groups (1 min)
6. ECS Service (5-7 min)
7. Container Startup (2-3 min)
```

**Order 5: Content Delivery (10-15 min)**
```
1. CloudFront Distribution (10-15 min) ⚠️ Slowest
2. DNS Propagation (5-10 min)
```

**Order 6: Messaging (2-3 min)**
```
1. SQS Queues (1 min)
2. SNS Topics (1 min)
```

**Order 7: Monitoring (1-2 min)**
```
1. CloudWatch Log Groups (30 sec)
2. CloudWatch Alarms (1 min)
```

### Phase 3: Verification (1-2 minutes)

1. **Health checks**
   - ALB health checks
   - ECS service health
   - Database connectivity

2. **Stack completion**
   - All resources: `CREATE_COMPLETE`
   - Stack status: `CREATE_COMPLETE`

---

## ✅ Verifying Deployment

### 1. Check Stack Status

```bash
aws cloudformation describe-stacks \
  --stack-name AIFilmStudio \
  --query 'Stacks[0].[StackName,StackStatus,CreationTime]' \
  --output table
```

**Expected output:**
```
----------------------------------------------------------
|                  DescribeStacks                      |
+------------------+------------------+-----------------+
|  StackName      |  StackStatus     |  CreationTime   |
+------------------+------------------+-----------------+
|  AIFilmStudio   |  CREATE_COMPLETE |  2026-01-22...  |
+------------------+------------------+-----------------+
```

### 2. Verify Resources

**VPC:**
```bash
aws ec2 describe-vpcs \
  --filters "Name=tag:Name,Values=ai-film-studio-dev" \
  --query 'Vpcs[0].[VpcId,CidrBlock,State]' \
  --output table
```

**RDS Database:**
```bash
aws rds describe-db-instances \
  --query 'DBInstances[?contains(DBInstanceIdentifier, `ai-film-studio`)].{ID:DBInstanceIdentifier,Status:DBInstanceStatus,Endpoint:Endpoint.Address}' \
  --output table
```

**ECS Service:**
```bash
aws ecs describe-services \
  --cluster ai-film-studio-dev \
  --services backend-service \
  --query 'services[0].[serviceName,status,runningCount,desiredCount]' \
  --output table
```

**S3 Buckets:**
```bash
aws s3 ls | grep ai-film-studio
```

**CloudFront:**
```bash
aws cloudfront list-distributions \
  --query 'DistributionList.Items[?contains(Comment, `AI Film Studio`)].{Id:Id,DomainName:DomainName,Status:Status}' \
  --output table
```

### 3. Test Endpoints

**Backend URL:**
```bash
# Get URL from stack outputs
BACKEND_URL=$(aws cloudformation describe-stacks \
  --stack-name AIFilmStudio \
  --query 'Stacks[0].Outputs[?OutputKey==`BackendURL`].OutputValue' \
  --output text)

# Test health endpoint
curl $BACKEND_URL/health
# Expected: {"status":"ok"} or similar
```

**Database Connection:**
```bash
# Get database endpoint
DB_ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name AIFilmStudio \
  --query 'Stacks[0].Outputs[?OutputKey==`DatabaseEndpoint`].OutputValue' \
  --output text)

# Test connection (requires psql)
psql -h $DB_ENDPOINT -U aifilmstudio -d aifilmstudio
```

---

## 🔧 Post-Deployment Configuration

### 1. Configure Application Secrets

```bash
# Store API keys in Secrets Manager
aws secretsmanager create-secret \
  --name ai-film-studio/api-keys/dev \
  --secret-string '{
    "openai_api_key": "sk-...",
    "youtube_api_key": "...",
    "other_service_key": "..."
  }'
```

### 2. Update ECS Service Environment Variables

```bash
# Update service to use secrets
aws ecs update-service \
  --cluster ai-film-studio-dev \
  --service backend-service \
  --task-definition backend-task:1 \
  --force-new-deployment
```

### 3. Configure DNS (Optional)

```bash
# Get CloudFront distribution domain
CLOUDFRONT_DOMAIN=$(aws cloudformation describe-stacks \
  --stack-name AIFilmStudio \
  --query 'Stacks[0].Outputs[?OutputKey==`CloudFrontURL`].OutputValue' \
  --output text)

# Create Route53 record (if you have a domain)
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890 \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "dev.aifilmstudio.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "'$CLOUDFRONT_DOMAIN'"}]
      }
    }]
  }'
```

### 4. Set Up Monitoring Dashboards

```bash
# Create CloudWatch dashboard
aws cloudwatch put-dashboard \
  --dashboard-name AIFilmStudio-Dev \
  --dashboard-body file://dashboard.json
```

---

## 🐛 Troubleshooting

### Issue: Deployment Fails at NAT Gateway

**Error:**
```
CREATE_FAILED | AWS::EC2::NatGateway | NatGateway
Resource handler returned message: "Insufficient IP addresses in subnet"
```

**Solution:**
- Check subnet CIDR blocks
- Ensure subnet has enough IP addresses
- Increase subnet size if needed

### Issue: RDS Creation Timeout

**Error:**
```
CREATE_FAILED | AWS::RDS::DBInstance | Database
Resource handler returned message: "DB instance creation timeout"
```

**Solution:**
- Check RDS subnet group configuration
- Verify security group allows connections
- Check AWS service limits

### Issue: ECS Service Won't Start

**Error:**
```
ECS Service: Status = DRAINING
Tasks: Status = STOPPED
```

**Solution:**
```bash
# Check task logs
aws logs tail /ecs/ai-film-studio-backend --follow

# Check task definition
aws ecs describe-task-definition \
  --task-definition backend-task

# Check service events
aws ecs describe-services \
  --cluster ai-film-studio-dev \
  --services backend-service \
  --query 'services[0].events' \
  --output table
```

### Issue: CloudFront Distribution Slow

**Error:**
CloudFront takes 20+ minutes to create

**Solution:**
- This is normal! CloudFront distributions take 10-20 minutes
- DNS propagation adds 5-10 minutes
- Be patient, it will complete

---

## 📊 Deployment Summary

### First Deployment Timeline

```
00:00 - Start deployment
00:01 - Tests pass
00:02 - CDK synthesis complete
00:03 - Upload assets to S3
00:05 - CloudFormation stack creation starts
00:10 - VPC and networking complete
00:15 - Security groups and IAM roles complete
00:20 - S3 buckets created
00:30 - RDS database creation starts
00:40 - RDS database complete
00:45 - ECS cluster and service starting
00:50 - ECS service running
00:55 - CloudFront distribution creating
01:10 - CloudFront distribution complete
01:15 - All resources complete
01:20 - Stack outputs displayed
01:20 - Deployment complete! ✅
```

### Resource Count

- **Total Resources:** ~50-60
- **VPC Resources:** 10-15
- **Compute Resources:** 5-10
- **Storage Resources:** 5-10
- **Networking Resources:** 10-15
- **Monitoring Resources:** 5-10

### Cost Breakdown (First Month)

- **RDS:** $15-20
- **ECS Fargate:** $10-15
- **ALB:** $16
- **S3:** $1-5
- **CloudFront:** $1-10
- **ElastiCache:** $12
- **Data Transfer:** $5-20
- **NAT Gateway:** $32 (if used)
- **Total:** ~$90-130/month (dev environment)

---

## 🎉 Success!

Once deployment completes, you'll have:

✅ Fully functional infrastructure
✅ Backend API running on ECS
✅ PostgreSQL database
✅ S3 storage for assets
✅ CloudFront CDN
✅ Redis caching
✅ Message queues
✅ Monitoring and alerts

**Your AI Film Studio is now live on AWS! 🚀**

---

**Need help?** Check the troubleshooting section or review CloudFormation events in AWS Console.
