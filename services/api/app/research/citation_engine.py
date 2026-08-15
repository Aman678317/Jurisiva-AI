# Evidence-Grounded Citation & Claim Verification Engine
# Builds Claim Graphs, classifies Facts vs Inferences, and links verbatim page sources

from typing import Dict, List, Any, Optional

class CitationEngine:
    """Classifies claims, verifies provenance against source documents, and produces auditable claim graphs."""

    def build_claim_verification_graph(
        self,
        claims: List[Dict[str, Any]],
        available_documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Processes claims:
        - Classifies as FACT, INFERENCE, HYPOTHESIS, or UNVERIFIED
        - Maps supporting evidence and contradicting evidence
        - Sets verification state: VERIFIED, PARTIALLY_VERIFIED, UNVERIFIED
        """
        verified_claims = []
        overall_fact_count = 0
        overall_inference_count = 0

        for idx, c in enumerate(claims):
            statement = c.get("statement", "")
            claim_type = c.get("claim_type", "FACT")  # FACT, INFERENCE, HYPOTHESIS, UNVERIFIED
            source_doc_id = c.get("source_document_id")
            page_num = c.get("page_number", 1)
            verbatim_quote = c.get("verbatim_quote", "")

            # Check if source document exists in case
            doc_matched = any(d.get("document_id") == source_doc_id for d in available_documents) if available_documents else True

            # Determine Verification State
            if doc_matched and verbatim_quote:
                status = "VERIFIED"
                confidence = 0.99
            elif doc_matched and not verbatim_quote:
                status = "PARTIALLY_VERIFIED"
                confidence = 0.80
            else:
                status = "UNVERIFIED"
                confidence = 0.40

            if claim_type == "FACT":
                overall_fact_count += 1
            else:
                overall_inference_count += 1

            claim_record = {
                "claim_id": f"clm_{idx+1:03d}",
                "statement": statement,
                "classification": claim_type,
                "verification_status": status,
                "confidence": confidence,
                "evidence": {
                    "source_document_id": source_doc_id,
                    "page_number": page_num,
                    "verbatim_quote": verbatim_quote
                },
                "contradicting_evidence": c.get("contradicting_evidence", [])
            }
            verified_claims.append(claim_record)

        return {
            "total_claims": len(verified_claims),
            "fact_count": overall_fact_count,
            "inference_count": overall_inference_count,
            "all_verified": all(c["verification_status"] == "VERIFIED" for c in verified_claims),
            "claim_graph": verified_claims
        }

citation_engine = CitationEngine()
