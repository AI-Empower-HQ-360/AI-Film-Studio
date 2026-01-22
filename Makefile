# AI Film Studio - Development Makefile
# Common commands for local development and deployment

.PHONY: help install dev test build deploy clean docker-up docker-down

# Default target
help:
	@echo "AI Film Studio - Development Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install      - Install all dependencies"
	@echo "  make dev          - Start development servers"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Run linters"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up    - Start all containers"
	@echo "  make docker-down  - Stop all containers"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-gpu   - Start with GPU support"
	@echo ""
	@echo "Database:"
	@echo "  make db-migrate   - Run database migrations"
	@echo "  make db-reset     - Reset database"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy-dev   - Deploy to DEV environment"
	@echo "  make deploy-prod  - Deploy to PRODUCTION"

# ==================== Development ====================
install:
	pip install --upgrade pip
	pip install -r requirements.txt
	cd frontend && npm install

dev:
	@echo "Starting development servers..."
	@make -j2 dev-backend dev-frontend

dev-backend:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

# ==================== Testing ====================
test:
	pytest tests/ -v --tb=short

test-unit:
	pytest tests/unit/ -v --tb=short

test-integration:
	pytest tests/integration/ -v --tb=short

test-e2e:
	pytest tests/e2e/ -v --tb=short

test-coverage:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

lint:
	flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
	black --check src/ tests/
	mypy src/ --ignore-missing-imports

format:
	black src/ tests/
	isort src/ tests/

# ==================== Docker ====================
docker-up:
	docker-compose up -d postgres redis localstack
	@echo "Waiting for services to be ready..."
	@sleep 5
	docker-compose up -d api frontend

docker-down:
	docker-compose down

docker-build:
	docker-compose build

docker-gpu:
	docker-compose --profile gpu up -d

docker-logs:
	docker-compose logs -f

docker-clean:
	docker-compose down -v --rmi local
	docker system prune -f

# ==================== Database ====================
db-migrate:
	alembic upgrade head

db-reset:
	docker-compose exec postgres psql -U aifilmstudio -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	docker-compose exec postgres psql -U aifilmstudio -f /docker-entrypoint-initdb.d/init.sql

db-shell:
	docker-compose exec postgres psql -U aifilmstudio -d aifilmstudio

# ==================== AWS CDK ====================
cdk-synth:
	cd infrastructure/aws-cdk && cdk synth

cdk-diff:
	cd infrastructure/aws-cdk && cdk diff

deploy-dev:
	cd infrastructure/aws-cdk && cdk deploy --all --context environment=dev

deploy-sandbox:
	cd infrastructure/aws-cdk && cdk deploy --all --context environment=sandbox

deploy-staging:
	cd infrastructure/aws-cdk && cdk deploy --all --context environment=staging

deploy-prod:
	cd infrastructure/aws-cdk && cdk deploy --all --context environment=production --require-approval broadening

# ==================== Utilities ====================
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .coverage htmlcov/ .mypy_cache/

logs:
	docker-compose logs -f --tail=100

shell:
	docker-compose exec api /bin/bash

redis-cli:
	docker-compose exec redis redis-cli
