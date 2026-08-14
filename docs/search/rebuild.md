# Index Rebuild & Idempotency Strategy

## Rebuild Procedure
If vector indexes or full-text search indexes become corrupted or require a model upgrade (e.g. switching embedding models from 1536-dim to a new multilingual model):

1. **Execution Command**:
   ```bash
   python -m app.search.rebuild --matter-id=mat_001 --force
   ```
2. **Rebuild Steps**:
   - Fetches canonical `document_pages` rows for target matter from PostgreSQL.
   - Re-chunks page text using `StructureAwareChunker`.
   - Re-generates 1536-dim vector embeddings via `EmbeddingProvider`.
   - Atomically updates `document_chunks` table within a single SQL transaction.
3. **Idempotency Guarantee**: Chunk content hash `SHA-256(text + page_id + version_id)` prevents creating duplicate vector rows during re-indexing.
