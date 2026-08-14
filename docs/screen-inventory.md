# Chapter 3 — Complete Screen Inventory (20 MVP Screens)

## Screen Specifications Matrix

### 1. AUTH-01: User Login
- **PURPOSE**: Authenticate registered Advocates and staff into the platform.
- **USER**: All users.
- **ENTRY POINT**: Root URL `/login`.
- **DATA REQUIRED**: Email, Password fields.
- **ACTIONS**: Submit login, Password reset link, Redirect to signup.
- **AI FEATURES**: None.
- **PERMISSIONS**: Public.
- **LOADING STATE**: Spinner on Submit button (`Authenticating...`).
- **EMPTY STATE**: N/A.
- **ERROR STATE**: "Invalid email or password. [Try Again]".
- **SUCCESS STATE**: JWT stored; redirect to `/matters`.
- **AUDIT EVENTS**: `user.login_attempted` (Success/Fail).
- **ANALYTICS EVENTS**: `page_view_login`.

---

### 2. AUTH-02: User Signup
- **PURPOSE**: Register new advocate or firm account.
- **USER**: New users.
- **ENTRY POINT**: `/signup`.
- **DATA REQUIRED**: Full Name, Email, Password, Bar ID, Firm Name.
- **ACTIONS**: Submit registration, Link to login.
- **AI FEATURES**: None.
- **PERMISSIONS**: Public.
- **LOADING STATE**: Button spinner (`Creating Account...`).
- **EMPTY STATE**: N/A.
- **ERROR STATE**: "Email already registered." / "Weak password."
- **SUCCESS STATE**: Verification email sent notice.
- **AUDIT EVENTS**: `user.signup`.
- **ANALYTICS EVENTS**: `signup_started`, `signup_completed`.

---

### 3. ORG-01: Organization Setup
- **PURPOSE**: Configure law firm / chambers workspace defaults.
- **USER**: Firm Admin.
- **ENTRY POINT**: Post-signup redirect `/onboarding/org`.
- **DATA REQUIRED**: Org Name, State Jurisdiction, Default Language, Billing Address.
- **ACTIONS**: Save Org Profile, Continue to Matters.
- **AI FEATURES**: None.
- **PERMISSIONS**: `ORG_ADMIN`.
- **LOADING STATE**: Skeleton form loader.
- **EMPTY STATE**: Pre-filled with user signup data.
- **ERROR STATE**: "Organization name required."
- **SUCCESS STATE**: Org created; redirect to `/matters`.
- **AUDIT EVENTS**: `organization.created`.
- **ANALYTICS EVENTS**: `org_setup_completed`.

---

### 4. MAT-01: Matter List
- **PURPOSE**: Dashboard table of all active legal/property matters.
- **USER**: All authenticated users.
- **ENTRY POINT**: `/matters`.
- **DATA REQUIRED**: List of matters (Title, Client, Status, Doc Count, Last Updated).
- **ACTIONS**: Create Matter button, Filter by status, Search matter title, Click matter row.
- **AI FEATURES**: None.
- **PERMISSIONS**: Authenticated users.
- **LOADING STATE**: Table row skeleton loader.
- **EMPTY STATE**: "No matters found. [Create Your First Matter]".
- **ERROR STATE**: "Failed to load matters. [Retry]".
- **SUCCESS STATE**: Rendered DataTable of matters.
- **AUDIT EVENTS**: `matter.list_viewed`.
- **ANALYTICS EVENTS**: `matter_list_opened`.

---

### 5. MAT-02: Matter Workspace Dashboard
- **PURPOSE**: Central hub for a specific legal/property matter.
- **USER**: Matter team members.
- **ENTRY POINT**: `/matters/{matter_id}`.
- **DATA REQUIRED**: Matter details, Document count, Quick Stats, Processing progress, Recent activity feed.
- **ACTIONS**: Tab navigation, Quick Upload button, Generate Report button.
- **AI FEATURES**: Matter intelligence summary card.
- **PERMISSIONS**: Matter members (`LEAD_ADVOCATE`, `ASSOCIATE`, `AUDITOR`).
- **LOADING STATE**: Workspace header skeleton.
- **EMPTY STATE**: "Matter workspace empty. Upload document bundle to begin."
- **ERROR STATE**: "Matter not found or access denied."
- **SUCCESS STATE**: Active matter header + quick stats cards.
- **AUDIT EVENTS**: `matter.opened`.
- **ANALYTICS EVENTS**: `matter_workspace_viewed`.

---

### 6. MAT-03: Matter Settings
- **PURPOSE**: Configure matter metadata, assign team members, manage permissions.
- **USER**: Lead Advocate.
- **ENTRY POINT**: `/matters/{matter_id}/settings`.
- **DATA REQUIRED**: Matter Metadata, Assigned Users list, Role matrix, Archive option.
- **ACTIONS**: Edit title/client, Add/Remove user, Change roles, Archive matter.
- **AI FEATURES**: None.
- **PERMISSIONS**: `LEAD_ADVOCATE` only.
- **LOADING STATE**: Form skeleton.
- **EMPTY STATE**: N/A.
- **ERROR STATE**: "Failed to update settings."
- **SUCCESS STATE**: "Settings saved successfully." Toast.
- **AUDIT EVENTS**: `matter.settings_updated`, `matter.user_assigned`.
- **ANALYTICS EVENTS**: `matter_settings_saved`.

---

### 7. DOC-01: Document List
- **PURPOSE**: Table listing all uploaded PDFs in a matter with OCR status badges.
- **USER**: All matter members.
- **ENTRY POINT**: `/matters/{matter_id}/documents`.
- **DATA REQUIRED**: Document list (Filename, Size, Upload Date, Hash, OCR Status, Page Count).
- **ACTIONS**: Upload Documents button, View PDF, Delete Document, Filter by OCR status.
- **AI FEATURES**: Auto document classification badge (Sale Deed, Pahani, EC, etc.).
- **PERMISSIONS**: All matter members.
- **LOADING STATE**: Table row skeletons.
- **EMPTY STATE**: "No documents in this matter. [Upload PDF Bundle]".
- **ERROR STATE**: "Error loading document list."
- **SUCCESS STATE**: DataTable rendering files with status badges (`PROCESSED`, `PROCESSING`, `FAILED`).
- **AUDIT EVENTS**: `document.list_viewed`.
- **ANALYTICS EVENTS**: `doc_list_opened`.

---

### 8. DOC-02: Document Upload Modal/Page
- **PURPOSE**: Drag-and-drop file uploader for adding document bundles.
- **USER**: Lead Advocate, Associate.
- **ENTRY POINT**: Modal trigger from `DOC-01` or `/matters/{id}/upload`.
- **DATA REQUIRED**: Target Matter ID.
- **ACTIONS**: Drag/Drop files, Select files, Cancel, Start Upload.
- **AI FEATURES**: Pre-upload document type auto-detection.
- **PERMISSIONS**: `LEAD_ADVOCATE`, `ASSOCIATE`.
- **LOADING STATE**: Per-file progress bars with speed (MB/s).
- **EMPTY STATE**: Dropzone illustration + file picker button.
- **ERROR STATE**: "File exceeds 100MB limit." / "Unsupported file format."
- **SUCCESS STATE**: All files uploaded banner + "Start OCR Ingestion" button.
- **AUDIT EVENTS**: `document.upload_batch_started`.
- **ANALYTICS EVENTS**: `upload_flow_completed`.

---

### 9. DOC-03: Split-Screen Document Viewer
- **PURPOSE**: Side-by-side view of original PDF page on left and OCR text + citations on right.
- **USER**: All matter members.
- **ENTRY POINT**: Click document row or citation link `/matters/{id}/documents/{doc_id}`.
- **DATA REQUIRED**: PDF file stream, Page image canvas, OCR text layer, Bounding box JSON.
- **ACTIONS**: Zoom In/Out, Page Jump, Select Text, Highlight Bounding Box, Toggle OCR View, Copy Text.
- **AI FEATURES**: Real-time bounding box highlighting from citations.
- **PERMISSIONS**: All matter members.
- **LOADING STATE**: PDF page loader skeleton + canvas spinner.
- **EMPTY STATE**: "Select a document page to view."
- **ERROR STATE**: "Failed to render PDF page."
- **SUCCESS STATE**: Dual-pane rendering with yellow highlight overlay over target text.
- **AUDIT EVENTS**: `document.viewed` (doc_id, page_num).
- **ANALYTICS EVENTS**: `doc_viewer_opened`.

---

### 10. DOC-04: Processing Status Dashboard
- **PURPOSE**: Real-time monitoring of OCR, indexing, and entity extraction jobs.
- **USER**: All matter members.
- **ENTRY POINT**: `/matters/{id}/processing`.
- **DATA REQUIRED**: Queue list, File processing progress %, Pipeline step (OCR -> Indexing -> Entities).
- **ACTIONS**: Cancel Job, Retry Failed OCR, View Processing Log.
- **AI FEATURES**: Asynchronous background pipeline status updates via WebSockets.
- **PERMISSIONS**: `LEAD_ADVOCATE`, `ASSOCIATE`.
- **LOADING STATE**: Animated progress bar per file.
- **EMPTY STATE**: "No background jobs running."
- **ERROR STATE**: "OCR Pipeline Error on Page 12. [Retry Processing]".
- **SUCCESS STATE**: 100% Complete banner -> Redirect to `PROP-01`.
- **AUDIT EVENTS**: `processing.job_status_checked`.
- **ANALYTICS EVENTS**: `processing_viewed`.

---

### 11. EVD-01: Evidence & Hybrid Search
- **PURPOSE**: Search across matter documents combining semantic vector distance and BM25 keywords.
- **USER**: All matter members.
- **ENTRY POINT**: `/matters/{id}/search`.
- **DATA REQUIRED**: Matter Search Index.
- **ACTIONS**: Search input, Filter by document type, Filter by date range, Click snippet.
- **AI FEATURES**: Hybrid vector similarity search (pgvector).
- **PERMISSIONS**: All matter members.
- **LOADING STATE**: Search snippet skeleton loader.
- **EMPTY STATE**: "Enter a query (e.g., 'Survey No 42/1' or 'mortgage amount') to search."
- **ERROR STATE**: "Search query failed. Check connection."
- **SUCCESS STATE**: Ranked snippet list displaying file name, page #, and highlighted match text.
- **AUDIT EVENTS**: `search.executed`.
- **ANALYTICS EVENTS**: `evidence_search_performed`.

---

### 12. EVD-02: Evidence Detail Panel
- **PURPOSE**: Deep inspection of a specific evidence snippet and metadata provenance.
- **USER**: All matter members.
- **ENTRY POINT**: Click search snippet or citation badge.
- **DATA REQUIRED**: Snippet text, Page #, File name, SHA-256 Hash, Vector distance score.
- **ACTIONS**: Open in Split Viewer (`DOC-03`), Copy Snippet, Add to Report Notes.
- **AI FEATURES**: Snippet contextual relevance classification.
- **PERMISSIONS**: All matter members.
- **LOADING STATE**: Snippet detail loader.
- **EMPTY STATE**: N/A.
- **ERROR STATE**: "Evidence metadata unavailable."
- **SUCCESS STATE**: Rendered metadata card with visual link to source PDF.
- **AUDIT EVENTS**: `evidence.detail_inspected`.
- **ANALYTICS EVENTS**: `evidence_detail_viewed`.

---

### 13. AI-01: Citation-Aware Copilot Workspace
- **PURPOSE**: Natural language Q&A assistant grounded strictly in matter documents.
- **USER**: All matter members.
- **ENTRY POINT**: `/matters/{id}/copilot`.
- **DATA REQUIRED**: Conversation history, Matter context, Document chunks.
- **ACTIONS**: Type Prompt, Select Preset Prompts ("Summarize Title", "Find Mortgages"), Click Citation Badge, Copy Response.
- **AI FEATURES**: RAG streaming response, inline citation insertion `[Doc, Page]`.
- **PERMISSIONS**: All matter members.
- **LOADING STATE**: Streaming text indicator + status messages ("Searching documents...").
- **EMPTY STATE**: Preset question cards ("What are the survey numbers?", "Build title timeline").
- **ERROR STATE**: "Insufficient evidence in uploaded documents to answer query."
- **SUCCESS STATE**: Formatted Markdown answer with interactive citation badges.
- **AUDIT EVENTS**: `copilot.query_submitted`, `copilot.response_received`.
- **ANALYTICS EVENTS**: `copilot_used`.

---

### 14. AI-02: AI Run Detail & Prompt Inspection
- **PURPOSE**: Inspect retrieved RAG chunks, raw LLM prompt, and generation parameters for transparency.
- **USER**: Lead Advocate, Auditor.
- **ENTRY POINT**: Click "Inspect AI Run" on Copilot message.
- **DATA REQUIRED**: System prompt text, Retrieved Context chunks, Model ID, Token usage, Execution time.
- **ACTIONS**: Toggle view raw prompt, Copy debug JSON.
- **AI FEATURES**: RAG context inspectability.
- **PERMISSIONS**: `LEAD_ADVOCATE`, `AUDITOR`.
- **LOADING STATE**: Json loader.
- **EMPTY STATE**: N/A.
- **ERROR STATE**: "Run details expired or unavailable."
- **SUCCESS STATE**: JSON tree viewer rendering prompt and retrieval chunks.
- **AUDIT EVENTS**: `copilot.debug_inspected`.
- **ANALYTICS EVENTS**: `ai_run_inspected`.

---

### 15. RES-01: Legal & Property Research Workspace
- **PURPOSE**: Conduct structured multi-document research queries across matter files.
- **USER**: All matter members.
- **ENTRY POINT**: `/matters/{id}/research`.
- **DATA REQUIRED**: Research query history, Matter document index.
- **ACTIONS**: New Research Query, Filter by Document Category, Save Research Findings.
- **AI FEATURES**: Structured research synthesis with multi-document aggregation.
- **PERMISSIONS**: All matter members.
- **LOADING STATE**: Research matrix skeleton.
- **EMPTY STATE**: "Start a research topic (e.g. 'Historical Encumbrances')."
- **ERROR STATE**: "Research query failed."
- **SUCCESS STATE**: Research summary cards grouped by document source.
- **AUDIT EVENTS**: `research.query_started`.
- **ANALYTICS EVENTS**: `research_started`.

---

### 16. RES-02: Research Results & Synthesis Panel
- **PURPOSE**: Display multi-document research matrix with side-by-side evidence columns.
- **USER**: All matter members.
- **ENTRY POINT**: Select research query from `RES-01`.
- **DATA REQUIRED**: Extracted facts grouped by document and date.
- **ACTIONS**: Export Research Notes, Add Fact to Report, Verify Fact.
- **AI FEATURES**: Automated factual contradiction highlighting across research sources.
- **PERMISSIONS**: All matter members.
- **LOADING STATE**: Matrix skeleton.
- **EMPTY STATE**: "No research results found for this query."
- **ERROR STATE**: "Unable to synthesize research findings."
- **SUCCESS STATE**: Multi-column comparison matrix with clickable citations.
- **AUDIT EVENTS**: `research.results_viewed`.
- **ANALYTICS EVENTS**: `research_results_viewed`.

---

### 17. PROP-01: Property Intelligence Dashboard
- **PURPOSE**: Primary due diligence hub displaying Property Schedule, Title Flow Timeline, Extent Matrix, and Red-Flag Contradictions.
- **USER**: Property Advocates, Title Search Specialists.
- **ENTRY POINT**: `/matters/{id}/property`.
- **DATA REQUIRED**: Extracted Property Entities, Chronological Title Flow, Contradictions list, Encumbrances.
- **ACTIONS**: Verify Entity Row, Edit Entity Value, Resolve Contradiction, View Link Gap, Export TSR.
- **AI FEATURES**: Chronological timeline ordering, Extent discrepancy detection, Verification badges.
- **PERMISSIONS**: All matter members (Edits restricted to Advocates/Associates).
- **LOADING STATE**: Timeline and matrix skeleton.
- **EMPTY STATE**: "Upload deeds to extract property intelligence."
- **ERROR STATE**: "Failed to load property schema."
- **SUCCESS STATE**: Fully populated Title Timeline + Contradiction Alerts + Verification Table.
- **AUDIT EVENTS**: `property.dashboard_opened`, `finding.verified`.
- **ANALYTICS EVENTS**: `property_intel_viewed`.

---

### 18. REP-01: Report Generation & Preview
- **PURPOSE**: Configure, preview, and export the draft Title Search Report (TSR).
- **USER**: Lead Advocate.
- **ENTRY POINT**: `/matters/{id}/report`.
- **DATA REQUIRED**: Verified Property Entities, Verified Title Flow, Encumbrance Notes, Advocate Comments, Org Letterhead.
- **ACTIONS**: Select Report Template, Add Custom Opinion Notes, Toggle Sections, Export DOCX, Export PDF.
- **AI FEATURES**: Automated report section drafting based on verified findings.
- **PERMISSIONS**: `LEAD_ADVOCATE` (Export blocked for unverified data unless confirmed).
- **LOADING STATE**: Live document preview skeleton.
- **EMPTY STATE**: "Verify at least one document entity to generate report preview."
- **ERROR STATE**: "Report export failed. Retry."
- **SUCCESS STATE**: Interactive formatted report preview with instant "Download DOCX" action.
- **AUDIT EVENTS**: `report.generated`, `report.exported`.
- **ANALYTICS EVENTS**: `report_downloaded`.

---

### 19. AUD-01: Audit Trail Viewer
- **PURPOSE**: Display immutable log of all actions taken in the matter for security and legal compliance.
- **USER**: Lead Advocate, Auditor.
- **ENTRY POINT**: `/matters/{id}/audit`.
- **DATA REQUIRED**: Audit Log Records (Timestamp, User, Action, Resource, IP).
- **ACTIONS**: Filter by User, Filter by Action Type, Date Range Filter, Export Audit Log CSV.
- **AI FEATURES**: None.
- **PERMISSIONS**: `LEAD_ADVOCATE`, `AUDITOR`.
- **LOADING STATE**: Log table skeleton loader.
- **EMPTY STATE**: "No audit events recorded."
- **ERROR STATE**: "Failed to load audit logs."
- **SUCCESS STATE**: Paginated DataTable of immutable system events.
- **AUDIT EVENTS**: `audit_log.accessed`.
- **ANALYTICS EVENTS**: `audit_trail_opened`.

---

### 20. SET-01: Organization & User Settings
- **PURPOSE**: Manage user profile, law firm metadata, team invitations, and API keys.
- **USER**: Org Admin, All Users (Profile only).
- **ENTRY POINT**: `/settings`.
- **DATA REQUIRED**: Profile settings, Team members list, Role matrix, Security settings.
- **ACTIONS**: Update Name/Password, Invite User, Revoke Role, Update Firm Metadata.
- **AI FEATURES**: None.
- **PERMISSIONS**: All users (Admin sections restricted).
- **LOADING STATE**: Settings form skeleton.
- **EMPTY STATE**: N/A.
- **ERROR STATE**: "Failed to update profile."
- **SUCCESS STATE**: "Profile updated successfully."
- **AUDIT EVENTS**: `settings.updated`.
- **ANALYTICS EVENTS**: `settings_viewed`.
