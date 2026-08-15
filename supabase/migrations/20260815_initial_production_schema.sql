-- ============================================================================
-- JURISIVA-AI PRODUCTION POSTGRESQL SCHEMA WITH PGVECTOR & ROW LEVEL SECURITY
-- ============================================================================

-- 1. Enable Required PostgreSQL Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- ----------------------------------------------------------------------------
-- 2. Organizations & Multi-Tenant Access Control
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan VARCHAR(50) DEFAULT 'ENTERPRISE',
    retention_days INT DEFAULT 90,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'LAWYER',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS memberships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'LAWYER', -- 'OWNER', 'ADMIN', 'LAWYER', 'REVIEWER', 'MEMBER'
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(organization_id, user_id)
);

-- ----------------------------------------------------------------------------
-- 3. Cases & Property Due Diligence Matters
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    case_name VARCHAR(255) NOT NULL,
    property_address TEXT NOT NULL,
    survey_numbers VARCHAR(255) NOT NULL,
    state VARCHAR(100) DEFAULT 'Karnataka',
    district VARCHAR(100) DEFAULT 'Bengaluru Rural',
    taluk VARCHAR(100) DEFAULT 'Devanahalli',
    hobli VARCHAR(100) DEFAULT 'Kasaba Hobli',
    village VARCHAR(100) DEFAULT 'Devanahalli',
    client_name VARCHAR(255) NOT NULL,
    lead_advocate VARCHAR(255) NOT NULL,
    sro_jurisdiction VARCHAR(255) DEFAULT 'SRO Devanahalli',
    status VARCHAR(50) DEFAULT 'ACTIVE_INVESTIGATION',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS properties (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    survey_number VARCHAR(100) NOT NULL,
    hissa VARCHAR(50) NOT NULL,
    extent_acres INT DEFAULT 2,
    extent_guntas INT DEFAULT 10,
    guidance_value VARCHAR(100),
    market_value VARCHAR(100),
    boundaries JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ----------------------------------------------------------------------------
-- 4. Case Documents & OCR Multilingual Intelligence
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    storage_path TEXT NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    page_count INT DEFAULT 1,
    ocr_status VARCHAR(50) DEFAULT 'COMPLETED',
    is_faded BOOLEAN DEFAULT FALSE,
    uploaded_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS document_pages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page_number INT NOT NULL,
    original_ocr_text TEXT,
    translated_text TEXT,
    language VARCHAR(50) DEFAULT 'en',
    ocr_confidence NUMERIC(5, 4) DEFAULT 0.9800,
    storage_path TEXT,
    UNIQUE(document_id, page_number)
);

CREATE TABLE IF NOT EXISTS ocr_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page_id UUID REFERENCES document_pages(id) ON DELETE CASCADE,
    raw_text TEXT NOT NULL,
    deskew_angle NUMERIC(5, 2) DEFAULT 0.00,
    contrast_enhanced BOOLEAN DEFAULT TRUE,
    stamps_detected INT DEFAULT 0,
    signatures_detected INT DEFAULT 0,
    confidence NUMERIC(5, 4) DEFAULT 0.9800,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS entities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    entity_type VARCHAR(100) NOT NULL, -- 'VENDOR', 'PURCHASER', 'EXTENT', 'SURVEY_NO', 'REG_NO', 'MORTGAGE'
    entity_value TEXT NOT NULL,
    standardized_value TEXT,
    page_number INT DEFAULT 1,
    confidence NUMERIC(5, 4) DEFAULT 0.9500,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    transaction_type VARCHAR(100) NOT NULL,
    execution_date DATE,
    vendor TEXT,
    purchaser TEXT,
    consideration_amount TEXT,
    registration_number VARCHAR(100),
    sro VARCHAR(150),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ----------------------------------------------------------------------------
-- 5. Ownership Devolution Graph & Chronological Timeline
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ownership_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    owner_name VARCHAR(255) NOT NULL,
    period VARCHAR(100) NOT NULL,
    extent VARCHAR(100) NOT NULL,
    transaction_type VARCHAR(100) NOT NULL,
    source_doc_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    page_number INT DEFAULT 1,
    confidence NUMERIC(5, 4) DEFAULT 0.9600,
    order_index INT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ownership_edges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    source_node_id UUID NOT NULL REFERENCES ownership_nodes(id) ON DELETE CASCADE,
    target_node_id UUID NOT NULL REFERENCES ownership_nodes(id) ON DELETE CASCADE,
    instrument_type VARCHAR(100) NOT NULL,
    transfer_date DATE,
    status VARCHAR(50) DEFAULT 'VERIFIED'
);

CREATE TABLE IF NOT EXISTS timeline_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    event_date VARCHAR(100) NOT NULL,
    event_year VARCHAR(10) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    parties TEXT NOT NULL,
    legal_significance TEXT NOT NULL,
    source_doc_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    page_number INT DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS risks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL, -- 'Title & Extent Risk', 'Encumbrance Risk', 'Missing Evidence'
    severity VARCHAR(50) NOT NULL, -- 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    finding TEXT NOT NULL,
    evidence TEXT NOT NULL,
    reason TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    source_doc_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    page_number INT DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ----------------------------------------------------------------------------
-- 6. Research Sessions, Sources & Verifiable Evidence
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS research_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    question TEXT NOT NULL,
    mode VARCHAR(50) DEFAULT 'CASE',
    status VARCHAR(50) DEFAULT 'COMPLETED',
    summary TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS research_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES research_sessions(id) ON DELETE CASCADE,
    source_name VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    authority_level VARCHAR(50) DEFAULT 'SUPREME_COURT',
    retrieved_at TIMESTAMPTZ DEFAULT NOW(),
    snippet TEXT
);

CREATE TABLE IF NOT EXISTS research_evidence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES research_sessions(id) ON DELETE CASCADE,
    source_id UUID REFERENCES research_sources(id) ON DELETE CASCADE,
    claim_text TEXT NOT NULL,
    verbatim_quote TEXT NOT NULL,
    verified BOOLEAN DEFAULT TRUE,
    confidence NUMERIC(5, 4) DEFAULT 0.9800
);

-- ----------------------------------------------------------------------------
-- 7. AI Runs, Drafting Studio, Reports & Immutable Audit Trail
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ai_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workflow_type VARCHAR(100) NOT NULL,
    model_used VARCHAR(100) NOT NULL,
    latency_ms INT NOT NULL,
    tokens_in INT DEFAULT 0,
    tokens_out INT DEFAULT 0,
    cost_estimate NUMERIC(8, 6) DEFAULT 0.000000,
    status VARCHAR(50) DEFAULT 'SUCCESS',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS drafts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    draft_type VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'REVIEW_REQUIRED',
    version INT DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    executive_summary TEXT NOT NULL,
    full_dossier_json JSONB NOT NULL,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    user_name VARCHAR(255) NOT NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(255),
    ip_address VARCHAR(100) DEFAULT '127.0.0.1',
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- ----------------------------------------------------------------------------
-- 8. Pgvector Embeddings for RAG & Hybrid Retrieval
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS document_embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page_id UUID REFERENCES document_pages(id) ON DELETE CASCADE,
    chunk_id VARCHAR(100) NOT NULL,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    chunk_text TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create HNSW Vector Index for fast cosine similarity search
CREATE INDEX IF NOT EXISTS document_embeddings_hnsw_idx 
ON document_embeddings USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- ----------------------------------------------------------------------------
-- 9. Background Worker Job Queue
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS job_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    job_type VARCHAR(100) NOT NULL, -- 'OCR_DOCUMENT', 'ANALYZE_DOCUMENT', 'REBUILD_OWNERSHIP', etc.
    status VARCHAR(50) DEFAULT 'QUEUED', -- 'QUEUED', 'RUNNING', 'COMPLETED', 'FAILED', 'RETRYING', 'CANCELLED'
    payload JSONB DEFAULT '{}'::jsonb,
    result JSONB DEFAULT '{}'::jsonb,
    attempts INT DEFAULT 0,
    max_attempts INT DEFAULT 3,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

-- ----------------------------------------------------------------------------
-- 10. Enable Row Level Security (RLS) on all Customer Tables
-- ----------------------------------------------------------------------------
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE properties ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_pages ENABLE ROW LEVEL SECURITY;
ALTER TABLE ocr_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE entities ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE ownership_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE ownership_edges ENABLE ROW LEVEL SECURITY;
ALTER TABLE timeline_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE risks ENABLE ROW LEVEL SECURITY;
ALTER TABLE research_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE research_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE research_evidence ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE drafts ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_embeddings ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_queue ENABLE ROW LEVEL SECURITY;

-- ----------------------------------------------------------------------------
-- 11. Define Tenant Isolation RLS Policies
-- ----------------------------------------------------------------------------

-- Helper function to check if current authenticated user belongs to an organization
CREATE OR REPLACE FUNCTION user_has_org_access(target_org_id UUID) 
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM memberships 
        WHERE memberships.organization_id = target_org_id 
        AND memberships.user_id = auth.uid()
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Organization Access Policy
CREATE POLICY org_tenant_isolation ON organizations
    FOR ALL USING (id IN (SELECT organization_id FROM memberships WHERE user_id = auth.uid()));

-- Cases Access Policy
CREATE POLICY cases_tenant_isolation ON cases
    FOR ALL USING (user_has_org_access(organization_id));

-- Documents Access Policy
CREATE POLICY documents_tenant_isolation ON documents
    FOR ALL USING (user_has_org_access(organization_id));

-- Embeddings Vector Search Tenant Isolation
CREATE POLICY embeddings_tenant_isolation ON document_embeddings
    FOR ALL USING (user_has_org_access(organization_id));

-- Risks & Analysis Tenant Isolation
CREATE POLICY risks_tenant_isolation ON risks
    FOR ALL USING (user_has_org_access(organization_id));

-- Ownership Graph Tenant Isolation
CREATE POLICY ownership_tenant_isolation ON ownership_nodes
    FOR ALL USING (user_has_org_access(organization_id));
