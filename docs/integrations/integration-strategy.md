# Enterprise Ecosystem Integration Strategy

## Ecosystem Category & Priority

| Category | Partner System | Target Use Case | Access Scope |
| :--- | :--- | :--- | :--- |
| **Document Management** | iManage / NetDocuments | Sync property title deeds | `document:read`, `document:write` |
| **Enterprise Identity** | Okta / Entra ID | SCIM 2.0 user deprovisioning | `admin:write` |
| **Practice Management** | Clio / Practice League | Matter status & title report sync | `matter:read`, `report:read` |

Unscoped master API keys (`admin:everything`) are strictly forbidden.
