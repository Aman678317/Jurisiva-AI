# Chapter 3 — UX Acceptance Test Suite

## Test Protocol Specification

| Test ID | Test Scenario | Precondition | Action Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **UX-TEST-001** | New User Product Orientation | User lands on `/matters` for first time. | Observes onboarding card and clicks "Create First Matter". | Clear visual path to matter creation; zero confusion. | **PASS** |
| **UX-TEST-002** | Create Matter Workflow | Authenticated user on `/matters`. | Clicks New Matter, enters Title, Client, Survey #, submits form. | Matter workspace created; redirects to `MAT-02`. | **PASS** |
| **UX-TEST-003** | Document Upload & Drag-Drop | Matter Workspace open. | Drops 5 PDF files into upload zone (`DOC-02`). | Progress bars render; files uploaded; status `QUEUED`. | **PASS** |
| **UX-TEST-004** | Processing Progress Perception | Documents queued. | Observes processing status (`DOC-04`). | Clear status bar ("Processing Page 4 of 12"); user understands state. | **PASS** |
| **UX-TEST-005** | Hybrid Search Evidence Discovery| Matter documents processed. | Types "Survey No 42/1" into `EVD-01`. | Returns ranked snippet list with document name and page #. | **PASS** |
| **UX-TEST-006** | Citation Inspection in Split Viewer | AI response rendered. | Clicks inline citation badge `[Doc 2, Page 4]`. | Opens `DOC-03` Split Viewer; page 4 centered with yellow highlight overlay. | **PASS** |
| **UX-TEST-007** | AI Uncertainty Transparency | Low confidence extraction. | Observes AI response card on `AI-01`. | Low confidence amber badge displayed with explanation message. | **PASS** |
| **UX-TEST-008** | Human Verification & Editing | Unverified entity present. | Advocate clicks `[Verify]` or edits value on `PROP-01`. | Badge state updates to `HUMAN VERIFIED`; timestamp logged. | **PASS** |
| **UX-TEST-009** | Property Schedule & Timeline View| Property deeds ingested. | Opens `PROP-01` tab. | Extracted property schedule table and title timeline rendered cleanly. | **PASS** |
| **UX-TEST-010** | Legal Research Execution | Matter Workspace open. | Enters query in `RES-01` ("Find un-discharged mortgages"). | Research synthesis cards displayed with source citations. | **PASS** |
| **UX-TEST-011** | Report Generation & DOCX Export | All matter entities verified. | Clicks Generate TSR on `REP-01`, selects DOCX export. | Editable `.docx` Title Search Report downloads to browser. | **PASS** |
| **UX-TEST-012** | Audit History Comprehension | Actions executed in matter. | Opens `AUD-01` tab. | Chronological audit table renders all user actions with IP/timestamps. | **PASS** |
| **UX-TEST-013** | Permission Failure Handling | User logged in as Auditor. | Attempts to delete a document or edit matter settings. | Action button disabled; tooltip explains "Requires Lead Advocate role." | **PASS** |
| **UX-TEST-014** | Error Recovery Path | Simulated OCR pipeline error. | Observes error state banner on `DOC-04`. | Error message clearly explains cause; `[Retry Processing]` recovers state. | **PASS** |
| **UX-TEST-015** | Full Keyboard Navigation | Workspace open. | Navigates workspace using `Tab`, `Enter`, `Cmd+K`, `PageUp/Down`. | All interactive controls accessible without mouse input. | **PASS** |
| **UX-TEST-016** | Intentional Mobile Adaptation | Access workspace on mobile device. | Opens `DOC-03` split viewer on mobile resolution (< 768px). | UI displays clean single-column view with clear desktop warning banner. | **PASS** |
