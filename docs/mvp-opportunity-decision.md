# Chapter 10 — MVP Opportunity Decision & Roadmap

## Strategic Recommendation Summary

Based on market research, competitor benchmarking, score-ranked opportunity mapping (41/45 score), and solo-founder execution feasibility, we make the following explicit workflow commitments:

```
[PRIMARY MVP WORKFLOW]
  └── Property Title Due Diligence & Search Report Generation

[SECONDARY WORKFLOW - Phase 2]
  └── Court Litigation Matter Bundle Fact & Timeline Extraction

[LATER WORKFLOW - Phase 3]
  └── Commercial Lease & Contract Key Clause Abstraction

[DO NOT BUILD YET - Excluded]
  └── Automated e-Courts Web Scraping & Autonomous Portal Filings
```

---

## Detailed Rationale & Justification

### 1. PRIMARY MVP WORKFLOW: Property Title Due Diligence & Search Report Generation
- **Target User**: Property Advocates, Title Search Professionals, Bank Panel Lawyers.
- **Core Bundle**: Sale Deeds, Mother Deeds, Partition Deeds, Gift Deeds, Encumbrance Certificates (EC), Pahani/RTC extracts, Property Tax Receipts.
- **Core Deliverable**: Workspace featuring OCR text layer, extracted property entity matrix, chronological title flow timeline, contradiction detection alerts, split-screen citation viewer, and one-click draft Title Search Report (.docx/PDF).
- **Why Selected**:
  1. **Maximum Pain & Economic Value**: Manual property title search requires 6–8 hours of tedious paper/PDF reading per transaction. Advocates earn direct fees per report and will gladly adopt tools that reduce draft time to < 45 minutes.
  2. **Clear Document Boundaries**: A property title bundle has a discrete start and end (13–30 year history). Unlike open-ended legal research, property due diligence is bounded by the uploaded bundle files.
  3. **High AI Advantage**: LLMs excel at structured entity extraction, date ordering, and cross-deed text comparison when supported by deterministic OCR and RAG citations.
  4. **Low Regulatory Barriers**: The platform acts strictly as an AI research assistant generating a draft report for the human Advocate's review and signature, avoiding unauthorized legal practice concerns.

---

### 2. SECONDARY WORKFLOW: Litigation Case Bundle Fact & Timeline Extraction (Phase 2)
- **Target User**: Indian Law Firm Litigation Associates, Advocate Practitioners.
- **Core Bundle**: Plaints, Written Statements, Affidavits, Lower Court Judgments, Depositions, Exhibit Bundles.
- **Why Deferred to Phase 2**:
  - Builds on the exact same core infrastructure (Ingestion, OCR, Hybrid Vector Search, Citation RAG, Split Viewer).
  - Litigation bundles are often larger (500–2,000 pages), requiring higher memory optimization and complex witness-statement cross-referencing. Deferring to Phase 2 ensures the core pipeline is rock-solid first.

---

### 3. LATER WORKFLOW: Commercial Lease & Agreement Abstraction (Phase 3)
- **Target User**: Corporate In-House Counsel, Enterprise Legal Ops.
- **Why Deferred to Phase 3**:
  - Corporate CLM space in India is already contested by established players (SpotDraft, SirionLabs).
  - Requires enterprise B2B sales cycles, SOC 2 compliance, and enterprise SSO integrations, which add friction for an initial lean launch.

---

### 4. DO NOT BUILD YET: Automated e-Courts Scraping & Autonomous Portal Filings
- **Why Explicitly Excluded**:
  - Extremely high technical fragility: Indian government land and court portals frequently change layout, introduce CAPTCHA challenges, or experience downtime.
  - High legal and security risk: Scraping protected portals can violate site terms or computer misuse regulations.
  - Core Principle Compliance: Violates the core engineering principle: *"Never invent APIs or rely on undocumented government web-scraping."* All data in our platform must enter via user-uploaded documents or official authorized APIs.
