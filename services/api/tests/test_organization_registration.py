# Automated tests for Enterprise Company & Law Firm Registration

import pytest
from app.organization_service import org_service
from app.main import backend_server

def test_register_organization_service():
    payload = {
        "company_name": "Trilegal Chambers & Partners",
        "first_name": "Aditya",
        "last_name": "Verma",
        "email": "aditya.verma@trilegal.com",
        "job_title": "Partner — Real Estate Practice",
        "phone": "+91 98110 99887",
        "org_type": "Top-Tier Law Firm (Full Service)",
        "jurisdiction": "Delhi NCR (Supreme Court & High Court)",
        "marketing_consent": True
    }
    
    reg = org_service.register_organization(payload)
    assert reg["registration_id"].startswith("reg_")
    assert reg["org_id"].startswith("org_")
    assert reg["company_name"] == "Trilegal Chambers & Partners"
    assert reg["status"] == "PENDING_VERIFICATION"

def test_enterprise_registration_api_endpoint():
    payload = {
        "company_name": "Prestige Estates Projects Ltd",
        "first_name": "Kavitha",
        "last_name": "Nair",
        "email": "kavitha.nair@prestigeconstructions.com",
        "job_title": "General Counsel & Head of Land Title",
        "phone": "+91 99001 55443",
        "org_type": "Real Estate Developer / Infrastructure Corp",
        "jurisdiction": "Karnataka (Bengaluru & High Court)",
        "marketing_consent": True
    }
    
    res = backend_server.handle_request("/api/v1/enterprise/register", "POST", body=payload)
    assert res["status"] == "200 OK"
    data = res["data"]
    assert data["company_name"] == "Prestige Estates Projects Ltd"
    assert data["email"] == "kavitha.nair@prestigeconstructions.com"
    
    # Verify retrieval
    list_res = backend_server.handle_request("/api/v1/enterprise/registrations", "GET")
    assert list_res["status"] == "200 OK"
    companies = [r["company_name"] for r in list_res["data"]]
    assert "Prestige Estates Projects Ltd" in companies
