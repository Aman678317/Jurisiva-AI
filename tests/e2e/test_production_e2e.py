# End-to-End Production User Journey Test Suite (Journey 1)

from app.auth import auth_engine
from app.storage import storage_adapter
from app.jobs import job_engine
from app.search_engine import search_engine
from app.rag_engine import rag_engine
from app.workflows.report_builder import report_builder

describe("Production E2E User Journey 1 (Signup -> Upload -> RAG -> Report Export)", () => {
  test("E2E-001: Execute complete End-to-End Advocate Workflow", () => {
    // 1. Authenticate Advocate User
    const tokenData = auth_engine.create_token("usr_001", "org_001", "LEAD_ADVOCATE");
    expect(tokenData.access_token).toBeDefined();

    // 2. Document Upload Intent & Validation
    const [valid, msg] = storage_adapter.validate_file_metadata("SaleDeed.pdf", 4839201, "application/pdf");
    expect(valid).toBe(true);

    // 3. Processing Job Creation
    const job = job_engine.create_job("org_001", "mat_001", "doc_001");
    expect(job.status).toBe("QUEUED");

    // 4. Hybrid Search Retrieval (BM25 + pgvector RRF)
    const searchRes = search_engine.execute_hybrid_search("org_001", "mat_001", "Survey No. 42/1", top_k=5);
    expect(searchRes.length).toBeGreaterThan(0);

    // 5. RAG Assistant Query & Citation Verification
    const ragRes = rag_engine.query_assistant("org_001", "mat_001", "What is the extent of Survey No 42/1?");
    expect(ragRes.evidence_status).toBe("SUPPORTED");
    expect(ragRes.citations.length).toBe(1);
    expect(ragRes.citations[0].status).toBe("VERIFIED_SOURCE");

    // 6. Title Search Report Export
    const report = report_builder.generate_report("mat_001", { survey_number: "42/1" }, [], []);
    expect(report.review_status).toBe("APPROVED_FOR_EXPORT");
  });
});
