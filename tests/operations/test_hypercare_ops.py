# Operations & Incident Management Test Suite

import pytest
from app.operations.ai_kill_switch import ai_kill_switch
from app.operations.incident_command import incident_command
from app.operations.telemetry_dashboard import telemetry_dashboard

def test_ops_101_ai_kill_switch():
    assert ai_kill_switch.is_feature_enabled("AI_COPILOT_ENABLED") is True

    disable_res = ai_kill_switch.disable_feature("AI_COPILOT_ENABLED", "Provider Outage", "usr_admin")
    assert disable_res["status"] == "DISABLED"
    assert ai_kill_switch.is_feature_enabled("AI_COPILOT_ENABLED") is False

    ai_kill_switch.enable_feature("AI_COPILOT_ENABLED", "usr_admin")
    assert ai_kill_switch.is_feature_enabled("AI_COPILOT_ENABLED") is True

def test_ops_102_incident_command_lifecycle():
    inc = incident_command.declare_incident("SEV-1", "Mock Test Incident", "usr_admin")
    assert inc["status"] == "DECLARED"
    assert inc["severity"] == "SEV-1"

    resolved = incident_command.resolve_incident(inc["incident_id"], "Patch Deployed")
    assert resolved["status"] == "RESOLVED"
    assert resolved["root_cause"] == "Patch Deployed"

def test_ops_103_telemetry_metrics():
    metrics = telemetry_dashboard.get_live_metrics()
    assert metrics["service_availability"] == 1.00
    assert metrics["auth_p95_ms"] < 150
    assert metrics["rag_p95_ms"] < 1500
    assert metrics["unit_cost_inr"] < 120.0
