# Role Permission Matrix & Matter-Level Access Controls

## Organization vs Matter Role Matrix

| Action / Resource | Org OWNER | Org ADMIN | Matter EDITOR | Matter VIEWER | Support Impersonation |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Manage Org Settings & Members** | ALLOWED | ALLOWED | DENIED | DENIED | DENIED |
| **Read General Matter Content** | ALLOWED | ALLOWED | ALLOWED | ALLOWED | Read-Only (Audited) |
| **Read Restricted Matter Content** | ALLOWED | DENIED (Unless Added) | ALLOWED (If Member) | DENIED | DENIED (Requires Break-Glass) |
| **Edit Title Deeds / Notes** | ALLOWED | ALLOWED | ALLOWED | DENIED | DENIED |
| **Export Data Archive** | ALLOWED | ALLOWED | DENIED | DENIED | DENIED |

Organization Admin role does NOT automatically grant access to confidential restricted matters.
