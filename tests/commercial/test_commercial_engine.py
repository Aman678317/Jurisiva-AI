# Sales Pipeline & Commercial Engine Test Suite

import pytest
from app.commercial.pipeline_engine import pipeline_engine

def test_cmr_001_create_and_advance_opportunity():
    opp = pipeline_engine.create_opportunity("Trilegal Pune Practice", 900000, "LEAD")
    assert opp["opp_id"] is not None
    assert opp["stage"] == "LEAD"

    advanced = pipeline_engine.advance_stage(opp["opp_id"], "PILOT")
    assert advanced["status"] == "SUCCESS"
    assert advanced["opportunity"]["stage"] == "PILOT"

def test_cmr_002_reject_invalid_stage():
    opp = pipeline_engine.create_opportunity("Unqualified Prospect", 100000, "LEAD")
    invalid_res = pipeline_engine.advance_stage(opp["opp_id"], "MAGIC_STAGE")
    assert invalid_res["status"] == "INVALID_STAGE"
