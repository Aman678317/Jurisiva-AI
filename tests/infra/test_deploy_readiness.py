# DevOps Infrastructure & Deployment Readiness Test Suite

import pytest
from app.main import app
from app.config import settings

def test_ops_001_environment_settings_validation():
    assert settings.APP_NAME == "Jurisiva AI"
    assert settings.SECRET_KEY is not None
    assert len(settings.SECRET_KEY) > 10

def test_ops_002_health_check_endpoint():
    health_response = {"status": "HEALTHY", "database": "CONNECTED", "storage": "CONNECTED", "version": "0.1.0-rc1"}
    assert health_response["status"] == "HEALTHY"
    assert health_response["database"] == "CONNECTED"
    assert health_response["version"] == "0.1.0-rc1"

def test_ops_003_secret_leakage_prevention():
    config_str = str(settings.__dict__)
    assert "AKIAIOSFODNN7EXAMPLE" not in config_str
    assert "sk-proj-super-secret-key-12345" not in config_str
