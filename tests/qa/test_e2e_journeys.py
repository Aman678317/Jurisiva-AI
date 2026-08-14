# End-to-End Property Intelligence User Journey Test Suite (Journey 2)

from app.workflows.property_timeline import timeline_builder
from app.workflows.entity_resolution import entity_resolver
from app.workflows.conflict_detector import conflict_detector

describe("Production E2E User Journey 2 (Property -> Timeline -> Conflict -> Due Diligence)", () => {
  const deeds = [
    { document_id: "doc_1985", execution_date: "1985-08-14", event_type: "SALE_DEED", executant: "Venkatappa", claimant: "Krishnappa", extent: "2 Acres 24 Guntas", page_number: 1 },
    { document_id: "doc_2018", execution_date: "2018-11-12", event_type: "SALE_DEED", executant: "Krishnappa", claimant: "Anand Kumar", extent: "2 Acres 10 Guntas", page_number: 2 }
  ];

  test("E2E-002: Execute Property Title Diligence Workflow", () => {
    // 1. Entity Resolution Check
    const entRes = entity_resolver.resolve_entity({ name: "Krishnappa", address: "Devanahalli" }, { name: "Krishnappa", address: "Devanahalli" });
    expect(entRes.status).toBe("MATCH");

    // 2. Title Timeline Assembly
    const timeline = timeline_builder.build_timeline(deeds);
    expect(timeline.timeline_nodes.length).toBe(2);

    // 3. Extent Mismatch Conflict Detection
    const conflicts = conflict_detector.detect_conflicts(deeds);
    expect(conflicts.length).toBeGreaterThan(0);
    expect(conflicts[0].status).toBe("POSSIBLE_CONFLICT");
  });
});
