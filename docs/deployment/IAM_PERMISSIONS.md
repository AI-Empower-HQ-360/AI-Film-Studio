# IAM Permissions for AWS Amplify Deployment

## Overview

This document outlines the required IAM permissions for deploying and managing the AI Film Studio frontend on AWS Amplify. It covers user permissions, service roles, and security best practices.

---

## 🔑 Required IAM Permissions

### For Deployment Administrator

Users who will deploy and manage Amplify apps need these permissions:

#### Minimum Permissions (Read-Only + Deploy)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AmplifyAppManagement",
      "Effect": "Allow",
      "Action": [
        "amplify:CreateApp",
        "amplify:DeleteApp",
        "amplify:GetApp",
        "amplify:ListApps",
        "amplify:UpdateApp",
        "amplify:CreateBranch",
        "amplify:DeleteBranch",
        "amplify:GetBranch",
        "amplify:ListBranches",
        "amplify:UpdateBranch",
        "amplify:StartJob",
        "amplify:StopJob",
        "amplify:GetJob",
        "amplify:ListJobs"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AmplifyDomainManagement",
      "Effect": "Allow",
      "Action": [
        "amplify:CreateDomainAssociation",
        "amplify:DeleteDomainAssociation",
        "amplify:GetDomainAssociation",
        "amplify:UpdateDomainAssociation"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AmplifyEnvironmentVariables",
      "Effect": "Allow",
      "Action": [
        "amplify:GetBackendEnvironment",
        "amplify:CreateBackendEnvironment",
        "amplify:DeleteBackendEnvironment",
        "amplify:UpdateBackendEnvironment"
      ],
      "Resource": "*"
    }
  ]
}
```

#### Full Permissions (Production Use)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AmplifyFullAccess",
      "Effect": "Allow",
      "Action": [
        "amplify:*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CloudFrontManagement",
      "Effect": "Allow",
      "Action": [
        "cloudfront:CreateDistribution",
        "cloudfront:GetDistribution",
        "cloudfront:UpdateDistribution",
        "cloudfront:DeleteDistribution",
        "cloudfront:TagResource"
      ],
      "Resource": "*"
    },
    {
      "Sid": "Route53DomainManagement",
      "Effect": "Allow",
      "Action": [
        "route53:CreateHostedZone",
        "route53:GetHostedZone",
        "route53:ListHostedZones",
        "route53:ChangeResourceRecordSets",
        "route53:ListResourceRecordSets"
      ],
      "Resource": "*"
    },
    {
      "Sid": "ACMCertificateManagement",
      "Effect": "Allow",
      "Action": [
        "acm:RequestCertificate",
        "acm:DescribeCertificate",
        "acm:DeleteCertificate",
        "acm:AddTagsToCertificate"
      ],
      "Resource": "*"
    },
    {
      "Sid": "IAMRolePassthrough",
      "Effect": "Allow",
      "Action": [
        "iam:PassRole"
      ],
      "Resource": "arn:aws:iam::*:role/amplifyconsole-backend-role"
    },
    {
      "Sid": "CloudWatchLogsAccess",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogStreams"
      ],
      "Resource": "arn:aws:logs:*:*:log-group:/aws/amplify/*"
    }
  ]
}
```

---

## 🛡️ Service Roles

### Amplify Service Role

Amplify needs a service role to access resources on your behalf:

#### Create Service Role

**Via AWS Console:**

1. Go to **IAM Console** → **Roles** → **Create role**
2. **Trusted entity type:** AWS service
3. **Use case:** Amplify
4. Click **Next**
5. Attach policies:
   - `AdministratorAccess-Amplify` (AWS managed)
   - Or use custom policy below

**Custom Service Role Policy:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AmplifyServiceRole",
      "Effect": "Allow",
      "Action": [
        "cloudformation:CreateStack",
        "cloudformation:UpdateStack",
        "cloudformation:DeleteStack",
        "cloudformation:DescribeStacks",
        "cloudformation:DescribeStackEvents",
        "cloudformation:DescribeStackResources",
        "s3:CreateBucket",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:PutObject",
        "s3:DeleteObject",
        "cloudfront:CreateDistribution",
        "cloudfront:GetDistribution",
        "cloudfront:UpdateDistribution",
        "cloudfront:DeleteDistribution",
        "cloudfront:CreateInvalidation",
        "acm:RequestCertificate",
        "acm:DescribeCertificate",
        "acm:DeleteCertificate",
        "route53:ChangeResourceRecordSets",
        "route53:ListResourceRecordSets",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

**Trust Relationship:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "amplify.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

**Role Name:** `amplifyconsole-backend-role`

---

## 👥 User Permission Examples

### DevOps Administrator (Full Access)

**Use case:** Team lead who manages all deployments

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "amplify:*",
        "cloudfront:*",
        "route53:*",
        "acm:*",
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
```

### Developer (Deploy Only)

**Use case:** Developer who can trigger deployments but not modify infrastructure

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "amplify:GetApp",
        "amplify:ListApps",
        "amplify:GetBranch",
        "amplify:ListBranches",
        "amplify:StartJob",
        "amplify:GetJob",
        "amplify:ListJobs"
      ],
      "Resource": "*"
    }
  ]
}
```

### QA Tester (Read Only)

**Use case:** QA engineer who needs to view deployments and logs

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "amplify:GetApp",
        "amplify:ListApps",
        "amplify:GetBranch",
        "amplify:ListBranches",
        "amplify:GetJob",
        "amplify:ListJobs",
        "logs:DescribeLogStreams",
        "logs:GetLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 🔐 Security Best Practices

### 1. Principle of Least Privilege

**Grant only necessary permissions:**
- Start with minimal permissions
- Add permissions as needed
- Review permissions quarterly

**Example:**
```bash
# Good: Specific resource ARN
"Resource": "arn:aws:amplify:us-east-1:123456789012:apps/d1234abcd5678/*"

# Bad: Wildcard access
"Resource": "*"
```

### 2. Use IAM Groups

**Create groups for different roles:**

```bash
# Create groups
aws iam create-group --group-name AmplifyAdministrators
aws iam create-group --group-name AmplifyDevelopers
aws iam create-group --group-name AmplifyQA

# Attach policies
aws iam attach-group-policy \
  --group-name AmplifyAdministrators \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess-Amplify

# Add users to groups
aws iam add-user-to-group \
  --user-name john.doe \
  --group-name AmplifyDevelopers
```

### 3. Enable MFA

**Require MFA for production access:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "amplify:*",
      "Resource": "*",
      "Condition": {
        "Bool": {
          "aws:MultiFactorAuthPresent": "true"
        }
      }
    }
  ]
}
```

### 4. Audit Permissions

**Use AWS CloudTrail:**

```bash
# Enable CloudTrail for Amplify events
aws cloudtrail create-trail \
  --name amplify-audit-trail \
  --s3-bucket-name my-cloudtrail-bucket

# Log all Amplify API calls
aws cloudtrail put-event-selectors \
  --trail-name amplify-audit-trail \
  --event-selectors '[{
    "ReadWriteType": "All",
    "IncludeManagementEvents": true,
    "DataResources": [{
      "Type": "AWS::Amplify::App",
      "Values": ["arn:aws:amplify:*:*:apps/*"]
    }]
  }]'
```

### 5. Rotate Access Keys

**For programmatic access:**

```bash
# Create new access key
aws iam create-access-key --user-name deploy-user

# Delete old access key (after verifying new one works)
aws iam delete-access-key \
  --user-name deploy-user \
  --access-key-id AKIAIOSFODNN7EXAMPLE
```

**Rotation schedule:**
- Development: Every 90 days
- Production: Every 30 days
- Service accounts: Every 60 days

---

## 🔍 Permission Troubleshooting

### Error: "User is not authorized to perform: amplify:CreateApp"

**Cause:** Missing Amplify permissions

**Solution:**
1. Check user's IAM policies
2. Verify policy includes `amplify:CreateApp`
3. Ensure no explicit Deny statements
4. Check resource-based policies

**Verify permissions:**
```bash
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:user/deploy-user \
  --action-names amplify:CreateApp \
  --resource-arns "*"
```

### Error: "Could not assume role"

**Cause:** Missing `iam:PassRole` permission

**Solution:**
Add this to user policy:
```json
{
  "Effect": "Allow",
  "Action": "iam:PassRole",
  "Resource": "arn:aws:iam::123456789012:role/amplifyconsole-backend-role"
}
```

### Error: "Access Denied creating CloudFront distribution"

**Cause:** Amplify service role lacks CloudFront permissions

**Solution:**
1. Go to **IAM → Roles → amplifyconsole-backend-role**
2. Click **Add permissions → Attach policies**
3. Attach `CloudFrontFullAccess` or custom policy

---

## 📋 Quick Setup Script

### Create All IAM Resources

```bash
#!/bin/bash
# setup-amplify-iam.sh

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION="us-east-1"

# 1. Create Amplify service role
echo "Creating Amplify service role..."
aws iam create-role \
  --role-name amplifyconsole-backend-role \
  --assume-role-policy-document file://trust-policy.json

aws iam attach-role-policy \
  --role-name amplifyconsole-backend-role \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess-Amplify

# 2. Create IAM groups
echo "Creating IAM groups..."
aws iam create-group --group-name AmplifyAdministrators
aws iam create-group --group-name AmplifyDevelopers
aws iam create-group --group-name AmplifyQA

# 3. Attach policies to groups
echo "Attaching policies..."
aws iam put-group-policy \
  --group-name AmplifyAdministrators \
  --policy-name AmplifyAdminPolicy \
  --policy-document file://admin-policy.json

aws iam put-group-policy \
  --group-name AmplifyDevelopers \
  --policy-name AmplifyDevPolicy \
  --policy-document file://developer-policy.json

aws iam put-group-policy \
  --group-name AmplifyQA \
  --policy-name AmplifyQAPolicy \
  --policy-document file://qa-policy.json

echo "✅ IAM setup complete!"
echo "Next steps:"
echo "1. Add users to groups: aws iam add-user-to-group --user-name USERNAME --group-name AmplifyDevelopers"
echo "2. Verify service role in Amplify Console"
```

**trust-policy.json:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "amplify.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

---

## ✅ Verification Checklist

### Pre-Deployment
- [ ] Service role created: `amplifyconsole-backend-role`
- [ ] Service role has CloudFront permissions
- [ ] Service role has Route53 permissions (if using custom domain)
- [ ] Service role has ACM permissions (for SSL)
- [ ] IAM groups created for different roles
- [ ] Users assigned to appropriate groups

### Permissions Testing
- [ ] Admin user can create Amplify app
- [ ] Developer can trigger deployments
- [ ] QA can view logs and build status
- [ ] Service role can create CloudFront distribution
- [ ] MFA enforced for production access

### Security Audit
- [ ] CloudTrail enabled for Amplify events
- [ ] Access keys rotated within policy timeframe
- [ ] No wildcard permissions in production policies
- [ ] Resource-based policies reviewed
- [ ] IAM Access Analyzer findings reviewed

---

## 📚 Additional Resources

- [AWS Amplify IAM Permissions](https://docs.aws.amazon.com/amplify/latest/userguide/security-iam.html)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [CloudTrail for Amplify](https://docs.aws.amazon.com/amplify/latest/userguide/logging-using-cloudtrail.html)

---

## 🆘 Support

**IAM Issues:**
- AWS Support: https://console.aws.amazon.com/support
- IAM Forum: https://forums.aws.amazon.com/forum.jspa?forumID=76

**Internal Team:**
- Slack: #ai-film-studio-security
- Email: security@aifilmstudio.com

---

*Last updated: January 2026*
*Maintained by: AI Film Studio Security Team*
