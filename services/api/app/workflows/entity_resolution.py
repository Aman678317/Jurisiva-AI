# Cautious Entity Resolution Engine

from typing import Dict, Any

class CautiousEntityResolver:
    """Matches entity candidates without silently merging ambiguous name matches."""

    @staticmethod
    def resolve_entity(entity_a: Dict[str, Any], entity_b: Dict[str, Any]) -> Dict[str, Any]:
        name_a = entity_a.get("name", "").strip().lower()
        name_b = entity_b.get("name", "").strip().lower()
        addr_a = entity_a.get("address", "").strip().lower()
        addr_b = entity_b.get("address", "").strip().lower()

        if name_a == name_b and addr_a == addr_b and name_a:
            return {"status": "MATCH", "confidence": 0.99, "action": "AUTO_LINK"}
        
        if name_a == name_b:
            return {"status": "POSSIBLE_MATCH", "confidence": 0.70, "action": "FLAG_FOR_REVIEW"}

        return {"status": "NO_MATCH", "confidence": 0.10, "action": "SEPARATE_ENTITIES"}

entity_resolver = CautiousEntityResolver()
