# Specialized Domain Agents for Legal & Property Intelligence
# Defines clear responsibilities, allowed tools, and execution pipelines

from typing import Dict, List, Any, Optional
from app.agents.agent_runtime import agent_runtime

class BaseAgent:
    """Base class for all specialized legal domain agents."""
    def __init__(self, name: str, allowed_tools: List[str]):
        self.name = name
        self.allowed_tools = allowed_tools

    def run(self, org_id: str, matter_id: str, user_id: str, goal: str, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        return agent_runtime.execute_workflow(
            agent_name=self.name,
            org_id=org_id,
            matter_id=matter_id,
            user_id=user_id,
            workflow_goal=goal,
            plan_steps=steps
        )


class CaseAgent(BaseAgent):
    def __init__(self):
        super().__init__("CaseAgent", ["document_search", "timeline_tool", "report_generate"])


class DocumentAgent(BaseAgent):
    def __init__(self):
        super().__init__("DocumentAgent", ["document_open", "page_open", "ocr_tool", "vision_tool"])


class PropertyAgent(BaseAgent):
    def __init__(self):
        super().__init__("PropertyAgent", ["document_search", "entity_search", "graph_search", "timeline_tool"])


class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("ResearchAgent", ["web_search", "legal_source_search", "citation_verify", "document_search"])


class ComparisonAgent(BaseAgent):
    def __init__(self):
        super().__init__("ComparisonAgent", ["document_open", "comparison_tool", "citation_verify"])


class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__("RiskAgent", ["document_search", "comparison_tool", "graph_search", "risk_evaluate"])


class DraftingAgent(BaseAgent):
    def __init__(self):
        super().__init__("DraftingAgent", ["document_search", "legal_source_search", "citation_verify", "draft_generate"])


class ReportAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReportAgent", ["document_search", "graph_search", "risk_evaluate", "report_generate"])


class VerificationAgent(BaseAgent):
    def __init__(self):
        super().__init__("VerificationAgent", ["document_open", "citation_verify", "comparison_tool"])


# Registry of Specialized Domain Agents
agent_registry: Dict[str, BaseAgent] = {
    "CaseAgent": CaseAgent(),
    "DocumentAgent": DocumentAgent(),
    "PropertyAgent": PropertyAgent(),
    "ResearchAgent": ResearchAgent(),
    "ComparisonAgent": ComparisonAgent(),
    "RiskAgent": RiskAgent(),
    "DraftingAgent": DraftingAgent(),
    "ReportAgent": ReportAgent(),
    "VerificationAgent": VerificationAgent()
}
