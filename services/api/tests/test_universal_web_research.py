# Automated Test Suite for Universal Web & Browser Research Agent
# Tests Browser Security, Structured Page Reader, Web Search Provider, and Agentic Research Loop

import pytest
import os
import sys

api_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

from app.research.browser_security import browser_security
from app.research.page_reader import page_reader
from app.research.browser_service import browser_service
from app.research.search_provider import search_provider
from app.research.research_agent import universal_research_agent
from app.research.research_routes import research_controller

# 1. Browser Security & SSRF Protection Tests
def test_browser_security_ssrf():
    # Valid Public URLs
    is_safe, clean_url = browser_security.validate_url("https://main.sci.gov.in/judgment/2023-INSC-891")
    assert is_safe is True
    assert clean_url.startswith("https://")

    # Localhost Block
    is_safe, err = browser_security.validate_url("http://localhost:8000/admin")
    assert is_safe is False
    assert "Blocked private/local target" in err

    # Loopback Block
    is_safe, err = browser_security.validate_url("http://127.0.0.1:3000")
    assert is_safe is False

    # Cloud Metadata Block
    is_safe, err = browser_security.validate_url("http://169.254.169.254/latest/meta-data")
    assert is_safe is False

    # Private IP Network Block
    is_safe, err = browser_security.validate_url("http://192.168.1.1/router")
    assert is_safe is False

    # Blocked Scheme
    is_safe, err = browser_security.validate_url("file:///etc/passwd")
    assert is_safe is False

# 2. Structured Page Reader Tests
def test_page_reader_structured_extraction():
    raw_html = """
    <html>
      <head><title>Supreme Court of India — 2023 INSC 891</title></head>
      <body>
        <h1>Civil Appellate Jurisdiction</h1>
        <h2>Anandram vs Land Acquisition Officer</h2>
        <p>This appeal arises out of the judgment in Survey No. 42/1 Hissa 2.</p>
        <p>The Supreme Court in 2023 INSC 891 held that revenue survey durasti Akarband holds precedence.</p>
        <table>
          <tr><th>Survey</th><th>Extent</th></tr>
          <tr><td>42/1</td><td>2A 24G</td></tr>
        </table>
        <a href="https://sci.gov.in/order.pdf">Download Judgment PDF</a>
        <a href="https://landrecords.karnataka.gov.in">Bhoomi Revenue Link</a>
      </body>
    </html>
    """
    struct = page_reader.parse_html_content(raw_html, "https://main.sci.gov.in/judgment/2023-INSC-891")
    assert struct["title"] == "Supreme Court of India — 2023 INSC 891"
    assert len(struct["headings"]) == 2
    assert len(struct["paragraphs"]) >= 2
    assert len(struct["tables"]) == 1
    assert len(struct["pdf_documents"]) == 1
    assert "2023 INSC 891" in struct["extracted_citations"]

# 3. Browser Service Controlled Navigation Tests
def test_browser_service_navigation():
    # Test safe controlled open with trace recording
    res = browser_service.open_url("https://main.sci.gov.in/judgment/2023-INSC-891", session_id="test_sess_001")
    assert res["status"] == "SUCCESS"
    assert "content_structure" in res

    traces = browser_service.get_session_trace("test_sess_001")
    assert len(traces) >= 1
    assert traces[0]["status"] == "SUCCESS"

    # Test SSRF block in browser service
    res_blocked = browser_service.open_url("http://127.0.0.1:8080/internal")
    assert res_blocked["status"] == "BLOCKED"

# 4. Web Search Provider Tests
def test_web_search_provider():
    results = search_provider.search_web("Survey number discrepancies and Akarband", mode="LEGAL")
    assert len(results) >= 2
    assert any("2023 INSC 891" in r["title"] for r in results)
    assert any(r["authority_score"] == 1.00 for r in results)

    # Company research query
    company_results = search_provider.search_web("MCA company master data", mode="WEB")
    assert len(company_results) >= 1
    assert any("MCA21" in r["title"] for r in company_results)

# 5. Universal Research Agent End-to-End Investigation Tests
def test_universal_research_agent_question():
    session = universal_research_agent.start_investigation(
        query_or_url="Survey number discrepancies and Akarband durasti precedence",
        mode="CASE",
        case_id="mat_001"
    )
    assert session["status"] == "COMPLETED"
    assert len(session["sources"]) >= 2
    assert len(session["citations"]) >= 2
    assert "answer" in session
    assert session["answer"]["summary"] is not None
    assert "comparison_matrix" in session

    # Test Save to Case
    saved = universal_research_agent.save_research_to_case(session["session_id"], "mat_001")
    assert saved is True
    history = universal_research_agent.get_case_research_history("mat_001")
    assert len(history) >= 1

def test_universal_research_agent_direct_url():
    session_url = universal_research_agent.start_investigation(
        query_or_url="https://main.sci.gov.in/judgment/2023-INSC-891",
        mode="WEB"
    )
    assert session_url["status"] == "COMPLETED"
    assert len(session_url["sources"]) == 1
    assert len(session_url["citations"]) >= 1

# 6. Research Controller API Tests
def test_research_controller_endpoints():
    res_query = research_controller.start_research({
        "query": "SARFAESI mortgage undischarged enforceability",
        "mode": "LEGAL",
        "case_id": "mat_001"
    })
    assert res_query["status"] == "SUCCESS"
    session_id = res_query["data"]["session_id"]

    res_get = research_controller.get_session_details(session_id)
    assert res_get["status"] == "SUCCESS"

    res_save = research_controller.save_session_to_case(session_id, {"case_id": "mat_001"})
    assert res_save["status"] == "SUCCESS"
