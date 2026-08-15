#!/usr/bin/env python3
"""
Jurisiva-AI Automated Production Smoke Test Suite
Verifies end-to-end functionality of deployed FastAPI on Render, Vercel frontend, and Supabase integration.
Usage:
    python scripts/smoke-test.py --api-url https://api.jurisiva.ai
"""

import sys
import argparse
import time
import requests

def run_smoke_tests(api_url: str) -> bool:
    print("=" * 70)
    print(f"JURISIVA-AI PRODUCTION SMOKE TEST SUITE")
    print(f"Target API Endpoint: {api_url}")
    print("=" * 70)

    session = requests.Session()
    tests_passed = 0
    total_tests = 0

    def assert_test(name: str, passed: bool, detail: str = ""):
        nonlocal tests_passed, total_tests
        total_tests += 1
        if passed:
            tests_passed += 1
            print(f" [PASS] {name} {detail}")
        else:
            print(f" [FAIL] {name} {detail}")

    # 1. Health & Liveness
    try:
        r = session.get(f"{api_url}/health", timeout=10)
        data = r.json()
        assert_test("GET /health Probe", r.status_code == 200 and data.get("status") == "ok", f"-> {r.status_code}")
    except Exception as e:
        assert_test("GET /health Probe", False, f"Exception: {e}")

    # 2. Readiness Probe
    try:
        r = session.get(f"{api_url}/ready", timeout=10)
        data = r.json()
        assert_test("GET /ready Probe", r.status_code == 200 and data.get("ready") is True, f"-> {data.get('status')}")
    except Exception as e:
        assert_test("GET /ready Probe", False, f"Exception: {e}")

    # 3. Subsystem Health Checks
    for sub in ["ai", "database", "storage"]:
        try:
            r = session.get(f"{api_url}/health/{sub}", timeout=10)
            assert_test(f"GET /health/{sub}", r.status_code == 200 and r.json().get("status") == "ok")
        except Exception as e:
            assert_test(f"GET /health/{sub}", False, f"Exception: {e}")

    # 4. Create New Due Diligence Case
    test_case_id = "mat_smoke_001"
    try:
        payload = {
            "case_id": test_case_id,
            "case_name": "Production Smoke Test Matter — Sy No. 42/1",
            "property_address": "Devanahalli, Bengaluru Rural, Karnataka",
            "client_name": "State Bank of India",
            "lead_advocate": "Adv. Rajesh Sharma",
            "survey_numbers": "42/1 Hissa 2"
        }
        r = session.post(f"{api_url}/api/v1/cases", json=payload, timeout=10)
        assert_test("POST /api/v1/cases (Create Case)", r.status_code in [200, 201])
    except Exception as e:
        assert_test("POST /api/v1/cases", False, f"Exception: {e}")

    # 5. Document Ingestion & Indic OCR
    try:
        doc_payload = {
            "filename": "Sale_Deed_1985_Smoke.pdf",
            "document_type": "Registered Sale Deed",
            "content": "DEED OF ABSOLUTE SALE. Vendor: Venkatappa. Purchaser: Krishnappa. Extent: 2 Acres 24 Guntas."
        }
        r = session.post(f"{api_url}/api/v1/cases/{test_case_id}/documents/upload", json=doc_payload, timeout=10)
        assert_test("POST /api/v1/cases/{id}/documents/upload (OCR Pipeline)", r.status_code == 200)
    except Exception as e:
        assert_test("POST /api/v1/cases/{id}/documents/upload", False, f"Exception: {e}")

    # 6. Ownership Devolution & Rebuild
    try:
        r = session.get(f"{api_url}/api/v1/cases/{test_case_id}/ownership", timeout=10)
        data = r.json()
        assert_test("GET /api/v1/cases/{id}/ownership", r.status_code == 200 and "nodes" in data)

        r_rebuild = session.post(f"{api_url}/api/v1/cases/{test_case_id}/ownership/rebuild", timeout=10)
        assert_test("POST /api/v1/cases/{id}/ownership/rebuild", r_rebuild.status_code == 200)
    except Exception as e:
        assert_test("Ownership Endpoints", False, f"Exception: {e}")

    # 7. AI Analysis & Inconsistencies Matrix
    try:
        r = session.get(f"{api_url}/api/v1/cases/{test_case_id}/analysis", timeout=10)
        assert_test("GET /api/v1/cases/{id}/analysis (Grounded Findings)", r.status_code == 200)
    except Exception as e:
        assert_test("GET /api/v1/cases/{id}/analysis", False, f"Exception: {e}")

    # 8. Document Comparison Matrix
    try:
        cmp_payload = {"doc_id_1": "doc_001", "doc_id_2": "doc_004"}
        r = session.post(f"{api_url}/api/v1/cases/{test_case_id}/compare", json=cmp_payload, timeout=10)
        assert_test("POST /api/v1/cases/{id}/compare (Deed Diffing)", r.status_code == 200)
    except Exception as e:
        assert_test("POST /api/v1/cases/{id}/compare", False, f"Exception: {e}")

    # 9. Title Opinion & Due Diligence Report Compilation
    try:
        r = session.get(f"{api_url}/api/v1/cases/{test_case_id}/reports", timeout=10)
        assert_test("GET /api/v1/cases/{id}/reports (Diligence Certificate)", r.status_code == 200)
    except Exception as e:
        assert_test("GET /api/v1/cases/{id}/reports", False, f"Exception: {e}")

    # 10. Multilingual Voice Legal Assistant Turn
    try:
        voice_payload = {
            "text": "Who was the previous owner?",
            "case_id": test_case_id,
            "language": "en"
        }
        r = session.post(f"{api_url}/api/v1/voice/interact", json=voice_payload, timeout=10)
        data = r.json()
        assert_test("POST /api/v1/voice/interact (Voice Assistant)", r.status_code == 200 and "spoken_text" in data)
    except Exception as e:
        assert_test("POST /api/v1/voice/interact", False, f"Exception: {e}")

    # 11. Security Audit: Unauthenticated / Wrong Case Authorization
    try:
        r = session.get(f"{api_url}/api/v1/cases/non_existent_case_999999", timeout=10)
        assert_test("Security 404 / 403 on Invalid Case", r.status_code in [404, 403, 401])
    except Exception as e:
        assert_test("Security Isolation Check", False, f"Exception: {e}")

    print("=" * 70)
    print(f"SMOKE TEST SUMMARY: {tests_passed}/{total_tests} Tests Passed ({(tests_passed/total_tests)*100:.1f}%)")
    print("=" * 70)
    return tests_passed == total_tests

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jurisiva Production Smoke Test")
    parser.add_argument("--api-url", default="http://127.0.0.1:8000", help="Base API URL (e.g. https://api.jurisiva.ai)")
    args = parser.parse_args()

    success = run_smoke_tests(args.api_url)
    sys.exit(0 if success else 1)
