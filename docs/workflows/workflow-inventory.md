# Legal & Property Intelligence Workflow Inventory

## 1. Approved Workflow Inventory & Prioritization

| Workflow | Category | Core Purpose | Risk Level | Human Review Trigger | Priority |
| :--- | :--- | :--- | :---: | :--- | :---: |
| **Property Due Diligence** | Property | 13-to-30 year chain of title analysis & title report generation | HIGH | Always required before report export | **P0 (MVP)** |
| **Document Comparison** | Legal | Side-by-side diff analysis between deed revisions or draft agreements | MEDIUM | Material clause changes | **P0 (MVP)** |
| **Property Timeline Builder**| Property | Chronological transaction graph from Sale Deeds, Mortgages, Releases | HIGH | Unlinked years in title chain (> 3 yrs) | **P0 (MVP)** |
| **Entity Resolution** | Property | Matching party names & addresses across 30-year deed history | MEDIUM | Ambiguous name matches ("R. Kumar") | **P0 (MVP)** |
| **Conflict Detector** | Property | Detecting owner, extent, or encumbrance contradictions | HIGH | Discrepancy in extent or active mortgage | **P0 (MVP)** |
| **Title Search Report Export**| Property | Evidence-backed Search Report with page citations & disclaimers | HIGH | Advocate review & signature required | **P0 (MVP)** |
| **Court Research Memo** | Court | Litigation history & court order extraction | MEDIUM | Unverified case numbers | P1 |

---

## 2. Professional Safety & Legal Boundaries
1. **No Autonomous Legal Advice**: Workflows automate evidence organization and draft generation; advocate review controls all final decisions.
2. **Provenance Traceability**: Every extracted transaction, party, and extent maps directly to source document pages.
3. **No Unsubstantiated Claims**: Fraud or invalidity labels are strictly forbidden; system outputs `"POSSIBLE_CONFLICT"` with supporting evidence links.
