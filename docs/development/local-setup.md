# Clean Machine Local Development Setup Guide

## Prerequisites
- Node.js 18+ & npm / pnpm
- Python 3.11+ & `pip` / `uv`
- Docker Desktop & Docker Compose
- Tesseract OCR (with `tessdata` Indic language packages: eng, hin, kan, mar, tam, tel)

---

## 1. Environment Configuration Setup
Clone repository and copy example environment files:

```bash
cp .env.example .env
```

`.env` defaults for local development:
```env
APP_ENV=development
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/legal_db
REDIS_URL=redis://localhost:6379/0
OBJECT_STORAGE_ENDPOINT=http://localhost:9000
OBJECT_STORAGE_BUCKET=legal-documents
OBJECT_STORAGE_ACCESS_KEY=minioadmin
OBJECT_STORAGE_SECRET_KEY=minioadmin
JWT_SECRET=super-secret-local-key-32-chars-minimum
OPENAI_API_KEY=mock-local-key
```

---

## 2. Infrastructure Services Startup

```bash
docker compose up -d postgres redis minio
```

---

## 3. Database Migration & Seed Data

```bash
cd services/api
pip install -r requirements.txt
alembic upgrade head
python -m app.db.seed
```

---

## 4. Launch Development Servers

```bash
# Terminal 1: Backend API
cd services/api
uvicorn app.main:app --reload --port 8000

# Terminal 2: Background Worker
cd services/api
celery -A app.jobs.worker worker --loglevel=info

# Terminal 3: React Frontend
cd apps/web
npm install
npm run dev
```

---

## 5. Verification Check
- Frontend Web UI: `http://localhost:5173`
- Backend API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/v1/health`
