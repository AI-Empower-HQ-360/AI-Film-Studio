# Tags Quick Reference Guide

## Overview

This repository uses multiple types of tags for organization, versioning, and resource management.

## Types of Tags

### 1. Git Version Tags

**Location**: Git repository  
**Format**: `vMAJOR.MINOR.PATCH` (e.g., `v0.1.0`, `v1.2.3`)  
**Purpose**: Mark release points in the repository

```bash
# List all version tags
git tag -l "v*"

# Show tag details
git show v0.1.0

# Create new tag
git tag -a v0.1.1 -m "Release message"

# Push tag to remote
git push origin v0.1.1
```

**Current Tag**: `v0.1.0`

### 2. Python Package Tags

**Location**: `src/__init__.py`, `src/*/__init__.py`  
**Purpose**: Package and module metadata

```python
# In src/__init__.py
__version__ = "0.1.0"
__author__ = "AI-Empower-HQ-360"
__tags__ = ["AI", "Film Production", "Video Generation", ...]
```

**Access in Code**:
```python
import src
print(src.__version__)  # "0.1.0"
print(src.__tags__)     # ["AI", "Film Production", ...]
```

### 3. PyPI Classifiers (Setup.py)

**Location**: `setup.py`  
**Purpose**: Package classification for PyPI

```python
classifiers=[
    "Development Status :: 3 - Alpha",
    "Topic :: Multimedia :: Video",
    "License :: OSI Approved :: MIT License",
    ...
]
keywords=["ai", "film", "video-generation", ...]
```

### 4. Docker Image Tags

**Location**: Dockerfile labels, Docker commands  
**Purpose**: Container metadata and versioning

**In Dockerfile**:
```dockerfile
LABEL version="0.1.0"
LABEL org.opencontainers.image.version="0.1.0"
LABEL org.opencontainers.image.title="AI Film Studio API"
```

**Docker Commands**:
```bash
# Build with version tag
docker build -t ai-film-studio:0.1.0 .
docker build -t ai-film-studio:latest .

# Tag for different environments
docker tag ai-film-studio:0.1.0 ai-film-studio:dev
docker tag ai-film-studio:0.1.0 ai-film-studio:prod

# Tag with commit SHA
docker tag ai-film-studio:0.1.0 ai-film-studio:sha-abc123f
```

### 5. AWS Resource Tags (Terraform)

**Location**: `infrastructure/terraform/environments/*/main.tf`  
**Purpose**: Resource organization, cost tracking, automation

```hcl
common_tags = {
  Environment = "dev"
  Project     = "AI-Film-Studio"
  Version     = "0.1.0"
  ManagedBy   = "Terraform"
  Owner       = "AI-Empower-HQ-360"
  CreatedDate = "2025-12-27"
  CostCenter  = "Development"
}
```

**Benefits**:
- Cost allocation and tracking
- Resource identification
- Automated operations
- Compliance requirements

### 6. GitHub Release Tags

**Location**: GitHub Releases page  
**Purpose**: Public release announcements

**Categories** (from `.github/release.yml`):
- 🚀 New Features
- 🐛 Bug Fixes
- 📚 Documentation
- 🏗️ Infrastructure
- 🔒 Security
- ⚡ Performance
- 🧪 Testing
- 🔧 Maintenance

## Tag Consistency

All version references are kept in sync:
- `VERSION` file: `0.1.0`
- `src/__init__.py`: `__version__ = "0.1.0"`
- `setup.py`: `version="0.1.0"`
- `Dockerfile`: `LABEL version="0.1.0"`
- `main.tf`: `Version = "0.1.0"`
- Git tag: `v0.1.0`

## Version Management

Use the provided script for consistency:

```bash
# Check current version
./scripts/version-tag.sh version

# Bump version
./scripts/version-tag.sh bump patch|minor|major

# Manual update
./scripts/version-tag.sh update 1.2.3
```

## Common Tasks

### Create a New Release

1. Update version:
   ```bash
   ./scripts/version-tag.sh bump minor
   ```

2. Update CHANGELOG.md with changes

3. Commit changes:
   ```bash
   git add .
   git commit -m "Release version X.Y.Z"
   ```

4. Create and push tag:
   ```bash
   git tag -a vX.Y.Z -m "Release message"
   git push origin main
   git push origin vX.Y.Z
   ```

5. Create GitHub Release from tag

### Deploy with Specific Version

```bash
# Docker
docker build -t myapp:1.2.3 .
docker push myapp:1.2.3

# Kubernetes
kubectl set image deployment/myapp myapp=myapp:1.2.3

# Terraform (uses Version tag)
terraform apply -var="version=1.2.3"
```

### Find Resources by Tag

```bash
# AWS CLI - Find all dev resources
aws resourcegroupstaggingapi get-resources \
  --tag-filters Key=Environment,Values=dev

# AWS CLI - Find by version
aws resourcegroupstaggingapi get-resources \
  --tag-filters Key=Version,Values=0.1.0

# AWS CLI - Cost allocation by project
aws ce get-cost-and-usage \
  --time-period Start=2025-01-01,End=2025-02-01 \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=TAG,Key=Project
```

## Best Practices

1. ✅ **Keep versions synchronized** across all files
2. ✅ **Use semantic versioning** (MAJOR.MINOR.PATCH)
3. ✅ **Tag all releases** with annotated tags
4. ✅ **Update CHANGELOG.md** for every release
5. ✅ **Tag AWS resources** consistently
6. ✅ **Use the version script** to prevent mistakes
7. ✅ **Never reuse or modify** existing release tags
8. ✅ **Document changes** in tag messages

## Troubleshooting

### Version Mismatch

Check all version locations:
```bash
cat VERSION
grep "__version__" src/__init__.py
grep "version=" setup.py
grep "LABEL version" Dockerfile
grep "Version" infrastructure/terraform/environments/dev/main.tf
git describe --tags
```

### Fix All Versions

```bash
./scripts/version-tag.sh update 0.1.0
```

### Delete Wrong Tag

```bash
# Local
git tag -d v0.1.0

# Remote (be careful!)
git push origin :refs/tags/v0.1.0
```

## References

- [Semantic Versioning](https://semver.org/)
- [Full Documentation](./docs/development/VERSIONING_AND_TAGGING.md)
- [CHANGELOG](./CHANGELOG.md)
- [VERSION File](./VERSION)

## Quick Commands

```bash
# Current version
cat VERSION

# All tags
git tag -l

# Version info
python -c "import src; print(src.__version__)"

# Docker labels
docker inspect ai-film-studio:latest | grep -A 10 Labels

# Terraform version
grep -A 5 "common_tags" infrastructure/terraform/environments/dev/main.tf
```
