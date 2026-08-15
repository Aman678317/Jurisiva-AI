# Research Agent Planner
# Formulates structured research plans, sub-tasks, and jurisdiction scoping.

import re
from typing import Dict, List, Any, Optional

class ResearchPlan:
    def __init__(
        self,
        query: str,
        mode: str,
        intent: str,
        jurisdiction: Dict[str, str],
        sub_tasks: List[str],
        required_tools: List[str]
    ):
        self.query = query
        self.mode = mode
        self.intent = intent
        self.jurisdiction = jurisdiction
        self.sub_tasks = sub_tasks
        self.required_tools = required_tools

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "mode": self.mode,
            "intent": self.intent,
            "jurisdiction": self.jurisdiction,
            "sub_tasks": self.sub_tasks,
            "required_tools": self.required_tools
        }


class ResearchPlanner:
    """Understands user queries and generates execution research plans."""

    def plan_research(
        self,
        query: str,
        mode: Optional[str] = None,
        case_context: Optional[Dict[str, Any]] = None
    ) -> ResearchPlan:
        q_lower = query.lower()
        context = case_context or {}

        # 1. Infer Research Mode if not explicitly provided
        selected_mode = mode or "FULL_DUE_DILIGENCE"
        if not mode:
            if any(k in q_lower for k in ["law", "act", "judgment", "case", "precedent", "statute", "section"]):
                selected_mode = "LEGAL_RESEARCH"
            elif any(k in q_lower for k in ["compare", "difference", "diff", "versus", "vs"]):
                selected_mode = "DOCUMENT_COMPARISON"
            elif any(k in q_lower for k in ["owner", "ownership", "title holder", "devolution", "chain"]):
                selected_mode = "OWNERSHIP_RESEARCH"
            elif any(k in q_lower for k in ["risk", "defect", "mismatch", "deficit", "mortgage", "sarfaesi", "gap"]):
                selected_mode = "RISK_INVESTIGATION"
            elif any(k in q_lower for k in ["survey", "extent", "area", "boundary", "acre", "gunta"]):
                selected_mode = "PROPERTY_RESEARCH"
            elif any(k in q_lower for k in ["document", "file", "ocr", "extract", "page"]):
                selected_mode = "CASE_DOCUMENTS"

        # 2. Classify Intent
        intent = "GENERAL_INVESTIGATION"
        if "owner" in q_lower or "ownership" in q_lower:
            intent = "OWNERSHIP_VERIFICATION"
        elif "survey" in q_lower or "extent" in q_lower or "area" in q_lower or "deficit" in q_lower:
            intent = "EXTENT_AND_BOUNDARY_AUDIT"
        elif "mortgage" in q_lower or "loan" in q_lower or "encumbrance" in q_lower or "sarfaesi" in q_lower:
            intent = "ENCUMBRANCE_AND_CHARGE_AUDIT"
        elif "missing" in q_lower or "gap" in q_lower:
            intent = "DOCUMENT_COMPLETENESS_CHECK"
        elif "compare" in q_lower:
            intent = "DEED_COMPARISON"
        elif "law" in q_lower or "judgment" in q_lower:
            intent = "STATUTE_AND_PRECEDENT_RESEARCH"

        # 3. Extract Jurisdiction Metadata
        jurisdiction = {
            "country": "India",
            "state": context.get("state", "Karnataka"),
            "district": context.get("district", "Bengaluru Rural"),
            "taluk": context.get("taluk", "Devanahalli"),
            "hobli": context.get("hobli", "Kasaba Hobli"),
            "village": context.get("village", "Devanahalli"),
            "survey_no": context.get("survey_no", "42/1 Hissa 2"),
            "sro": context.get("sro", "SRO Devanahalli")
        }

        # Override from query if specified
        if "maharashtra" in q_lower or "mumbai" in q_lower or "pune" in q_lower:
            jurisdiction["state"] = "Maharashtra"
        elif "tamil nadu" in q_lower or "chennai" in q_lower:
            jurisdiction["state"] = "Tamil Nadu"

        # 4. Formulate Sub-Tasks
        sub_tasks = []
        required_tools = ["retrieval", "evidence_extractor"]

        if selected_mode in ["OWNERSHIP_RESEARCH", "FULL_DUE_DILIGENCE"]:
            sub_tasks.append("Trace 30-year devolution of title from earliest parent deed to present date")
            sub_tasks.append("Verify seller title competence, execution recitals, and registration endorsements")
            required_tools.append("ownership_builder")

        if selected_mode in ["PROPERTY_RESEARCH", "DOCUMENT_COMPARISON", "FULL_DUE_DILIGENCE", "RISK_INVESTIGATION"]:
            sub_tasks.append("Compare recorded property extent and schedule boundaries across all conveyances")
            sub_tasks.append("Check for unrectified extent deficit, phodi durasti, or boundary shifts")
            required_tools.append("conflict_detector")

        if selected_mode in ["RISK_INVESTIGATION", "FULL_DUE_DILIGENCE"]:
            sub_tasks.append("Inspect SRO Book 1 encumbrance certificates and banking mortgage charges")
            sub_tasks.append("Identify missing intermediate deeds, NOCs, or revenue mutation entries")
            required_tools.append("risk_evaluator")

        if selected_mode in ["LEGAL_RESEARCH", "FULL_DUE_DILIGENCE"]:
            sub_tasks.append("Retrieve applicable statutory provisions from State Land Revenue Act & Central Acts")
            sub_tasks.append("Retrieve binding Supreme Court & High Court judicial precedents")
            required_tools.extend(["external_research", "source_validator"])

        return ResearchPlan(
            query=query,
            mode=selected_mode,
            intent=intent,
            jurisdiction=jurisdiction,
            sub_tasks=sub_tasks,
            required_tools=required_tools
        )

research_planner = ResearchPlanner()
