# Document Processing Pipeline Architecture

## Pipeline Stage Workflow

```
[UPLOAD]
  ↓ Validate file extension, size <= 100MB, calculate client-side SHA-256 hash.
[STORE ORIGINAL]
  ↓ Save raw binary file to `tenants/{tenant_id}/matters/{matter_id}/documents/{doc_id}/originals/`.
[SAFETY CHECK]
  ↓ Magic bytes validation & virus scan check.
[EXTRACT LAYOUT]
  ↓ Convert PDF pages to 200 DPI images; extract page count.
[INDIC OCR ENGINE]
  ↓ Run PaddleOCR / Tesseract Indic model -> Extract raw OCR text layer & bounding box JSON.
[NORMALIZE & CLASSIFY]
  ↓ Clean control characters; auto-classify document type (Sale Deed, Pahani, EC, etc.).
[CHUNK & EMBED]
  ↓ Split text into 512-token chunks with 64-token overlap; compute 1536-dim vector embeddings.
[INDEX & EVIDENCE READY]
  ↓ Store chunks & embeddings in pgvector; update document status to `PROCESSED`.
```

---

## Idempotency & Failure Handling
- **Idempotency**: Retrying a processing job for document `doc_id` deletes previous derived page/chunk rows before re-extracting, preventing duplicate vector rows.
- **Retries**: Exponential backoff retry (3 attempts) on transient OCR/embedding errors. Permanent failure marks status `FAILED` with actionable error code.
