# Data Platform & Governed Intelligence Test Suite

from app.intelligence.evidence_graph import evidence_graph_engine
from app.intelligence.claim_verifier import claim_verifier

describe("Chapter 19 Data Platform, Analytics & Intelligence Layer", () => {
  test("DAT-001: Add evidence graph edge with complete provenance", () => {
    const prov = { document_id: "doc_1985", page_number: 1, extraction_method: "INDIC_OCR" };
    const edge = evidence_graph_engine.add_evidence_edge("org_001", "person_venkatappa", "TRANSFERRED_TITLE_TO", "person_krishnappa", prov);
    expect(edge.edge_id).toBeDefined();
    expect(edge.provenance.document_id).toBe("doc_1985");
  });

  test("DAT-002: Zero cross-tenant graph traversal enforcement", () => {
    evidence_graph_engine.add_evidence_edge("org_002", "person_unauthorized", "OWNS", "parcel_999", { source: "test" });

    const tenantAEdges = evidence_graph_engine.query_tenant_graph("org_001", "person_unauthorized");
    expect(tenantAEdges.length).toBe(0);

    const tenantBEdges = evidence_graph_engine.query_tenant_graph("org_002", "person_unauthorized");
    expect(tenantBEdges.length).toBe(1);
  });

  test("DAT-003: Claim verifier classifies unsupported and contradicted claims", () => {
    const unverified = claim_verifier.verify_claim("Venkatappa owns Survey 999", []);
    expect(unverified.status).toBe("UNVERIFIED");

    const contradicted = claim_verifier.verify_claim("Venkatappa owns 5 Acres", [{ status: "POSSIBLE_CONFLICT" }]);
    expect(contradicted.status).toBe("CONTRADICTED");
  });
});
