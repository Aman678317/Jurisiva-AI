# Chapter 3 — Human-in-the-Loop (HITL) Workflow & Verification Architecture

## Overview
In consequential legal and property transactions, AI operates strictly as an assistant. Every material extraction, timeline connection, and report conclusion must undergo explicit human review and verification before final legal export.

---

## 1. Mandatory vs. Recommended Human Review Points

| Review Point | Trigger Condition | Review Level | Consequence if Unverified |
| :--- | :--- | :--- | :--- |
| **Land Extent & Boundaries** | Extracted Property Schedule | **MANDATORY** | Export blocked until extent is verified or acknowledged. |
| **Title Ownership Chain** | Extracted Executant/Claimant pairs | **MANDATORY** | Highlighted as unverified in draft Title Search Report. |
| **Contradictions & Red Flags** | Extent mismatch or missing link deed | **MANDATORY** | Requires Advocate classification (`MATERIAL DEFECT` / `CLERICAL ERROR`). |
| **Uncertain OCR Text** | Character confidence < 80% on scan | **RECOMMENDED** | Yellow banner warning on Document Viewer. |
| **Encumbrance Discharge Status**| Unmatched mortgage entry in EC | **RECOMMENDED** | Alert badge displayed in Property Intelligence panel. |
| **Title Report Export** | Final DOCX report generation | **MANDATORY** | Modal prompt detailing unverified fields before export. |

---

## 2. Standardized HITL Decision Flow Pattern

```
  AI OUTPUT GENERATED
          ↓
  [REVIEW REQUIRED BADGE]
          ↓
   ADVOCATE INSPECTION
          ↓
  USER DECISION SELECTION
  ├── [ACCEPT] ─────────► Entity status updated to `HUMAN VERIFIED`
  ├── [EDIT]   ─────────► Advocate modifies value -> Saved as `HUMAN VERIFIED`
  ├── [REJECT] ─────────► Entity status updated to `REJECTED` (Excluded from report)
  └── [REQUEST EVIDENCE] ► System launches targeted search for supporting deed
          ↓
     AUDIT EVENT LOGGED (`finding.verified` / `finding.rejected`)
```

---

## 3. Detailed Review Point Specifications

### A. Property Extent & Schedule Verification
- **AI OUTPUT**: `Extracted Extent: 2 Acres 24 Guntas (104,544 Sq.Ft) [Doc 1, Page 3]`.
- **REVIEW REQUIRED**: Extent value tagged `AI EXTRACTION - UNVERIFIED`.
- **USER DECISION**:
  - `ACCEPT`: Advocate clicks checkmark -> Badge changes to `HUMAN VERIFIED` (Green).
  - `EDIT`: Advocate opens inline edit input, changes value to `2 Acres 20 Guntas`, clicks Save -> Badge changes to `HUMAN VERIFIED (EDITED)`.
  - `REJECT`: Advocate clicks X -> Entity excluded from report.
  - `REQUEST MORE EVIDENCE`: Launches search for Pahani extract to verify extent.
- **AUDIT EVENT**: `finding.verified` logged with user ID, original value, final value, timestamp.

### B. Extent Contradiction Resolution
- **AI OUTPUT**: `CONTRADICTION DETECTED: 1985 Sale Deed (2,400 sq.ft) vs 2012 Partition Deed (2,100 sq.ft)`.
- **REVIEW REQUIRED**: Red-flag banner rendered on `PROP-01`.
- **USER DECISION**: Advocate selects classification:
  - `MATERIAL TITLE DEFECT`: Added to Title Search Report Query Sheet for bank/client resolution.
  - `CLERICAL ERROR`: Marked resolved with advocate note "Typographical error in 2012 deed".
- **AUDIT EVENT**: `conflict.resolved` logged with conflict ID, resolution status, advocate comments.
