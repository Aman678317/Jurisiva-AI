# Technical Requirements & System Standards

## Stack Definition
- **Frontend**: Web application (HTML/JS/Vanilla CSS or React/Vite shell) with Split-Screen PDF rendering.
- **Backend API**: Python FastAPI / Node.js async server.
- **Database**: PostgreSQL 16+ with `pgvector` extension for relational and vector embeddings.
- **OCR Engine**: Tesseract OCR / PaddleOCR with Indic script packages (eng, hin, kan, tam, mar, tel).
- **AI/LLM Layer**: LiteLLM wrapper supporting OpenAI / Anthropic / Local Ollama models.
- **Vector Search**: pgvector hybrid search (HNSW index + BM25 full text search).

## Technical Guardrails
- Desktop-first responsive layout (min resolution 1280x720).
- Sub-2 second response latency for cached search / RAG retrieval.
- Asynchronous task processing for document ingestion and OCR via Celery / Redis / Background workers.
