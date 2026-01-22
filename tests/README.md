<<<<<<< HEAD
# AI Film Studio Testing Suite

Comprehensive testing suite including unit tests, integration tests, and CLI testing tools.

## Test Structure

```
tests/
├── __init__.py                      # Test package initialization
├── test_ai_models.py                # AI model unit tests
├── test_ai_services.py              # AI service unit tests
├── test_api.py                      # API unit tests
├── cli_test_tool.py                 # CLI testing tool
├── requirements-test.txt            # Testing dependencies
├── integration/                     # Integration tests
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_full_pipeline.py        # End-to-end pipeline tests
│   └── test_api_endpoints.py        # API integration tests
└── README.md                        # This file
```

## Quick Start

### 1. Install Test Dependencies

```bash
pip install -r tests/requirements-test.txt
```

### 2. Run Unit Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run tests by marker
pytest -m unit          # Only unit tests
pytest -m integration   # Only integration tests
pytest -m "not slow"    # Skip slow tests
```

### 3. Run Integration Tests

```bash
# Ensure services are running first
uvicorn src.api.main:app --reload

# Run integration tests (in another terminal)
pytest -m integration

# Run full pipeline test
pytest tests/integration/test_full_pipeline.py -v
```

## CLI Testing Tool

Interactive command-line tool for testing the API manually.

### Installation

```bash
# Install CLI dependencies
pip install rich requests

# Make executable (optional)
chmod +x tests/cli_test_tool.py
```

### Usage

#### Check API Health
```bash
python tests/cli_test_tool.py health
python tests/cli_test_tool.py --base-url http://localhost:8000 health
```

#### Generate Video
```bash
# Basic generation
python tests/cli_test_tool.py generate "A young explorer discovers a hidden world"

# With options
python tests/cli_test_tool.py generate "Your script here" --duration 60 --voice professional-male-1

# Wait for completion
python tests/cli_test_tool.py generate "Your script" --wait
```

#### Check Job Status
```bash
python tests/cli_test_tool.py status <job_id>
```

#### List Available Voices
```bash
python tests/cli_test_tool.py voices
```

#### Run Quick Integration Tests
```bash
python tests/cli_test_tool.py test
```

#### With API Key Authentication
```bash
python tests/cli_test_tool.py --api-key YOUR_API_KEY generate "Your script"
```

## Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.unit` - Fast unit tests, no external dependencies
- `@pytest.mark.integration` - Integration tests requiring services
- `@pytest.mark.slow` - Tests that take >30 seconds
- `@pytest.mark.gpu` - Tests requiring GPU (CUDA)
- `@pytest.mark.api` - API endpoint tests

### Running Tests by Marker

```bash
# Only unit tests (fast)
pytest -m unit

# Only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# GPU tests only
pytest -m gpu

# API tests only
pytest -m api
```

## Configuration

### Environment Variables

Set these for testing:

```bash
export ENVIRONMENT=test
export TEST_S3_BUCKET=ai-film-studio-test
export TEST_API_KEY=test_key_12345
export GPU_DEVICE_ID=0
```

### pytest.ini

Configuration file at project root defines:
- Test discovery patterns
- Default options
- Marker definitions
- Coverage settings

## Integration Test Examples

### Test Complete Pipeline
```bash
pytest tests/integration/test_full_pipeline.py::TestFullPipeline::test_end_to_end_pipeline -v
```

### Test Specific Service
```bash
pytest tests/integration/test_full_pipeline.py::TestFullPipeline::test_video_generation_pipeline -v
```

### Test API Endpoints
```bash
pytest tests/integration/test_api_endpoints.py -v
```

## Continuous Integration

Tests run automatically on:
- Pull requests to `dev` branch
- Merges to `staging` and `main`
- Scheduled nightly builds

### GitHub Actions Workflow

```yaml
- name: Run tests
  run: |
    pytest -m "unit and not slow" --cov=src --cov-report=xml
```

## Writing New Tests

### Unit Test Example
=======
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
>>>>>>> origin/copilot/integrate-auto-testing-infrastructure

```python
import pytest

<<<<<<< HEAD
@pytest.mark.unit
def test_video_service_initialization():
    """Test video service initializes correctly"""
    service = VideoGenerationService(s3_bucket="test-bucket")
    assert service.s3_bucket == "test-bucket"
```

### Integration Test Example

```python
import pytest

@pytest.mark.integration
@pytest.mark.asyncio
async def test_generate_video_integration():
    """Test complete video generation"""
    service = VideoGenerationService()
    result = await service.generate_video({
        "script": "Test script",
        "duration": 10
    })
    assert result.success is True
```

## Troubleshooting

### Common Issues

**Import errors**
```bash
# Install in development mode
pip install -e .
```

**Async test failures**
```bash
# Ensure pytest-asyncio is installed
pip install pytest-asyncio
```

**GPU tests failing**
```bash
# Skip GPU tests if no GPU available
pytest -m "not gpu"
```

**Integration tests timeout**
```bash
# Increase timeout
pytest --timeout=300 -m integration
```

## Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html

# Generate terminal report
pytest --cov=src --cov-report=term-missing
```

## Performance Testing

Use the CLI tool for basic performance testing:

```bash
# Time a single request
time python tests/cli_test_tool.py generate "Test script" --wait

# Multiple concurrent requests (bash)
for i in {1..5}; do
  python tests/cli_test_tool.py generate "Test $i" &
done
wait
```

## Support

For issues or questions about testing:
- Check test logs: `pytest --log-cli-level=DEBUG`
- View coverage: `pytest --cov=src --cov-report=term`
- GitHub Issues: https://github.com/AI-Empower-HQ-360/AI-Film-Studio/issues
=======
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
>>>>>>> origin/copilot/integrate-auto-testing-infrastructure
