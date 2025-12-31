# Branch-Specific Environment Documentation

This directory contains documentation specific to each environment branch.

## Purpose

Each environment branch (dev, sandbox, staging, main) should have its own configuration and documentation that describes:

- Environment-specific variables
- Deployment procedures
- Testing requirements
- Access controls
- Monitoring and alerting

## Branch Documentation Files

- `BRANCH_DEV.md` - Development environment documentation
- `BRANCH_SANDBOX.md` - Sandbox/QA environment documentation
- `BRANCH_STAGING.md` - Staging environment documentation
- `BRANCH_PRODUCTION.md` - Production environment documentation

## Creating Environment Branches

The repository uses the following branches:

1. **dev** - Development environment
2. **sandbox** - Testing/QA environment
3. **staging** - Pre-production environment
4. **main** - Production environment

These branches are created and managed according to the branching strategy defined in `BRANCHING_STRATEGY.md`.
