# Chapter 14 Prompt — Deployment Security Review

```markdown
Act as a Cloud Security Engineer.

Audit the deployed staging infrastructure before production.

Test:
- public exposure
- IAM
- secrets
- storage
- database
- network
- TLS
- CORS
- security headers
- signed URLs
- tenant isolation
- CI/CD permissions
- artifact security

Return: CRITICAL | HIGH | MEDIUM | LOW

Any CRITICAL issue blocks production.
Create a regression check for every resolved critical/high finding.
```
