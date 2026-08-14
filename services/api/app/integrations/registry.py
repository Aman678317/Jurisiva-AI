# India Data Source Registry & Authority Engine

from typing import Dict, List, Optional

class SourceRegistry:
    """Central registry for official & public India legal & property data sources."""

    def __init__(self):
        self._sources: Dict[str, Dict] = {
            "src_ecourts": {
                "source_id": "src_ecourts",
                "name": "eCourts Services India",
                "authority_level": "LEVEL_1",
                "jurisdiction": "IN-NATIONAL",
                "access_method": "PUBLIC_WEB_PORTAL",
                "freshness_window_hours": 24,
                "enabled": True,
                "is_official": True
            },
            "src_kaveri": {
                "source_id": "src_kaveri",
                "name": "Kaveri 2.0 Karnataka Land Records",
                "authority_level": "LEVEL_1",
                "jurisdiction": "IN-KA",
                "access_method": "PUBLIC_WEB_PORTAL",
                "freshness_window_hours": 24,
                "enabled": True,
                "is_official": True
            },
            "src_mahabhulekh": {
                "source_id": "src_mahabhulekh",
                "name": "MahaBhulekh Maharashtra 7/12 Extract",
                "authority_level": "LEVEL_1",
                "jurisdiction": "IN-MH",
                "access_method": "PUBLIC_WEB_PORTAL",
                "freshness_window_hours": 24,
                "enabled": True,
                "is_official": True
            }
        }

    def get_source(self, source_id: str) -> Optional[Dict]:
        return self._sources.get(source_id)

    def list_sources(self, jurisdiction: Optional[str] = None) -> List[Dict]:
        if not jurisdiction:
            return list(self._sources.values())
        return [s for s in self._sources.values() if s["jurisdiction"] == jurisdiction or s["jurisdiction"] == "IN-NATIONAL"]

source_registry = SourceRegistry()
