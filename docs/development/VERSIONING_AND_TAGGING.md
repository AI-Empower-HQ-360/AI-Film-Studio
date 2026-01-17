# Versioning and Tagging Guide

## Overview

This document describes the versioning, tagging, and release management practices for the AI Film Studio project.

## Semantic Versioning

This project follows [Semantic Versioning 2.0.0](https://semver.org/) (SemVer):

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backward-compatible manner
- **PATCH**: Backward-compatible bug fixes

### Version Tags

Version tags follow this format: `vMAJOR.MINOR.PATCH`

Examples:
- `v0.1.0` - Initial alpha release
- `v1.0.0` - First stable release
- `v1.2.3` - Minor update with bug fixes

## Git Tags

### Creating Version Tags

When creating a new release, tag the commit with the version number:

```bash
# Create an annotated tag
git tag -a v0.1.0 -m "Release version 0.1.0 - Initial alpha release"

# Push the tag to remote
git push origin v0.1.0

# Push all tags
git push origin --tags
```

### Tag Categories

#### 1. Version Tags (Release Tags)
Format: `v{version}` (e.g., `v0.1.0`, `v1.0.0`)
- Used for official releases
- Should be annotated tags with release notes
- Triggers CI/CD deployment pipelines

#### 2. Pre-release Tags
Format: `v{version}-{prerelease}` (e.g., `v1.0.0-alpha.1`, `v1.0.0-beta.2`, `v1.0.0-rc.1`)
- `alpha` - Early testing, unstable
- `beta` - Feature complete, testing phase
- `rc` - Release candidate, final testing

#### 3. Environment Tags
Format: `{env}-{date}` (e.g., `dev-2025-12-27`, `prod-2025-12-27`)
- Optional tags for tracking deployments
- Used for deployment audit trail

### Tag Naming Best Practices

1. **Always use annotated tags** for releases:
   ```bash
   git tag -a v1.0.0 -m "Release message"
   ```

2. **Include release notes** in the tag message

3. **Tag the merge commit** on the main/master branch

4. **Never reuse or move tags** - create a new version instead

## Resource Tags

### Python Package Tags

Located in:
- `setup.py` - Package classifiers and keywords
- `src/__init__.py` - Package metadata

```python
__version__ = "0.1.0"
__author__ = "AI-Empower-HQ-360"
__tags__ = ["AI", "Film Production", "Video Generation"]
```

### Docker Image Tags

Images are tagged with:
- Version number: `ai-film-studio:0.1.0`
- Latest: `ai-film-studio:latest`
- Environment: `ai-film-studio:dev`, `ai-film-studio:prod`
- Git commit: `ai-film-studio:sha-abc123f`

Labels in Dockerfile:
```dockerfile
LABEL version="0.1.0"
LABEL org.opencontainers.image.version="0.1.0"
```

### Terraform Resource Tags

All AWS resources are tagged via `common_tags` in Terraform:

```hcl
common_tags = {
  Environment = "dev"
  Project     = "AI-Film-Studio"
  ManagedBy   = "Terraform"
  Owner       = "AI-Empower-HQ-360"
  CreatedDate = "2025-12-27"
  CostCenter  = "Development"
  Version     = "0.1.0"
}
```

## Release Process

### 1. Pre-release Checklist

- [ ] Update version in `VERSION` file
- [ ] Update version in `setup.py`
- [ ] Update version in `src/__init__.py`
- [ ] Update version in `Dockerfile` labels
- [ ] Update `CHANGELOG.md` with release notes
- [ ] Run all tests: `pytest`
- [ ] Build and test Docker image
- [ ] Update documentation if needed

### 2. Create Release

```bash
# Ensure you're on main branch
git checkout main
git pull origin main

# Create and push tag
git tag -a v0.1.0 -m "Release v0.1.0

Initial alpha release featuring:
- Basic FastAPI backend
- AWS infrastructure setup
- Configuration management
"

git push origin v0.1.0
```

### 3. GitHub Release

1. Go to GitHub repository → Releases
2. Click "Create a new release"
3. Select the version tag
4. Add release title: "v0.1.0 - Initial Release"
5. Copy content from CHANGELOG.md
6. Attach any release artifacts
7. Publish release

### 4. Post-release

- [ ] Verify deployment in target environments
- [ ] Update project board/issues
- [ ] Announce release to team
- [ ] Monitor for issues

## Version Update Strategy

### For PATCH releases (0.1.x)
- Bug fixes
- Security patches
- Documentation updates
- No new features

### For MINOR releases (0.x.0)
- New features (backward compatible)
- Deprecations (with warnings)
- Performance improvements
- Significant documentation changes

### For MAJOR releases (x.0.0)
- Breaking API changes
- Removal of deprecated features
- Major architectural changes
- Migration guides required

## Changelog Management

All changes must be documented in `CHANGELOG.md` under the appropriate section:

- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security vulnerability fixes

## Automated Versioning

### CI/CD Integration

GitHub Actions workflows can automatically:
- Build and tag Docker images with version
- Deploy specific versions to environments
- Create GitHub releases
- Update documentation

### Version Extraction

Extract version from various sources:

```bash
# From VERSION file
cat VERSION

# From Python package
python -c "from src import __version__; print(__version__)"

# From Git tag
git describe --tags --abbrev=0
```

## Tags for Resource Classification

### Code Organization Tags

Module-level tags help categorize components:

```python
# In src/api/__init__.py
__tags__ = ["REST API", "FastAPI", "Backend", "Orchestration"]

# In src/services/__init__.py
__tags__ = ["Services", "Business Logic", "AI Processing"]
```

### Infrastructure Tags

AWS resources use tags for:
- **Cost tracking**: `CostCenter`, `Owner`
- **Environment identification**: `Environment`
- **Automation**: `ManagedBy`
- **Organization**: `Project`, `Team`

### Benefits

1. **Cost Allocation**: Track spending by project/environment
2. **Resource Management**: Identify and manage resources
3. **Automation**: Target resources for automated operations
4. **Compliance**: Meet organizational tagging policies
5. **Troubleshooting**: Quickly identify related resources

## Best Practices

1. **Consistency**: Use the same tag structure across all resources
2. **Documentation**: Document all tag meanings and usage
3. **Validation**: Validate tags in CI/CD pipelines
4. **Immutability**: Don't change historical release tags
5. **Automation**: Automate tagging where possible
6. **Review**: Regular audits of tagging compliance

## Troubleshooting

### Fixing incorrect tags

```bash
# Delete local tag
git tag -d v0.1.0

# Delete remote tag
git push origin :refs/tags/v0.1.0

# Create correct tag
git tag -a v0.1.0 -m "Corrected release message"
git push origin v0.1.0
```

**Note**: Only do this if the tag hasn't been released to production!

### Tag not showing in CI/CD

Ensure you pushed the tag:
```bash
git push origin --tags
```

Verify tag exists:
```bash
git ls-remote --tags origin
```

## References

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Git Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
- [Docker Image Tagging](https://docs.docker.com/engine/reference/commandline/tag/)
- [AWS Resource Tagging](https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html)
