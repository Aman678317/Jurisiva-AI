# Chapter 4 — Realistic Workflow-Based User Personas

## Persona 1: Property Advocate & Title Search Specialist (PRIMARY PERSONA)

- **Role**: Senior Property Advocate / Title Search Counsel
- **Organization Type**: Independent Law Practice / Property Legal Firm (Tier 1 & Tier 2 Indian Cities)
- **Workflow**: Receives 13–30 year property document bundles from banks, homebuyers, or real estate developers. Reads sale deeds, mother deeds, mutation extracts (Pahani/RTC), encumbrance certificates (EC), layout plans, and property tax receipts. Verifies ownership chain continuity, checks boundary/extent alignment, identifies pending mortgages or court stays, and drafts formal Title Search Reports (TSR) for bank loan approvals.
- **Current Tools**: Adobe Acrobat Reader, MS Word, physical page markers, WhatsApp for client file sharing, manual notes on paper pads.
- **Pain Points**:
  1. Spending 6–10 hours per matter manually reading scanned/faded Indian stamp papers and regional language deeds (e.g. Kannada, Hindi, Marathi).
  2. Risk of missing subtle extent discrepancies (e.g. Sale Deed says 2,400 sq.ft, Pahani extract says 2,100 sq.ft).
  3. Tedious manual construction of chronological title flow dates.
- **Frequency**: 5 to 15 property title searches per week.
- **Decision Authority**: High (Owner / Managing Partner of independent practice).
- **Budget Sensitivity**: Medium; willing to pay per-matter (~₹150 – ₹500) if it billably reduces draft time by 4+ hours per matter.
- **Security Concerns**: Critical; client property deeds and personal identifiers must remain strictly confidential and matter-isolated.
- **AI Concerns**: High anxiety regarding AI "hallucinations" or false claims that could lead to legal liability or bank rejection of a Title Search Report.
- **Success Definition**: Ability to generate a verified, citation-backed draft title timeline and entity summary in < 30 minutes, with split-screen visual verification.
- **Current Workaround**: Hiring junior Advocates/clerks to read deeds and summarize them manually, leading to variable quality and ongoing overhead.

---

## Persona 2: Indian Law-Firm Associate (SECONDARY PERSONA)

- **Role**: Senior Associate / Associate (Litigation & Arbitration)
- **Organization Type**: Mid-Sized Indian Law Firm (10–50 Advocates)
- **Workflow**: Manages court matter bundles (500–2000 pages) containing affidavits, lower court orders, cross-examinations, expert testimony, and contract exhibits. Constructs case timelines, prepares brief notes for Senior Advocates, and searches for contradictory statements across witness depositions.
- **Current Tools**: Adobe PDF, Foxit Phantom, MS Word, Manupatra / SCC Online for judgment research.
- **Pain Points**: Late-night crunch before court hearings spent searching for specific dates or contradictory statements in 1000-page court records.
- **Frequency**: Daily matter preparation; 3–5 active court bundles per week.
- **Decision Authority**: Low/Medium; recommends software to partners.
- **Budget Sensitivity**: Low (Firm pays for technology subscriptions).
- **Security Concerns**: Very high; strict client confidentiality (attorney-client privilege).
- **AI Concerns**: Demands exact page and paragraph citations for every AI assertion to present to Senior Counsel.
- **Success Definition**: Finding exact contradictions across witness statements in seconds with clickable page citations.
- **Current Workaround**: Ctrl+F keyword searching across non-searchable scanned PDFs or relying on memory.

---

## Persona 3: In-House Corporate Legal Manager (TERTIARY PERSONA)

- **Role**: Manager – Legal & Compliance
- **Organization Type**: Real Estate Developer / Housing Finance NBFC / Commercial Enterprise
- **Workflow**: Reviews large volumes of vendor contracts, commercial lease agreements, joint development agreements (JDA), and land acquisition bundles. Audits compliance obligations, renewal dates, and indemnity risks.
- **Current Tools**: MS Excel, MS Word, Google Drive, Email.
- **Pain Points**: Untracked lease renewal dates; manual extraction of liability caps and termination clauses across hundreds of executed contracts.
- **Frequency**: Continuous weekly review of incoming agreements.
- **Decision Authority**: Medium (Requires General Counsel or VP Legal sign-off).
- **Budget Sensitivity**: Low/Medium; corporate software budget available.
- **Security Concerns**: SOC 2 compliance, enterprise SSO, data residency within India.
- **AI Concerns**: Data leakage prevention (ensuring corporate contracts are not used for public model training).
- **Success Definition**: Automated extraction of key lease terms, indemnities, and title status into structured exportable spreadsheets.
- **Current Workaround**: Maintaining manual MS Excel tracking sheets updated by junior paralegals.
