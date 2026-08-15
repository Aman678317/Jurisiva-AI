# Production Deployment & Infrastructure Manual — Jurisiva AI

This operating guide details the production deployment, infrastructure architecture, environment secret management, and disaster recovery procedures for **Jurisiva AI**.

---

## 🏗️ Architecture Targets

- **Local Development**: Node.js Web Server (`http://127.0.0.1:3000`) + Python FastAPI Backend (`http://127.0.0.1:8000`).
- **Containerized Stack**: Single-command orchestration via `docker-compose.up` (FastAPI + PostgreSQL pg16 with pgvector extension + Redis 7 + MinIO S3 Object Storage + Web Client UI).
- **Production Canary / Cloud VM**: Linux Ubuntu 22.04 LTS / Cloud VM with Nginx reverse proxy, TLS/SSL certificates, systemd unit services, and automated pg_dump database backups.

---

## 🚀 Quick Deployment Commands

### 1. Local Python & Node Launch
```powershell
# Terminal 1: Backend API
cd services/api
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Web Application
npm run dev
```

### 2. Full Docker Compose Deployment
```bash
# Build and launch all services in background
docker compose up --build -d

# Verify container status
docker compose ps

# View live API logs
docker compose logs -f api
```

---

## 🔐 Environment Variables Reference

| Variable Name | Required | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `APP_ENV` | Yes | `production` | Environment mode (`development`, `staging`, `production`) |
| `JWT_SECRET` | Yes | `32-chars-min-hash` | Secret key for issuing & validating JWT tokens |
| `DATABASE_URL` | Yes | `postgresql+asyncpg://...` | Relational DB connection string (PostgreSQL + pgvector) |
| `REDIS_URL` | Yes | `redis://localhost:6379/0` | Cache and message queue connection string |
| `OBJECT_STORAGE_ENDPOINT` | Yes | `http://localhost:9000` | S3-compatible MinIO / AWS S3 endpoint |
| `LLM_PROVIDER` | Yes | `ollama` | AI gateway provider adapter (`ollama`, `openai`, `anthropic`) |
| `OCR_ENGINE` | Yes | `tesseract` | Indic OCR processing engine (`tesseract`, `paddleocr`) |

---

## 🧪 Production Quality Assurance Checklist

- [x] **Tenant Isolation**: Deny-by-default server-side tenant boundary enforcement (`SEC-002`).
- [x] **Evidence Sufficiency Gate**: Content word overlap verification issuing `INSUFFICIENT_EVIDENCE` refusals for out-of-domain prompts.
- [x] **Prompt Injection Defense**: Untrusted user documents wrapped in structural delimiters (`<source_document>`).
- [x] **Disaster Recovery (RTO)**: Automated pg_dump restoration verified in under 10 seconds.
- [x] **Zero Data Retention AI Policy**: Customer text zero-training policy enforced at model gateway.
- [x] **CI/CD Pipeline**: GitHub Actions quality workflow passing 100% on `pytest tests/`.
