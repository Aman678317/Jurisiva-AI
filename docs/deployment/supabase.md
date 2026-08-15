# Supabase Database, Auth, Storage & pgvector Setup

This guide details configuring Supabase as the primary relational database, authentication provider, vector index, and private file vault for Jurisiva-AI.

---

## 1. Database Migrations

Apply the migration file to your Supabase project:

```bash
# Using Supabase CLI
supabase db push

# Or via Supabase SQL Editor:
# Copy and execute supabase/migrations/20260815_initial_production_schema.sql
```

### Key Extensions Enabled
- `uuid-ossp`: For secure, non-sequential UUID primary keys.
- `vector`: For storing 1536-dimensional legal document embeddings.

---

## 2. Row Level Security (RLS) & Multi-Tenancy

Every table in the Jurisiva schema enforces Row Level Security:
- Users can only query or modify rows matching their organization membership (`user_has_org_access(organization_id)`).
- Customer A can never access or leak data belonging to Customer B.

---

## 3. Storage Buckets & Privacy

Create 3 private storage buckets in the Supabase Dashboard:

1. **`case-documents`**:
   - **Public**: `false` (Private)
   - **Allowed MIME types**: `application/pdf`, `image/jpeg`, `image/png`, `image/tiff`
   - **Path Pattern**: `organizations/{org_id}/cases/{case_id}/documents/{doc_id}/...`

2. **`case-artifacts`**:
   - **Public**: `false` (Private)
   - **Allowed MIME types**: `image/*`, `application/json`
   - **Path Pattern**: `organizations/{org_id}/cases/{case_id}/artifacts/...`

3. **`reports`**:
   - **Public**: `false` (Private)
   - **Allowed MIME types**: `application/pdf`, `application/json`
   - **Path Pattern**: `organizations/{org_id}/cases/{case_id}/reports/...`

---

## 4. Vector Search & RAG

The `document_embeddings` table uses an HNSW index with cosine similarity:

```sql
SELECT chunk_text, 1 - (embedding <=> query_vector) AS similarity
FROM document_embeddings
WHERE organization_id = $org_id
  AND case_id = $case_id
ORDER BY embedding <=> query_vector
LIMIT 5;
```
All vector queries MUST be filtered by `organization_id` and `case_id`. Unrestricted global vector queries are strictly forbidden.
