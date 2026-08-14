# Automated Authorization Matrix & Security Gate

## Server-Enforced RBAC Permission Matrix

| Role | Matter Read | Matter Create | Document Upload | Document Delete | Research Run | Report Export | Admin |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **ADMIN** | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW |
| **LEAD_ADVOCATE**| ALLOW | ALLOW | ALLOW | DENY | ALLOW | ALLOW | DENY |
| **ASSOCIATE** | ALLOW | DENY | ALLOW | DENY | ALLOW | DENY | DENY |
| **AUDITOR** | ALLOW | DENY | DENY | DENY | DENY | DENY | DENY |
| **SUSPENDED** | DENY | DENY | DENY | DENY | DENY | DENY | DENY |
| **NON_MEMBER** | DENY | DENY | DENY | DENY | DENY | DENY | DENY |

All DENY rules return HTTP 403 Forbidden with structured code `PERMISSION_DENIED`.
