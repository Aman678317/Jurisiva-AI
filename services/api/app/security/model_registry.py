# AI Model Registry & Compliance Approval Engine

from typing import Dict, List, Optional

class ModelRegistry:
    """Registry enforcing explicit approval, zero-data-retention compliance, and token context limits."""

    def __init__(self):
        self._approved_models: Dict[str, Dict] = {
            "gpt-4o-mini": {
                "model_id": "gpt-4o-mini",
                "provider": "openai",
                "max_context_tokens": 128000,
                "zero_training_guarantee": True,
                "status": "APPROVED_FOR_PRODUCTION",
                "approved_workflows": ["MATTER_SUMMARY", "PROPERTY_DUE_DILIGENCE", "DOCUMENT_REVIEW"]
            },
            "claude-3-haiku": {
                "model_id": "claude-3-haiku",
                "provider": "anthropic",
                "max_context_tokens": 200000,
                "zero_training_guarantee": True,
                "status": "APPROVED_FOR_PRODUCTION",
                "approved_workflows": ["DOCUMENT_COMPARISON", "COURT_RESEARCH"]
            },
            "text-embedding-3-small": {
                "model_id": "text-embedding-3-small",
                "provider": "openai",
                "max_context_tokens": 8191,
                "zero_training_guarantee": True,
                "status": "APPROVED_FOR_PRODUCTION",
                "approved_workflows": ["VECTOR_EMBEDDING"]
            }
        }

    def is_model_approved(self, model_id: str, workflow: Optional[str] = None) -> bool:
        model = self._approved_models.get(model_id)
        if not model or model["status"] != "APPROVED_FOR_PRODUCTION":
            return False
        if workflow and workflow not in model["approved_workflows"]:
            return False
        return True

    def get_model(self, model_id: str) -> Optional[Dict]:
        return self._approved_models.get(model_id)

model_registry = ModelRegistry()
