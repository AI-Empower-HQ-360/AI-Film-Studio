# 🔐 Secrets Setup Guide - What You Need to Do

## ❌ I Don't Need Your Secrets

**Important:** I (the AI assistant) do NOT need your actual secret values. You will add them directly to GitHub yourself.

## ✅ What You Need to Do

### Step 1: Generate Secrets (Using the Script)

Run the automated script to create IAM users and generate access keys:

```powershell
cd C:\Users\ctrpr\Projects\AI-Film-Studio\Deployment-Process
.\create-iam-users.ps1 -CreateAll
```

**What this does:**
- Creates IAM users in AWS
- Generates access keys
- Shows you the keys (you'll copy these to GitHub)

**Output example:**
```
User: dev-deployer
  Status: Created
  Access Key ID: AKIAIOSFODNN7EXAMPLE
  Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### Step 2: Copy Secrets to GitHub

You'll manually add these to GitHub (I don't see them):

1. **Go to GitHub:**
   - Repository → Settings → Environments → `dev`

2. **Add each secret:**
   - Click "Add secret"
   - Name: `AWS_ACCESS_KEY_ID`
   - Value: (paste from script output)
   - Click "Add secret"
   - Repeat for `AWS_SECRET_ACCESS_KEY` and `AWS_ACCOUNT_ID`

### Step 3: Get API Keys (For Production)

You'll need to get these from their respective services:

- **STABILITY_AI_API_KEY:** https://platform.stability.ai/account/keys
- **ELEVENLABS_API_KEY:** https://elevenlabs.io/app/settings/api-keys
- **OPENAI_API_KEY:** https://platform.openai.com/api-keys

Then add them to GitHub → Environments → `production`

## 📋 Complete Secrets Checklist

### Repository-Level (Shared)
- [ ] `AWS_REGION` = `us-east-1`
  - **Where:** Settings → Secrets → Actions → Repository secrets
  - **Value:** `us-east-1`

### Environment: dev
- [ ] `AWS_ACCESS_KEY_ID` (from script output)
- [ ] `AWS_SECRET_ACCESS_KEY` (from script output)
- [ ] `AWS_ACCOUNT_ID` = `996099991638`
  - **Where:** Settings → Environments → `dev`

### Environment: production
- [ ] `AWS_ACCESS_KEY_ID` (from script output)
- [ ] `AWS_SECRET_ACCESS_KEY` (from script output)
- [ ] `AWS_ACCOUNT_ID` = `996099991638` (or your production account)
- [ ] `STABILITY_AI_API_KEY` (from stability.ai)
- [ ] `ELEVENLABS_API_KEY` (from elevenlabs.io)
- [ ] `OPENAI_API_KEY` (from openai.com)
  - **Where:** Settings → Environments → `production`

## 🚀 Quick Setup Process

### 1. Run Script (Generates AWS Keys)
```powershell
.\create-iam-users.ps1 -CreateAll
```

### 2. Copy Output
- Copy the Access Key ID and Secret Access Key from the script output
- Save them temporarily (you'll paste into GitHub)

### 3. Add to GitHub
- Go to GitHub → Settings → Environments
- Add secrets to each environment
- Paste the values you copied

### 4. Delete Local Output File
```powershell
# After copying to GitHub, delete the output file
Remove-Item iam-users-output-*.txt
```

## ⚠️ Security Notes

1. **Never share secrets with me** - I don't need them
2. **Never commit secrets to git** - They're only in GitHub Secrets
3. **Delete script output files** - After copying to GitHub
4. **Rotate keys regularly** - Every 90 days recommended

## 🆘 What I Can Help With

I can help you:
- ✅ Understand what secrets you need
- ✅ Run the script to generate AWS keys
- ✅ Guide you through adding secrets to GitHub
- ✅ Troubleshoot if secrets aren't working
- ✅ Explain what each secret is for

I **cannot** help you:
- ❌ Get your actual secret values (you do this)
- ❌ Access your GitHub account (you do this)
- ❌ See what secrets you've added (they're encrypted)

## 📚 Related Documentation

- **GITHUB_ENVIRONMENTS_SETUP.md** - Complete setup guide
- **ENVIRONMENT_SETUP_CHECKLIST.md** - Step-by-step checklist
- **create-iam-users.ps1** - Script to generate AWS keys

---

**Summary:** You'll generate secrets using the script, then manually add them to GitHub. I'll guide you through the process, but you'll do the actual secret entry yourself.
