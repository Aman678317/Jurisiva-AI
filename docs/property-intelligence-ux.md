# Chapter 3 — Property Intelligence UX Architecture

## Property Intelligence Workflow Pipeline

```
PROPERTY DASHBOARD (PROP-01)
  ↓
1. IDENTIFY PROPERTY
   └── Enter Survey #, Khata #, Village, District, Extent
  ↓
2. COLLECT & UPLOAD DOCUMENTS
   └── Bundle Upload (Sale Deeds, Pahani/RTC, EC, Tax Receipts)
  ↓
3. EXTRACT ENTITIES
   └── Auto-parse Executants, Claimants, Dates, Extent, Boundaries
  ↓
4. BUILD TITLE TIMELINE
   └── Order deeds chronologically; flag missing link deeds
  ↓
5. LINK PEOPLE & ENTITIES
   └── Construct party transfer graph (Seller 1985 -> Buyer 1985 / Seller 2002)
  ↓
6. IDENTIFY CONFLICTS
   └── Run extent & boundary reconciliation rules
  ↓
7. SHOW EVIDENCE
   └── Attach inline citation badges [Doc X, Page Y] to every cell
  ↓
8. HUMAN REVIEW
   └── Advocate verifies or edits rows; status updates to `HUMAN VERIFIED`
  ↓
9. REPORT GENERATION
   └── Export draft Title Search Report (.docx)
```

---

## Detailed UI Layout Strategy (`PROP-01`)

### Tab 1: Property Overview & Schedule Matrix
- **Property Identity Card**: Survey No, Khasra/Khata No, Sy. No. Hissa, Village, Taluk, District.
- **Normalized Extent Card**: Displays total land area in Acres, Guntas, Cents, and Sq.Ft.
- **Boundary Schedule Table**:
  - North: `Govt Road [Doc 1, Page 4]`
  - South: `Property of Ramappa [Doc 1, Page 4]`
  - East: `Survey No 42/2 [Doc 1, Page 4]`
  - West: `Drainage Canal [Doc 1, Page 4]`

### Tab 2: Chronological Title Flow Timeline
- Vertical flow graph showing unbroken ownership transfers over 30 years.
- Each node represents a registered transaction:
  - **Date**: `14-Aug-1985`
  - **Doc No**: `1234/1985`
  - **Type**: `Absolute Sale Deed`
  - **Executant (Seller)**: `Venkatappa S/o Ramaiah`
  - **Claimant (Buyer)**: `Krishnappa S/o Govindappa`
  - **Consideration**: `₹150,000`
  - **Verification**: `[Verify Row]` button + Citation `[Doc 1, Page 1]`.

### Tab 3: Encumbrance & Mortgage Audit
- Table listing EC entries paired with corresponding Discharge Deeds.
- Highlights un-discharged bank mortgages in amber.

### Tab 4: Contradiction & Missing Evidence Alerts
- Red-flag banner listing extent mismatches or missing link deeds with direct `[Inspect Evidence]` links.
