# 🚀 Quick Deployment Reference

## TL;DR - Deploy in 3 Steps

### Option 1: CI/CD (Easiest)
```bash
# Push to develop branch
git push origin develop
# → Auto-deploys via GitHub Actions
```

### Option 2: Manual
```bash
cd infrastructure/aws-cdk
.venv-cdk\Scripts\activate
cdk deploy
```

---

## 📋 Pre-Deployment Checklist

- [ ] GitHub secrets configured (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ACCOUNT_ID)
- [ ] AWS IAM user created with PowerUserAccess
- [ ] Python 3.12 installed
- [ ] CDK CLI installed (`npm install -g aws-cdk`)
- [ ] AWS CLI configured (`aws configure`)

---

## 🎯 Deployment Commands

### Test First
```bash
cd infrastructure/aws-cdk
.venv-cdk\Scripts\activate
pytest tests/              # Run tests
cdk synth                  # Validate
cdk diff                   # Preview changes
```

### Deploy
```bash
cdk deploy                  # With prompts
cdk deploy --require-approval never  # Without prompts
```

### Verify
```bash
aws cloudformation describe-stacks --stack-name AIFilmStudio
aws ecs describe-services --cluster ai-film-studio-dev
```

---

## ⏱️ Deployment Timeline

| Phase | Duration | What's Happening |
|-------|----------|------------------|
| Preparation | 1-2 min | Tests, synthesis, upload assets |
| Networking | 5-10 min | VPC, subnets, NAT gateway |
| Database | 10-15 min | RDS PostgreSQL creation |
| Compute | 10-15 min | ECS cluster, service, containers |
| CDN | 10-15 min | CloudFront distribution |
| **Total** | **30-45 min** | First deployment |

---

## 📊 What Gets Created

- ✅ VPC with 6 subnets (2 AZs × 3 types)
- ✅ RDS PostgreSQL 16.1 database
- ✅ ECS Fargate cluster + service
- ✅ Application Load Balancer
- ✅ 3 S3 buckets (assets, characters, marketing)
- ✅ CloudFront distribution
- ✅ ElastiCache Redis cluster
- ✅ 4 SQS queues (jobs + DLQs)
- ✅ 3 SNS topics
- ✅ CloudWatch alarms
- ✅ Security groups & IAM roles

**Total:** ~50-60 AWS resources

---

## 🔍 Verify Deployment

### Stack Status
```bash
aws cloudformation describe-stacks \
  --stack-name AIFilmStudio \
  --query 'Stacks[0].StackStatus'
# Expected: CREATE_COMPLETE
```

### Get Outputs
```bash
aws cloudformation describe-stacks \
  --stack-name AIFilmStudio \
  --query 'Stacks[0].Outputs' \
  --output table
```

### Test Backend
```bash
BACKEND_URL=$(aws cloudformation describe-stacks \
  --stack-name AIFilmStudio \
  --query 'Stacks[0].Outputs[?OutputKey==`BackendURL`].OutputValue' \
  --output text)

curl $BACKEND_URL/health
```

---

## 🐛 Common Issues

### "Cannot find version 15.3 for postgres"
✅ **Fixed!** Using PostgreSQL 16.1

### "CDK toolkit stack not found"
```bash
cdk bootstrap aws://ACCOUNT-ID/us-east-1
```

### "Access Denied"
- Check IAM user permissions
- Verify GitHub secrets are correct

### Deployment takes too long
- NAT Gateway: 5-7 min (normal)
- RDS Database: 10-15 min (normal)
- CloudFront: 10-20 min (normal)
- **Total: 30-45 min is expected**

---

## 📚 Full Documentation

- **Detailed Guide:** `DETAILED_DEPLOYMENT_GUIDE.md` (comprehensive step-by-step)
- **CI/CD Setup:** `CI_CD_SETUP.md`
- **Deployment Fix:** `DEPLOYMENT_FIX.md`
- **Readiness:** `DEPLOYMENT_READINESS.md`

---

## 💰 Cost Estimate

**Development Environment:**
- Monthly: ~$60-100
- Components: RDS ($15-20), ECS ($10-15), ALB ($16), S3 ($1-5), CloudFront ($1-10), Redis ($12), Data Transfer ($5-20)

**Production Environment:**
- Monthly: ~$200-400
- Differences: Multi-AZ, larger instances, higher traffic

---

## ✅ Success Indicators

After deployment, you should see:

1. ✅ Stack status: `CREATE_COMPLETE`
2. ✅ ECS service: `RUNNING` with desired count
3. ✅ RDS database: `available`
4. ✅ ALB health checks: `healthy`
5. ✅ Stack outputs displayed with URLs

---

**Ready to deploy?** See `DETAILED_DEPLOYMENT_GUIDE.md` for complete walkthrough! 🚀
