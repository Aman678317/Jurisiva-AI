# AI Quality & Evaluation Benchmark Test Suite

from app.ai_quality.evaluation_engine import evaluation_engine

describe("Chapter 26 AI Product Intelligence & Continuous Evaluation", () => {
  test("EVL-001: Golden dataset BENCH-PROP-01 benchmark passes regression gate", () => {
    const res = evaluation_engine.evaluate_benchmark("BENCH-PROP-01", "v1.2.0", "gpt-4o-mini");
    expect(res.status).toBe("PASS");
    expect(res.metrics.grounding_precision).toBeGreaterThanOrEqual(0.95);
    expect(res.metrics.citation_validity).toBeGreaterThanOrEqual(0.98);
  });

  test("EVL-002: Hallucination rate is below 1% threshold", () => {
    const res = evaluation_engine.evaluate_benchmark("BENCH-CIT-02", "v1.0.0", "gpt-4o-mini");
    expect(res.metrics.hallucination_rate).toBeLessThanOrEqual(0.01);
  });

  test("EVL-003: Abstention accuracy on out-of-scope queries passes minimum 90% threshold", () => {
    const res = evaluation_engine.evaluate_benchmark("BENCH-HARD-03", "v1.1.0", "gpt-4o-mini");
    expect(res.metrics.abstention_accuracy).toBeGreaterThanOrEqual(0.90);
  });
});
