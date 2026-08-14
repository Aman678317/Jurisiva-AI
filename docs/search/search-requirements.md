# Search & Retrieval Requirements Specification

## 1. Core Requirements & Latency Targets
- **SRCH-REQ-001 (Exact Match Search)**: Must return exact matches for legal identifiers (Survey Numbers, Khasra Numbers, Deed Registration Numbers, Case Numbers) with 100% precision.
- **SRCH-REQ-002 (Hybrid Retrieval)**: Merges BM25 lexical search and pgvector cosine similarity search using Reciprocal Rank Fusion (RRF).
- **SRCH-REQ-003 (Strict Tenant Isolation)**: Authorization filters (`organization_id` & `matter_id`) enforced prior to similarity scoring.
- **SRCH-REQ-004 (Latency Target)**: Hybrid search response time < 1,500ms for p95 requests.
- **SRCH-REQ-005 (Evidence Sufficiency Gate)**: RAG system must return `INSUFFICIENT_EVIDENCE` when retrieved candidate similarity score falls below threshold (< 0.65).

---

## 2. Supported Search Types
- **Exact Match**: `Survey No. 42/1` -> Exact token match in `document_chunks`.
- **Phrase / Keyword**: `Deposit of Title Deeds` -> BM25 full-text rank.
- **Semantic Query**: `"documents discussing transfer of land ownership"` -> pgvector cosine distance.
- **Hybrid Multi-Factor**: RRF score = `1 / (60 + LexicalRank) + 1 / (60 + VectorRank)`.
