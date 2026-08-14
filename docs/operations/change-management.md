# Change Management & Feature Flag Policy

## Production Change Categories
1. **Standard Release (Normal)**: Planned feature deployment following full CI/CD pipeline, staging promotion, and manual release sign-off.
2. **Emergency Hotfix**: Critical P0/SEV-1 patch requiring expedited approval by Incident Commander + Lead Engineer with post-deployment regression test within 24 hrs.
3. **AI Circuit Breaker / Flag Toggle**: Feature-level toggle using `AIKillSwitch` to disable degraded AI workflows without taking down the platform.
