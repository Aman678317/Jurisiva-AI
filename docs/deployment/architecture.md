# Jurisiva-AI Production Deployment Architecture

This document describes the enterprise production deployment topology for Jurisiva-AI across **Vercel** (Frontend), **Render** (FastAPI Gateway & Background Workers), and **Supabase** (PostgreSQL, Auth, Private Storage, pgvector).

---

## 🏛️ Target Production Topology

```
                         INTERNET
                             │
                   ┌─────────┴─────────┐
                   │                   │
                   ▼                   ▼
                VERCEL             API DOMAIN
              FRONTEND          api.jurisiva.ai
           app.jurisiva.ai             │
                   │                   │
                   │ HTTPS             │
                   └─────────>─────────┘
                             │
                        RENDER API
                      FastAPI Gateway
                      (Python 3.11.9)
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
      SUPABASE           RENDER WORKER      AI / SEARCH
  Postgres + pgvector    Asynchronous       PROVIDERS
  Auth + RBAC (RLS)      OCR / AI / RAG     (OpenAI, Claude,
  Private Storage        Research / Reports Google, Whisper,
          │                  │              Apex Gateways)
          │                  ▼                  │
          └───────────>  Job Queue  <───────────┘
                       (Redis Broker)
                             │
                             ▼
                    Persistent Case Data
                  Documents • Scans • OCR
                  Evidence • Title Graphs
                  Research • Court Drafts
```

---

## 🔒 Security Boundaries & Responsibilities

| Tier | Component | Security Boundary & Responsibilities |
| :--- | :--- | :--- |
| **Edge / CDN** | **Vercel** | Delivers compiled frontend assets over global edge CDN. Receives only browser-safe environment variables (`NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`). **Zero server secrets exposed.** |
| **API Gateway** | **Render Web Service** | Runs FastAPI on `0.0.0.0:$PORT` with 4 uvicorn workers. Validates JWT auth tokens, enforces tenant isolation, manages CORS whitelist, and delegates long-running tasks to the background worker. |
| **Asynchronous Compute** | **Render Worker** | Dedicated daemon processing `OCR_DOCUMENT`, `EXTRACT_DOCUMENT`, `REBUILD_OWNERSHIP`, `RUN_RESEARCH`, and `GENERATE_REPORT` without blocking HTTP requests. |
| **Database & Vector** | **Supabase Postgres** | Primary relational store with `pgvector` HNSW index for high-speed legal embeddings. All customer tables have Row Level Security (RLS) enabled. |
| **Identity & Access** | **Supabase Auth** | JWT-based authentication with role-based access control (`OWNER`, `ADMIN`, `LAWYER`, `REVIEWER`, `MEMBER`). |
| **Encrypted Storage** | **Supabase Storage** | Private encrypted buckets (`case-documents`, `case-artifacts`, `reports`). Accessible only via authenticated backend requests or signed URLs. |

---

## ⚡ Data Flow Lifecycle

1. **User Authentication**: Client authenticates against Supabase Auth, receiving an ephemeral JWT.
2. **Case Operation**: Client sends HTTPS request to `https://api.jurisiva.ai` with Bearer token.
3. **Authorization & RLS**: FastAPI verifies token signature and scopes queries by `organization_id` and `case_id`.
4. **Document Ingestion**: Scanned deeds (PDF/JPG/PNG/TIFF) are uploaded to private Supabase Storage, and an `OCR_DOCUMENT` task is dispatched to the Redis queue.
5. **Background OCR & Intelligence**: Render worker leases the task, applies 300 DPI deskew/denoise, executes multilingual Indic OCR, extracts legal entities, and updates the database.
6. **Workspace Synchronization**: Frontend automatically reflects updated Ownership Chains, Timelines, AI Analysis findings, and Risk Ledgers.
