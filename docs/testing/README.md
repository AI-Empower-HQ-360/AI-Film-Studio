# Testing Documentation

This folder contains documentation for testing the AI Film Studio project.

## Contents

- **AI_TESTING_TOOLS.md** - AI-powered testing tools and frameworks
- **FRONTEND_TESTING_CHECKLIST.md** - Frontend testing checklist
- **INSTALL_TEST_DEPENDENCIES.md** - How to install test dependencies
- **PRE_DEPLOYMENT_TESTING_GUIDE.md** - Pre-deployment testing checklist
- **TESTING_SETUP_COMPLETE.md** - Testing setup completion notes
- **TESTING_TOOLS_REQUIREMENTS.md** - Required testing tools
- **TEST_CASES_COMPLETE.md** - Complete test case documentation

## Test Commands

### Backend (Python)
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Frontend (Next.js)
```bash
cd frontend
npm run test        # Unit tests (Vitest)
npm run test:e2e    # E2E tests (Playwright)
```
