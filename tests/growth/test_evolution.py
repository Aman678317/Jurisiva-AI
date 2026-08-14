# Post-Production Evolution & Experimentation Test Suite

from app.growth.feedback_collector import feedback_collector
from app.growth.experiment_gate import experiment_gate

describe("Chapter 18 Post-Production Evolution & Continuous Delivery", () => {
  test("EVO-001: Record advocate AI citation feedback and queue regression fixture", () => {
    const res = feedback_collector.record_feedback("org_001", "usr_001", "run_999", "POOR", "Citation linked page 3 instead of page 4", true);
    expect(res.feedback_id).toBeDefined();
    expect(res.is_citation_error).toBe(true);
    expect(res.regression_fixture_status).toBe("QUEUED_FOR_REGRESSION_TEST");
  });

  test("EVO-002: Product Experiment Gate canary cohort routing", () => {
    expect(experiment_gate.should_apply_variant("exp_fast_reranker", 5)).toBe(true);
    expect(experiment_gate.should_apply_variant("exp_fast_reranker", 15)).toBe(false);
  });

  test("EVO-003: Safety threshold breach triggers experiment rollback", () => {
    const rolledBack = experiment_gate.trigger_rollback_if_unsafe("exp_fast_reranker", 0.95);
    expect(rolledBack).toBe(true);
    expect(experiment_gate.should_apply_variant("exp_fast_reranker", 5)).toBe(false);
  });
});
