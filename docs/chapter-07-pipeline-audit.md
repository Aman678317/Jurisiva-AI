# Chapter 7 — Document Ingestion & OCR Pipeline Audit

## 1. Pipeline Audit & Ingestion Architecture Inspection

| Component / Layer | Chapter 6 Baseline | Target Chapter 7 Implementation | Status & Action |
| :--- | :--- | :--- | :--- |
| **Supported File Formats**| PDF, PNG, JPEG, TIFF metadata limits | Multilingual scanned PDFs, digital PDFs, TIFF, JPEG | **IMPLEMENTING** multi-stage file validator |
| **Original File Preservation**| Storage key generator in `storage.py` | Immutable original storage; versioned derived artifacts | Sealed original binary storage path |
| **Processing State Machine** | Basic transitions in `jobs.py` | Complete lifecycle (`UPLOADED` -> `VALIDATING` -> `EXTRACTING` -> `OCR` -> `READY`) | Enforced explicit state machine |
| **PDF Text vs Scan Detection**| Stubbed metadata check | Page-by-page text density & raster image inspection | `PDFTextDetector` engine |
| **Indic OCR Engine** | Abstract pipeline specification | Replaceable `OCRGateway` with Indic script support (English + Devanagari/Hindi/Marathi) | `OCRGateway` with bounding box JSON |
| **Raw vs. Normalized Text** | Single text field | Distinct `raw_ocr_text` vs `normalized_text` preservation | Provenance-preserving text model |
| **Entity Extraction** | Schema definitions | Entity candidate extractor (Survey #, Extent, Executant, Claimant, Dates) | `EntityCandidateExtractor` |
| **OCR Evaluation Harness** | N/A | Synthetic evaluation dataset & CER/WER benchmark harness | Benchmark evaluation test suite |

---

## 2. Risk & Vulnerability Mitigation Analysis
- **Original File Corruption**: Silently overwriting source PDFs with OCR or compressed output.
  - *Fix*: Originals are immutable; derived page images, OCR text layers, and chunks are stored as versioned derived artifacts.
- **Multilingual Legal Identifier Destruction**: Aggressive text normalization altering survey numbers (e.g. converting `123/4A` to `1234a`).
  - *Fix*: Strict conservative normalization rule: raw OCR text is preserved intact; normalization cleans whitespace and Unicode encoding only.
- **Malformed & Decompression Bombs**: Processing corrupted or zip-bomb PDFs.
  - *Fix*: File signature validation, page count limits (max 500 pages), and memory-bounded isolated worker processing.
