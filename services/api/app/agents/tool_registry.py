# Governed Tool Registry & Permission Enforcer

from typing import Dict, Any, Optional

class GovernedToolRegistry:
    """Manages allowed tools, tool schemas, permission levels, and prompt injection defense."""

    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {
            "search_matter_documents": {
                "permission": "READ",
                "requires_approval": False,
                "input_schema": ["query", "limit"]
            },
            "propose_report_draft": {
                "permission": "PROPOSE",
                "requires_approval": True,
                "input_schema": ["section", "draft"]
            },
            "delete_matter_document": {
                "permission": "DELETE",
                "requires_approval": True,
                "input_schema": ["document_id"]
            }
        }

    def validate_tool_call(self, tool_name: str, tool_args: Dict[str, Any], user_role: str) -> Dict[str, Any]:
        tool = self._tools.get(tool_name)
        if not tool:
            return {"status": "BLOCKED", "reason": f"Tool '{tool_name}' is not registered in GovernedToolRegistry."}

        # Check permission level
        if tool["permission"] == "DELETE" and user_role not in ["OWNER", "ADMIN"]:
            return {"status": "FORBIDDEN", "reason": "Administrative privilege required for DELETE tool call."}

        # Prompt injection defense check
        for val in tool_args.values():
            if isinstance(val, str) and ("ignore previous instructions" in val.lower() or "reveal system prompt" in val.lower()):
                return {"status": "BLOCKED", "reason": "PROMPT_INJECTION_DETECTED: Malicious instruction intercepted."}

        return {
            "status": "ALLOWED",
            "requires_human_approval": tool["requires_approval"],
            "tool_name": tool_name
        }

tool_registry = GovernedToolRegistry()
