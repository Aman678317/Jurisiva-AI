# Product Scope Matrix — MoSCoW Prioritization

## Overview
This scope matrix governs all feature inclusions and exclusions for the MVP build, enforcing strict guardrails against feature creep.

---

## 1. MUST HAVE (Core MVP — Non-Negotiable)

| Feature / Module | Description | Rationale |
| :--- | :--- | :--- |
| **Authentication & RBAC** | Login, Password Reset, Roles (Lead Advocate, Associate, Auditor). | Essential for client data security and matter access control. |
| **Matter Workspace** | Create, view, search, and manage legal/property matters. | Core organizational structure for isolating document bundles. |
| **Document Ingestion & Storage** | PDF/TIFF upload, SHA-256 hashing, immutable storage. | Foundation for all document intelligence workflows. |
| **Indic Multilingual OCR** | Text layer + page bounding-box JSON extraction (Eng, Hin, Kan, Mar, Tam, Tel). | Critical for Indian historical deeds and scanned stamp papers. |
| **Split-Screen Document Viewer** | Side-by-side PDF rendering with live yellow bounding-box highlights. | Non-negotiable for visual evidence verification by Advocates. |
| **Hybrid Search (Vector + BM25)** | Combined semantic vector search (pgvector) and keyword search. | Enables sub-2s document retrieval across matter files. |
| **Citation-Aware RAG Copilot** | Natural language Q&A strictly grounded in matter text with inline clickable `[Doc, Page]` citations. | Core AI assistant workflow; eliminates hallucination risk. |
| **Property Entity Extraction** | Extract Survey #, Extent, Parties, Boundaries, Encumbrance details into structured schema. | Core requirement for automated land title due diligence. |
| **Title Flow Timeline** | Automated chronological ordering of registered deeds; flags missing link deeds. | Primary time-saver for Advocate title search report preparation. |
| **Extent & Boundary Contradictions**| Automated cross-deed discrepancy detection (e.g., Extent mismatches). | High-value risk detection for bank panel due diligence. |
| **Human Verification Badging** | UI for Advocates to inspect, edit, and tag findings as `HUMAN VERIFIED`. | Enforces human-in-the-loop accountability. |
| **Title Search Report Export** | Export editable MS Word (.docx) Title Search Report. | Primary deliverable expected by Advocates and bank clients. |
| **Immutable Audit Logging** | Log user ID, action, matter ID, timestamp, client IP for every operation. | Required for legal compliance and security auditing. |

---

## 2. SHOULD HAVE (Post-MVP / Fast Follow — Phase 2)

| Feature / Module | Description | Rationale |
| :--- | :--- | :--- |
| **Litigation Case Bundle Analysis** | Court affidavit fact extraction, witness statement contradiction finder. | Expands platform into litigation practice once title diligence is stable. |
| **Batch PDF Zip Upload** | Drag and drop folder containing 30 PDFs in a single zip archive. | Speeds up initial matter onboarding for large historical archives. |
| **Custom TSR Bank Templates** | Pre-configured templates for specific Indian banks (e.g. SBI, HDFC, ICICI TSR formats). | High convenience for bank panel Advocates; deferrable to Phase 2. |
| **Advanced OCR Preprocessing Controls**| Manual thresholding, deskew slider, and manual crop tools in UI viewer. | Helpful for severely degraded scans; manual workaround exists. |

---

## 3. COULD HAVE (Future Enhancements — Phase 3)

| Feature / Module | Description | Rationale |
| :--- | :--- | :--- |
| **Commercial Lease Abstraction** | Extract rent escalations, termination clauses, indemnity caps. | Corporate legal feature; lower priority than property diligence. |
| **Multi-Matter Cross Search** | Search across all firm matters simultaneously. | Useful for large firms; adds cross-tenant search complexity. |
| **Voice Query Support (Indic)** | Ask copilot questions via Hindi/Kannada speech-to-text. | Impressive demo feature; desktop lawyers prefer typing. |

---

## 4. NOT NOW (Explicitly Excluded from MVP)

| Feature / Module | Description | Rationale for Exclusion |
| :--- | :--- | :--- |
| **Autonomous Court / e-Courts Filing** | Automated submission of petitions to e-Courts portals. | High regulatory risk; fragile third-party web portals. |
| **Undocumented Government Web Scraping**| Scraping Bhoomi/Kaveri/AnyRoR land portals without official API. | Violates core principle: *Never invent APIs or rely on undocumented web-scraping.* |
| **Autonomous Multi-Agent Swarms** | Looping LLM agents taking actions without human step-approval. | High risk of unguided execution and unexpected API costs. |
| **Native Mobile App (iOS/Android)** | Dedicated smartphone applications. | Title diligence is an intensive desktop workflow (multi-monitor split view). |
| **Complex Enterprise Billing Engine** | Metered stripe usage engines, complex seat management. | Keep billing flat/simple per-matter during initial MVP phase. |
