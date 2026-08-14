# Chapter 3 — Information Architecture & Site Map

## System Information Hierarchy

```
Organization Workspace
 ├── Matters List [MAT-01]
 │    └── Active Matter Workspace [MAT-02]
 │         ├── Overview Dashboard (Status, Quick Stats, Activity Feed)
 │         ├── Documents [DOC-01] (File List, Upload [DOC-02], Viewer [DOC-03], Processing [DOC-04])
 │         ├── Evidence & Search [EVD-01] (Hybrid Search, Snippet Detail [EVD-02])
 │         ├── Property Intelligence [PROP-01] (Summary, Title Timeline, Contradictions, Encumbrances)
 │         ├── Legal Research & Copilot [AI-01] (Citation Q&A, Research History [RES-01])
 │         ├── Reports [REP-01] (TSR Preview, Custom Comments, DOCX/PDF Export)
 │         └── Audit Trail [AUD-01] (Immutable Matter Event Logs)
 │
 ├── Team Management [SET-01] (User Invites, RBAC Roles, Member List)
 ├── Organization Settings [SET-01] (Firm Metadata, Jurisdiction, Default Preferences)
 └── Usage & Billing [SET-01] (Matter Processing Credits, Resource Metrics)
```

---

## Detailed Section Purpose & Rationale

### 1. Organization Level
- **Matters List**: High-level table of all ongoing legal and property matters. Exists to give Advocates a fast overview of active case deadlines and status.
- **Team Management**: User invitation and role management (`ADMIN`, `LEAD_ADVOCATE`, `ASSOCIATE`, `AUDITOR`). Exists to enforce multi-user security and privilege boundaries.
- **Settings & Usage**: Account settings, firm letterhead customization, and usage credit tracking.

### 2. Matter Level (Core Professional Workspace)
- **Overview**: High-level matter summary, team members, recent document uploads, processing status.
- **Documents**: Document upload dropzone, file list, OCR status indicators, split-screen PDF viewer with bounding-box highlight canvas.
- **Evidence & Search**: Dedicated hybrid vector/keyword search interface returning page-level snippets.
- **Property Intelligence**: Core due diligence dashboard displaying property schedule, ownership chain timeline, boundary matrix, encumbrance verification, and red-flag contradiction alerts.
- **Legal Research & Copilot**: Evidence-grounded RAG assistant for natural language document Q&A with inline clickable citations.
- **Reports**: Report configuration, preview, and DOCX/PDF export engine.
- **Audit Trail**: Transparent, immutable log of all matter actions.
