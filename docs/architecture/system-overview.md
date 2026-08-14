# System Overview & Architecture Diagram

## High-Level System Architecture

```mermaid
graph TD
    User[Legal Professional / Advocate] -->|HTTPS / WSS| WebApp[Web Application - React UI]
    
    subgraph Frontend Boundary
        WebApp --> Router[Client Router & State]
        WebApp --> Viewer[Split-Screen PDF Viewer]
    end

    WebApp -->|REST API + JWT| APIGateway[FastAPI Application Gateway]

    subgraph Backend Core (Modular Monolith)
        APIGateway --> AuthMiddleware[AuthN / AuthZ & RBAC Middleware]
        AuthMiddleware --> TenantIsolation[Tenant & Matter Isolation Guard]
        
        TenantIsolation --> IdentityMod[Identity Module]
        TenantIsolation --> MattersMod[Matters Module]
        TenantIsolation --> DocumentsMod[Documents Module]
        TenantIsolation --> EvidenceMod[Evidence & Search Module]
        TenantIsolation --> PropertyMod[Property Intelligence Module]
        TenantIsolation --> ResearchMod[Research & Copilot Module]
        TenantIsolation --> ReportsMod[Reports Module]
        TenantIsolation --> AuditMod[Audit Logging Module]
    end

    subgraph Infrastructure Layer
        IdentityMod --> Postgres[(PostgreSQL 16 DB)]
        MattersMod --> Postgres
        DocumentsMod --> ObjStore[(S3 / MinIO Object Storage)]
        EvidenceMod --> PgVector[(pgvector - HNSW Index)]
        EvidenceMod --> BM25[(Postgres BM25 Full-Text)]
        DocumentsMod --> JobQueue[(Redis + Celery Queue)]
        ResearchMod --> AIGateway[LiteLLM AI Gateway Adapter]
        AuditMod --> Postgres
    end

    subgraph Worker & Background Execution Layer
        JobQueue --> IngestionWorker[Document Ingestion Worker]
        JobQueue --> OCRWorker[Indic OCR Worker Engine]
        JobQueue --> VectorWorker[Embedding & Index Worker]
    end

    subgraph External Provider Boundary
        OCRWorker -->|Local / Cloud| OCREngine[Tesseract / PaddleOCR Engine]
        AIGateway -->|API Gateway| LLMProvider[OpenAI / Anthropic / Local Ollama]
    end
```

---

## Architectural Principles Enforcement
1. **Modular Monolith**: All domain services run within a single structured FastAPI application, maintaining clear boundary contracts.
2. **Worker Separation**: High-CPU or long-running tasks (OCR, chunking, embedding) operate on asynchronous worker processes off Redis queues.
3. **Unified SQL + Vector Store**: PostgreSQL + pgvector houses relational metadata, audit logs, full-text indexes, and 1536-dim vector embeddings, eliminating multi-database sync complexity.
