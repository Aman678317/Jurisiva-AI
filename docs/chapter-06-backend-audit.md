# Chapter 6 — Backend Foundation Audit

## 1. Audit Summary & Architecture Inspection

| Component / Layer | Existing Specification | Target Implementation | Status & Action |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | FastAPI (Python 3.11+ async) | FastAPI Application Server | **IMPLEMENTING** in `services/api/app` |
| **Database & Migration**| PostgreSQL 16+ + Alembic | SQLAlchemy 2.0 Async + Alembic Migrations | Database schemas & migration scripts |
| **Authentication** | JWT with HttpOnly cookies | Passlib bcrypt hashing + PyJWT session issuance | Auth router & middleware |
| **Authorization** | Server-side RBAC + Tenant Scoping | Custom Policy Middleware (`LEAD_ADVOCATE`, `ASSOCIATE`, `AUDITOR`) | Strict resource level verification guard |
| **Multi-Tenancy** | Column-level (`organization_id` & `matter_id`) | Scoped Repository pattern & SQL query filters | Cross-tenant access block test suite |
| **Object Storage** | S3 / MinIO S3-compatible | Boto3 / Local File Storage Adapter | Secure file path hashing & presigned URLs |
| **Async Jobs** | Redis + Celery / ARQ Job Queue | Job State Machine & Worker Foundation | Processing queue & retry handling |
| **Observability** | Structured JSON logs + Request IDs | ContextVar `request_id` & `trace_id` logging | Middleware logging pipeline |

---

## 2. Risk & Vulnerability Mitigation Analysis
- **IDOR / Tenant Leakage**: Client passing `organization_id` or `matter_id` in request body.
  - *Fix*: Server resolves user membership from authenticated JWT session; rejects request if matter does not belong to authorized org.
- **Unchecked File Access**: Exposing direct disk paths for uploaded PDFs.
  - *Fix*: Controlled endpoint generating short-lived signed URLs with authorization verification.
- **Unbounded Async Job Retries**: Workers looping indefinitely on corrupt documents.
  - *Fix*: Bounded exponential backoff (max 3 attempts); state transitions to `FAILED` with safe error codes.
