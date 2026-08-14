# Runbook: Production Application Rollback

## Emergency Rollback Trigger Conditions
- API 5xx error rate exceeds 2% over a 5-minute window.
- Tenant isolation test failure detected in production health check.
- Data corruption or critical database error reported.

## Step-by-Step Rollback Execution
1. **Stop Traffic Promotion**: Direct reverse proxy / load balancer traffic back to Blue (Previous Known-Good Version).
   ```bash
   docker compose -f infra/docker-compose.prod.yml up -d --no-recreate web api
   ```
2. **Verify Database Schema Compatibility**:
   - Ensure previous schema version is active or forward-compatible migration holds.
3. **Verify Worker Heartbeat**:
   - Restart worker containers with previous image digest.
4. **Post-Rollback Health Check**:
   - Query `/health` and verify HTTP 200 OK.
