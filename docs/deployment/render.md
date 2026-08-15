# Render API & Background Worker Deployment Guide

This guide covers deploying the FastAPI Web Service, Background Worker, Redis Queue, and Scheduled Maintenance Cron on Render using `render.yaml`.

---

## 1. Blueprint Architecture

The Render deployment consists of 4 tightly integrated services:

1. **`jurisiva-api` (Web Service)**:
   - **Runtime**: Python 3.11.9
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn services.api.app.main:app --host 0.0.0.0 --port $PORT --workers 4`
   - **Health Check**: `/health`

2. **`jurisiva-worker` (Background Worker)**:
   - **Runtime**: Python 3.11.9
   - **Start Command**: `python -m workers.worker`
   - **Role**: Continuously processes heavy OCR, RAG embedding, title graph recalculation, and PDF report jobs without blocking API requests.

3. **`jurisiva-redis` (Key-Value / Queue Broker)**:
   - **Plan**: Starter / Standard
   - **Role**: Dispatches job payloads between FastAPI and the background worker.

4. **`jurisiva-maintenance-cron` (Cron Job)**:
   - **Schedule**: `0 2 * * *` (Daily at 02:00 UTC)
   - **Start Command**: `python -m workers.worker --run-cron-cleanup`
   - **Role**: Cleans expired temporary data, compacts audit logs, and vacuums vector indexes.

---

## 2. Environment Variables Configuration

Configure the following secrets in the Render Dashboard for `jurisiva-api` and `jurisiva-worker`:

```ini
ENVIRONMENT=production
PYTHON_VERSION=3.11.9
CORS_ORIGINS=https://app.jurisiva.ai,https://www.jurisiva.ai,https://jurisiva-ai.vercel.app

# Supabase Credentials (Privileged Server-Side)
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<service-role-secret>
SUPABASE_DB_URL=postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres
SUPABASE_JWT_SECRET=<jwt-secret>

# AI & OCR Provider Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
OCR_PROVIDER=GOOGLE_VISION_AND_TESSERACT
OCR_API_KEY=...
SEARCH_PROVIDER=APEX_LEGAL_AND_WEB
SEARCH_API_KEY=...
STT_PROVIDER=WHISPER_AND_GOOGLE
STT_API_KEY=...
TTS_PROVIDER=GOOGLE_NEURAL2
TTS_API_KEY=...
```

---

## 3. Deploying with Blueprint

1. Go to **Render Dashboard > Blueprints > New Blueprint Instance**.
2. Connect `github.com/Aman678317/Jurisiva-AI`.
3. Select `render.yaml`.
4. Enter the required secret values when prompted.
5. Click **Apply**.
