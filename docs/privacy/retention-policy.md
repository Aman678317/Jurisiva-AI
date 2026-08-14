# Data Retention & Deletion Specification

## Deletion Execution Mechanics
When a user or organization initiates a matter or document deletion request:

1. **Immediate Soft Delete**: Sets `deleted_at = NOW()` and status = `ARCHIVED`. Document becomes un-queryable instantly.
2. **Hard Database Deletion**: Async worker deletes `document_pages`, `document_chunks`, `extracted_entities`, and `property_evidence_links` rows within 24 hours.
3. **Storage Artifact Wipe**: Removes immutable binary PDF and derived PNG thumbnails from S3 object storage.
4. **Vector Cache Eviction**: Purges vector index embeddings from `pgvector` store.
