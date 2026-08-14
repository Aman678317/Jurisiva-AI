# Production Deployment & Staging Promotion Plan

## Release Information
- **Release Version**: `v0.1.0-rc1`
- **Release Commit**: `HEAD` (Git tag `chapter-14-production-deployment`)
- **Deployment Strategy**: Blue/Green Container Swappable Deployment with zero downtime.

## Execution Sequence
1. **Pre-Deployment Checks**:
   - Verify DB backup WAL snapshot is completed (`snap_2026_08_14`).
   - Confirm staging test suite passed 100%.
2. **Database Migration Stage**:
   - Execute backward-compatible migrations: `python -m app.db.migrate`.
3. **Application Deployment Stage**:
   - Deploy API server and worker containers with updated release digest.
4. **Health Verification Stage**:
   - Query `/health`, `/readiness`, `/worker-health`, `/ai-health`.
5. **Post-Deployment Smoke Test**:
   - Run synthetic smoke test in production test organization `ORG-A`.
