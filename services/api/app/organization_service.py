# Enterprise Law Firm & Company Registration Engine
# Handles onboarding, tenant org creation, and diligence seat provisioning.

import time
from typing import Dict, List, Any
from app.audit import audit_logger

class OrganizationRegistrationService:
    """Manages enterprise law firm and company registrations."""

    def __init__(self):
        self._registrations: List[Dict[str, Any]] = [
            {
                "registration_id": "reg_001",
                "org_id": "org_001",
                "company_name": "Sharma & Associates Legal Chambers",
                "first_name": "Rajesh",
                "last_name": "Sharma",
                "email": "rajesh@sharmalegal.in",
                "job_title": "Senior Managing Partner",
                "phone": "+91 98450 12345",
                "org_type": "Litigation Chambers & Property Diligence",
                "jurisdiction": "Karnataka (Bengaluru / High Court)",
                "status": "ACTIVE_VERIFIED",
                "created_at": "2026-08-01T10:00:00Z"
            }
        ]

    def register_organization(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        reg_id = f"reg_{len(self._registrations) + 1:03d}"
        org_id = f"org_{len(self._registrations) + 1:03d}"
        
        record = {
            "registration_id": reg_id,
            "org_id": org_id,
            "company_name": payload.get("company_name", "Enterprise Chambers"),
            "first_name": payload.get("first_name", ""),
            "last_name": payload.get("last_name", ""),
            "email": payload.get("email", ""),
            "job_title": payload.get("job_title", "Legal Counsel"),
            "phone": payload.get("phone", ""),
            "org_type": payload.get("org_type", "Law Firm"),
            "jurisdiction": payload.get("jurisdiction", "All India Practice"),
            "marketing_consent": payload.get("marketing_consent", True),
            "status": "PENDING_VERIFICATION",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        
        self._registrations.append(record)
        
        # Log to immutable audit ledger
        audit_logger.log_event(
            org_id=org_id,
            user_id=f"usr_{record['first_name'].lower()}",
            user_name=f"{record['first_name']} {record['last_name']}",
            action="ORGANIZATION_REGISTRATION_SUBMITTED",
            resource_type="EnterpriseRegistration",
            resource_id=reg_id,
            metadata={
                "company_name": record["company_name"],
                "org_type": record["org_type"],
                "email": record["email"]
            }
        )
        
        return record

    def list_registrations(self) -> List[Dict[str, Any]]:
        return self._registrations

org_service = OrganizationRegistrationService()
