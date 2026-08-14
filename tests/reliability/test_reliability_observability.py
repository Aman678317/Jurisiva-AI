# Production Reliability & Observability Test Suite

import pytest
from app.operations.circuit_breaker import CircuitBreaker
from app.operations.dead_letter_queue import dlq_manager

def test_rel_001_circuit_breaker_trips_open():
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout_sec=30)

    def failing_func():
        raise Exception("AI provider API 503")

    def fallback_func():
        return "DEGRADED_MODE_FALLBACK"

    # 1st call fails
    res1 = cb.execute(failing_func, fallback_func)
    assert res1 == "DEGRADED_MODE_FALLBACK"
    assert cb.state == "CLOSED"

    # 2nd call fails -> Trips OPEN
    res2 = cb.execute(failing_func, fallback_func)
    assert res2 == "DEGRADED_MODE_FALLBACK"
    assert cb.state == "OPEN"

def test_rel_002_dead_letter_queue_quarantine_and_replay():
    record = dlq_manager.quarantine_failed_job("job_ocr_99", "ingestion_worker", "s3://bucket/pdf_99.pdf", "PDF corrupt", 3)
    assert record["job_id"] == "job_ocr_99"
    assert record["status"] == "QUARANTINED"

    replay_res = dlq_manager.replay_job("job_ocr_99")
    assert replay_res["status"] == "SUCCESS"
    assert replay_res["job"]["status"] == "REPLAY_QUEUED"
