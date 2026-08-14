# Enterprise Workspaces & Collaboration Test Suite

import time
import pytest
from app.enterprise.workspace_manager import workspace_manager

def test_wks_001_add_collaboration_comment():
    res = workspace_manager.add_matter_comment("org_001", "mat_001", "usr_001", "ASSOCIATE", "Verified encumbrance certificate.")
    assert res["status"] == "SUCCESS"
    assert "Verified" in res["comment"]["text"]

def test_wks_002_restricted_matter_access():
    denied = workspace_manager.add_matter_comment("org_001", "mat_restricted", "usr_002", "ASSOCIATE", "Attempt comment", is_restricted=True)
    assert denied["status"] == "FORBIDDEN"

    allowed = workspace_manager.add_matter_comment("org_001", "mat_restricted", "usr_owner", "OWNER", "Owner comment", is_restricted=True)
    assert allowed["status"] == "SUCCESS"

def test_wks_003_support_breakglass_session():
    sess = workspace_manager.initiate_support_breakglass("op_sre_01", "org_001", "TICK-999", "Investigating OCR timeout")
    assert sess["session_id"] is not None
    assert sess["status"] == "ACTIVE_AUDITED"
    assert sess["expires_at"] > time.time()
