# Organization Hierarchy & Membership Lifecycle

## Organization Domain Hierarchy

```mermaid
graph TD
    Org[Organization / Tenant] --> Admin[Org Admin Console]
    Org --> Team[Team: Litigation / Real Estate]
    Team --> Member[Team Member / Advocate]
    Org --> Workspace[Matter Workspace]
    Workspace --> Access[Matter Access Control]
    Access --> Restricted[Restricted Matter A]
    Access --> General[General Matter B]
```

---

## Member Lifecycle States
- **`INVITED`**: Email invitation token sent; access blocked until acceptance.
- **`ACTIVE`**: Full access granted according to assigned Organization and Matter roles.
- **`SUSPENDED`**: Temporary access pause; all active sessions & token refreshes revoked.
- **`DEACTIVATED`**: Permanent account closure; user removed from all matter workspaces.
