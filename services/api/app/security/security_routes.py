# Security Endpoints Router & API Controllers

from typing import Dict, List, Any
from app.security.security_config import SECURITY_POSTURE
from app.security.provider_registry import provider_registry
from app.security.audit_service import security_audit_service

class SecurityController:
    """Handles REST requests for Trust & Security Center and Admin Security."""

    def get_security_status(self) -> Dict[str, Any]:
        return {
            "organization": SECURITY_POSTURE["organization"],
            "positioning": SECURITY_POSTURE["positioning"],
            "core_pledges": SECURITY_POSTURE["core_pledges"],
            "trust_indicators": SECURITY_POSTURE["trust_indicators"],
            "compliance_status": SECURITY_POSTURE["compliance_status"],
            "security_contacts": SECURITY_POSTURE["security_contacts"]
        }

    def get_subprocessors(self) -> List[Dict[str, Any]]:
        return provider_registry.list_subprocessors()

    def get_security_documents(self) -> List[Dict[str, Any]]:
        return SECURITY_POSTURE["security_documents"]

    def get_audit_log(self, org_id: str = "org_001") -> List[Dict[str, Any]]:
        return security_audit_service.get_audit_logs(org_id)

    def get_security_settings(self) -> Dict[str, Any]:
        return security_audit_service.get_security_settings()

    def update_security_settings(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        return security_audit_service.update_security_settings(updates)

security_controller = SecurityController()
