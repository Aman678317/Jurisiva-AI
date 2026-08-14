# Capacity Modeling & 1x to 100x Growth Scaling

## Growth Tier Projections

| Component | 1x Baseline | 10x Scale | 50x Scale | 100x Scale | Scaling Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **API Replicas** | 2 Replicas | 5 Replicas | 15 Replicas | 30 Replicas | Horizontal Container Scaling |
| **PostgreSQL DB** | Single Instance | Primary + 1 Read Replica | Primary + 3 Read Replicas | Partitioned Tables + Read Replicas | Connection Pooling (PgBouncer) + Archival |
| **Worker Queue** | 4 Workers | 16 Workers | 48 Workers | 100 Workers | Redis Backpressure Queue Auto-scaling |
| **pgvector Index** | HNSW (m=16, ef=64)| HNSW (m=16, ef=64)| Dedicated Vector Index | Distributed Vector Store | Partitioned vector index per tenant |
