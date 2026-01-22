# CI/CD Documentation

This folder contains documentation for Continuous Integration and Continuous Deployment pipelines.

## Contents

- **AWS_CDK_COMPLETE.md** - AWS CDK infrastructure completion status
- **AWS_CDK_PUSH_STATUS.md** - CDK deployment push status
- **CI_CD_SUMMARY.md** - CI/CD pipeline summary
- **FRONTEND_COMPLETE.md** - Frontend deployment completion status

## CI/CD Workflow

1. **Dev** → Automatic deployment to development environment
2. **Sandbox** → QA testing environment
3. **Staging** → Pre-production UAT
4. **Main** → Production deployment

## Pipeline Configuration

- GitHub Actions: `.github/workflows/`
- AWS Amplify: `amplify.yml`
- Infrastructure: `infrastructure/`
