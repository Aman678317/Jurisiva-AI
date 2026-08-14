# Governed Agent Orchestrator & Execution Loop Engine

import time
from typing import Dict, List, Any
from app.agents.tool_registry import tool_registry

class AgentOrchestrator:
    """Runs bounded multi-step agent workflows with max step limits, dry-run support, and human approval gates."""

    MAX_STEPS = 5

    def run_agent_workflow(self, org_id: str, matter_id: str, user_role: str, plan_steps: List[Dict[str, Any]], dry_run: bool = False) -> Dict[str, Any]:
        run_id = f"RUN-{int(time.time())}"
        executed_steps = []

        if len(plan_steps) > self.MAX_STEPS:
            return {
                "run_id": run_id,
                "status": "FAILED",
                "reason": f"Plan steps ({len(plan_steps)}) exceed maximum bounded limit ({self.MAX_STEPS})."
            }

        for idx, step in enumerate(plan_steps):
            tool_name = step.get("tool_name", "")
            tool_args = step.get("tool_args", {})

            validation = tool_registry.validate_tool_call(tool_name, tool_args, user_role)
            if validation["status"] != "ALLOWED":
                return {
                    "run_id": run_id,
                    "status": "BLOCKED",
                    "reason": validation["reason"],
                    "failed_step": idx
                }

            if validation["requires_human_approval"] and not dry_run:
                return {
                    "run_id": run_id,
                    "status": "WAITING_FOR_REVIEW",
                    "proposed_action": tool_name,
                    "step_index": idx,
                    "reason": "Human-in-the-loop approval required before executing high-risk action."
                }

            executed_steps.append({
                "step_index": idx,
                "tool_name": tool_name,
                "status": "DRY_RUN_SIMULATED" if dry_run else "EXECUTED"
            })

        return {
            "run_id": run_id,
            "status": "COMPLETED",
            "executed_steps_count": len(executed_steps),
            "dry_run": dry_run
        }

agent_orchestrator = AgentOrchestrator()
