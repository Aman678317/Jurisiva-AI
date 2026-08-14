# Product Requirements Document (PRD) — India-First Legal & Property Intelligence Platform

## 1. Product Overview
An original, India-first, AI-powered Legal & Property Intelligence Platform built to assist property Advocates, title due-diligence specialists, law firm associates, and in-house legal teams in analyzing complex document bundles, conducting citation-grounded research, building chronological property timelines, reconciling title records, and generating auditable, evidence-backed legal work products.

---

## 2. Problem Statement
In the Indian legal and property domain:
1. **Extreme Document Density & Manual Overhead**: Title search and litigation review require manually reading 13 to 30+ year document bundles (100–1000 pages of scanned PDFs, stamp papers, and regional deeds), taking 6–10 hours per matter.
2. **Scanned & Multilingual Friction**: Pre-2005 deeds exist as low-resolution scanned PDFs combining English, Hindi, Kannada, Marathi, Tamil, and Telugu scripts, rendering generic OCR and search useless.
3. **High Discrepancy & Title Risk**: Manual review frequently overlooks extent mismatches (e.g. Sale Deed vs. Pahani/RTC), missing link deeds, or un-discharged bank mortgages.
4. **Hallucination Risk in Generic AI**: Standard AI tools lack citation grounding, rendering their outputs legally inadvisable without re-reading source documents.

---

## 3. Target Users
- Primary: **Property Advocates & Title Search Specialists** (Bank Panel Lawyers, Solo Practitioners, Property Law Firms).
- Secondary: **Indian Law-Firm Litigation Associates** & **In-House Corporate Legal Managers**.

---

## 4. Primary User
**Property Advocate / Title Search Specialist**: Focuses on real-estate transactions, mortgage due diligence, land title search reports, and boundary/extent verification.

---

## 5. Secondary Users
- **Law-Firm Associate**: Handles litigation case bundles, court filings, and evidence discovery.
- **In-House Legal Professional**: Manages commercial leases, corporate agreements, and compliance audits.

---

## 6. Jobs-to-be-Done (JTBD Summary)
- **JTBD-01**: Property Ownership & Extent Reconciliation.
- **JTBD-02**: Chronological Title Flow Timeline Construction.
- **JTBD-03**: Citation-Aware Document Q&A & Evidence Search.
- **JTBD-04**: Cross-Document Contradiction & Gap Detection.
- **JTBD-05**: Draft Title Search Report (TSR) Generation.

---

## 7. MVP Goal
Deliver an end-to-end, evidence-grounded desktop workspace where a Property Advocate can upload a 20-document property bundle, perform OCR text extraction, inspect side-by-side split citations, view an automated title flow timeline, detect extent discrepancies, and export an editable Title Search Report in < 45 minutes with 100% citation traceability.

---

## 8. MVP Scope
1. Secure Authentication & Matter-isolated RBAC.
2. Workspace & Matter Creation.
3. Document Bundle Upload & Immutable Storage.
4. Indic Multilingual OCR & Text Extraction (English, Hindi, Kannada, Marathi, Tamil, Telugu).
5. Split-Screen Document Viewer with visual bounding-box citation highlights.
6. Hybrid Vector (pgvector) + BM25 Search.
7. Citation-Aware RAG Copilot Assistant.
8. Property Entity Extraction (Parties, Dates, Extent, Survey #, Boundaries, Encumbrances).
9. Chronological Title Flow Timeline Construction.
10. Cross-Document Contradiction & Missing Link-Deed Detection.
11. Human Review & Data Badging Workflow (`SOURCE FACT`, `AI EXTRACTION`, `AI INFERENCE`, `HUMAN VERIFIED`, `UNKNOWN`).
12. Editable Title Search Report (.docx / PDF) Export.
13. Immutable Audit Logging.

---

## 9. Non-Goals (Explicitly Excluded)
- Autonomous legal decision making.
- Direct automated court or e-Courts portal filing.
- Undocumented government portal scraping.
- Autonomous unguided AI agents.
- Complex multi-tenant enterprise billing engines.
- Mobile-first native application.

---

## 10–13. Requirements Specification Table (Functional & Non-Functional)

| Requirement ID | Description | Priority | Target User | Acceptance Criteria | Dependencies | Test Method |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-AUTH-001** | User Authentication & Session Management | P0 | All | Validates credentials, issues JWT, handles session expiration gracefully. | DB Auth Schema | Automated Auth E2E Test |
| **REQ-MAT-001** | Matter Workspace Creation | P0 | Advocate | Create matter with Title, Client, Property Details, and Access Roles. | REQ-AUTH-001 | Integration Test |
| **REQ-DOC-001** | Multi-file Document Bundle Upload | P0 | Advocate | Upload PDF/TIFF/PNG up to 100MB per file; client-side SHA-256 hash generation. | REQ-MAT-001 | E2E Upload Test |
| **REQ-OCR-001** | Indic Multilingual OCR Processing | P0 | Advocate | Extracts clean text layer + page bounding-box JSON across English & Indic scripts (CER < 10%). | REQ-DOC-001 | OCR CER Benchmark Test |
| **REQ-VIEW-001** | Split-Screen Document Viewer | P0 | Advocate | Renders PDF page on left, extracted OCR text on right; highlights search/citation bounding box. | REQ-OCR-001 | Visual Component Test |
| **REQ-SRCH-001** | Hybrid Keyword + Vector Search | P0 | All | Returns matter search results in < 2s ranked by BM25 + pgvector cosine similarity. | REQ-OCR-001 | Search Recall@k Test |
| **REQ-AI-001** | Citation-Aware RAG Copilot | P0 | All | Answers user queries strictly grounded in matter docs; inline clickable `[Doc, Page]` citations. | REQ-SRCH-001 | Ragas Faithfulness Test |
| **REQ-PROP-001** | Property Entity Extraction | P0 | Advocate | Extracts Survey #, Extent, Executants, Claimants, Boundaries, Encumbrance values into schema. | REQ-OCR-001 | Extraction Schema Test |
| **REQ-TIME-001** | Property Title Flow Timeline | P0 | Advocate | Chronologically orders registered deeds; flags missing link-deed gaps in chain of title. | REQ-PROP-001 | Timeline Logic Test |
| **REQ-CONT-001** | Contradiction & Gap Detection | P0 | Advocate | Flags extent discrepancies (e.g. 2400 sq.ft vs 2100 sq.ft) across deeds in matter. | REQ-PROP-001 | Red-Flag Assertion Test |
| **REQ-HUM-001** | Human Verification & Badging | P0 | Advocate | User can mark entity extractions as `HUMAN VERIFIED` or `REJECTED`; records user timestamp. | REQ-PROP-001 | Verification State Test |
| **REQ-REP-001** | Title Search Report Export | P0 | Advocate | Generates formatted MS Word (.docx) TSR populated with verified entities and title flow. | REQ-HUM-001 | DOCX Structure Test |
| **REQ-AUD-001** | Immutable Audit Trail Logging | P0 | All | Logs every upload, search, query, verification, and export action with IP and timestamp. | All | Audit Trail Query Test |

---

## 14. AI Requirements
- RAG context assembly strictly enforced with system-level non-hallucination prompts.
- Streaming responses with real-time token rendering.
- Mandatory citation generation: Every claim must cite `[Document Name, Page Number, Snippet ID]`.
- Abstention requirement: Model must respond "Insufficient evidence in uploaded documents" if context lacks supporting proof.

---

## 15. Security Requirements
- Logical tenant isolation by Matter ID.
- AES-256 encryption at rest; TLS 1.3 in transit.
- Role-Based Access Control (Admin, Lead Advocate, Associate, Auditor).
- Zero user data transmission to public LLM training datasets.

---

## 16. Audit Requirements
- Immutable logging of User ID, Action, Matter ID, Resource ID, Client IP, and UTC Timestamp.
- Exportable audit log report for compliance verification.

---

## 17. Evidence & Citation Requirements
- Interactive citations: Clicking inline badge highlights bounding-box text in split viewer.
- Citation integrity check: System validates that cited page exists before rendering badge.

---

## 18. Multilingual Requirements
- Indic OCR support for English, Hindi, Kannada, Marathi, Tamil, and Telugu.
- Unicode UTF-8 string preservation across UI components.

---

## 19. Property-Intelligence Requirements
- Normalized land area units (Acres, Guntas, Cents, Sq.Ft, Sq.Yards).
- Property Schedule parser extracting North, South, East, West boundaries.

---

## 20. Research Requirements
- Matter-scoped research history log.
- Query refinement and filter by document category (Deed, EC, Land Extract, Litigation).

---

## 21. Reporting Requirements
- Export formats: Editable DOCX and read-only PDF.
- Report template options: Bank Standard Title Search Report, Short Legal Opinion.

---

## 22–25. UX State Requirements
- **Error States**: Clear human-readable message + action recovery button (e.g. "OCR processing timed out. [Retry OCR]").
- **Empty States**: Helpful onboarding illustration + primary action call-to-action (e.g. "No documents uploaded yet. [Upload PDF Bundle]").
- **Loading States**: Skeleton screens + explicit status text ("Processing Page 4 of 12...").
- **Permission States**: Disabled action state + tooltip explaining required role ("Requires Lead Advocate permission").

---

## 26. Product Analytics Events
- Tracked events: `matter_created`, `document_uploaded`, `ocr_completed`, `citation_clicked`, `finding_verified`, `report_exported`. Zero raw document text sent to analytics.

---

## 27. Success Metrics
- 10 quantitative targets defined in [`docs/success-metrics.md`](file:///c:/Users/acer/Desktop/legal/docs/success-metrics.md).
