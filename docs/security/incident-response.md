# Incident Response Plan & Playbooks

## Incident Playbook: Cross-Tenant Data Leakage Containment
1. **Detection**: Automated alert triggered by `auth_guard` authorization failure spike or test failure.
2. **Containment**: Revoke active JWT session tokens for impacted organization; isolate affected DB tenant scope.
3. **Investigation**: Trace `request_id` and `trace_id` in immutable audit logs (`audit_logger`).
4. **Eradication**: Deploy patch to server-side authorization middleware with regression test.
5. **Postmortem**: Document root cause, timeline, and mitigation within 48 hours.
