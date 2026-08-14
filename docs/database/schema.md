# Relational Database Schema Specification (PostgreSQL 16+)

## Core Entities & Tables

### 1. `organizations`
- `id`: `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- `name`: `VARCHAR(255) NOT NULL`
- `jurisdiction`: `VARCHAR(100) DEFAULT 'India'`
- `created_at`: `TIMESTAMPTZ DEFAULT clock_timestamp()`

### 2. `users`
- `id`: `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- `email`: `VARCHAR(255) UNIQUE NOT NULL`
- `hashed_password`: `VARCHAR(255) NOT NULL`
- `full_name`: `VARCHAR(255) NOT NULL`
- `bar_council_id`: `VARCHAR(100)`
- `created_at`: `TIMESTAMPTZ DEFAULT clock_timestamp()`

### 3. `memberships`
- `id`: `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- `organization_id`: `UUID REFERENCES organizations(id) ON DELETE CASCADE`
- `user_id`: `UUID REFERENCES users(id) ON DELETE CASCADE`
- `role`: `VARCHAR(50) NOT NULL` -- `ADMIN`, `LEAD_ADVOCATE`, `ASSOCIATE`, `AUDITOR`

### 4. `matters`
- `id`: `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- `organization_id`: `UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE`
- `title`: `VARCHAR(255) NOT NULL`
- `client_name`: `VARCHAR(255) NOT NULL`
- `survey_number`: `VARCHAR(100)`
- `district`: `VARCHAR(100)`
- `state`: `VARCHAR(100)`
- `created_by`: `UUID REFERENCES users(id)`
- `created_at`: `TIMESTAMPTZ DEFAULT clock_timestamp()`

### 5. `documents`
- `id`: `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- `organization_id`: `UUID NOT NULL REFERENCES organizations(id)`
- `matter_id`: `UUID NOT NULL REFERENCES matters(id) ON DELETE CASCADE`
- `filename`: `VARCHAR(255) NOT NULL`
- `file_hash`: `CHAR(64) NOT NULL` -- SHA-256
- `file_size_bytes`: `BIGINT NOT NULL`
- `mime_type`: `VARCHAR(100) NOT NULL`
- `storage_path`: `TEXT NOT NULL`
- `ocr_status`: `VARCHAR(50) DEFAULT 'QUEUED'`
- `page_count`: `INT DEFAULT 0`
- `uploaded_by`: `UUID REFERENCES users(id)`
- `created_at`: `TIMESTAMPTZ DEFAULT clock_timestamp()`

### 6. `document_pages`
- `id`: `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- `document_id`: `UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE`
- `page_number`: `INT NOT NULL`
- `raw_ocr_text`: `TEXT`
- `ocr_confidence`: `FLOAT`
- `bbox_json`: `JSONB`

### 7. `document_chunks`
- `id`: `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- `document_id`: `UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE`
- `page_number`: `INT NOT NULL`
- `chunk_index`: `INT NOT NULL`
- `content`: `TEXT NOT NULL`
- `embedding`: `vector(1536)` -- pgvector extension

### 8. `extracted_entities`
- `id`: `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- `matter_id`: `UUID NOT NULL REFERENCES matters(id) ON DELETE CASCADE`
- `document_id`: `UUID REFERENCES documents(id)`
- `entity_type`: `VARCHAR(50) NOT NULL` -- `SURVEY_NO`, `EXTENT`, `EXECUTANT`, `CLAIMANT`, `BOUNDARY`, `MORTGAGE`
- `extracted_value`: `TEXT NOT NULL`
- `verified_value`: `TEXT`
- `verification_status`: `VARCHAR(50) DEFAULT 'AI_EXTRACTION'` -- `SOURCE_FACT`, `AI_EXTRACTION`, `HUMAN_VERIFIED`, `REJECTED`
- `source_page`: `INT`
- `verified_by`: `UUID REFERENCES users(id)`
- `verified_at`: `TIMESTAMPTZ`

### 9. `property_timelines`
- `id`: `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- `matter_id`: `UUID NOT NULL REFERENCES matters(id) ON DELETE CASCADE`
- `event_date`: `DATE`
- `document_id`: `UUID REFERENCES documents(id)`
- `deed_type`: `VARCHAR(100)`
- `executant`: `TEXT`
- `claimant`: `TEXT`
- `extent_description`: `TEXT`
- `consideration_amount`: `DECIMAL(15,2)`
- `is_link_gap_warning`: `BOOLEAN DEFAULT FALSE`

### 10. `audit_logs`
- `id`: `UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- `organization_id`: `UUID NOT NULL REFERENCES organizations(id)`
- `matter_id`: `UUID REFERENCES matters(id)`
- `user_id`: `UUID REFERENCES users(id)`
- `action`: `VARCHAR(100) NOT NULL`
- `resource_type`: `VARCHAR(50) NOT NULL`
- `resource_id`: `UUID`
- `ip_address`: `VARCHAR(45)`
- `timestamp`: `TIMESTAMPTZ DEFAULT clock_timestamp()`
