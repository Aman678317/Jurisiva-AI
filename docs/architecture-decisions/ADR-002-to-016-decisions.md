# ADR-002 through ADR-016: Core Architectural Decisions

## ADR-002: Frontend Framework — React / Next.js / Vite Shell
- **Decision**: React with TypeScript & Tailwind CSS / Vanilla CSS tokens.
- **Rationale**: High performance for split-screen PDF viewer canvas rendering; rich ecosystem for PDF.js and interactive component libraries.
- **Trade-Offs**: Requires client-side state management for multi-panel workspace.

## ADR-003: Backend Framework — FastAPI (Python 3.11+)
- **Decision**: FastAPI async Python framework.
- **Rationale**: Native integration with Python AI/ML ecosystem (LiteLLM, PyPDF, Tesseract/PaddleOCR, Pydantic), high async I/O performance, automatic OpenAPI documentation generation.
- **Trade-Offs**: Python concurrency requires async/await discipline and background worker offloading for CPU-bound OCR tasks.

## ADR-004: Relational Database — PostgreSQL 16+
- **Decision**: PostgreSQL 16+ as canonical relational database.
- **Rationale**: Proven ACID compliance, JSONB support for OCR layout schemas, row-level security capabilities, and robust SQL querying.

## ADR-005: Object Storage — MinIO (Local) / AWS S3 (Production)
- **Decision**: S3-compatible Object Storage.
- **Rationale**: Decouples binary file storage from relational DB; MinIO provides 100% free local development parity.

## ADR-006: Queue & Asynchronous Workers — Redis + Celery / ARQ
- **Decision**: Redis-backed async task queue.
- **Rationale**: Offloads long-running OCR, embedding generation, and report compilation out of synchronous API HTTP request cycles.

## ADR-007 & ADR-008: Search & Vector Storage — pgvector (HNSW Index) + BM25 Full-Text Search
- **Decision**: PostgreSQL `pgvector` extension for vector embeddings + PostgreSQL Full-Text Search for BM25 keyword matching.
- **Rationale**: Keeps relational data and 1536-dim vector embeddings inside the primary PostgreSQL database. Eliminates third-party vector DB costs (Pinecone/Weaviate) and eliminates cross-database sync errors.

## ADR-009: OCR Adapter Pipeline — Tesseract / PaddleOCR Indic Pipeline
- **Decision**: Open-source Indic OCR pipeline with fallback adapter interface.
- **Rationale**: Local open-source execution for Indic scripts (Eng, Hin, Kan, Mar, Tam, Tel); zero per-page cloud API costs during development.

## ADR-010: AI Provider Abstraction — LiteLLM Model Gateway
- **Decision**: Abstract all LLM operations through a unified adapter (LiteLLM / Custom AI Gateway).
- **Rationale**: Enables instant switching between OpenAI, Anthropic, Gemini, or local Ollama models via environment variables with zero application code changes.

## ADR-011 & ADR-012: Authentication & Authorization — Session JWT + Server-Side RBAC Middleware
- **Decision**: JWT with HttpOnly cookies + server-side RBAC middleware (`LEAD_ADVOCATE`, `ASSOCIATE`, `AUDITOR`).
- **Rationale**: Enforces authorization strictly at the backend boundary before database access or LLM invocation.

## ADR-013: Multi-Tenancy Architecture — Column-Level Isolation (`organization_id` & `matter_id`)
- **Decision**: Column-level tenant scoping enforced in all database queries and repository methods.
- **Rationale**: Simple, highly performant, and testable multi-tenant isolation model for relational and vector data.

## ADR-014: Observability Architecture — OpenTelemetry + Structured JSON Logging
- **Decision**: Structured JSON logs featuring `request_id`, `trace_id`, `tenant_id`, and `matter_id`.
- **Rationale**: Provides complete end-to-end request tracing without logging sensitive raw document content.

## ADR-015 & ADR-016: Infrastructure & Deployment — Single-Node Docker Compose / Caddy / VPS
- **Decision**: Docker Compose for local/staging; Docker-based VPS deployment with automated GitHub Actions CI/CD.
- **Rationale**: Minimal operational overhead, reproducible local environment, free open-source infrastructure foundation.
