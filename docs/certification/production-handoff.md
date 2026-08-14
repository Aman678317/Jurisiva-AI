# Production Handoff & Operator Handbook

## Daily Operator Checklist
1. **Deployment Execution**:
   ```bash
   git checkout v1.0.0
   docker compose -f infra/docker-compose.yml up -d
   ```
2. **Health Verification**:
   Query `http://localhost:8000/health` and confirm HTTP 200 OK with status `HEALTHY`.
3. **Emergency Rollback**:
   Execute runbook in [`docs/runbooks/rollback.md`](file:///c:/Users/acer/Desktop/legal/docs/runbooks/rollback.md).
4. **AI Kill Switch Circuit Breaker**:
   Use `AIKillSwitch.disable_feature("AI_COPILOT_ENABLED", "Reason", "operator_id")` in `services/api/app/operations/ai_kill_switch.py`.
