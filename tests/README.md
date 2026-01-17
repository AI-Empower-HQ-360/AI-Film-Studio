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

```python
import pytest

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
