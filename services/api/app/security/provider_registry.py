# Subprocessor & AI Provider Registry
# Tracks all third-party infrastructure, inference engines, OCR pipelines, and search gateways.

from typing import Dict, List, Any

SUBPROCESSORS_REGISTRY = [
    {
        "provider": "Amazon Web Services (AWS) India",
        "purpose": "Cloud Hosting, Encrypted Storage (S3 KMS) & VPC Isolation",
        "data_processed": "Encrypted property documents, metadata & database records",
        "region": "Mumbai (ap-south-1) / Hyderabad (ap-south-2), India",
        "status": "VERIFIED & ACTIVE",
        "data_residency": "Strictly within India",
        "last_reviewed": "2026-08-01"
    },
    {
        "provider": "Google Cloud Platform (GCP) India",
        "purpose": "Enterprise AI Inference & Indic OCR Acceleration",
        "data_processed": "Transient document text for extraction (Zero-retention contract)",
        "region": "Delhi (asia-south2) / Mumbai (asia-south1), India",
        "status": "VERIFIED & ACTIVE",
        "data_residency": "Strictly within India",
        "last_reviewed": "2026-08-10"
    },
    {
        "provider": "Microsoft Azure India",
        "purpose": "High-Availability Disaster Recovery & Backup Replication",
        "data_processed": "Encrypted snapshot archives (AES-256)",
        "region": "Pune (Central India), India",
        "status": "VERIFIED & ACTIVE",
        "data_residency": "Strictly within India",
        "last_reviewed": "2026-07-25"
    },
    {
        "provider": "Bhoomi & Kaveri 2.0 State Gateways",
        "purpose": "Official Land Record & Encumbrance Certificate Verification",
        "data_processed": "Survey number, Village, SRO registration queries",
        "region": "Karnataka Government SDC, Bengaluru, India",
        "status": "VERIFIED & ACTIVE",
        "data_residency": "Government of Karnataka",
        "last_reviewed": "2026-08-15"
    },
    {
        "provider": "Supreme Court eCourts API Gateway",
        "purpose": "Official Judicial Judgment & Precedent Verification",
        "data_processed": "Citation numbers and legal subject queries",
        "region": "NIC, New Delhi, India",
        "status": "VERIFIED & ACTIVE",
        "data_residency": "Supreme Court of India / NIC",
        "last_reviewed": "2026-08-12"
    }
]

class ProviderRegistry:
    """Manages verified subprocessors and external data flow governance."""

    def list_subprocessors(self) -> List[Dict[str, Any]]:
        return SUBPROCESSORS_REGISTRY

    def get_provider(self, provider_name: str) -> Dict[str, Any]:
        return next((p for p in SUBPROCESSORS_REGISTRY if provider_name.lower() in p["provider"].lower()), {})

provider_registry = ProviderRegistry()
