# Production Reliability & Observability Test Suite

from app.operations.circuit_breaker import CircuitBreaker
from app.operations.dead_letter_queue import dlq_manager

describe("Chapter 12 Production Reliability, Observability & Incident Response", () => {
  test("REL-001: Circuit Breaker trips OPEN on threshold failures and triggers fallback", () => {
    const cb = new CircuitBreaker(2, 30);
    const failingFunc = () => { throw new Error("AI provider API 503"); };
    const fallbackFunc = () => "DEGRADED_MODE_FALLBACK";

    // 1st call fails
    const res1 = cb.execute(failingFunc, fallbackFunc);
    expect(res1).toBe("DEGRADED_MODE_FALLBACK");
    expect(cb.state).toBe("CLOSED");

    // 2nd call fails -> Trips OPEN
    const res2 = cb.execute(failingFunc, fallbackFunc);
    expect(res2).toBe("DEGRADED_MODE_FALLBACK");
    expect(cb.state).toBe("OPEN");
  });

  test("REL-002: Dead Letter Queue quarantines failed jobs and allows operator replay", () => {
    const record = dlq_manager.quarantine_failed_job("job_ocr_99", "ingestion_worker", "s3://bucket/pdf_99.pdf", "PDF corrupt", 3);
    expect(record.job_id).toBe("job_ocr_99");
    expect(record.status).toBe("QUARANTINED");

    const replayRes = dlq_manager.replay_job("job_ocr_99");
    expect(replayRes.status).toBe("SUCCESS");
    expect(replayRes.job.status).toBe("REPLAY_QUEUED");
  });
});
