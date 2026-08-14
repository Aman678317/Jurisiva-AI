# Analytics Architecture & Privacy Isolation

## Privacy-Isolated Telemetry Pipelines
1. **Product Analytics**: Tracks feature adoption, document upload counts, and report generation events. Raw title deed texts and personal customer identities are NEVER sent to product analytics.
2. **Operational Telemetry**: Logs API latencies, server error rates, and queue depth.
3. **AI Quality Evaluation**: Samples synthetic and anonymized evaluation benchmarks in CI.
