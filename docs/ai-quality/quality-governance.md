# AI Quality Governance & Evaluation Ownership

## Quality Governance Roles & Responsibilities

| Role | Designated Owner | Core Responsibilities |
| :--- | :--- | :--- |
| **AI Evaluation Lead** | AI Engineering Lead | Golden dataset curation, regression gate enforcement, & model benchmark comparison |
| **Quality Architect** | QA Lead | Grounding precision, citation validity verification, & abstention rate tracking |
| **Safety & Red Team Lead** | Security Architect | Prompt injection resistance testing & adversarial prompt suites |
| **Legal Reviewer** | Lead Advocate | Human-in-the-loop evaluation form reviews & inter-rater agreement checks |

---

## Evaluation Principles
1. **Evidence First**: Model fluency is secondary to factual grounding and non-zero page citation traceability.
2. **Regression Prevention**: No model or prompt update is deployed if ground truth precision or citation accuracy regresses beyond 0.5%.
3. **Continuous Monitoring**: Model drift, source drift, and latency anomalies monitored continuously in production telemetry.
