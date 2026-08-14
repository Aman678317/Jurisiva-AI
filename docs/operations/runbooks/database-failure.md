# Runbook — Database Failure Recovery

## Operator Action Sequence
1. Verify database connectivity: `docker exec -it legal-db pg_isready`.
2. Inspect connection pool utilization and active locks: `SELECT * FROM pg_stat_activity WHERE state = 'active';`.
3. If pool is exhausted, scale PgBouncer connection limits or restart idle poolers.
4. If corruption occurs, trigger point-in-time recovery using the latest WAL snapshot via `DisasterRecoverySimulator`.
