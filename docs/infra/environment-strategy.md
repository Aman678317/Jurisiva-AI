# Environment Strategy & Promotion Pipeline

## 1. Environment Topology

| Environment | Purpose | Database | Storage | Cost |
| :--- | :--- | :--- | :--- | :--- |
| **LOCAL** | Development & unit testing | Local Docker Postgres | Local MinIO | Zero-budget |
| **CI** | Automated validation gates | Ephemeral Postgres service | Ephemeral storage | Free-tier CI |
| **STAGING** | Pre-release validation & E2E smoke tests | Staging Postgres snapshot | Staging S3 bucket | Minimal |
| **PRODUCTION**| Real user advocate workloads | Production Postgres VPC | Production S3 bucket | Usage-based |

---

## 2. CI/CD Promotion Sequence
1. Developer pushes commit to `main` branch.
2. GitHub Actions runs CI pipeline: Lint -> Typecheck -> Unit tests -> Security scan.
3. Build immutable release container artifact tagged `v0.1.0-rc1`.
4. Deploy artifact to Staging environment.
5. Run automated Staging smoke tests and cross-tenant isolation verifications.
6. Upon manual Release Sign-Off, promote `v0.1.0-rc1` to Production.
7. Execute post-deployment 30-minute health validation.
