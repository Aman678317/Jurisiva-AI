# Chapter 5 — Jobs-to-be-Done (JTBD) & Functional Requirements

## Ranked Overview of Core Jobs

| Job ID | Job Title | Target User | Importance Rank | MVP Priority |
| :--- | :--- | :--- | :---: | :---: |
| **JTBD-01** | Property Ownership & Extent Reconciliation | Property Advocate / Due Diligence Specialist | **#1** | **Core MVP** |
| **JTBD-02** | Chronological Title Flow Timeline Construction | Property Advocate / Due Diligence Specialist | **#2** | **Core MVP** |
| **JTBD-03** | Citation-Aware Document Q&A & Evidence Search | Law Firm Associate / Advocate | **#3** | **Core MVP** |
| **JTBD-04** | Cross-Document Contradiction & Gap Detection | Property Advocate / Litigation Associate | **#4** | **Core MVP** |
| **JTBD-05** | Draft Title Search Report Generation | Property Advocate / Bank Panel Lawyer | **#5** | **Core MVP** |
| **JTBD-06** | Multilingual Indic Document Text Extraction | Property Advocate / In-House Legal | **#6** | **Core MVP** |
| **JTBD-07** | Commercial Lease / Contract Key Clause Extraction | In-House Legal Manager | **#7** | **Post-MVP / Phase 2** |

---

## Detailed Job Descriptions

### JTBD-01: Property Ownership & Extent Reconciliation
- **Statement**: **When** I receive a 20-page property deed bundle (Sale Deed, Mother Deed, Pahani/RTC), **I want to** automatically extract and compare the registered owners, survey numbers, schedules, boundaries, and land extent, **So that** I can instantly catch any discrepancy in title ownership or land measurement before issuing my opinion.
- **Trigger**: Bank or client requests a property title search report for a loan or purchase.
- **Input**: Scanned PDF bundle containing 13–30 year property deeds and land extracts.
- **Workflow**: Upload bundle -> OCR text extraction -> Entity Extraction -> Cross-document alignment -> Visual verification.
- **Decision**: Does the seller have clean, undisputed title to the exact extent of land specified in the sale agreement?
- **Output**: Structured property entity table with extent comparison across deeds and source citations.
- **Failure Mode**: OCR fails on blurry handwritten stamp paper, or AI misinterprets regional land units (e.g. Gunta, Ankanam, Cents, Bigha, Acre).

---

### JTBD-02: Chronological Title Flow Timeline Construction
- **Statement**: **When** I examine multiple historical conveyances spanning 30 years, **I want to** build a chronological sequence of deeds, mortgages, court orders, and registrations, **So that** I can verify that every link in the chain of title is unbroken.
- **Trigger**: Opening a new property due diligence matter.
- **Input**: Mixed bundle of registered sale deeds, partition deeds, gift deeds, release deeds, and encumbrance certificates.
- **Workflow**: Date & Party extraction -> Event sorting -> Link deed validation -> Timeline graph/list rendering.
- **Decision**: Is there a missing link deed (e.g. transfer between 1994 and 2002 missing)?
- **Output**: Chronological timeline displaying Date, Document Type, Executant, Claimant, Property Description, and Link Status.
- **Failure Mode**: Incorrect date parsing from registration endorsements vs execution dates.

---

### JTBD-03: Citation-Aware Document Q&A & Evidence Search
- **Statement**: **When** I am reviewing a complex 500-page case file or document bundle, **I want to** ask specific natural language questions and receive accurate answers with exact page citations, **So that** I can instantly locate source evidence without reading hundreds of pages manually.
- **Trigger**: Preparing brief notes or researching specific legal/factual questions in a matter.
- **Input**: User query (e.g. "What is the mortgage amount registered in the 2012 Deposit of Title Deeds?").
- **Workflow**: User query -> Hybrid vector/keyword retrieval -> RAG prompt assembly -> LLM response generation with page/snippet citations -> UI render.
- **Decision**: Is the AI answer backed by exact text on the cited page?
- **Output**: Formatted answer text with clickable source inline badges (`[Doc 2, Page 4]`) that jump to the exact page and highlight the relevant passage.
- **Failure Mode**: Model generates an answer without inline citations or cites the wrong document page.

---

### JTBD-04: Cross-Document Contradiction & Gap Detection
- **Statement**: **When** I process multiple deeds and affidavits in a matter, **I want to** automatically scan for conflicting facts (e.g. differing party names, conflicting survey numbers, uncancelled mortgages in EC), **So that** I can highlight critical risks in my legal report.
- **Trigger**: Pre-export verification check of matter documents.
- **Input**: All uploaded document text and extracted entity schemas in the matter workspace.
- **Workflow**: Entity reconciliation -> Boundary/Extent comparison -> Encumbrance matching -> Red-flag highlight generation.
- **Decision**: Are there unresolved contradictions that make the title unmarketable or litigation risky?
- **Output**: Contradiction card list detailing: Source Document A vs. Source Document B, Discrepancy Type, Severity, and Recommended Human Action.
- **Failure Mode**: False positive alerts caused by minor spelling variations in Indian names (e.g. "Ramappa" vs "Ramappa").

---

### JTBD-05: Draft Title Search Report Generation
- **Statement**: **When** I complete my due diligence review, **I want to** export an editable, structured draft Title Search Report containing the title flow, property description, encumbrance findings, and legal opinion template, **So that** I can deliver a professional report to my bank or client in a fraction of the time.
- **Trigger**: Finalization of matter review and human verification.
- **Input**: Verified entity extractions, timeline events, contradiction notes, and lawyer's custom comments.
- **Workflow**: User clicks Export TSR -> Selects Report Template (Bank Standard / General Opinion) -> System compiles Markdown/DOCX report -> User downloads.
- **Decision**: Is the draft report clean, well-formatted, and completely accurate to hand over to the client?
- **Output**: Clean, editable MS Word (.docx) or PDF Title Search Report.
- **Failure Mode**: Unformatted export or inclusion of unverified AI assumptions in the final report.
