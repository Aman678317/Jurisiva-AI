# Post-Production Evolution & Experimentation Test Suite

import pytest
from app.growth.feedback_collector import feedback_collector
from app.growth.experiment_gate import experiment_gate

def test_evo_001_record_advocate_feedback():
    res = feedback_collector.record_feedback("org_001", "usr_001", "run_999", "POOR", "Citation linked page 3 instead of page 4", True)
    assert res["feedback_id"] is not None
    assert res["is_citation_error"] is True
    assert res["regression_fixture_status"] == "QUEUED_FOR_REGRESSION_TEST"

def test_evo_002_canary_cohort_routing():
    assert experiment_gate.should_apply_variant("exp_fast_reranker", 5) is True
    assert experiment_gate.should_apply_variant("exp_fast_reranker", 15) is False

def test_evo_003_safety_threshold_breach_rollback():
    rolled_back = experiment_gate.trigger_rollback_if_unsafe("exp_fast_reranker", 0.95)
    assert rolled_back is True
    assert experiment_gate.should_apply_variant("exp_fast_reranker", 5) is False
