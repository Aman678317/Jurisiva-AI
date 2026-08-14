# Security Threat Model & Risk Assessment

## 1. Threat Matrix & Controls

| Asset / Boundary | Threat Vector | Risk Level | Security Control | Residual Risk |
| :--- | :--- | :---: | :--- | :---: |
| **Tenant Document Storage** | Unauthorized cross-tenant document download | CRITICAL | Server-side `verify_tenant_access` + signed S3 URLs | LOW |
| **AI Prompt Engine** | Direct & Indirect Prompt Injection via scanned PDF text | HIGH | Context wrapping inside `<source_document>` + System Policy `v1.2.0` | LOW |
| **Citation System** | Hallucinated page number citations | HIGH | Application-level `CitationValidator` checking DB page bounds | LOW |
| **External Research APIs** | SSRF requesting internal private subnets | HIGH | `SSRFSecurityGuard` blocking localhost & private IP ranges | LOW |
| **User Identity & Sessions**| Session hijacking or token theft | MEDIUM | HttpOnly cookies + 24-hr token expiration + PBKDF2 hashing | LOW |
| **Database & Vector Store** | Direct unauthorized SQL access | CRITICAL | Column-level tenant isolation + least-privilege DB credentials | LOW |

---

## 2. Security Boundaries & Trust Zones
- **Trust Zone 0 (Core Engine)**: Database, S3 Object Storage, Worker Processes, FastAPI Server.
- **Trust Zone 1 (User Session)**: Authenticated Advocate session with JWT token.
- **Trust Zone 2 (Untrusted Data)**: Uploaded PDF/PNG documents, external public research web responses, user search queries.
