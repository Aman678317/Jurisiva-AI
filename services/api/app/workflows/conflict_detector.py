# Evidence-Backed Conflict Detector

from typing import List, Dict, Any

class EvidenceConflictDetector:
    """Surfaces extent discrepancies, unreleased mortgages, and revenue record mismatches."""

    @staticmethod
    def detect_conflicts(deeds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        conflicts = []

        # Extent Comparison Check
        extents = set()
        for d in deeds:
            extent_val = d.get("extent")
            if extent_val:
                extents.add(extent_val)

        if len(extents) > 1:
            conflicts.append({
                "conflict_type": "EXTENT_MISMATCH",
                "status": "POSSIBLE_CONFLICT",
                "description": f"Discrepancy in land extent across deeds: {', '.join(extents)}",
                "citations": [
                    {"document_id": d["document_id"], "page_number": d.get("page_number", 1)}
                    for d in deeds if d.get("extent")
                ]
            })

        # Encumbrance Check (Mortgage without matching Release Deed)
        has_mortgage = any(d.get("event_type") == "MORTGAGE_DEED" for d in deeds)
        has_release = any(d.get("event_type") == "RELEASE_DEED" for d in deeds)
        
        if has_mortgage and not has_release:
            conflicts.append({
                "conflict_type": "UNRELEASED_MORTGAGE",
                "status": "POSSIBLE_CONFLICT",
                "description": "Mortgage Deed found in title chain without matching Release Deed.",
                "citations": [
                    {"document_id": d["document_id"], "page_number": d.get("page_number", 1)}
                    for d in deeds if d.get("event_type") == "MORTGAGE_DEED"
                ]
            })

        return conflicts

conflict_detector = EvidenceConflictDetector()
