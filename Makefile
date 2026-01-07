.PHONY: help install install-dev test test-unit test-integration test-e2e test-cov lint format clean

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

test:  ## Run all tests
	pytest tests/

test-unit:  ## Run unit tests only
	pytest tests/unit/ -m unit

test-integration:  ## Run integration tests only
	pytest tests/integration/ -m integration

test-e2e:  ## Run end-to-end tests only
	pytest tests/e2e/ -m e2e

test-cov:  ## Run tests with coverage report
	pytest tests/ --cov=src --cov-report=html --cov-report=term

test-fast:  ## Run tests in parallel
	pytest tests/ -n auto

lint:  ## Run linters
	black --check src tests
	flake8 src tests
	mypy src

format:  ## Format code with black
	black src tests
	isort src tests

clean:  ## Clean up generated files
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .tox
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

setup-dev:  ## Setup development environment
	python -m venv venv
	. venv/bin/activate && make install-dev

run-api:  ## Run the API server
	python -m src.api.main

docker-build:  ## Build Docker image
	docker build -t ai-film-studio .

docker-run:  ## Run Docker container
	docker run -p 8000:8000 ai-film-studio
