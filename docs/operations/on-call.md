# On-Call Rotation & Incident Escalation Framework

## On-Call Duty Structure
- **Primary On-Call Engineer**: Lead SRE / Platform Engineer (24/7 Pagerduty rotation).
- **Secondary On-Call Engineer**: Lead Product Engineer.
- **Escalation Path**: Primary -> Secondary -> Founder / CTO within 15 minutes of un-acknowledged SEV-1 alert.

## Alert Response Guidelines
- Every alert triggered by Prometheus/Grafana or structured logging must point to an explicit runbook in `docs/runbooks/`.
- No alert may be silenced or ignored without creating a tracked incident log entry.
