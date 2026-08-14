# Performance Benchmarks & Latency Targets

## Performance SLA Targets

| Operation / Endpoint | Target p50 | Target p95 | Target p99 | Max Error Rate |
| :--- | :---: | :---: | :---: | :---: |
| **Authentication (`/auth/login`)** | < 50ms | < 150ms | < 300ms | 0.00% |
| **Matter Detail (`/matters/{id}`)** | < 80ms | < 250ms | < 500ms | 0.01% |
| **Hybrid Search (`/search`)** | < 200ms | < 600ms | < 1,200ms | 0.01% |
| **RAG Copilot (`/assistant/query`)**| < 400ms | < 1,500ms | < 2,500ms | 0.05% |
| **OCR Pipeline Ingestion (per page)**| < 800ms | < 2,000ms | < 4,000ms | 0.10% |

All benchmarks are evaluated automatically in `tests/performance/test_performance.py`.
