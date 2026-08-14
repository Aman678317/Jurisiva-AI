# Governed Agent Architecture & Execution State Machine

## Agent Execution State Machine

```mermaid
stateDiagram-v2
    [*] --> CREATED
    CREATED --> PLANNING
    PLANNING --> EXECUTING: Plan Validated
    EXECUTING --> WAITING_FOR_REVIEW: High-Risk Action Proposed
    WAITING_FOR_REVIEW --> APPROVED: Advocate Confirms
    WAITING_FOR_REVIEW --> CANCELLED: Advocate Rejects
    EXECUTING --> COMPLETED: Bounded Steps Finished
    EXECUTING --> FAILED: Step/Token/Budget Exceeded
```

---

## Non-Negotiable Limits
- **Max Steps**: 5 execution steps per agent run.
- **Max Tool Calls**: 8 tool calls total.
- **Max Execution Time**: 30 seconds limit.
- **Max Token Budget**: 15,000 tokens per agent invocation.
