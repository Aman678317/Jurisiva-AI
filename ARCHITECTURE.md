# High-Level System Architecture

```mermaid
graph TD
    Client[Web Client UI] -->|REST / WebSocket| API[FastAPI Server]
    API --> Auth[Authentication & RBAC]
    API --> Worker[Async Background Queue]
    Worker --> OCR[OCR Pipeline - Tesseract/PaddleOCR]
    Worker --> Extractor[Text & Layout Extractor]
    Worker --> Embedder[Embedding Generator]
    Embedder --> DB[(PostgreSQL + pgvector)]
    API --> RAG[RAG Orchestration Engine]
    RAG --> DB
    RAG --> LLM[LiteLLM Adapter Layer]
```

## System Components
1. **Frontend Workspace**: Split-screen viewer, chat interface, timeline graph, verification panels.
2. **Core API Service**: Handles matter management, document ingestion workflows, RBAC enforcement.
3. **Ingestion & OCR Pipeline**: Converts uploaded PDFs into clean Markdown/text chunks with page bounding box coordinates.
4. **Hybrid Search & Vector Store**: PostgreSQL storing document metadata, raw text, entity extractions, and 1536-dim vector embeddings.
5. **RAG & Citation Engine**: Constructs prompts with explicit snippet metadata; validates returned citations before sending to client.
