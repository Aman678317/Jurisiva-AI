# Security Audit Service & Admin Settings Engine
# Provides immutable audit event logging, user session tracking, and tenant data retention policies.

import time
from typing import Dict, List, Any, Optional
from app.audit import audit_logger

class SecurityAuditService:
    """Enterprise Audit Service tracking all security, diligence, and access events."""

    def __init__(self):
        self._settings = {
            "data_retention_days": 90,
            "mfa_required": True,
            "session_timeout_minutes": 30,
            "ip_whitelist": ["127.0.0.1", "192.168.1.0/24"],
            "ai_data_sharing": False,
            "audit_log_immutable": True,
            "last_policy_update": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        # Pre-seed realistic tenant audit events
        self._seed_initial_events()

    def _seed_initial_events(self):
        if len(audit_logger._audit_store) < 3:
            audit_logger.log_event(
                org_id="org_001",
                user_id="usr_rajesh",
                user_name="Adv. Rajesh Sharma",
                action="USER_LOGIN",
                resource_type="Authentication",
                resource_id="session_01",
                ip_address="127.0.0.1",
                metadata={"mfa_verified": True, "auth_method": "FIDO2_PASSKEY"}
            )
            audit_logger.log_event(
                org_id="org_001",
                user_id="usr_rajesh",
                user_name="Adv. Rajesh Sharma",
                action="DOCUMENT_UPLOADED",
                resource_type="Document",
                resource_id="doc_001",
                matter_id="mat_001",
                metadata={"filename": "Registered_Sale_Deed_1985.pdf", "encryption": "AES_256_GCM"}
            )
            audit_logger.log_event(
                org_id="org_001",
                user_id="usr_rajesh",
                user_name="Adv. Rajesh Sharma",
                action="AI_ANALYSIS_EXECUTED",
                resource_type="AI Engine",
                resource_id="analysis_mat_001",
                matter_id="mat_001",
                metadata={"model": "Jurisiva Indic Legal Core", "zero_retention_enforced": True}
            )

    def get_audit_logs(self, org_id: str = "org_001", limit: int = 50) -> List[Dict[str, Any]]:
        return audit_logger._audit_store[-limit:]

    def get_security_settings(self) -> Dict[str, Any]:
        return self._settings

    def update_security_settings(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        for k, v in updates.items():
            if k in self._settings:
                self._settings[k] = v
        self._settings["last_policy_update"] = time.strftime("%Y-%m-%d %H:%M:%S")
        audit_logger.log_event(
            org_id="org_001",
            user_id="usr_admin",
            user_name="System Administrator",
            action="SECURITY_SETTINGS_UPDATED",
            resource_type="SecurityPolicy",
            metadata=updates
        )
        return self._settings

security_audit_service = SecurityAuditService()
