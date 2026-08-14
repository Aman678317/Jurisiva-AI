# Product & AI Experimentation Gate Engine

from typing import Dict, Any

class ProductExperimentGate:
    """Manages canary experiment rollouts (5% -> 100%) and automatic rollback triggers."""

    def __init__(self):
        self._experiments: Dict[str, Dict[str, Any]] = {
            "exp_fast_reranker": {
                "experiment_id": "exp_fast_reranker",
                "cohort_percent": 10,
                "status": "CANARY_ACTIVE",
                "target_metric": "rag_p95_ms",
                "safety_threshold_accuracy": 0.99
            }
        }

    def should_apply_variant(self, experiment_id: str, user_hash_mod: int) -> bool:
        exp = self._experiments.get(experiment_id)
        if not exp or exp["status"] != "CANARY_ACTIVE":
            return False
        return user_hash_mod < exp["cohort_percent"]

    def trigger_rollback_if_unsafe(self, experiment_id: str, measured_accuracy: float) -> bool:
        exp = self._experiments.get(experiment_id)
        if not exp:
            return False
        if measured_accuracy < exp["safety_threshold_accuracy"]:
            exp["status"] = "ROLLED_BACK"
            return True
        return False

experiment_gate = ProductExperimentGate()
