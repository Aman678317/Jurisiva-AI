# Final Production System Inventory

## Production Component Audit Matrix

| Component Name | Category | Repository Location | Health Check Endpoint | Operational Status |
| :--- | :--- | :--- | :--- | :---: |
| **React Web UI** | Frontend SPA | `apps/web/` | Nginx Static / TLS Port 443 | **PASS** |
| **FastAPI Core Server** | Backend API | `services/api/app/main.py` | `/health`, `/readiness` | **PASS** |
| **PostgreSQL 16 DB** | Relational Store | `services/api/app/db/` | `pg_isready` (Port 5432) | **PASS** |
| **pgvector Index** | Vector Store | `services/api/app/search_engine.py` | RRF Hybrid Search Query | **PASS** |
| **Redis Broker** | Queue / Cache | `services/api/app/jobs.py` | Redis `PING` (Port 6379) | **PASS** |
| **MinIO / S3 Storage** | Object Storage | `services/api/app/storage.py` | Bucket Access Policy Check | **PASS** |
| **Document Worker** | Asynchronous Pipeline | `workers/ingestion_worker/` | Worker Heartbeat Metric | **PASS** |
| **Indic OCR Gateway** | OCR Engine | `workers/ingestion_worker/ocr_engine.py` | Indic Tesseract Benchmark Test | **PASS** |
| **LiteLLM AI Gateway** | AI Provider Router | `services/api/app/ai_gateway.py` | `ModelRegistry` Approval Check | **PASS** |
| **Red-Team Verifier** | Security Audit | `services/api/app/security/red_team.py` | `SEC-002` Zero Leakage Audit | **PASS** |
| **DR Simulator** | Disaster Recovery | `services/api/app/security/disaster_recovery.py` | Backup Restore Test | **PASS** |
