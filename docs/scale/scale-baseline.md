# Production Scale Baseline & Workload Measurements

## 1. Observed Production Baseline

| Metric Domain | Measured Production Baseline | Target Peak Capacity (10x) | Bottleneck Component |
| :--- | :--- | :--- | :--- |
| **Active Advocate Organizations** | 10 Organizations | 100 Organizations | Connection pool limits |
| **Active Legal Matters** | 150 Matters | 1,500 Matters | Database query indexes |
| **Ingested Documents** | 1,200 PDF Title Deeds | 12,000 PDF Title Deeds | S3 storage throughput |
| **OCR Ingestion Throughput** | 50 Pages/minute | 500 Pages/minute | Asynchronous worker concurrency |
| **Hybrid Vector Queries** | 2,500 Searches/day | 25,000 Searches/day | `pgvector` HNSW index memory |
| **RAG Copilot Completions** | 800 Runs/day | 8,000 Runs/day | Provider API rate limits |
| **Database Storage Footprint**| 12.5 GB | 125 GB | Disk I/O & WAL archiving |

---

## 2. Scalability Principles
1. **Scale Problems You Actually Have**: Avoid premature microservices or distributed databases without empirical metrics.
2. **Asynchronous Isolation**: Long-running OCR processing and research web indexing operate out-of-band on dedicated background queues.
3. **Preserve Multi-Tenant Isolation**: Tenant filtering via `organization_id` is enforced in every database query and vector index search.
