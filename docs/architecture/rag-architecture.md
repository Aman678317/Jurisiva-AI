# RAG & Citation Architecture Specification

## RAG Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Advocate as Advocate User
    participant API as FastAPI Backend Gateway
    participant Guard as Tenant Isolation Guard
    participant DB as pgvector & BM25 Index
    participant LLM as LiteLLM Gateway
    participant Val as Citation Validator

    Advocate->>API: POST /api/v1/matters/{matter_id}/chat (Query String)
    API->>Guard: Validate User Membership (Org ID, Matter ID)
    Guard-->>API: Authorized
    API->>DB: Execute Hybrid Vector Search (Scoped by Matter ID)
    DB-->>API: Return Top 5 Relevant Chunks + Page Metadatas
    API->>LLM: Assemble RAG Prompt + Chunks (Context-Bounded System Prompt)
    LLM-->>API: Streamed Markdown Response + Inline Citations [Doc X, Page Y]
    API->>Val: Verify Cited Pages Exist in Matter Chunk DB
    Val-->>API: Citation Integrity Verified
    API-->>Advocate: Stream Response + Interactive Citation Badges
```

---

## Application-Level Citation Validation Layer
- **Rule**: The LLM is NEVER the final authority on citation validity.
- **Validation Engine**: Backend inspects every returned citation tag `[Doc X, Page Y]`:
  1. Checks if `doc_id=X` belongs to `matter_id`.
  2. Verifies `page_number=Y` is within `doc.page_count`.
  3. Validates text snippet overlap against `document_pages.raw_ocr_text`.
  4. If invalid, transforms badge to `[Citation Unverified]` alert state.
