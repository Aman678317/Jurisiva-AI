# AI Provider Governance & Model Registry Policy

## AI Model Approval Policy
1. Models must be explicitly registered in `ModelRegistry` before production deployment.
2. Unregistered or deprecated model identifiers generated dynamically are strictly blocked.
3. Every model approved for production must enforce a zero data retention agreement with zero model training on customer prompt context.

## Approved Production Models
- `gpt-4o-mini`: Primary reasoning & copilot summary model (Max 128k context, zero training).
- `claude-3-haiku`: Secondary fallback model for complex document comparisons (Zero retention agreement).
- `text-embedding-3-small`: 1536-dim vector embedding generator.
