# Compliance Control Matrix & Evidence Mapping

## Compliance Controls & Verification Table

| Control ID | Requirement | Requirement Source | Implementation & Control | Verification Evidence | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **CTRL-SEC-01** | Multi-tenant data isolation | Internal Security Policy | Column-level `organization_id` check in `auth_guard` | `test_security_compliance.py` red-team test | **VERIFIED** |
| **CTRL-SEC-02** | Password hashing safety | Industry Standard (OWASP) | PBKDF2 SHA-256 with salt in `auth.py` | Unit test `BE-TEST-001` | **VERIFIED** |
| **CTRL-AI-01** | Evidence-first citation grounding | Product Requirement | Application-level `CitationValidator` in `rag_engine.py` | `test_copilot.py` citation test | **VERIFIED** |
| **CTRL-AI-02** | Anti-hallucination abstention | Product Requirement | `EvidenceSufficiencyGate` in `rag_engine.py` | Negative query test `COP-004` | **VERIFIED** |
| **CTRL-PRIV-01**| Sensitive PII minimization | Digital Personal Data Protection Act | Sensitive field masking & purpose-bounded access | `test_security_compliance.py` PII test | **VERIFIED** |
| **CTRL-OPS-01** | Automated disaster recovery | Internal Policy | `DisasterRecoverySimulator` backup restore drill | `test_security_compliance.py` DR test | **VERIFIED** |
