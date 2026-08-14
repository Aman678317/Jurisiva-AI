# Server-Side Role-Based Access Control (RBAC) & Tenant Isolation Guard

from typing import Set, Dict

# Explicit Permission Matrix
ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    "ADMIN": {
        "org.manage", "user.invite", "matter.read", "matter.create", "matter.edit", "matter.archive",
        "document.upload", "document.read", "document.delete", "property.verify", "report.export", "audit.read"
    },
    "LEAD_ADVOCATE": {
        "matter.read", "matter.create", "matter.edit", "document.upload", "document.read",
        "property.verify", "research.run", "copilot.run", "report.export", "audit.read"
    },
    "ASSOCIATE": {
        "matter.read", "document.upload", "document.read", "property.verify", "research.run", "copilot.run"
    },
    "AUDITOR": {
        "matter.read", "document.read", "audit.read"
    }
}

class AuthorizationGuard:
    @staticmethod
    def check_permission(role: str, permission: str) -> bool:
        allowed = ROLE_PERMISSIONS.get(role, set())
        return permission in allowed

    @staticmethod
    def verify_tenant_access(user_org_id: str, resource_org_id: str) -> bool:
        """Enforces multi-tenant isolation. Organization A cannot access Organization B data."""
        if not user_org_id or not resource_org_id:
            return False
        return user_org_id == resource_org_id

    @staticmethod
    def verify_matter_access(user_org_id: str, matter_org_id: str, is_member: bool) -> bool:
        """Verifies authenticated member belongs to the authorized matter and tenant."""
        return AuthorizationGuard.verify_tenant_access(user_org_id, matter_org_id) and is_member

auth_guard = AuthorizationGuard()
