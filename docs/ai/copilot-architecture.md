# Production AI Copilot Architecture

## Architecture Flow

```mermaid
graph TD
    UserQuery[User Question] --> AuthGuard[Tenant Authorization Guard]
    AuthGuard --> RetrievalEngine[Authorized Hybrid Retrieval (Chapter 8)]
    RetrievalEngine --> SufficiencyGate[Evidence Sufficiency Gate]
    
    SufficiencyGate -->|Insufficient| Abstain[Return Abstention Response]
    SufficiencyGate -->|Sufficient Evidence| PromptAssembler[Context Assembler + Safety Guard]
    
    PromptAssembler --> AIGateway[AI Gateway (LiteLLM / Model Router)]
    AIGateway --> StructuredParser[Structured Response Parser]
    
    StructuredParser --> CitationVal[Server-Side Citation Validator]
    CitationVal --> GroundingCheck[Grounding & Conflict Evaluator]
    
    GroundingCheck --> AIRunLogger[Immutable AIRun Logger]
    AIRunLogger --> ClientUI[Grounded Response with Clickable Page Citations]
```

---

## Non-Negotiable AI Rules
1. **No Autonomous Legal Advice**: AI responses are provided strictly for research assistance and document analysis; human review is required for high-risk legal decisions.
2. **Strict Server-Side Authorization**: AI model calls never bypass tenant scope.
3. **Traceable Citations**: Every claim must link directly to an authorized document, page, and chunk.
