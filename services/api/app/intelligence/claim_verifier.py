# Claim Verification & Contradiction Intelligence Engine

from typing import Dict, List, Any

class ClaimVerifier:
    """Classifies claims into SUPPORTED, CONTRADICTED, UNVERIFIED, or REVIEW_REQUIRED."""

    @staticmethod
    def verify_claim(claim_text: str, retrieved_evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not retrieved_evidence:
            return {
                "claim": claim_text,
                "status": "UNVERIFIED",
                "evidence_count": 0,
                "reason": "No retrieved document evidence found to support claim."
            }

        # Check for contradicting extent or party facts
        has_contradiction = any(e.get("status") == "POSSIBLE_CONFLICT" for e in retrieved_evidence)
        if has_contradiction:
            return {
                "claim": claim_text,
                "status": "CONTRADICTED",
                "evidence_count": len(retrieved_evidence),
                "reason": "Retrieved evidence presents conflicting extent or owner records."
            }

        return {
            "claim": claim_text,
            "status": "SUPPORTED",
            "evidence_count": len(retrieved_evidence),
            "citations": [e.get("citation") for e in retrieved_evidence if "citation" in e]
        }

claim_verifier = ClaimVerifier()
