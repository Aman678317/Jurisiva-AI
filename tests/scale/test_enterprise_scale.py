# Enterprise Scale & Governance Test Suite

import pytest
from app.scale.capacity_planner import capacity_planner
from app.scale.enterprise_governance import enterprise_governance

def test_scl_001_capacity_planner_scale_thresholds():
    scale_10x = capacity_planner.calculate_scale_capacity(10.0)
    assert scale_10x["target_api_rpm"] == 15000
    assert scale_10x["use_pgbouncer"] is True

    scale_100x = capacity_planner.calculate_scale_capacity(100.0)
    assert scale_100x["target_api_rpm"] == 150000
    assert scale_100x["recommended_db_connections"] == 200

def test_scl_002_enterprise_data_export_permissions():
    valid_export = enterprise_governance.generate_organization_export("org_001", "ADMIN")
    assert valid_export["status"] == "SUCCESS"
    assert valid_export["export_format"] == "JSON_ZIP"

    invalid_export = enterprise_governance.generate_organization_export("org_001", "ASSOCIATE")
    assert invalid_export["status"] == "FORBIDDEN"

def test_scl_003_scim_deprovisioning():
    assert enterprise_governance.verify_scim_deprovisioning("DISABLED") is True
    assert enterprise_governance.verify_scim_deprovisioning("SUSPENDED") is True
    assert enterprise_governance.verify_scim_deprovisioning("ACTIVE") is False
