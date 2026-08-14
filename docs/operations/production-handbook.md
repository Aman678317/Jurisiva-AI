# Production Operations Handbook

## Operational Rhythms & Maintenance Cadence

### Daily Operations Rhythm
1. **08:00 IST Morning Telemetry Audit**: Review API error rates, worker queue backlogs, and OCR failure spikes.
2. **Database Backup Verification**: Verify night's PostgreSQL 5-minute WAL archiving snapshot to object storage.
3. **AI Cost & Token Utilization Check**: Inspect token expenditure across OpenAI/Anthropic models via LiteLLM gateway.

### Weekly Operations Rhythm
1. **Model & RAG Quality Review**: Sample 5% of production AI responses for citation accuracy and grounding sufficiency.
2. **Security & Access Log Audit**: Audit active organization admin memberships and break-glass log entries.

### Monthly Operations Rhythm
1. **Disaster Recovery Drill**: Run automated restoration test (`DisasterRecoverySimulator`).
2. **FinOps Unit Economics Review**: Measure cost per matter due diligence against the ₹85 unit budget.
