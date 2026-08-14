# Immutable Audit Logging Engine

import time
from typing import List, Dict, Optional

class AuditLogEngine:
    def __init__(self):
        self._audit_store: List[Dict] = []

    def log_event(
        self,
        org_id: str,
        user_id: str,
        user_name: str,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        matter_id: Optional[str] = None,
        ip_address: str = "127.0.0.1",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Appends immutable audit event record."""
        event = {
            "id": f"aud_{len(self._audit_store) + 1}",
            "organization_id": org_id,
            "matter_id": matter_id,
            "user_id": user_id,
            "user_name": user_name,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "ip_address": ip_address,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "metadata": metadata or {}
        }
        self._audit_store.append(event)
        return event

    def get_matter_logs(self, org_id: str, matter_id: str) -> List[Dict]:
        """Returns matter logs scoped strictly by organization ID."""
        return [
            log for log in self._audit_store
            if log["organization_id"] == org_id and log["matter_id"] == matter_id
        ]

audit_logger = AuditLogEngine()
