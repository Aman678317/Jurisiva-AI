# Chapter 3 — Complete User Journeys Architecture

## Journey Format Standard
Every journey is structured as:
`TRIGGER` -> `USER ACTION` -> `SYSTEM RESPONSE` -> `AI ACTION` -> `EVIDENCE` -> `HUMAN REVIEW` -> `OUTPUT` -> `AUDIT EVENT`

---

## Journey 1: Sign Up
- **TRIGGER**: Advocate lands on marketing page and wants to start using the platform.
- **USER ACTION**: Fills out email, password, advocate registration number, and firm name on `AUTH-02`.
- **SYSTEM RESPONSE**: Validates form input, creates User record, sends verification email, displays "Check Your Inbox".
- **AI ACTION**: None.
- **EVIDENCE**: None.
- **HUMAN REVIEW**: User clicks email verification link.
- **OUTPUT**: Authenticated user session created; redirects to `ORG-01`.
- **AUDIT EVENT**: `user.signup` logged with email, IP, and timestamp.

---

## Journey 2: Organization Setup
- **TRIGGER**: First-time login after email verification.
- **USER ACTION**: Enters Law Firm / Chambers Name, State Jurisdiction, Bar Council ID, and selects default language preferences on `ORG-01`.
- **SYSTEM RESPONSE**: Provisions Organization workspace, assigns user as `ORG_ADMIN`, redirects to `MAT-01`.
- **AI ACTION**: None.
- **EVIDENCE**: None.
- **HUMAN REVIEW**: Admin approves org setup details.
- **OUTPUT**: Active organization workspace ready for matter creation.
- **AUDIT EVENT**: `organization.created` logged with org ID and admin user ID.

---

## Journey 3: Create Matter
- **TRIGGER**: Client or bank assigns a new property title due diligence case.
- **USER ACTION**: Clicks "New Matter" on `MAT-01`, enters Matter Title, Client Name, Property Survey #, State/District, and assigns team members on `MAT-02`.
- **SYSTEM RESPONSE**: Validates inputs, creates Matter record with unique UUID, initializes matter file storage directory and vector namespace, redirects to Matter Workspace.
- **AI ACTION**: Initializes default property extraction schema.
- **EVIDENCE**: None.
- **HUMAN REVIEW**: Lead Advocate confirms matter metadata.
- **OUTPUT**: Empty Matter Workspace ready for document upload.
- **AUDIT EVENT**: `matter.created` logged with matter ID, title, created_by.

---

## Journey 4: Invite User
- **TRIGGER**: Lead Advocate wants a junior associate to assist on a matter.
- **USER ACTION**: Navigates to `SET-01` / Team tab, enters associate's email, selects Role (`ASSOCIATE`), clicks "Send Invitation".
- **SYSTEM RESPONSE**: Generates secure token invitation link, sends email notification, displays pending invite badge in team table.
- **AI ACTION**: None.
- **EVIDENCE**: None.
- **HUMAN REVIEW**: Invited associate accepts link and sets up profile.
- **OUTPUT**: Associate granted access to matter workspace under RBAC rules.
- **AUDIT EVENT**: `user.invited` logged with inviter ID, invitee email, role.

---

## Journey 5: Upload Document Bundle
- **TRIGGER**: Advocate receives PDF deeds and land extracts from client.
- **USER ACTION**: Opens Matter Workspace (`DOC-02`), drops 10 PDF files (Sale Deed, Pahani, EC, etc.) into upload dropzone.
- **SYSTEM RESPONSE**: Calculates client-side SHA-256 hashes, checks file format validity, displays real-time progress bars for each file upload.
- **AI ACTION**: Triggers asynchronous background ingestion worker.
- **EVIDENCE**: File integrity validated via hash match.
- **HUMAN REVIEW**: User verifies uploaded file list.
- **OUTPUT**: Immutable document records saved in storage with status `QUEUED`.
- **AUDIT EVENT**: `document.uploaded` logged for each file with doc ID, filename, hash, size.

---

## Journey 6 & 7: Document Processing & OCR
- **TRIGGER**: Ingestion worker picks up `QUEUED` documents.
- **USER ACTION**: Observes processing status progress bar on `DOC-04`.
- **SYSTEM RESPONSE**: Converts PDF pages to images, runs layout engine, extracts text layer via Indic Tesseract/PaddleOCR, generates page bounding-box JSON, creates text chunks, and computes vector embeddings.
- **AI ACTION**: Layout segmentation -> Indic OCR -> Entity extraction model -> Vector embedding generation.
- **EVIDENCE**: Scanned pages associated with page-level OCR text and bounding-box coordinates.
- **HUMAN REVIEW**: Advocate can inspect raw OCR layer on `DOC-03` to verify text extraction accuracy.
- **OUTPUT**: Document status updated to `PROCESSED`; matter vector index updated.
- **AUDIT EVENT**: `document.processed` logged with page count, OCR confidence score, duration.

---

## Journey 8: Search
- **TRIGGER**: Advocate needs to find all mentions of "Survey No. 42/1" across matter documents.
- **USER ACTION**: Types query into global search bar on `EVD-01`.
- **SYSTEM RESPONSE**: Executes hybrid BM25 + pgvector query across matter chunks, returns ranked snippet list with document names, page numbers, and similarity scores.
- **AI ACTION**: Generates query vector embedding; executes vector distance calculation.
- **EVIDENCE**: Each search result displays snippet text linked to exact page offset.
- **HUMAN REVIEW**: Advocate clicks result to view in document viewer.
- **OUTPUT**: Ranked search result list rendered in UI.
- **AUDIT EVENT**: `search.executed` logged with query string, result count, duration.

---

## Journey 9: Evidence Inspection
- **TRIGGER**: Advocate clicks a search result or extracted entity.
- **USER ACTION**: Clicks "View Source" button on `EVD-02`.
- **SYSTEM RESPONSE**: Opens Split-Screen Document Viewer (`DOC-03`), loads PDF page on left, highlights exact text bounding-box in yellow, displays OCR text on right.
- **AI ACTION**: None.
- **EVIDENCE**: Highlighted original PDF snippet proves exact location of claim.
- **HUMAN REVIEW**: Advocate visually confirms source text matches legal claim.
- **OUTPUT**: Verified evidence panel view.
- **AUDIT EVENT**: `evidence.inspected` logged with doc ID, page, snippet ID.

---

## Journey 10: Property Intelligence
- **TRIGGER**: Ingestion completes for a property title bundle.
- **USER ACTION**: Clicks "Property Intelligence" tab on `PROP-01`.
- **SYSTEM RESPONSE**: Renders Property Summary Matrix (Survey #, Extent, Executants, Claimants, Boundaries, Encumbrance list, Chronological Title Timeline).
- **AI ACTION**: Runs Property Extraction Pipeline across all matter chunks; constructs chronological title chain; flags missing link deeds.
- **EVIDENCE**: Every cell in the matrix contains a clickable citation badge `[Doc X, Page Y]`.
- **HUMAN REVIEW**: Advocate verifies each extracted row, editing values if necessary, and clicks "Verify Row".
- **OUTPUT**: Status changes from `AI EXTRACTION` to `HUMAN VERIFIED`.
- **AUDIT EVENT**: `property.intelligence_viewed` logged with matter ID.

---

## Journey 11 & 12: Copilot Question & Research
- **TRIGGER**: Advocate wants to know if there are any uncancelled mortgages in the bundle.
- **USER ACTION**: Types query into Copilot input on `AI-01`: "List all bank mortgages in the EC and state if discharge deeds exist."
- **SYSTEM RESPONSE**: Renders streaming assistant response with real-time status indicators ("Searching documents...", "Comparing evidence...").
- **AI ACTION**: Retrieves relevant EC and deed chunks -> Constructs RAG prompt -> Generates response strictly citing source passages.
- **EVIDENCE**: Response includes inline clickable badges `[Doc 3 (EC), Page 4, Para 2]`.
- **HUMAN REVIEW**: Advocate clicks citation badges to inspect source pages.
- **OUTPUT**: Grounded AI response with verified source citations.
- **AUDIT EVENT**: `copilot.queried` logged with query ID, prompt tokens, response tokens.

---

## Journey 13: Citation Inspection
- **TRIGGER**: Advocate reads AI response and wants to verify citation `[Doc 1, Page 3]`.
- **USER ACTION**: Clicks citation badge `[Doc 1, Page 3]`.
- **SYSTEM RESPONSE**: Opens Citation Popover or side drawer, loads PDF preview, centers page 3, highlights target sentence.
- **AI ACTION**: None.
- **EVIDENCE**: Visual yellow highlight over target sentence in scanned PDF.
- **HUMAN REVIEW**: Advocate confirms AI correctly summarized the cited sentence.
- **OUTPUT**: Citation trust verified.
- **AUDIT EVENT**: `citation.inspected` logged with citation ID, doc ID, page.

---

## Journey 14: Conflict & Contradiction Detection
- **TRIGGER**: System completes entity extraction across multiple matter documents.
- **USER ACTION**: Clicks "Contradictions" tab on `PROP-01`.
- **SYSTEM RESPONSE**: Displays Red-Flag Conflict Banner listing extent discrepancies (e.g. `1985 Deed: 2,400 sq.ft` vs `2012 Deed: 2,100 sq.ft`).
- **AI ACTION**: Cross-compares extracted entity attributes across document timeline; flags statistical/textual mismatches.
- **EVIDENCE**: Displays side-by-side comparison card with citations to both conflicting source documents.
- **HUMAN REVIEW**: Advocate marks discrepancy as "Material Legal Defect" or "Clerical Error".
- **OUTPUT**: Updated contradiction resolution status in matter workspace.
- **AUDIT EVENT**: `conflict.detected` and `conflict.reviewed` logged.

---

## Journey 15: Human Review & Verification Workflow
- **TRIGGER**: Advocate prepares matter for report generation.
- **USER ACTION**: Opens Review Panel on `PROP-01`, reviews unverified extractions, edits incorrect fields, clicks "Approve All Verified".
- **SYSTEM RESPONSE**: Updates entity status badges from `AI EXTRACTION` to `HUMAN VERIFIED`, records advocate's user ID and timestamp.
- **AI ACTION**: None.
- **EVIDENCE**: Verified entries locked for report compilation.
- **HUMAN REVIEW**: Human Advocate takes full legal ownership of final verified values.
- **OUTPUT**: All matter entities marked `HUMAN VERIFIED`.
- **AUDIT EVENT**: `finding.verified` logged with user ID, finding ID, action (`ACCEPTED`/`EDITED`).

---

## Journey 16 & 17: Report Generation & Export
- **TRIGGER**: All matter entities verified; Advocate needs to issue Title Search Report to client bank.
- **USER ACTION**: Navigates to `REP-01`, selects "Bank Standard TSR Template", clicks "Generate Report", then clicks "Export DOCX".
- **SYSTEM RESPONSE**: Compiles verified title flow, property schedule, encumbrance notes, and lawyer comments into a pristine MS Word document (.docx); initiates browser download.
- **AI ACTION**: Assembles report sections; formats Markdown tables.
- **EVIDENCE**: Report includes source citation footnotes mapping back to uploaded document bundle.
- **HUMAN REVIEW**: Advocate opens downloaded DOCX in MS Word for final signature.
- **OUTPUT**: Downloaded `.docx` Title Search Report file.
- **AUDIT EVENT**: `report.generated` and `report.exported` logged with matter ID, template type, format.

---

## Journey 18: Audit History Inspection
- **TRIGGER**: Compliance auditor or lead partner wants to verify who uploaded files and modified extractions.
- **USER ACTION**: Navigates to `AUD-01` tab in Matter Workspace.
- **SYSTEM RESPONSE**: Displays chronological, filterable DataTable listing all system events (Uploads, Searches, AI queries, Human edits, Exports) with User Name, Action Type, Resource, Timestamp, and IP Address.
- **AI ACTION**: None.
- **EVIDENCE**: Immutable DB log records.
- **HUMAN REVIEW**: Auditor inspects event trail.
- **OUTPUT**: Filtered audit log table; exportable CSV audit report.
- **AUDIT EVENT**: `audit_log.viewed` logged.
