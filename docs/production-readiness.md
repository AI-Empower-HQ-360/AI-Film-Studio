# Production readiness gap assessment

**Date:** 2025-12-27  
**Scope:** Repository state in `copilot/check-files-for-production`

## Current snapshot (observed)
- Backend is a minimal FastAPI app with only two health endpoints; no domain models, persistence, auth, background jobs, or business logic.
- Worker, frontend, and most service code described in the README are absent. Infrastructure code is limited to Terraform variable stubs with no modules or resources.
- No CI/CD workflows exist (no `.github/workflows/`). Dockerfile entrypoint in `./Dockerfile` is malformed (currently `CMD ["python", "-m", "src.api. main"]`; it needs the space removed → `src.api.main` and a production ASGI server configuration).
- No environment template (`.env.example`) or secrets management wiring. Logging is basic and not structured; no metrics/tracing hooks.
- Tests only cover health checks; no linting configuration, coverage enforcement, or performance/resilience tests. No lockfile to pin transitive dependencies.

## Critical blockers before production
1. **Core application features**
   - Implement API endpoints for auth, projects/jobs, asset management, billing/quotas, and job orchestration.
   - Add database models, schema migrations (Alembic), and persistence layer wiring.
   - Build GPU worker service (SQS polling, model loading, rendering pipeline, upload to S3, status updates).
   - Deliver frontend (Next.js/TypeScript) for user workflows and admin/operations panels.
2. **Infrastructure & deployment**
   - Flesh out Terraform modules for VPC, subnets, ALB, ECS/EKS services, RDS, S3, SQS/DLQ, Redis/ElastiCache, Secrets Manager/SSM, CloudFront, and IAM roles/policies.
   - Provide per-environment configs (dev/test/stage/prod) and remote state/backend locking.
   - Fix container builds: correct entrypoints, add multi-stage builds, and produce separate images for API/worker.
   - Publish versioned artifacts (container registry) and document release promotion.
3. **CI/CD & quality gates**
   - Add GitHub Actions (or equivalent) for lint → test → build → security scan → image push → deploy with approvals.
   - Enforce formatting (Black/Ruff/Flake8), typing (MyPy), unit/integration tests, and coverage thresholds.
   - Add dependency scanning (pip-audit/Snyk/Trivy) and container image scanning.
4. **Security & compliance**
   - Implement authentication/authorization (JWT/RBAC), input validation, rate limiting, and request size limits.
   - Centralize secrets via AWS Secrets Manager/SSM; add `.env.example` and config management.
   - Enable HTTPS everywhere, WAF rules, CORS policy, and Content Security Policy for the frontend.
   - Add backup/DR plans (RDS backups, S3 versioning/replication) and access logging (ALB/CloudFront/S3).
5. **Observability & operations**
   - Add structured logging, request IDs, and correlation across services.
   - Expose metrics (Prometheus/CloudWatch), tracing (OpenTelemetry/X-Ray), and health/readiness/liveness probes.
   - Create runbooks for incidents, on-call rotations, and SLO/SLA definitions with alerting rules.
6. **Testing & performance**
   - Expand automated tests: API contract tests, worker pipeline tests with fixtures, load/performance tests (Locust), chaos/resiliency checks.
   - Add seed data and local dev tooling (docker-compose) to run API + worker + DB locally.

## Immediate next steps (suggested order)
1. Stand up CI lint/test workflow and fix the `./Dockerfile` entrypoint to use `uvicorn src.api.main:app --host 0.0.0.0 --port 8000` (ASGI) with the correct module path.
2. Add `.env.example`, settings schema, and secrets loading strategy.
3. Define minimal database schema + Alembic migrations and wire FastAPI to a Postgres instance.
4. Implement core job lifecycle (enqueue → worker → status updates) with SQS placeholders and unit tests.
5. Add Terraform modules for networking + API/worker + data stores; validate `terraform plan` for dev.
6. Build initial frontend shell to exercise auth and job submission flows; add E2E smoke tests.
7. Layer in observability (logging/metrics/tracing) and security controls (rate limiting, CORS/WAF guidance).
8. Document runbooks (deploy, rollback, DR, incident response) and attach them under `docs/operations/`.
