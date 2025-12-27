# AI Film Studio Testing Guide

This directory contains the comprehensive test suite for the AI Film Studio project.

## 📁 Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── README.md                # This file
├── unit/                    # Unit tests for individual components
│   ├── test_logger.py      # Logger utility tests
│   ├── test_settings.py    # Configuration tests
│   └── test_utils.py       # Utility function tests
├── integration/            # Integration tests for APIs and services
│   ├── test_api_endpoints.py  # API endpoint tests
│   └── test_services.py    # Service layer tests
├── e2e/                    # End-to-end workflow tests
│   ├── test_film_workflow.py  # Film creation workflow
│   └── test_user_journey.py   # User interaction tests
└── mocks/                  # Mock implementations
    ├── mock_aws.py         # AWS service mocks
    ├── mock_redis.py       # Redis mocks
    └── mock_db.py          # Database mocks
```

## 🚀 Running Tests

### Run All Tests
```bash
make test
# or
pytest
```

### Run Specific Test Types
```bash
# Unit tests only
make test-unit
pytest tests/unit/ -m unit

# Integration tests only
make test-integration
pytest tests/integration/ -m integration

# End-to-end tests only
make test-e2e
pytest tests/e2e/ -m e2e
```

### Run Tests with Coverage
```bash
make test-cov
# or
pytest --cov=src --cov-report=html --cov-report=term
```

### Run Tests in Parallel
```bash
make test-fast
# or
pytest -n auto
```

### Run Specific Test File
```bash
pytest tests/unit/test_logger.py
```

### Run Specific Test Function
```bash
pytest tests/unit/test_logger.py::test_logger_setup
```

## 📊 Coverage Reports

After running tests with coverage, you can view the HTML report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## ✍️ Writing Tests

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Unit Tests
Unit tests should test individual functions or classes in isolation:

```python
import pytest
from src.utils.logger import setup_logger

def test_logger_setup():
    """Test basic logger setup"""
    logger = setup_logger("test", "INFO")
    assert logger.name == "test"
    assert logger.level == 20  # INFO level
```

### Integration Tests
Integration tests should test interactions between components:

```python
import pytest

@pytest.mark.asyncio
async def test_api_endpoint(async_api_client):
    """Test API endpoint integration"""
    response = await async_api_client.get("/api/v1/health")
    assert response.status_code == 200
```

### End-to-End Tests
E2E tests should test complete user workflows:

```python
import pytest

@pytest.mark.e2e
def test_film_creation_workflow(api_client, sample_script_data):
    """Test complete film creation workflow"""
    # Submit script
    response = api_client.post("/api/v1/scripts", json=sample_script_data)
    assert response.status_code == 201
    
    # Check job status
    job_id = response.json()["job_id"]
    response = api_client.get(f"/api/v1/jobs/{job_id}")
    assert response.status_code == 200
```

### Using Fixtures
Fixtures provide reusable test data and mock objects:

```python
def test_with_fixtures(api_client, sample_script_data, mock_s3):
    """Test using fixtures"""
    response = api_client.post("/api/v1/scripts", json=sample_script_data)
    assert response.status_code == 201
```

## 🏷️ Test Markers

Tests are automatically marked based on their location, but you can also use explicit markers:

```python
@pytest.mark.unit
def test_unit_example():
    """Unit test"""
    pass

@pytest.mark.integration
def test_integration_example():
    """Integration test"""
    pass

@pytest.mark.e2e
def test_e2e_example():
    """E2E test"""
    pass

@pytest.mark.slow
def test_slow_example():
    """Slow test"""
    pass
```

## 🔧 Testing Best Practices

1. **Isolation**: Each test should be independent and not rely on other tests
2. **Clear Names**: Use descriptive test names that explain what is being tested
3. **One Assertion**: Focus on testing one thing per test (when possible)
4. **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification
5. **Mock External Dependencies**: Mock external services (AWS, Redis, databases)
6. **Use Fixtures**: Leverage pytest fixtures for reusable test components
7. **Fast Tests**: Keep tests fast by mocking expensive operations
8. **Coverage**: Aim for 80%+ code coverage

## 🔍 Debugging Tests

### Run Tests in Verbose Mode
```bash
pytest -v
```

### Stop on First Failure
```bash
pytest -x
```

### Run Last Failed Tests
```bash
pytest --lf
```

### Show Print Statements
```bash
pytest -s
```

### Use Python Debugger
```python
import pdb; pdb.set_trace()
```

## 🤖 CI/CD Integration

Tests run automatically on:
- Push to any branch
- Pull request creation/update
- Multiple Python versions (3.9, 3.10, 3.11)

See `.github/workflows/test.yml` for CI configuration.

## 📦 Test Dependencies

Test dependencies are in `requirements-dev.txt`:
- **pytest**: Test framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities
- **httpx**: Async HTTP client
- **faker**: Test data generation
- **moto**: AWS service mocking
- **fakeredis**: Redis mocking

## 🆘 Troubleshooting

### Import Errors
Ensure you're running tests from the project root:
```bash
cd /path/to/AI-Film-Studio
pytest
```

### Async Test Errors
Make sure async tests are marked:
```python
@pytest.mark.asyncio
async def test_async():
    pass
```

### Fixture Not Found
Check that fixtures are defined in `conftest.py` or in the same test file.

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
