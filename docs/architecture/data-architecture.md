# Data Architecture & Storage Taxonomy

## Primary Data Classifications

### 1. Canonical Data (Authoritative Source of Truth)
- **Store**: PostgreSQL 16 Relational Database + Object Storage (S3 / MinIO).
- **Contents**: Original PDF deeds, User profiles, Matter metadata, Verified Property Entities, Audit Event Logs, System Configuration.
- **Rule**: PostgreSQL is the single source of truth for all business operations.

### 2. Derived Data (Re-buildable Processing Artifacts)
- **Store**: PostgreSQL tables (`ocr_results`, `document_pages`, `document_chunks`).
- **Contents**: Raw OCR text layers, Page bounding-box JSONs, Normalized markdown text.
- **Rule**: Derived data can be fully re-extracted from original source PDFs if processing algorithms update.

### 3. Vector & Search Indexes
- **Store**: PostgreSQL `pgvector` extension (HNSW index) + PostgreSQL Full-Text Search (tsvector BM25 index).
- **Contents**: 1536-dimensional float vectors of document chunks.
- **Critical Rule**: **The vector index is NOT the source of truth.** Vector search acts strictly as a retrieval accelerator. Every retrieved vector chunk must resolve back to a canonical `document_id` and `page_number` in PostgreSQL.

### 4. Cache & Temporary Data
- **Store**: Redis 7.0+.
- **Contents**: User sessions, OCR progress status, ephemeral RAG context buffers.
