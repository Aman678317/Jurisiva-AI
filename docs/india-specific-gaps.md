# Chapter 7 — India-Specific Gaps & Technical Hurdles

## Overview
Generic global AI tools fail in India due to deep regional domain complexities, language diversity, and non-standard record formats. This document details India-specific gaps and categorizes each into Verified Fact vs. Design Hypothesis.

---

## 1. Multilingual Documents & Indic OCR

### VERIFIED FACT
- **Language Mixed Deeds**: Indian legal and property documents frequently mix English stamp paper header text with regional language body text (Hindi, Kannada, Marathi, Tamil, Telugu, Bengali) and handwritten notes.
- **OCR Degraded Inputs**: Pre-2005 deeds stored in Sub-Registrar archives are often low-resolution monochrome scans (100–150 DPI) with ink bleeds, physical tears, and skewed pages.
- **Generic Engine Failure**: Standard off-the-shelf English OCR models (e.g. basic Tesseract default engine) produce unusable gibberish on Indic legal scans.

### DESIGN HYPOTHESIS
- Combining specialized Tesseract/PaddleOCR Indic models with pre-processing pipelines (deskewing, adaptive binarization, contrast enhancement) will achieve > 95% character accuracy on standard Indian deed scans.

---

## 2. Indian Names & Transliteration Discrepancies

### VERIFIED FACT
- **Phonetic Spelling Variations**: Indian names undergo varied English transliterations across historical documents (e.g. "Ramappa", "Ramappa Gowda", "Ramaiah"; or "Choudhury", "Chowdhury", "Choudhry").
- **Father/Husband Name Inclusions**: Land records rely heavily on relational names (e.g. "S/o Venkatappa" or "W/o Ramesh") to uniquely identify owners rather than unique alphanumeric IDs (Aadhaar/PAN are absent in historical deeds).

### DESIGN HYPOTHESIS
- Incorporating phonetic matching algorithms (Double Metaphone / Levenshtein distance) combined with relational graph models (Name + S/o + Village) will reduce false-positive name contradiction alerts by > 80%.

---

## 3. Regional Property Record Terminology & Measurement Units

### VERIFIED FACT
- **Fragmented Regional Terminology**: Land records use distinct state terminology:
  - *Karnataka*: RTC (Record of Rights, Tenancy and Crops), Pahani, Khata Extract, Mutation Extract (MR).
  - *Maharashtra*: 7/12 Extract (Saat Bara), Ferfar, City Survey Extract.
  - *North India (UP/MP/Delhi)*: Khasra, Khatauni, Jamabandi, Aks Shajra.
  - *Tamil Nadu*: Patta, Chitta, Adangal.
  - *Telangana/AP*: Pahani, Dharani 1-B extract.
- **Non-Standard Area Units**: Land extent is measured in regional units across states:
  - *Acre, Gunta* (1 Acre = 40 Guntas; 1 Gunta = 1,089 sq.ft) - South/West India.
  - *Bigha, Biswa, Kattha* - North/East India (unit size varies by state).
  - *Cents, Ground, Ankanam* - Tamil Nadu / Andhra Pradesh.

### DESIGN HYPOTHESIS
- A unified India Property Schema with automatic unit conversion into normalized Square Feet and Acres will eliminate extent calculation errors across historical deeds.

---

## 4. Document Formats & Inconsistent Metadata

### VERIFIED FACT
- **Non-Standard Layouts**: Unlike standard US contracts, Indian property deeds feature official stamp duty endorsements printed in margins, registration stamps on reverse sides of pages, and handwritten Sub-Registrar seals.
- **Registration Endorsements**: Critical legal facts (Doc No, Volume No, Book No, Registration Date) are often hand-stamped on the final page or margin.

### DESIGN HYPOTHESIS
- Multi-region bounding-box layout parsing will successfully capture marginal and reverse-page registration stamps that standard single-column text extractors miss.

---

## 5. Evidence Traceability & Legal Admissibility

### VERIFIED FACT
- **Section 63 / 65B Compliance**: Under the Bharatiya Sakshya Adhiniyam / Indian Evidence Act, electronic summaries must maintain unalterable, verifiable provenance to original source documents. Lawyers cannot present unverified AI output in court or to institutional lenders.

### DESIGN HYPOTHESIS
- Storing immutable SHA-256 hashes of all uploaded source document pages and anchoring every AI assertion to a specific page bounding-box satisfies internal compliance audit requirements for bank panel Advocates.
