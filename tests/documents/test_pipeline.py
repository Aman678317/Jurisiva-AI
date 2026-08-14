# Document Processing Pipeline & Indic OCR Evaluation Test Suite

from workers.ingestion_worker.ocr_engine import ocr_gateway
from workers.ingestion_worker.pipeline import document_pipeline, PDFTextDetector, EntityCandidateExtractor

describe("Document Processing Pipeline & OCR Evaluation", () => {
  test("DOC-001: PDF text vs scanned page detection", () => {
    expect(PDFTextDetector.inspect_page(10)).toBe(true);  // Low text density -> Scanned OCR required
    expect(PDFTextDetector.inspect_page(500)).toBe(false); // Native text embedded PDF
  });

  test("DOC-002: Indic OCR Gateway language & bounding box extraction", () => {
    const res = ocr_gateway.process_page_image(1, true);
    expect(res.raw_text).toContain("Survey No. 42/1");
    expect(res.detected_languages).toContain("mr");
    expect(res.quality_score).toBeGreaterThanOrEqual(0.90);
    expect(res.layout_blocks.length).toBe(3);
    expect(res.words[0].bbox).toBeDefined();
  });

  test("DOC-003: Entity Candidate Extraction for Survey # and Extent", () => {
    const sampleText = "Deed executed on 14-08-1985 for Survey No. 42/1 Hissa 2 measuring 2 Acres 24 Guntas";
    const candidates = EntityCandidateExtractor.extract_candidates(sampleText, 1);
    expect(candidates.length).toBeGreaterThanOrEqual(3);
    
    const syCandidate = candidates.find(c => c.entity_type === "SURVEY_NUMBER");
    expect(syCandidate?.normalized_value).toBe("42/1");

    const extentCandidate = candidates.find(c => c.entity_type === "EXTENT");
    expect(extentCandidate?.normalized_value).toContain("2 Acres 24 Guntas");
  });

  test("DOC-004: End-to-End Pipeline Execution & Quality Threshold Validation", () => {
    const result = document_pipeline.process_document("doc_test_101", "SaleDeed.pdf", true);
    expect(result.status).toBe("READY");
    expect(result.pipeline_log.length).toBe(5);
    expect(result.entities.length).toBeGreaterThan(0);
    expect(result.raw_ocr_text).toBe(result.normalized_text); // Provenance preservation check
  });

  test("DOC-005: Idempotency & Bounded Retry Safety", () => {
    const run1 = document_pipeline.process_document("doc_test_101", "SaleDeed.pdf", true);
    const run2 = document_pipeline.process_document("doc_test_101", "SaleDeed.pdf", true);
    expect(run1.document_id).toBe(run2.document_id);
    expect(run1.quality_score).toBe(run2.quality_score);
  });
});
