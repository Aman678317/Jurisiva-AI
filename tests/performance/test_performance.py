# Automated Performance & Latency Benchmark Test Suite

import time
import pytest
from app.auth import auth_engine
from app.search_engine import search_engine
from app.rag_engine import rag_engine

def test_perf_001_authentication_latency():
    start = time.time()
    token_data = auth_engine.create_token("usr_001", "org_001", "LEAD_ADVOCATE")
    verified = auth_engine.verify_token(token_data["access_token"])
    duration_ms = (time.time() - start) * 1000

    assert verified is not None
    assert duration_ms < 150.0

def test_perf_002_hybrid_search_latency():
    start = time.time()
    results = search_engine.execute_hybrid_search("org_001", "mat_001", "Survey No 42/1", top_k=5)
    duration_ms = (time.time() - start) * 1000

    assert results is not None
    assert duration_ms < 600.0

def test_perf_003_rag_copilot_latency():
    start = time.time()
    res = rag_engine.query_assistant("org_001", "mat_001", "What is the extent of Survey No 42/1?")
    duration_ms = (time.time() - start) * 1000

    assert res.evidence_status == "SUPPORTED"
    assert duration_ms < 1500.0
