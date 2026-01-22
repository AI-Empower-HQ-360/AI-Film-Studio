# Pre-Deployment Testing Guide

**AI Film Studio - Complete Testing Checklist Before Deployment**

---

## 🎯 Testing Pyramid

```
      🔺 E2E Tests (Critical Paths)
     🔺🔺 Integration Tests (Service Integration)
    🔺🔺🔺 Unit Tests (All Functions)
```

---

## ✅ Required Tests Before Deployment

### **1. Unit Tests** ✅ **MANDATORY**

**Purpose:** Test individual functions and methods in isolation

**Location:** `tests/unit/`

**What to Test:**
- ✅ All 8 engine modules (Character, Writing, Pre-Production, etc.)
- ✅ Service classes and utilities
- ✅ Data validation and transformation
- ✅ Error handling and edge cases
- ✅ Business logic correctness

**Command:**
```bash
pytest tests/unit/ -v --cov=src --cov-report=term-missing
```

**Acceptance Criteria:**
- ✅ All unit tests pass
- ✅ Code coverage ≥ 80%
- ✅ No critical functions untested
- ✅ All engines have test coverage

**Status:** ✅ **5,500+ lines of unit tests ready**

---

### **2. Integration Tests** ✅ **MANDATORY**

**Purpose:** Test interactions between components and services

**Location:** `tests/integration/`

**What to Test:**
- ✅ API endpoints (`test_api_endpoints.py`)
- ✅ Full production pipeline (`test_full_pipeline.py`)
- ✅ AI service integrations (`test_ai_apis.py`)
- ✅ AWS services (S3, SQS, RDS) (`test_aws_services.py`)
- ✅ Database operations
- ✅ External API integrations

**Command:**
```bash
pytest tests/integration/ -v -m integration
```

**Acceptance Criteria:**
- ✅ All API endpoints respond correctly
- ✅ Database operations succeed
- ✅ External services integrate properly
- ✅ Error scenarios handled gracefully

**Status:** ✅ **Integration tests ready**

---

### **3. End-to-End (E2E) Tests** ✅ **MANDATORY**

**Purpose:** Test complete user workflows from start to finish

**Location:** `tests/e2e/` and `frontend/e2e/`

**What to Test:**
- ✅ Complete film production pipeline
- ✅ API workflows (create project → generate → complete)
- ✅ Character creation workflows
- ✅ Video generation workflows
- ✅ Voice synthesis workflows
- ✅ User journey: Login → Create → Generate → Download

**Command:**
```bash
# Backend E2E
pytest tests/e2e/ -v -m e2e

# Frontend E2E
cd frontend && npm run test:e2e
```

**Acceptance Criteria:**
- ✅ Complete workflows execute successfully
- ✅ All critical user paths tested
- ✅ Error recovery tested
- ✅ Data persistence verified

**Status:** ✅ **E2E tests ready**

---

### **4. Smoke Tests** ⚠️ **CRITICAL FOR PRODUCTION**

**Purpose:** Quick validation that critical features work after deployment

**Location:** Create `tests/smoke/`

**What to Test:**
- ✅ Health check endpoints respond
- ✅ API is accessible
- ✅ Database connections work
- ✅ Authentication/authorization works
- ✅ Basic CRUD operations succeed
- ✅ Frontend loads without errors

**Command:**
```bash
pytest tests/smoke/ -v -m smoke
```

**Acceptance Criteria:**
- ✅ All smoke tests pass (< 2 minutes)
- ✅ Core functionality accessible
- ✅ No blocking errors

**Status:** ⚠️ **Need to create smoke tests**

---

### **5. Performance Tests** ⚠️ **REQUIRED FOR PRODUCTION**

**Purpose:** Ensure system meets performance requirements

**Location:** `tests/performance/`

**What to Test:**
- ✅ API response times (< 200ms p95)
- ✅ Video generation time (< 5 min for 1-min video)
- ✅ Concurrent user handling (100+ users)
- ✅ Database query performance
- ✅ Memory usage and leaks
- ✅ Load handling (spike tests)

**Command:**
```bash
pytest tests/performance/ -v -m performance
pytest tests/performance/ --benchmark-only
```

**Acceptance Criteria:**
- ✅ API p95 latency < 200ms
- ✅ Video generation < 5 minutes
- ✅ System handles 100+ concurrent users
- ✅ No memory leaks detected
- ✅ CPU usage < 80% under load

**Status:** ✅ **Performance tests framework ready**

---

### **6. Security Tests** ⚠️ **MANDATORY**

**Purpose:** Identify security vulnerabilities

**What to Test:**
- ✅ Authentication and authorization
- ✅ Input validation and sanitization
- ✅ SQL injection prevention
- ✅ XSS prevention
- ✅ CSRF protection
- ✅ API rate limiting
- ✅ Secrets management
- ✅ HTTPS enforcement
- ✅ Dependency vulnerabilities

**Command:**
```bash
# Dependency scanning
pip-audit
npm audit

# Code security scanning (if configured)
bandit -r src/
safety check
```

**Acceptance Criteria:**
- ✅ No high/critical vulnerabilities
- ✅ Authentication working correctly
- ✅ Input validation in place
- ✅ Dependencies up to date

**Status:** ⚠️ **Need security test suite**

---

### **7. Accessibility Tests** ✅ **REQUIRED FOR PRODUCTION**

**Purpose:** Ensure WCAG 2.1 AA compliance

**Location:** `frontend/e2e/accessibility.spec.ts`

**What to Test:**
- ✅ Keyboard navigation
- ✅ Screen reader compatibility
- ✅ Color contrast ratios
- ✅ ARIA labels and roles
- ✅ Focus management
- ✅ Alternative text for images

**Command:**
```bash
cd frontend && npm run test:e2e -- --grep accessibility
```

**Acceptance Criteria:**
- ✅ WCAG 2.1 AA compliance
- ✅ All interactive elements keyboard accessible
- ✅ Color contrast ratios meet standards

**Status:** ✅ **Accessibility tests ready**

---

### **8. Browser Compatibility Tests** ✅ **REQUIRED**

**Purpose:** Ensure app works across browsers

**What to Test:**
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

**Command:**
```bash
cd frontend && npm run test:e2e
```

**Acceptance Criteria:**
- ✅ Tests pass on all major browsers
- ✅ No critical rendering issues
- ✅ Mobile responsive on all devices

**Status:** ✅ **Playwright configured for multiple browsers**

---

### **9. Load & Stress Tests** ⚠️ **RECOMMENDED FOR PRODUCTION**

**Purpose:** Verify system handles expected load

**Tools:** Locust, pytest-benchmark

**What to Test:**
- ✅ 1,000 concurrent users
- ✅ API rate limits
- ✅ Database connection pooling
- ✅ Memory under load
- ✅ GPU worker scaling
- ✅ Queue processing capacity

**Command:**
```bash
# Using Locust
locust -f tests/performance/locustfile.py --host=http://localhost:8000

# Using pytest-benchmark
pytest tests/performance/ --benchmark-only
```

**Acceptance Criteria:**
- ✅ System handles expected load
- ✅ Auto-scaling triggers correctly
- ✅ No degradation under load
- ✅ Graceful degradation if overloaded

**Status:** ✅ **Locust configured**

---

### **10. Regression Tests** ✅ **ONGOING**

**Purpose:** Ensure new changes don't break existing features

**Command:**
```bash
pytest tests/ -v --tb=short
```

**Acceptance Criteria:**
- ✅ All existing tests still pass
- ✅ No breaking changes introduced

**Status:** ✅ **Continuous regression testing**

---

## 📋 Pre-Deployment Testing Checklist

### **Before Staging Deployment**

#### **Code Quality** ✅
- [ ] All unit tests pass
- [ ] Code coverage ≥ 80%
- [ ] Linting passes (flake8/ruff)
- [ ] Type checking passes (mypy)
- [ ] Code formatting (black)

#### **Integration** ✅
- [ ] Integration tests pass
- [ ] API endpoints tested
- [ ] Database operations verified
- [ ] External services integrated

#### **E2E** ✅
- [ ] Critical user workflows tested
- [ ] Complete production pipeline tested
- [ ] Error scenarios handled

---

### **Before Production Deployment**

#### **All Staging Tests** ✅
- [ ] All staging tests pass
- [ ] Staging environment validated

#### **Smoke Tests** ⚠️
- [ ] Health checks pass
- [ ] Core features accessible
- [ ] No blocking errors

#### **Performance** ⚠️
- [ ] Response times meet SLOs
- [ ] Load tests passed
- [ ] Memory usage acceptable
- [ ] No performance regressions

#### **Security** ⚠️
- [ ] Security scan passed
- [ ] No vulnerabilities (high/critical)
- [ ] Authentication tested
- [ ] Input validation verified
- [ ] Rate limiting active

#### **Accessibility** ✅
- [ ] WCAG 2.1 AA compliance
- [ ] Keyboard navigation works
- [ ] Screen reader compatible

#### **Browser Compatibility** ✅
- [ ] All major browsers tested
- [ ] Mobile devices tested
- [ ] No rendering issues

#### **Load Testing** ⚠️
- [ ] Expected load handled
- [ ] Auto-scaling verified
- [ ] Queue processing verified

#### **Infrastructure** ✅
- [ ] AWS CDK stack deployed
- [ ] Database migrations applied
- [ ] Environment variables set
- [ ] Secrets configured
- [ ] Monitoring active

#### **Documentation** ✅
- [ ] API documentation updated
- [ ] Deployment guide reviewed
- [ ] Runbooks available
- [ ] Incident response plan ready

---

## 🚀 Pre-Deployment Testing Workflow

### **Step 1: Local Testing**

```bash
# 1. Run all unit tests
pytest tests/unit/ -v --cov=src

# 2. Run integration tests (requires services)
pytest tests/integration/ -v -m integration

# 3. Run E2E tests
pytest tests/e2e/ -v -m e2e

# 4. Frontend tests
cd frontend
npm run test:run
npm run test:e2e

# 5. Performance benchmarks
pytest tests/performance/ --benchmark-only
```

### **Step 2: CI/CD Pipeline (Automated)**

The following run automatically on push:

```yaml
# GitHub Actions runs:
- Backend CI (unit + integration tests)
- Frontend CI (unit tests + linting)
- Frontend E2E (Playwright tests)
- Security scanning (CodeQL)
- Code coverage reporting
```

### **Step 3: Staging Environment**

```bash
# Deploy to staging
git push origin staging

# Run smoke tests on staging
pytest tests/smoke/ -v --base-url=https://staging.aifilmstudio.com

# Run load tests
locust -f tests/performance/locustfile.py --host=https://staging.aifilmstudio.com
```

### **Step 4: Pre-Production Checklist**

- [ ] All tests pass on staging
- [ ] Performance benchmarks met
- [ ] Security scan clean
- [ ] Documentation updated
- [ ] Rollback plan ready
- [ ] Monitoring configured

### **Step 5: Production Deployment**

```bash
# Merge to main triggers production deployment
git push origin main

# Immediate smoke tests
pytest tests/smoke/ -v --base-url=https://aifilmstudio.com
```

---

## 📊 Test Coverage Requirements

### **Minimum Coverage Targets**

| Component | Target Coverage | Current Status |
|-----------|----------------|----------------|
| **Backend Engines** | ≥ 85% | ⚠️ Check needed |
| **API Endpoints** | ≥ 90% | ⚠️ Check needed |
| **Business Logic** | ≥ 80% | ⚠️ Check needed |
| **Utilities** | ≥ 75% | ⚠️ Check needed |
| **Frontend Components** | ≥ 70% | ⚠️ Check needed |

### **Critical Path Coverage** (Must be 100%)
- ✅ Authentication/Authorization
- ✅ Payment/Credit processing
- ✅ Video generation pipeline
- ✅ Error handling

---

## 🔍 Test Execution Commands

### **Complete Test Suite**

```bash
# All backend tests
pytest tests/ -v --cov=src --cov-report=html --cov-report=term

# All frontend tests
cd frontend && npm run test:all

# Quick smoke test
pytest tests/smoke/ -v -m smoke

# Performance test
pytest tests/performance/ --benchmark-only

# Load test
locust -f tests/performance/locustfile.py
```

### **By Priority**

```bash
# Critical tests only (fast, < 5 min)
pytest tests/unit/ tests/smoke/ -v -m "unit or smoke"

# Full test suite (< 30 min)
pytest tests/ -v --maxfail=5

# Extended suite with E2E (< 60 min)
pytest tests/ -v && cd frontend && npm run test:e2e
```

---

## ⚠️ Missing Test Types (Need to Create)

### **1. Smoke Tests** 🔴 **HIGH PRIORITY**

**Create:** `tests/smoke/test_smoke.py`

**Include:**
- Health check endpoint
- Basic API connectivity
- Database connectivity
- Authentication flow
- One complete workflow

### **2. Security Tests** 🔴 **HIGH PRIORITY**

**Create:** `tests/security/test_security.py`

**Include:**
- Authentication bypass attempts
- SQL injection attempts
- XSS attempts
- CSRF protection
- Rate limiting validation

### **3. Contract Tests** 🟡 **MEDIUM PRIORITY**

**Create:** `tests/contract/`

**Include:**
- API contract validation
- Schema validation
- Version compatibility

---

## ✅ Current Testing Status

### **Ready & Configured** ✅

- ✅ Unit tests (5,500+ lines)
- ✅ Integration tests
- ✅ E2E tests (backend & frontend)
- ✅ Performance test framework
- ✅ Accessibility tests
- ✅ Browser compatibility (Playwright)

### **Need to Create** ⚠️

- ⚠️ Smoke tests (CRITICAL)
- ⚠️ Security test suite (CRITICAL)
- ⚠️ Contract tests (Recommended)

---

## 🎯 Pre-Deployment Test Execution Order

```
1. Unit Tests (5 min)
   ↓
2. Integration Tests (10 min)
   ↓
3. E2E Tests (15 min)
   ↓
4. Smoke Tests (2 min) ⚠️ CREATE
   ↓
5. Performance Tests (10 min)
   ↓
6. Security Tests (5 min) ⚠️ CREATE
   ↓
7. Accessibility Tests (5 min)
   ↓
8. Load Tests (optional, 30 min)
   ↓
✅ READY FOR DEPLOYMENT
```

**Total Time:** ~60 minutes (with optional load tests)

---

## 📝 Testing Documentation

- ✅ `TESTING_TOOLS_REQUIREMENTS.md` - Tools needed
- ✅ `TESTING_SETUP_COMPLETE.md` - Setup guide
- ✅ `tests/README.md` - Test structure
- ✅ `PRE_DEPLOYMENT_TESTING_GUIDE.md` - This document

---

## 🚨 Critical Tests (Must Pass Before Production)

1. ✅ All unit tests pass
2. ✅ All integration tests pass
3. ✅ Health check endpoint responds
4. ✅ Authentication works
5. ✅ Database connections successful
6. ✅ Video generation pipeline completes
7. ✅ Error handling works
8. ✅ Security scan clean
9. ✅ Performance benchmarks met
10. ✅ Smoke tests pass

---

**Status:** ✅ **Testing framework ready, smoke & security tests needed**
