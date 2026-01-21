# How to Get AWS Access Keys for Amplify Deployment

## Quick Guide: Creating AWS Access Keys

### Step 1: Log into AWS Console
1. Go to: https://console.aws.amazon.com/
2. Sign in with your AWS account credentials

### Step 2: Navigate to IAM
1. In the search bar at the top, type "IAM"
2. Click on **"IAM"** (Identity and Access Management)
3. Or go directly to: https://console.aws.amazon.com/iam/

### Step 3: Create Access Keys

#### Option A: For Your User Account
1. In the left sidebar, click **"Users"**
2. Click on your username
3. Click the **"Security credentials"** tab
4. Scroll down to **"Access keys"** section
5. Click **"Create access key"**
6. Select use case: **"Command Line Interface (CLI)"**
7. Check the confirmation box
8. Click **"Next"**
9. (Optional) Add a description tag
10. Click **"Create access key"**
11. **IMPORTANT**: Copy both keys NOW:
    - **Access key ID** (looks like: AKIAIOSFODNN7EXAMPLE)
    - **Secret access key** (only shown once!)
12. Click **"Download .csv file"** to save them securely
13. Click **"Done"**

#### Option B: Create New IAM User (Recommended for Production)
1. In IAM console, click **"Users"** → **"Create user"**
2. Username: `amplify-deploy-user`
3. Check **"Provide user access to AWS Management Console"** (optional)
4. Click **"Next"**
5. Select **"Attach policies directly"**
6. Search and attach these policies:
   - `AdministratorAccess-Amplify`
   - `IAMFullAccess` (for role creation)
7. Click **"Next"** → **"Create user"**
8. Click on the new user
9. Go to **"Security credentials"** tab
10. Click **"Create access key"**
11. Follow steps from Option A

### Step 4: Keep Keys Secure
⚠️ **IMPORTANT SECURITY NOTES:**
- Never commit access keys to Git
- Don't share them publicly
- Rotate keys every 90 days
- Use separate keys for different projects
- Store in password manager or AWS Secrets Manager

---

## Using Your AWS Credentials

Once you have your keys, you have 3 options:

### Option 1: Interactive Configuration (Easiest)
```bash
aws configure
```
Then enter when prompted:
- AWS Access Key ID: [paste your key]
- AWS Secret Access Key: [paste your secret]
- Default region name: us-east-1
- Default output format: json

### Option 2: Environment Variables (Current Session)
```bash
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export AWS_DEFAULT_REGION="us-east-1"
```

### Option 3: Create Credentials File
```bash
mkdir -p ~/.aws
cat > ~/.aws/credentials <<EOF
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
EOF

cat > ~/.aws/config <<EOF
[default]
region = us-east-1
output = json
EOF
```

---

## Verify Authentication

After configuring, test your credentials:
```bash
aws sts get-caller-identity
```

You should see output like:
```json
{
    "UserId": "AIDAI...",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-username"
}
```

---

## Quick Reference: What You Need

✅ **GitHub Token** (you have this):
```
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
```

❓ **AWS Access Key ID** (get from IAM):
```
AKIAIOSFODNN7EXAMPLE  ← looks like this
```

❓ **AWS Secret Access Key** (get from IAM):
```
wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY  ← looks like this
```

---

## Troubleshooting

### "Access Denied" when creating access keys
- You might not have permission to create keys for your user
- Ask your AWS administrator to:
  - Create access keys for you, OR
  - Grant you `iam:CreateAccessKey` permission

### "Unable to locate credentials"
- Make sure you ran `aws configure` successfully
- Check that credentials are saved in `~/.aws/credentials`
- Verify environment variables are set (run `echo $AWS_ACCESS_KEY_ID`)

### "Invalid security token"
- Your access keys might be deactivated
- Check in IAM console if keys are "Active"
- You may need to create new keys

---

## Next Steps

After getting your AWS credentials:

1. **Configure AWS CLI:**
   ```bash
   aws configure
   ```

2. **Run deployment script:**
   ```bash
   ./scripts/deploy-to-amplify.sh
   ```

3. **Or use the quick deploy command (I'll create this for you)**

---

## Security Best Practices

1. ✅ Store keys in AWS Secrets Manager or password manager
2. ✅ Use IAM roles instead of keys when possible
3. ✅ Rotate access keys every 90 days
4. ✅ Use MFA for production accounts
5. ✅ Create separate users for different purposes
6. ❌ Never commit keys to Git
7. ❌ Never share keys via email or messaging
8. ❌ Don't use root account access keys

---

**Need Help?**
- AWS IAM Documentation: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
- AWS Security Best Practices: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
