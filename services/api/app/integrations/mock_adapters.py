# Deterministic Mock Source Adapters for Development & Automated Testing

import time
import hashlib
from typing import Dict, List, Any
from app.integrations.adapter_base import ExternalDataSource

class MockCourtAdapter(ExternalDataSource):
    """Mock Adapter for eCourts public litigation lookup."""

    def search(self, query: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "case_id": "OS_104_2019",
                "court": "Additional Civil Judge, Devanahalli",
                "case_number": "O.S. No. 104/2019",
                "parties": "Venkatappa vs Krishnappa",
                "status": "DISPOSED",
                "date_filed": "2019-03-15",
                "source_id": "src_ecourts"
            }
        ]

    def fetch(self, record_id: str) -> Dict[str, Any]:
        return {
            "record_id": record_id,
            "order_text": "ORDER: Suit for permanent injunction dismissed as withdrawn on 12-10-2021.",
            "order_date": "2021-10-12",
            "source_id": "src_ecourts"
        }

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "canonical_type": "COURT_ORDER",
            "case_number": raw_data.get("case_number"),
            "order_text": raw_data.get("order_text"),
            "provenance": {
                "source_id": raw_data.get("source_id"),
                "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "content_hash": hashlib.sha256(str(raw_data).encode()).hexdigest()
            }
        }

    def health_check(self) -> Dict[str, Any]:
        return {"status": "HEALTHY", "adapter": "MockCourtAdapter", "latency_ms": 15}

class MockPropertyAdapter(ExternalDataSource):
    """Mock Adapter for Kaveri 2.0 / MahaBhulekh Land Record lookup."""

    def search(self, query: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "parcel_id": "KA_BLR_DEV_42_1",
                "survey_number": "42/1",
                "hissa_number": "2",
                "taluk": "Devanahalli",
                "village": "Singahalli",
                "extent": "2 Acres 24 Guntas",
                "owner_name": "Krishnappa S/o Govindappa",
                "source_id": "src_kaveri"
            }
        ]

    def fetch(self, record_id: str) -> Dict[str, Any]:
        return {
            "parcel_id": record_id,
            "rtc_extract": "RTC Form 16: Survey No. 42/1, Extent 2A 24G, Owner Krishnappa, Cultivator Owner.",
            "mutation_entry": "MR No. 14/1985-86",
            "source_id": "src_kaveri"
        }

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "canonical_type": "LAND_RECORD",
            "survey_number": raw_data.get("survey_number", "42/1"),
            "owner_name": raw_data.get("owner_name"),
            "provenance": {
                "source_id": raw_data.get("source_id"),
                "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "content_hash": hashlib.sha256(str(raw_data).encode()).hexdigest()
            }
        }

    def health_check(self) -> Dict[str, Any]:
        return {"status": "HEALTHY", "adapter": "MockPropertyAdapter", "latency_ms": 12}

mock_court_adapter = MockCourtAdapter()
mock_property_adapter = MockPropertyAdapter()
