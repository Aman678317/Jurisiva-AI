# Chapter 6 — Detailed Workflow Decomposition & Transformation Analysis

## Overview
This document analyzes the current manual vs. future AI-assisted states for the top 5 legal and property workflows.

---

## Workflow 1: Property Title Chain Verification & Link Deed Audit

### CURRENT STATE (Manual)
1. **Manual Document Sorting**: Advocate receives physical paper bundle or PDF folder containing 15+ deeds. Manually inspects each page to identify document types (Sale Deed, Mother Deed, Gift Deed, EC, RTC).
2. **Page-by-Page Reading**: Manually reads 100+ pages of dense legal text to locate execution dates, registration numbers, executants, claimants, and property schedule descriptions.
3. **Manual Paper Note Taking**: Writes down title flow on a notepad (e.g. 1978: A transfers to B -> 1995: B transfers to C -> 2012: C mortgages to Bank).
4. **Manual Link Identification**: Checks if any year gap exists or if a link deed is missing between conveyances.
5. **Decision & Drafting**: Types out the title flow manually into MS Word to produce the draft Title Search Report.
- *Total Elapsed Time*: **6 to 8 hours**
- *Failure Points*: Missing an unindexed link deed, misreading handwritten registration numbers, fatigue leading to oversight.

### FUTURE STATE (AI-Assisted + Human Verification)
1. **Upload & Auto-Classification**: Advocate uploads 15-document PDF bundle into Matter Workspace. System automatically classifies document types, performs OCR, and indexes text.
2. **AI Entity & Date Extraction**: Automated extraction of Executants, Claimants, Registration Date, Doc No, Extent, and Property Schedule.
3. **Automated Title Flow Timeline**: System automatically orders deeds chronologically, highlights unbroken transfers, and flags missing link deeds (`LINK GAP DETECTED: 1995 to 2004`).
4. **Split-Screen Human Verification**: Advocate clicks timeline items to view split-screen bounding-box highlight on the original scanned deed, verifying exact facts.
5. **One-Click Export**: Verified title flow is exported into the editable draft Title Search Report.
- *Total Elapsed Time*: **30 to 45 minutes**
- *Human Role*: Critical verifier of AI extraction badges (`AI EXTRACTION` -> `HUMAN VERIFIED`).

---

## Workflow 2: Cross-Document Property Extent & Boundary Reconciliation

### CURRENT STATE (Manual)
1. **Document Comparison**: Advocate opens Sale Deed in one window and Encumbrance Certificate / Pahani extract in another.
2. **Manual Extent Comparison**: Checks if the extent in the 1982 Sale Deed (e.g. 2 Acres 10 Guntas) matches the extent in the 2015 Partition Deed and the current RTC Pahani extract.
3. **Manual Boundary Inspection**: Compares North/South/East/West boundary descriptions across multiple schedule deeds to verify physical boundary consistency.
4. **Discrepancy Logging**: Manually notes discrepancies in a query sheet to send to the developer/client.
- *Total Elapsed Time*: **2 to 3 hours**
- *Failure Points*: Overlooking unit conversions (e.g. Cents to Sq.Ft or Sq.Yards to Sq.Meters), failing to spot minor boundary shifts across deeds.

### FUTURE STATE (AI-Assisted + Human Verification)
1. **Automated Schedule Parser**: System parses Property Schedule tables and text across all bundle documents.
2. **Extent Reconciliation Engine**: System normalizes extent measurements (Acres, Guntas, Sq.Ft, Cents) and presents a unified Extent Matrix.
3. **Contradiction Alerting**: System generates automated red-flag alerts if Extent or Boundaries conflict across documents (`ALERT: 1982 Sale Deed specifies North boundary as Govt Road; 2015 Deed specifies Private Property`).
4. **Human Review**: Advocate inspects side-by-side highlighted text to confirm or dismiss the boundary discrepancy.
- *Total Elapsed Time*: **15 minutes**
- *Human Role*: Evaluates whether the discrepancy is a material legal defect or a clerical mistake.

---

## Workflow 3: Litigation Bundle Fact Discovery & Citation Q&A

### CURRENT STATE (Manual)
1. **Bulk Document Search**: Advocate searches 800-page case file for specific claims made in affidavits or cross-examinations.
2. **Ctrl+F / Physical Page Turning**: Attempts keyword searches (often fails due to non-searchable scanned PDFs).
3. **Manual Citation Copying**: Manually types out quotes and page numbers into court brief notes.
- *Total Elapsed Time*: **3 to 5 hours**
- *Failure Points*: Incorrect page citations, missing key evidence buried in deep annexures.

### FUTURE STATE (AI-Assisted + Human Verification)
1. **OCR & Vector Indexing**: Full matter bundle indexed with hybrid vector/BM25 search.
2. **Citation-Aware RAG Chat**: Advocate types natural language query: "What did Witness 2 state regarding the payment date in his cross-examination?".
3. **Grounded Answer & Citation Badge**: System returns direct answer with inline citation: `[Doc 4 (Cross-Exam), Page 12, Para 3]`.
4. **Instant Split-Screen Jump**: Clicking citation instantly opens Document Viewer to Page 12 with snippet highlighted in yellow.
- *Total Elapsed Time*: **5 minutes**
- *Human Role*: Reads highlighted snippet to confirm context before incorporating into court argument.

---

## Workflow 4: Encumbrance Certificate (EC) Audit & Mortgage Verification

### CURRENT STATE (Manual)
1. **Line-by-Line EC Scan**: Advocate examines 15-year Encumbrance Certificate containing hundreds of handwritten entry rows in tabular format.
2. **Cross-Checking Mortgages**: Checks if registered Bank Mortgages (Deposit of Title Deeds) listed in EC are accompanied by corresponding Reconveyance / Discharge Deeds.
- *Total Elapsed Time*: **2 hours**

### FUTURE STATE (AI-Assisted + Human Verification)
1. **Tabular OCR & Parsing**: System extracts EC table rows (Entry No, Period, Property Description, Executant, Claimant, Vol/Page, Doc No).
2. **Mortgage-Discharge Matching Engine**: System pairs registered Bank Mortgages with corresponding Discharge Deeds. Flags any un-discharged encumbrance (`WARNING: 2011 Mortgage to SBI has no matching Discharge Deed in EC`).
3. **Advocate Review**: Advocate checks the flagged entry in the split viewer and requests a Discharge Certificate from the seller.
- *Total Elapsed Time*: **10 minutes**

---

## Workflow 5: Draft Title Search Report Generation

### CURRENT STATE (Manual)
1. **Template Copy-Paste**: Advocate opens an old Word template from a previous matter, manually deletes old names, dates, and property descriptions.
2. **Manual Re-entry**: Manually re-types all title flow dates, survey numbers, boundary details, and encumbrance notes.
- *Total Elapsed Time*: **2 hours**
- *Failure Points*: Residual text left over from old client matters leading to severe confidentiality breach.

### FUTURE STATE (AI-Assisted + Human Verification)
1. **Template Auto-Populate**: System aggregates all `HUMAN VERIFIED` entity extractions, verified title flow timeline, and approved encumbrance notes.
2. **Clean Generation**: Generates a pristine, fresh DOCX Title Search Report formatted to bank standards with zero residual text.
3. **Final Advocate Sign-Off**: Advocate reviews final document, signs, and issues to bank/client.
- *Total Elapsed Time*: **10 minutes**
