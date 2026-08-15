# Research Route Handlers & Controllers

from typing import Dict, Any, Optional
from app.research.research_agent import universal_research_agent
from app.research.browser_service import browser_service

class ResearchController:
    """REST API controller for Universal Web and Browser Research Agent."""

    @staticmethod
    def start_research(payload: Dict[str, Any]) -> Dict[str, Any]:
        query = payload.get("query") or payload.get("question") or payload.get("url") or "Survey number discrepancies"
        mode = payload.get("mode", "LEGAL")
        case_id = payload.get("case_id", "mat_001")
        org_id = payload.get("org_id", "org_001")
        user_id = payload.get("user_id", "usr_rajesh")

        session = universal_research_agent.start_investigation(
            query_or_url=query,
            mode=mode,
            case_id=case_id,
            org_id=org_id,
            user_id=user_id
        )
        return {"status": "SUCCESS", "data": session}

    @staticmethod
    def inspect_url(payload: Dict[str, Any]) -> Dict[str, Any]:
        url = payload.get("url", "")
        session = universal_research_agent.start_investigation(
            query_or_url=url,
            mode="WEB"
        )
        return {"status": "SUCCESS", "data": session}

    @staticmethod
    def get_session_details(session_id: str) -> Dict[str, Any]:
        sess = universal_research_agent.get_session(session_id)
        if not sess:
            return {"status": "NOT_FOUND", "error": f"Research session '{session_id}' not found."}
        return {"status": "SUCCESS", "data": sess}

    @staticmethod
    def save_session_to_case(session_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        case_id = payload.get("case_id", "mat_001")
        success = universal_research_agent.save_research_to_case(session_id, case_id)
        return {
            "status": "SUCCESS" if success else "FAILED",
            "message": f"Research session '{session_id}' attached to Matter '{case_id}'."
        }

    @staticmethod
    def get_case_history(case_id: str) -> Dict[str, Any]:
        history = universal_research_agent.get_case_research_history(case_id)
        return {"status": "SUCCESS", "case_id": case_id, "history": history}

research_controller = ResearchController()
