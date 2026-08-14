# Chapter 3 — Implementation-Ready User Stories

## Story 1: Document Upload & Ingestion (US-DOC-001)

- **USER STORY**:
  **AS A** Property Advocate,
  **I WANT TO** upload a batch of scanned PDF deeds and Encumbrance Certificates into a matter,
  **SO THAT** the system can perform OCR and extract structured legal text for analysis.

- **ACCEPTANCE CRITERIA**:
  1. User can drag-and-drop or select up to 30 PDF/TIFF/PNG files simultaneously (max 100MB per file).
  2. Client-side computes SHA-256 hash before upload transmission.
  3. Upload progress bar displays percentage complete and transfer speed per file.
  4. Backend validates MIME type, file integrity, and stores file in immutable object storage.
  5. UI displays file status badge: `QUEUED` -> `PROCESSING` -> `PROCESSED`.

- **EDGE CASES**:
  - Corrupted PDF upload: System detects invalid header, flags status `CORRUPTED`, presents error toast.
  - Duplicate file upload: System matches SHA-256 hash, warns user `Duplicate Document Detected`, offers option to view existing file or re-upload.

- **PERMISSIONS**: `LEAD_ADVOCATE`, `ASSOCIATE` (Read-Only auditors blocked).

- **ERROR STATES**: Network disconnect during upload displays "Upload Interrupted. [Resume Upload]".

- **AUDIT REQUIREMENTS**: Log `document.uploaded` with file_name, hash, size, user_id, matter_id.

- **TESTS**: Unit test SHA-256 calculator; E2E upload flow test; Permission denial test for auditor role.

---

## Story 2: Split-Screen Citation Navigation (US-VIEW-001)

- **USER STORY**:
  **AS A** Title Search Specialist,
  **I WANT TO** click an inline citation badge in an AI response or property matrix,
  **SO THAT** the document viewer opens the exact PDF page with a yellow bounding-box highlight over the source text.

- **ACCEPTANCE CRITERIA**:
  1. Clicking `[Doc 2, Page 4]` smoothly transitions or opens the Split-Screen Document Viewer (`DOC-03`).
  2. PDF viewer loads Document 2, navigates directly to Page 4, and centers the viewport.
  3. Extracted OCR bounding box renders a semi-transparent yellow highlight (`#FEF08A` fill, `#CA8A04` border) over the target text.
  4. Right side of split viewer displays raw OCR text snippet with copy button.

- **EDGE CASES**:
  - Cited page number exceeds document page count: Displays error badge `Invalid Page Citation`, falls back to page 1.
  - Bounding box coordinates missing: Highlights full page text fallback banner.

- **PERMISSIONS**: All authenticated matter users (`LEAD_ADVOCATE`, `ASSOCIATE`, `AUDITOR`).

- **ERROR STATES**: Missing PDF asset displays "Document File Unavailable. [Contact Support]".

- **AUDIT REQUIREMENTS**: Log `citation.inspected` with citation_id, doc_id, page_num, user_id.

- **TESTS**: Component test for viewer navigation props; Integration test verifying bounding box canvas rendering.

---

## Story 3: Property Title Flow Timeline Construction (US-PROP-001)

- **USER STORY**:
  **AS A** Property Advocate,
  **I WANT TO** view an automatically generated chronological timeline of registered property deeds,
  **SO THAT** I can verify that every link deed in the 30-year chain of title is present and unbroken.

- **ACCEPTANCE CRITERIA**:
  1. System extracts registration date, document type, executant, claimant, and property extent from all matter deeds.
  2. Displays chronological vertical timeline graph on `PROP-01`.
  3. Every timeline card displays Date, Doc No, Deed Type, Executant -> Claimant, Extent, and Citation Badge.
  4. System automatically detects year gaps where transfer continuity is broken and inserts a `LINK GAP WARNING` card.

- **EDGE CASES**:
  - Missing execution date: Places document in `Undated Conveyances` drawer with amber warning badge.
  - Multiple deeds registered on same date: Sorts by Sub-Registrar Document Registration Number.

- **PERMISSIONS**: All matter users.

- **ERROR STATES**: Zero deeds uploaded renders empty state: "Upload property deeds to construct title flow timeline."

- **AUDIT REQUIREMENTS**: Log `timeline.viewed` with matter_id.

- **TESTS**: Unit test date sorting & missing link gap detection logic; Component render test for timeline cards.

---

## Story 4: Cross-Document Contradiction Alerting (US-CONT-001)

- **USER STORY**:
  **AS A** Bank Panel Lawyer,
  **I WANT TO** receive automated red-flag alerts when land extent or property boundaries conflict across deeds,
  **SO THAT** I can flag unmarketable title defects in my report before the bank approves the loan.

- **ACCEPTANCE CRITERIA**:
  1. System cross-compares extracted Extent (Acres/Guntas/Sq.Ft) across all historical conveyances in the matter.
  2. Displays Red-Flag Banner on `PROP-01` detailing Extent Discrepancy (e.g., `1985 Sale Deed: 2,400 sq.ft` vs `2012 Partition Deed: 2,100 sq.ft`).
  3. User can click "Inspect Discrepancy" to open side-by-side split cards with direct citations to both deeds.
  4. Advocate can set status to `MATERIAL DEFECT` or `CLERICAL ERROR` with custom notes.

- **EDGE CASES**:
  - Extent specified in regional units (e.g., Guntas vs Sq.Ft): System converts units to normalized Sq.Ft before comparing.

- **PERMISSIONS**: `LEAD_ADVOCATE`, `ASSOCIATE`.

- **ERROR STATES**: Discrepancy comparison timeout displays "Re-calculating contradictions...".

- **AUDIT REQUIREMENTS**: Log `conflict.reviewed` with conflict_id, decision, user_id, timestamp.

- **TESTS**: Unit test extent unit converter; Integration test contradiction alert trigger.

---

## Story 5: Human Verification & Report Export (US-REP-001)

- **USER STORY**:
  **AS A** Lead Advocate,
  **I WANT TO** verify extracted property data and export an editable Title Search Report (.docx),
  **SO THAT** I can deliver a professional legal opinion to my client.

- **ACCEPTANCE CRITERIA**:
  1. User can click "Verify" on extracted entity rows, changing badge state to `HUMAN VERIFIED`.
  2. User clicks "Generate Title Search Report" on `REP-01`.
  3. System populates verified title flow, property schedule, encumbrance findings, and lawyer comments into a clean DOCX file.
  4. DOCX file downloads to user's local browser immediately.

- **EDGE CASES**:
  - User attempts export with unverified `AI EXTRACTION` fields: Displays modal warning "3 fields remain unverified. [Export Anyway] or [Review Fields]".

- **PERMISSIONS**: `LEAD_ADVOCATE` only.

- **ERROR STATES**: DOCX template generation failure displays "Report Generation Error. [Retry Export]".

- **AUDIT REQUIREMENTS**: Log `report.exported` with matter_id, doc_format, unverified_count, user_id.

- **TESTS**: Integration test verifying DOCX file structure; Permission check blocking non-lead users from export.
