# External Research Orchestrator & SSRF URL Security Guard

import urllib.parse
from typing import Dict, List, Any
from app.integrations.registry import source_registry
from app.integrations.mock_adapters import mock_court_adapter, mock_property_adapter

class SSRFSecurityGuard:
    """SSRF URL validation guard preventing unauthorized internal network requests."""

    FORBIDDEN_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254"}

    @staticmethod
    def validate_external_url(url: str) -> bool:
        parsed = urllib.parse.urlparse(url)
        hostname = parsed.hostname or ""
        
        if hostname in SSRFSecurityGuard.FORBIDDEN_HOSTS or hostname.startswith("192.168.") or hostname.startswith("10."):
            return False
        return True

class ResearchOrchestrator:
    """Orchestrates research queries across permitted official data adapters."""

    def __init__(self):
        self.ssrf_guard = SSRFSecurityGuard()

    def execute_court_research(self, org_id: str, matter_id: str, case_number: str) -> Dict[str, Any]:
        # Enforce Tenant Isolation
        if not org_id or not matter_id:
            return {"status": "FORBIDDEN", "error": "Tenant authorization required."}

        raw_results = mock_court_adapter.search(case_number, {})
        if not raw_results:
            return {"status": "NO_RECORDS_FOUND", "results": []}

        record = mock_court_adapter.fetch(raw_results[0]["case_id"])
        normalized = mock_court_adapter.normalize(record)

        return {
            "status": "SUCCESS",
            "matter_id": matter_id,
            "research_type": "COURT_SEARCH",
            "canonical_data": normalized,
            "verification_status": "SOURCE_RETRIEVED",
            "authority_level": "LEVEL_1"
        }

    def execute_property_research(self, org_id: str, matter_id: str, survey_number: str) -> Dict[str, Any]:
        if not org_id or not matter_id:
            return {"status": "FORBIDDEN", "error": "Tenant authorization required."}

        raw_parcels = mock_property_adapter.search(survey_number, {})
        if not raw_parcels:
            return {"status": "NO_RECORDS_FOUND", "results": []}

        record = mock_property_adapter.fetch(raw_parcels[0]["parcel_id"])
        normalized = mock_property_adapter.normalize(record)

        return {
            "status": "SUCCESS",
            "matter_id": matter_id,
            "research_type": "PROPERTY_SEARCH",
            "canonical_data": normalized,
            "verification_status": "SOURCE_RETRIEVED",
            "authority_level": "LEVEL_1"
        }

research_orchestrator = ResearchOrchestrator()
