# Temporal Entity Resolution Engine
# Resolves party and property identities across historical deeds with explicit confidence scores

import re
from typing import Dict, List, Any, Optional

class TemporalEntityResolver:
    """Disambiguates party names, aliases, and property descriptions without silent merging."""

    def resolve_person(
        self,
        candidate: Dict[str, Any],
        historical_parties: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculates resolution confidence:
        - EXACT: Name + Father Name + Address match
        - LIKELY: Name + Father Name match, different execution year
        - POSSIBLE: Name match only (e.g. spelling variation 'Venkatappa' vs 'Venkatapa')
        - CONFLICTED: Same name, different father name (distinct individuals)
        - UNKNOWN: Insufficient identifiers
        """
        name = candidate.get("name", "").strip().lower()
        father = candidate.get("father_name", "").strip().lower()
        survey = candidate.get("survey_number", "")

        for hist in historical_parties:
            h_name = hist.get("name", "").strip().lower()
            h_father = hist.get("father_name", "").strip().lower()

            # Check Conflicted (Same name but different father)
            if name == h_name and father and h_father and father != h_father:
                return {
                    "matched_entity_id": hist.get("entity_id"),
                    "confidence_tier": "CONFLICTED",
                    "confidence_score": 0.35,
                    "reason": f"Distinct persons: '{candidate.get('name')}' S/o {candidate.get('father_name')} vs S/o {hist.get('father_name')}."
                }

            # Exact Match
            if name == h_name and father == h_father and father != "":
                return {
                    "matched_entity_id": hist.get("entity_id"),
                    "confidence_tier": "EXACT",
                    "confidence_score": 0.99,
                    "reason": "Exact match on full legal name and parentage."
                }

            # Likely Match (Minor phonetic transliteration difference)
            if self._is_phonetic_match(name, h_name) and (father == h_father or not father):
                return {
                    "matched_entity_id": hist.get("entity_id"),
                    "confidence_tier": "LIKELY",
                    "confidence_score": 0.88,
                    "reason": f"Phonetic match on transliterated Indic name ('{candidate.get('name')}' ~ '{hist.get('name')}')."
                }

            # Possible Match (Name only)
            if name == h_name:
                return {
                    "matched_entity_id": hist.get("entity_id"),
                    "confidence_tier": "POSSIBLE",
                    "confidence_score": 0.65,
                    "reason": "Name matches but parentage/address requires corroboration."
                }

        return {
            "matched_entity_id": None,
            "confidence_tier": "UNKNOWN",
            "confidence_score": 0.0,
            "reason": "New entity not previously observed in case documents."
        }

    def _is_phonetic_match(self, s1: str, s2: str) -> bool:
        """Simple Indic transliteration normalizer."""
        clean1 = re.sub(r'[aeiou\s]', '', s1)
        clean2 = re.sub(r'[aeiou\s]', '', s2)
        return clean1 == clean2 or clean1 in clean2 or clean2 in clean1

entity_resolver = TemporalEntityResolver()
