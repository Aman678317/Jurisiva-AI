# Agent Incident Classification & Containment Protocols

## Agent Failure Taxonomy
- **`AGENT_STEP_EXHAUSTION`**: Agent reached 5-step limit; execution stopped safely.
- **`UNAUTHORIZED_TOOL_ATTEMPT`**: Agent attempted to call unregistered or write-level tool; invocation blocked.
- **`PROMPT_INJECTION_DETECTED`**: External document content attempted to alter system prompt; query isolated.
