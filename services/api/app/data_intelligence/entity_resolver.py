# Evidence-Aware Entity Resolver & Match Confidence Engine

import time
from typing import Dict, List, Any, Optional

class EntityResolver:
    """Resolves party and property entities with evidence-based match confidence states (EXACT, LIKELY, POSSIBLE, CONFLICTED, UNKNOWN)."""

    def resolve_entity_match(self, record_a: Dict[str, Any], record_b: Dict[str, Any]) -> Dict[str, Any]:
        # Check unique identifier match
        if record_a.get("pan_or_survey") and record_a.get("pan_or_survey") == record_b.get("pan_or_survey"):
            confidence = "EXACT"
            requires_review = False
        elif record_a.get("name") == record_b.get("name") and record_a.get("address") == record_b.get("address"):
            confidence = "LIKELY"
            requires_review = True
        elif record_a.get("name") == record_b.get("name"):
            confidence = "POSSIBLE"
            requires_review = True
        elif record_a.get("conflicting_record"):
            confidence = "CONFLICTED"
            requires_review = True
        else:
            confidence = "UNKNOWN"
            requires_review = True

        return {
            "entity_a_id": record_a.get("entity_id"),
            "entity_b_id": record_b.get("entity_id"),
            "confidence_state": confidence,
            "requires_human_review": requires_review,
            "evidence_refs": record_a.get("evidence_refs", []) + record_b.get("evidence_refs", []),
            "resolved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

entity_resolver = EntityResolver()
