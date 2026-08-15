# Research Domain Data Models & Schemas

import time
from typing import Dict, List, Any, Optional

class ResearchModels:
    """Helper factories for standardized Research Session objects."""

    @staticmethod
    def create_session(
        session_id: str,
        user_id: str,
        org_id: str,
        case_id: str,
        query: str,
        mode: str = "LEGAL"
    ) -> Dict[str, Any]:
        return {
            "session_id": session_id,
            "user_id": user_id,
            "org_id": org_id,
            "case_id": case_id,
            "query": query,
            "mode": mode,
            "status": "QUEUED",
            "progress_steps": [],
            "sources": [],
            "evidence": [],
            "citations": [],
            "comparison_matrix": {},
            "answer": None,
            "started_at": time.time(),
            "completed_at": None,
            "duration_seconds": None
        }

    @staticmethod
    def create_citation(
        citation_id: str,
        url: str,
        title: str,
        publisher: str,
        quoted_evidence: str,
        source_type: str = "Official Court Judgment",
        confidence: float = 0.99
    ) -> Dict[str, Any]:
        return {
            "citation_id": citation_id,
            "url": url,
            "title": title,
            "publisher": publisher,
            "retrieved_at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "quoted_evidence": quoted_evidence,
            "source_type": source_type,
            "confidence": confidence,
            "verification_status": "VERIFIED"
        }
