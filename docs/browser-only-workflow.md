# Browser-Only GitHub Development & Delivery

This repo is configured so you can build, test, and deploy AI Film Studio entirely from the browser—no local setup or VS Code desktop required.

## What you get
- **GitHub Codespaces**: cloud dev machine with VS Code in the browser, Docker, and Copilot preinstalled (see `.devcontainer/devcontainer.json`).
- **GitHub Copilot**: AI pair programmer to scaffold backend, frontend, workers, Terraform, tests, and workflows directly in the editor.
- **GitHub Actions**: CI on every push/PR, CD on `main` (guarded by secrets), and Terraform pipeline for infra changes.
- **GitHub Secrets**: central place to store AWS and deployment credentials for automated runs.

## Quick start (100% in the browser)
1. **Open Codespace**  
   - On GitHub: **Code → Codespaces → Create codespace**.  
   - Devcontainer auto-creates a Python venv and installs dependencies using CPU wheels for PyTorch.
2. **Build with Copilot**  
   - Use natural language comments/commands, e.g.  
     - `# Create FastAPI endpoint for /jobs that accepts a script and enqueues to SQS`  
     - `# Scaffold Terraform for VPC, ECS services, RDS, S3, and SQS`  
     - `# Add GitHub Actions job to build and deploy backend/worker/frontend images`
3. **Commit & push from Codespaces**  
   - Push changes; **CI** (`cloud-dev-platform` workflow) runs lint/tests automatically.
4. **Automatic deploys**  
   - On `main`, the **CD** job builds Docker images. It deploys when AWS secrets are present.
5. **Infra as code**  
   - For Terraform updates, push infra changes and run the `infra` job via **workflow_dispatch** (guarded by AWS secrets).

## Required GitHub secrets (configure in **Settings → Secrets and variables → Actions**)
- `AWS_ACCESS_KEY_ID`  
- `AWS_SECRET_ACCESS_KEY`  
- `AWS_REGION`  
- `ECR_REPO_BACKEND` (ECR URI for backend image)  
- `ECR_REPO_WORKER` (ECR URI for worker image)  
- `S3_FRONTEND_BUCKET` (bucket for built frontend)

## Workflows (see `.github/workflows/cloud-dev.yml`)
- **CI**: Runs on every push/PR; installs deps and executes `pytest -q`.
- **CD**: Runs on `main` after CI when AWS secrets exist; builds Docker image and is ready for ECR/ECS/EKS/S3 deploy steps.
- **Infra**: Runs on push or manual dispatch when AWS secrets exist; performs Terraform plan (and apply on manual dispatch).

## Daily browser-only loop
1. Open GitHub → launch Codespace.  
2. Use Copilot to generate/edit code, tests, Terraform, and workflow steps.  
3. Run tests in the Codespace terminal (`pytest -q`).  
4. Commit & push. Actions handle build/test/deploy automatically.  
5. Verify the deployed frontend (CloudFront/S3) and APIs (ECS/EKS).  
6. Repeat—never leave the browser.

## Optional: Browser automation
Ask Copilot to create Playwright tests and commit them; Actions will run them as part of CI once added.

## Troubleshooting
- **Dependencies**: Devcontainer installs with CPU PyTorch wheels. If GPU is needed, update `postCreateCommand` to install CUDA builds.  
- **Secrets missing**: CD/Infra jobs skip when AWS secrets aren’t set to avoid failures.  
- **Terraform**: Point `TERRAFORM_DIR` in the workflow to the environment you want to plan/apply.
