# AI Cost Controls & Token Budgeting

## Budget & Rate Limits
- **Max Input Tokens**: 8,000 tokens per query.
- **Max Output Tokens**: 2,000 tokens per query.
- **Per-Matter Cost Limit**: ₹120 target cost per matter (tracked in `AIRun`).
- **Embedding Cache**: Hash-based caching (`SHA-256` content hash) prevents re-embedding unchanged chunks.
