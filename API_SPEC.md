# API Specifications

## Authentication & Workspace Endpoints
- `POST /api/v1/auth/login`: User authentication & JWT issuance.
- `GET /api/v1/matters`: List active legal matters.
- `POST /api/v1/matters`: Create a new matter workspace.

## Document & Ingestion Endpoints
- `POST /api/v1/matters/{matter_id}/documents`: Upload document bundle.
- `GET /api/v1/documents/{doc_id}`: Get document metadata and OCR status.
- `GET /api/v1/documents/{doc_id}/pages/{page_num}`: Fetch page image + OCR bounding boxes.

## Intelligence & Analysis Endpoints
- `POST /api/v1/matters/{matter_id}/search`: Execute hybrid keyword + semantic search.
- `POST /api/v1/matters/{matter_id}/chat`: Citation-aware RAG query.
- `GET /api/v1/matters/{matter_id}/entities`: Retrieve extracted entities & verification status.
- `GET /api/v1/matters/{matter_id}/timeline`: Retrieve property timeline.
- `GET /api/v1/matters/{matter_id}/contradictions`: Detect inconsistencies across matter documents.
- `POST /api/v1/entities/{entity_id}/verify`: Human review verification endpoint.
