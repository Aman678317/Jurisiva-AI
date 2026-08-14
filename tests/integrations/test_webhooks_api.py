# Webhooks Engine & Public API Scoping Test Suite

import json
import time
import pytest
from app.integrations.webhook_engine import webhook_engine
from app.integrations.api_key_manager import api_key_manager

def test_int_001_hmac_webhook_signature():
    secret = "whsec_test_secret_123"
    payload = json.dumps({"event": "matter.created", "matter_id": "mat_001"})
    sig_headers = webhook_engine.generate_signature(secret, payload)

    assert "X-Jurisiva-Signature" in sig_headers
    is_valid = webhook_engine.verify_signature(secret, payload, sig_headers["X-Jurisiva-Signature"])
    assert is_valid is True

def test_int_002_replay_attack_rejected():
    secret = "whsec_test_secret_123"
    payload = json.dumps({"event": "matter.created"})
    old_timestamp = int(time.time()) - 600  # 10 minutes ago
    sig_headers = webhook_engine.generate_signature(secret, payload, old_timestamp)

    is_valid = webhook_engine.verify_signature(secret, payload, sig_headers["X-Jurisiva-Signature"])
    assert is_valid is False

def test_int_003_scoped_api_key():
    key_info = api_key_manager.issue_api_key("org_001", "Matter Sync Key", ["matter:read"])
    assert "jur_live_" in key_info["raw_key"]

    valid_auth = api_key_manager.verify_api_key(key_info["raw_key"], "matter:read")
    assert valid_auth["status"] == "AUTHORIZED"

    missing_scope_auth = api_key_manager.verify_api_key(key_info["raw_key"], "export:create")
    assert missing_scope_auth["status"] == "FORBIDDEN"
