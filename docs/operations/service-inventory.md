# Production Service Inventory & Operational Failure Modes

## Operational Service Catalog

| Service / Dependency | Criticality Tier | Failure Mode | Graceful Fallback / Recovery Strategy |
| :--- | :---: | :--- | :--- |
| **FastAPI Core API** | Tier 1 (Critical) | Container crash / OOM | Auto-restart via Docker compose / K8s replica pool |
| **PostgreSQL 16 DB** | Tier 1 (Critical) | Connection pool saturation | Connection throttling via PgBouncer; 5-min WAL restore |
| **MinIO / S3 Store** | Tier 1 (Critical) | Storage backend timeout | Bounded exponential retry; static viewer fallback |
| **Redis Queue** | Tier 2 (High) | Queue broker memory exhaustion | Job quarantine; dead-letter queue inspection (`DLQ-001`) |
| **LiteLLM Gateway** | Tier 2 (High) | Provider API outage / 5xx | Circuit breaker (`CircuitBreaker`) tripping to degraded mode |
| **Indic OCR Worker** | Tier 2 (High) | Tesseract worker crash | Worker auto-restart; asynchronous job status `RETRY_QUEUED` |

Infrastructure health alone is insufficient; all workflows require correlation ID propagation (`X-Correlation-ID`).
