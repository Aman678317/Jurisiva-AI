# Control Mapping Matrix (ISO 27001 / SOC 2 / NIST / DPDP)

## Framework Control Mapping

| Control ID | Description | ISO 27001 Ref | SOC 2 TSC Ref | DPDP Act Ref | Implementation Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`CTL-SEC-01`** | Encryption at rest and in transit | A.10.1.1 | CC6.1 | Sec 8(5) | AES-256 / TLS 1.3 (`SEC-001`) |
| **`CTL-TEN-02`** | Tenant isolation enforcement | A.9.4.1 | CC6.3 | Sec 8(4) | Scoped DB & Qdrant Queries (`SEC-002`) |
| **`CTL-AI-03`** | AI zero customer data retention | A.12.1.1 | CC6.8 | Sec 7(1) | Gateway DPA Zero-Log (`AI-003`) |
| **`CTL-AUD-04`** | Append-only security audit log | A.12.4.1 | CC7.2 | Sec 8(7) | Immutable Audit Trail (`AUD-001`) |

Control mapping does NOT imply formal third-party certification until an independent audit report is issued.
