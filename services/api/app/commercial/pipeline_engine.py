# CRM Pipeline Engine & Revenue Operations System

import time
from typing import Dict, List, Any

class CRMPipelineEngine:
    """Manages sales pipeline stages, opportunity qualification scoring, and contract-to-billing reconciliation."""

    VALID_STAGES = {"LEAD", "QUALIFIED", "DISCOVERY", "DEMO", "PILOT", "CONTRACT", "CLOSED_WON", "CLOSED_LOST"}

    def __init__(self):
        self._opportunities: Dict[str, Dict[str, Any]] = {}

    def create_opportunity(self, account_name: str, deal_value_inr: int, initial_stage: str = "LEAD") -> Dict[str, Any]:
        if initial_stage not in self.VALID_STAGES:
            raise ValueError(f"Invalid sales stage '{initial_stage}'.")

        opp_id = f"OPP-{len(self._opportunities) + 1}"
        opp = {
            "opp_id": opp_id,
            "account_name": account_name,
            "deal_value_inr": deal_value_inr,
            "stage": initial_stage,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self._opportunities[opp_id] = opp
        return opp

    def advance_stage(self, opp_id: str, target_stage: str) -> Dict[str, Any]:
        if target_stage not in self.VALID_STAGES:
            return {"status": "INVALID_STAGE", "reason": f"Stage '{target_stage}' not recognized."}

        opp = self._opportunities.get(opp_id)
        if not opp:
            return {"status": "NOT_FOUND", "reason": "Opportunity ID not found."}

        opp["stage"] = target_stage
        opp["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        return {"status": "SUCCESS", "opportunity": opp}

pipeline_engine = CRMPipelineEngine()
