# Technical Requirements Document (TRD) — India-First Legal & Property Intelligence Platform

## 1. System Objectives
Establish a production-grade, modular, secure, and auditable technical architecture designed for the Indian legal and property domain. The system supports multi-tenant matter isolation, Indic multilingual OCR, hybrid vector search, citation-aware RAG generation, automated land record contradiction detection, and editable Title Search Report export.

---

## 2. Functional Requirements Summary
- **TRD-FUNC-001**: Tenant & Matter Isolation (Logical partitioning by Org ID & Matter ID).
- **TRD-FUNC-002**: Multi-file Ingestion & Immutable Storage (SHA-256 validation).
- **TRD-FUNC-003**: Asynchronous Indic OCR & Text Extraction (Tesseract / PaddleOCR).
- **TRD-FUNC-004**: Hybrid Vector (pgvector HNSW) + Lexical (BM25) Search Engine.
- **TRD-FUNC-005**: Citation-Aware RAG Copilot with application-level citation validation.
- **TRD-FUNC-006**: Extent & Boundary Contradiction Engine with unit normalization.
- **TRD-FUNC-007**: Human Verification Workflow (`SOURCE FACT` -> `HUMAN VERIFIED`).
- **TRD-FUNC-008**: Formatted DOCX/PDF Title Search Report Generation.

---

## 3–5. Non-Functional & Availability Targets

| Target Metric | Benchmark Target | Measurement Method |
| :--- | :--- | :--- |
| **System Uptime / Availability** | 99.9% Availability | Synthetic HTTP ping monitoring on `/health/readiness`. |
| **API Response Latency (p95)** | < 250 ms | Middleware request timer on non-AI REST endpoints. |
| **Search Retrieval Latency (p95)** | < 1,500 ms | Vector distance calculation + BM25 execution time. |
| **RAG First Token Time (TTFT)** | < 2.5 seconds | LLM Gateway streaming TTFT benchmark. |
| **OCR Processing Speed** | < 3.5s per page | Asynchronous worker task execution timer. |

---

## 6. Security Requirements
- **TRD-SEC-001**: Authentication via JWT with secure HttpOnly cookies.
- **TRD-SEC-002**: Server-side Role-Based Access Control (RBAC) enforced in backend middleware.
- **TRD-SEC-003**: TLS 1.3 in transit; AES-256 for files at rest in Object Storage.
- **TRD-SEC-004**: Prompt Injection Guard: Untrusted document text wrapped in XML delimiters (`<context_document>`); tool execution blocked unless authorized by backend server rules.

---

## 7. Privacy & Data Isolation Requirements
- **TRD-PRIV-001**: Strict tenant scoping (`organization_id` & `matter_id`) on all database queries and vector namespaces.
- **TRD-PRIV-002**: Zero user document data passed to public LLM model training datasets.

---

## 8. Multi-Tenancy Requirements
- **TRD-TEN-001**: Schema-level / Column-level tenant partitioning enforced by repository access layers.

---

## 9–10. AI & RAG Requirements
- **TRD-AI-001**: Model Interchangeability via LiteLLM / custom model gateway.
- **TRD-RAG-001**: Application-level citation validator enforcing `[Doc ID, Page Num]` matching against retrieved chunks before client rendering.

---

## 11. OCR Requirements
- **TRD-OCR-001**: Multi-engine Indic OCR adapter (Tesseract / PaddleOCR) outputting page text layer and bounding-box JSON `[xmin, ymin, xmax, ymax]`.

---

## 12. Search Requirements
- **TRD-SRCH-001**: Reciprocal Rank Fusion (RRF) combining BM25 keyword scores and pgvector cosine similarity distance.

---

## 13. Storage Requirements
- **TRD-STOR-001**: Original PDF files stored immutably in S3-compatible Object Storage under server-generated keys `tenants/{tenant_id}/matters/{matter_id}/documents/{doc_id}/originals/`.

---

## 14. Audit Requirements
- **TRD-AUD-001**: Synchronous immutable database logging of all upload, view, search, query, verification, and export events.

---

## 15. Observability Requirements
- **TRD-OBS-001**: Structured JSON logging featuring `request_id`, `trace_id`, `tenant_id`, `matter_id`, and execution latency.

---

## 16. Backup & Recovery Requirements
- **TRD-BAC-001**: Automated daily PostgreSQL WAL archiving and S3 bucket versioning.

---

## 17–19. Deployment, Testing & Cost Constraints
- Single-node Docker Compose setup for local development.
- Target operating cost < ₹150 (~$1.80 USD) per 100-page matter processed.

---

## 20. Technical Requirements Matrix

| Requirement ID | Description | Priority | Rationale | Acceptance Test |
| :--- | :--- | :--- | :--- | :--- |
| **TRD-REQ-001** | Modular Monolith Backend | P0 | Prevents premature microservice overhead while preserving domain boundaries. | Architecture boundary test |
| **TRD-REQ-002** | PostgreSQL + pgvector Storage | P0 | Keeps relational and vector data in a unified SQL engine; zero vector DB cost. | SQL vector query test |
| **TRD-REQ-003** | Server-Side Citation Validation | P0 | Eliminates hallucinated page numbers from LLM output. | Citation validator unit test |
| **TRD-REQ-004** | Async Redis Job Queue | P0 | Offloads long-running OCR and chunking tasks from HTTP threads. | Worker idempotency test |
| **TRD-REQ-005** | Indic OCR Bounding Box Extractor | P0 | Provides visual coordinates for split-screen PDF highlighting. | Bounding box schema test |
| **TRD-REQ-006** | Tenant Access Isolation Guard | P0 | Ensures User from Org A cannot read files from Org B. | Cross-tenant access test |
