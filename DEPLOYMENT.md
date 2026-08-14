# Deployment & Infrastructure Strategy

## Environment Targets
- **Local Dev / Single Node**: Docker Compose orchestrating FastAPI, PostgreSQL + pgvector, Redis, and Tesseract.
- **Staging / Production**: Linux VPS / Cloud VM with SSL termination, automated database backups, and environment secret management.
- **Infra Principles**: Free-first / Open-source foundation, simple single-command deployment, zero enterprise cloud overhead for MVP.
