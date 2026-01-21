# Install Test Dependencies - Quick Guide

**Status:** Test files ready ✅ | Dependencies need installation ⚠️

---

## 🎯 Current Status

### ✅ **AVAILABLE (Already in Repo)**
- ✅ Test Framework: `pytest.ini` configured with coverage, HTML reports, parallel execution
- ✅ Test Files: 5,500+ lines across unit, integration, E2E, performance tests
- ✅ Fixtures: `conftest.py` & `conftest_enhanced.py` with mocks for AWS, OpenAI, ElevenLabs
- ✅ Requirements: `tests/requirements-test.txt` with all dependencies listed
- ✅ Source Code: Full `src/` directory with engines, services, API to test

### ⚠️ **NEEDS INSTALLATION**
The test dependencies are **NOT installed yet**. Only `httpx` may be present.

---

## 🚀 Installation Command

### **Option 1: Install from requirements file (Recommended)**

```bash
pip install -r tests/requirements-test.txt
```

### **Option 2: Install manually**

```bash
# Core testing framework
pip install pytest>=7.4.0 pytest-asyncio>=0.21.0 pytest-cov>=4.1.0

# Parallel execution & reporting
pip install pytest-xdist>=3.3.0 pytest-html>=4.1.0

# Mocking & utilities
pip install pytest-mock>=3.12.0 pytest-timeout>=2.2.0 freezegun>=1.2.0

# HTTP testing
pip install httpx>=0.25.2 requests>=2.32.4 requests-mock>=1.11.0

# Test data generation
pip install faker>=20.1.0 factory-boy>=3.3.0 responses>=0.24.1

# Performance testing
pip install pytest-benchmark>=4.0.0 locust>=2.18.3

# JSON reports
pip install pytest-json-report>=1.5.0

# Optional: AWS mocking
pip install moto>=5.0.0
```

---

## 📋 What Gets Installed

| Package | Purpose | Priority |
|---------|---------|----------|
| **pytest** | Core test runner | ✅ Essential |
| **pytest-asyncio** | Async test support | ✅ Essential |
| **pytest-cov** | Code coverage | ✅ Essential |
| **pytest-xdist** | Parallel test execution | ✅ Essential |
| **pytest-html** | HTML test reports | ✅ Essential |
| **pytest-mock** | Mocking utilities | ✅ Essential |
| **pytest-timeout** | Test timeout handling | ✅ Essential |
| **httpx** | Async HTTP testing | ✅ Essential |
| **requests** | HTTP client | ✅ Essential |
| **requests-mock** | HTTP request mocking | ✅ Essential |
| **faker** | Fake data generation | ✅ Essential |
| **factory-boy** | Test fixtures | ✅ Essential |
| **responses** | HTTP mocking library | ✅ Essential |
| **freezegun** | Date/time mocking | ✅ Essential |
| **pytest-benchmark** | Performance testing | ⭐ Recommended |
| **pytest-json-report** | JSON reports for CI/CD | ⭐ Recommended |
| **locust** | Load testing | ⭐ Recommended |
| **moto** | AWS service mocking | ⚙️ Optional |

---

## ✅ Verification

After installation, verify everything works:

```bash
# Check pytest is installed
pytest --version

# Check if all required packages are available
python -c "import pytest, pytest_asyncio, pytest_cov, pytest_xdist, pytest_html, pytest_mock, freezegun, faker; print('✅ All packages installed!')"

# Run a quick test
pytest tests/unit/ -v --collect-only

# Run tests with coverage
pytest tests/unit/ -v --cov=src --cov-report=term-missing
```

---

## 🎯 Quick Start After Installation

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run with coverage
pytest tests/unit/ --cov=src --cov-report=html

# Run in parallel (faster)
pytest tests/ -n auto

# Generate HTML report
pytest tests/ --html=test-report.html --self-contained-html

# Run specific test file
pytest tests/unit/test_character_engine.py -v

# Run tests by marker
pytest -m unit  # Only unit tests
pytest -m integration  # Only integration tests
pytest -m "not slow"  # Skip slow tests
```

---

## 📊 Expected Installation Output

```
Collecting pytest>=7.4.0
  Downloading pytest-7.4.3...
Successfully installed pytest-7.4.3 pytest-asyncio-0.21.1 pytest-cov-4.1.0 ...
```

---

## ⚠️ Troubleshooting

### **If installation fails:**

1. **Update pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Use virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r tests/requirements-test.txt
   ```

3. **Install one by one** if batch fails:
   ```bash
   pip install pytest pytest-asyncio pytest-cov
   # ... continue with other packages
   ```

### **If tests fail to run:**

1. **Check Python version** (requires Python 3.8+):
   ```bash
   python --version
   ```

2. **Verify pytest installation:**
   ```bash
   pytest --version
   ```

3. **Check test discovery:**
   ```bash
   pytest --collect-only
   ```

---

## 📝 Next Steps

1. **Install dependencies** using one of the methods above
2. **Run tests** to verify everything works
3. **Start writing tests** for new features
4. **Use CI/CD** - Tests run automatically on push

---

**Ready to install? Run:** `pip install -r tests/requirements-test.txt`
