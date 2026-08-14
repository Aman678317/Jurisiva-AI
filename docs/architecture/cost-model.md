# Cost Architecture & Unit Economics Model

## Estimated Processing Cost per 100-Page Property Matter

| Component / Layer | Free / Self-Hosted Option (Dev & Baseline) | Production Cloud Cost (Estimated) | Unit Cost per 100-Page Bundle |
| :--- | :--- | :--- | :--- |
| **Compute & API Server** | Local Docker / VPS ($10/mo fixed) | Linux VPS (4 vCPU, 8GB RAM) | ~₹15 ($0.18 USD) |
| **Database & Vector Storage**| PostgreSQL 16 + pgvector (Free) | Managed Postgres / VPS | ~₹10 ($0.12 USD) |
| **Object Storage** | MinIO (Free local) | AWS S3 / Cloudflare R2 | ~₹5 ($0.06 USD) |
| **OCR Text Extraction** | Local Tesseract / PaddleOCR (Free) | Local GPU worker / Cloud OCR | ~₹20 ($0.24 USD) |
| **Embeddings (1536-dim)** | Open-source Sentence Transformers / Ollama | OpenAI `text-embedding-3-small` | ~₹10 ($0.12 USD) |
| **LLM RAG Inference** | Local Qwen 2.5 / Llama 3 via Ollama | GPT-4o-mini / Claude 3.5 Haiku | ~₹60 ($0.72 USD) |
| **Total Processing Cost** | **₹0 / Local Dev** | **Production Cloud Target** | **< ₹120 (~$1.44 USD)** |

---

## Cost Guardrails & Architecture Principles
- **No Per-Vector Storage Subscriptions**: Relying on pgvector inside PostgreSQL keeps vector storage costs at ₹0 above database hosting.
- **Model Provider Replaceability**: If cloud LLM prices increase, LiteLLM gateway can route background tasks to lower-cost models (e.g. DeepSeek / Qwen / local Ollama) without application rewrites.
