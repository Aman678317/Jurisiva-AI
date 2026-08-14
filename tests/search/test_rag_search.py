# Hybrid Search, RAG & Citation Validation Test Suite

from app.chunking import chunker
from app.embeddings import embedding_provider, vector_index
from app.search_engine import search_engine
from app.rag_engine import rag_engine, EvidenceSufficiencyGate, CitationValidator

describe("Hybrid Search, RAG & Evidence Grounding", () => {
  // Setup Test Fixtures
  const testPages = [
    { page_number: 1, raw_ocr_text: "REGISTERED NO: 1234/1985\n\nTHIS DEED OF SALE executed on 14-08-1985." },
    { page_number: 3, raw_ocr_text: "SCHEDULE PROPERTY: Survey No. 42/1 Hissa 2, Extent: 2 Acres 24 Guntas (104,544 Sq.Ft), Devanahalli." }
  ];

  const chunks = chunker.chunk_document("org_001", "mat_001", "doc_001", "v1", testPages);
  vector_index.upsert_chunks(chunks);

  test("RAG-001: Structure-aware chunking & content hashing", () => {
    expect(chunks.length).toBe(2);
    expect(chunks[0].content_hash).toBeDefined();
    expect(chunks[1].page_number).toBe(3);
  });

  test("RAG-002: Exact identifier overboost search (Survey No. 42/1)", () => {
    const results = search_engine.execute_hybrid_search("org_001", "mat_001", "Survey No. 42/1", top_k=5);
    expect(results.length).toBeGreaterThan(0);
    expect(results[0].text).toContain("Survey No. 42/1");
    expect(results[0].page_number).toBe(3);
  });

  test("RAG-003: Cross-tenant search block (Tenant Isolation)", () => {
    // Org 002 searching Org 001 matter files
    const crossTenantResults = search_engine.execute_hybrid_search("org_002", "mat_001", "Survey No. 42/1", top_k=5);
    expect(crossTenantResults.length).toBe(0); // MUST return empty array for unauthorized tenant
  });

  test("RAG-004: Evidence Sufficiency Gate (Negative Query Refusal)", () => {
    const [status, sufficient] = EvidenceSufficiencyGate.evaluate_sufficiency([], "Non-existent query text");
    expect(status).toBe("INSUFFICIENT_EVIDENCE");
    expect(sufficient).toBe(false);

    const ragRes = rag_engine.query_assistant("org_001", "mat_001", "Where is the secret nuclear code?");
    expect(ragRes.evidence_status).toBe("INSUFFICIENT_EVIDENCE");
    expect(ragRes.answer).toContain("Insufficient evidence");
  });

  test("RAG-005: Grounded answer & server-side citation validation", () => {
    const ragRes = rag_engine.query_assistant("org_001", "mat_001", "What is the extent of Survey No 42/1?");
    expect(ragRes.evidence_status).toBe("SUPPORTED");
    expect(ragRes.citations.length).toBe(1);
    expect(ragRes.citations[0].status).toBe("VERIFIED_SOURCE");
    expect(ragRes.citations[0].page_number).toBe(3);
  });

  test("RAG-006: Server-side Citation Validator catches invalid page citation", () => {
    const invalidCitation = [{ document_id: "doc_001", page_number: 99, excerpt: "Fake text" }];
    const validChunks = [{ page_number: 3, text: "Real text" }];
    const validated = CitationValidator.validate_citations(invalidCitation, validChunks);
    expect(validated[0].status).toBe("UNVERIFIED_CITATION");
  });
});
