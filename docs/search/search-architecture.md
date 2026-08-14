# Search & Hybrid RAG Architecture

## Search Retrieval Pipeline

```mermaid
graph TD
    Query[User Query: 'Find mortgage details for Sy No 42/1'] --> AuthGuard[Tenant Isolation & Matter Authorization Guard]
    AuthGuard --> LexicalEngine[Lexical BM25 Search Engine]
    AuthGuard --> VectorEngine[pgvector HNSW Cosine Search]
    
    LexicalEngine -->|Lexical Candidates| RRFMerger[Reciprocal Rank Fusion Reranker]
    VectorEngine -->|Vector Candidates| RRFMerger
    
    RRFMerger --> SufficiencyGate[Evidence Sufficiency Gate]
    SufficiencyGate -->|Score >= 0.65| PromptAssembler[Context-Bounded Prompt Assembler]
    SufficiencyGate -->|Score < 0.65| RefusalHandler[Return INSUFFICIENT_EVIDENCE]
    
    PromptAssembler --> LLM[LiteLLM Gateway]
    LLM --> CitationVal[Server-Side Citation Validator]
    CitationVal --> ClientOutput[Grounded Response with Clickable Citations]
```

---

## Derived Data Model Rule
The PostgreSQL database, raw OCR pages, and immutable source PDFs are the sole canonical truth. Vector embeddings and full-text indexes are **derived data artifacts** that can be completely wiped and reconstructed at any time using `python -m app.search.rebuild`.
