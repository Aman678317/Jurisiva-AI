# MVP Scope & Non-Goals

## MVP Included Features (13 Core Capabilities)
1. **Secure Authentication & RBAC**: Role-based access control, matter level permissions, secure session handling.
2. **Workspace & Matter Management**: Organization into discrete legal matters/cases with metadata, tags, and team assignment.
3. **Document Upload & Storage**: Multi-format support (PDF, TIFF, JPEG, PNG, DOCX) with client-side hashing and immutable storage.
4. **OCR & Indic Text Extraction**: High-accuracy OCR for clean, scanned, and multilingual documents (English, Hindi, Kannada, Tamil, Marathi, Telugu).
5. **Interactive Document Viewer**: Split-screen viewer with side-by-side document rendering, OCR text layer overlay, and bounding box highlights.
6. **Unified Hybrid Search**: Keyword (BM25) and Semantic (Vector) search across matter documents with metadata filtering.
7. **Citation-Aware RAG Assistant**: Q&A assistant providing answers strictly backed by inline, clickable source document citations.
8. **Basic Document Analysis & Key Clause Extraction**: Automated entity extraction (Parties, Dates, Considerations, Property Descriptions, Clauses).
9. **Property Evidence Extraction**: Extraction of Survey Numbers, Khata Numbers, Boundaries, Extent/Area, Encumbrances, and Title Ownership chain.
10. **Property Timeline Construction**: Automatic chronological sequence generation of title conveyances, mortgages, court orders, and registrations.
11. **Contradiction & Missing-Evidence Detection**: Cross-document consistency checking (name mismatches, extent discrepancies, missing link deeds, encumbrance gaps).
12. **Human Review & Verification Workflow**: UI for human experts to review, edit, approve, or reject AI-generated findings with verification badges.
13. **Comprehensive Audit Logs**: Immutably logged actions tracking document uploads, views, queries, AI prompts, human edits, and exports.

## MVP Non-Goals (Explicitly Out of Scope)
- **Autonomous Legal Decisions**: The system will never issue final legal opinions without human approval.
- **Autonomous Court Filing**: No direct automated submission to e-Courts or government portals.
- **Nationwide Undocumented Web Scraping**: No scraping of protected government sites or bypass of CAPTCHA/paywalls.
- **Uncontrolled Autonomous Swarms**: No looping multi-agent systems without step-level guardrails.
- **Complex Enterprise Billing Engines**: Simple flat or usage-based tiering for MVP phase.
- **Kubernetes / Over-engineered Infrastructure**: Simple Docker Compose / Single-server / Serverless deployment model for initial traction.
- **Mobile-First App**: Desktop-first web application tailored for intensive document review.
