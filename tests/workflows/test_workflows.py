# Legal & Property Intelligence Workflows Test Suite

from app.workflows.property_timeline import timeline_builder
from app.workflows.comparator import document_comparator
from app.workflows.entity_resolution import entity_resolver
from app.workflows.conflict_detector import conflict_detector
from app.workflows.report_builder import report_builder

describe("Chapter 10 Legal & Property Workflows", () => {
  const sampleDeeds = [
    { document_id: "doc_1985", execution_date: "1985-08-14", event_type: "SALE_DEED", executant: "Venkatappa", claimant: "Krishnappa", extent: "2 Acres 24 Guntas", page_number: 1 },
    { document_id: "doc_2010", execution_date: "2010-05-20", event_type: "MORTGAGE_DEED", executant: "Krishnappa", claimant: "State Bank of India", extent: "2 Acres 24 Guntas", page_number: 1 },
    { document_id: "doc_2018", execution_date: "2018-11-12", event_type: "SALE_DEED", executant: "Krishnappa", claimant: "Anand Kumar", extent: "2 Acres 10 Guntas", page_number: 2 }
  ];

  test("WORKFLOW-001: Property Timeline Builder & Gap Detection", () => {
    const timeline = timeline_builder.build_timeline(sampleDeeds);
    expect(timeline.timeline_nodes.length).toBe(3);
    expect(timeline.title_gaps.length).toBeGreaterThan(0); // 25 year gap between 1985 and 2010
  });

  test("WORKFLOW-002: Document Comparator Line Diffs", () => {
    const textA = "Clause 1: Consideration is Rs 50,00,000.\nClause 2: Possession transferred.";
    const textB = "Clause 1: Consideration is Rs 60,00,000.\nClause 2: Possession transferred.";
    const diffRes = document_comparator.compare_documents(textA, textB);
    expect(diffRes.added_count).toBe(1);
    expect(diffRes.removed_count).toBe(1);
    expect(diffRes.unchanged_count).toBe(1);
  });

  test("WORKFLOW-003: Cautious Entity Resolution", () => {
    const ent1 = { name: "Rajesh Sharma", address: "Devanahalli, Bengaluru" };
    const ent2 = { name: "Rajesh Sharma", address: "Devanahalli, Bengaluru" };
    const matchRes = entity_resolver.resolve_entity(ent1, ent2);
    expect(matchRes.status).toBe("MATCH");

    const entAmbiguous = { name: "Rajesh Sharma", address: "Whitefield, Bengaluru" };
    const ambigRes = entity_resolver.resolve_entity(ent1, entAmbiguous);
    expect(ambigRes.status).toBe("POSSIBLE_MATCH");
    expect(ambigRes.action).toBe("FLAG_FOR_REVIEW");
  });

  test("WORKFLOW-004: Evidence Conflict Detector", () => {
    const conflicts = conflict_detector.detect_conflicts(sampleDeeds);
    expect(conflicts.length).toBeGreaterThanOrEqual(2);
    
    const extentConflict = conflicts.find(c => c.conflict_type === "EXTENT_MISMATCH");
    expect(extentConflict?.status).toBe("POSSIBLE_CONFLICT");

    const mortgageConflict = conflicts.find(c => c.conflict_type === "UNRELEASED_MORTGAGE");
    expect(mortgageConflict?.status).toBe("POSSIBLE_CONFLICT");
  });

  test("WORKFLOW-005: Title Search Report Generation with Citations & Disclaimer", () => {
    const timeline = timeline_builder.build_timeline(sampleDeeds);
    const conflicts = conflict_detector.detect_conflicts(sampleDeeds);
    const propDetails = { survey_number: "42/1", extent: "2 Acres 24 Guntas", location: "Devanahalli" };
    
    const report = report_builder.generate_report("mat_001", propDetails, timeline.timeline_nodes, conflicts);
    expect(report.title).toContain("MATTER mat_001");
    expect(report.disclaimer).toContain("LEGAL DISCLAIMER");
    expect(report.review_status).toBe("APPROVED_FOR_EXPORT");
  });
});
