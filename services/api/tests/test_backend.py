# Backend Core & Security Integration Test Suite

import pytest
from app.auth import auth_engine
from app.authorization import auth_guard
from app.audit import audit_logger
from app.storage import storage_adapter
from app.jobs import job_engine
from app.main import backend_server

def test_be_001_password_hashing():
    hashed = auth_engine.hash_password("Password123!")
    assert hashed != "Password123!"
    assert auth_engine.verify_password("Password123!", hashed) is True
    assert auth_engine.verify_password("WrongPass", hashed) is False

def test_be_002_token_creation():
    token_data = auth_engine.create_token("usr_001", "org_001", "LEAD_ADVOCATE")
    verified = auth_engine.verify_token(token_data["access_token"])
    assert verified is not None
    assert verified["user_id"] == "usr_001"
    assert verified["org_id"] == "org_001"

def test_be_003_rbac_permission_matrix():
    assert auth_guard.check_permission("LEAD_ADVOCATE", "matter.create") is True
    assert auth_guard.check_permission("ASSOCIATE", "matter.create") is False
    assert auth_guard.check_permission("AUDITOR", "document.delete") is False

def test_be_004_tenant_isolation():
    is_allowed = auth_guard.verify_tenant_access("org_001", "org_002")
    assert is_allowed is False
    assert auth_guard.verify_tenant_access("org_001", "org_001") is True

def test_be_005_idor_cross_tenant_block():
    token_data = auth_engine.create_token("usr_001", "org_001", "LEAD_ADVOCATE")
    res = backend_server.handle_request(
        "/api/v1/matters/mat_001/documents",
        "POST",
        {"Authorization": token_data["access_token"]},
        {"filename": "deed.pdf", "byte_size": 1024, "mime_type": "application/pdf"},
        {"matter_org_id": "org_002"}
    )
    assert res["status"] == "403 Forbidden"
    assert res["error"]["code"] == "TENANT_ACCESS_DENIED"

def test_be_006_file_validation():
    valid_size, size_msg = storage_adapter.validate_file_metadata("large.pdf", 150 * 1024 * 1024, "application/pdf")
    assert valid_size is False
    assert "FILE_TOO_LARGE" in size_msg

    valid_mime, mime_msg = storage_adapter.validate_file_metadata("script.exe", 1024, "application/x-msdownload")
    assert valid_mime is False
    assert "UNSUPPORTED_FORMAT" in mime_msg

def test_be_007_job_state_machine_transitions():
    job = job_engine.create_job("org_001", "mat_001", "doc_001")
    assert job["status"] == "QUEUED"

    valid_trans, _ = job_engine.transition_state(job["job_id"], "VALIDATING")
    assert valid_trans is True

    invalid_trans, err = job_engine.transition_state(job["job_id"], "READY")
    assert invalid_trans is False
    assert "INVALID_TRANSITION" in err

def test_be_008_immutable_audit_logging():
    log = audit_logger.log_event("org_001", "usr_001", "Advocate Rajesh", "MATTER_CREATED", "Matter", "mat_999", "mat_999")
    assert log["action"] == "MATTER_CREATED"
    org_logs = audit_logger.get_matter_logs("org_001", "mat_999")
    assert len(org_logs) == 1
