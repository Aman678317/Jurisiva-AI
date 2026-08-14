# Test Data Strategy & Synthetic Fixtures

## Synthetic Test Tenants & Users
- **Tenant ORG-A**: `org_001` ("Sharma & Associates Legal Counsel")
  - `usr_001`: Advocate Rajesh Sharma (`LEAD_ADVOCATE`)
  - `usr_002`: Associate Priya Verma (`ASSOCIATE`)
- **Tenant ORG-B**: `org_002` ("Patel Property Title Solutions")
  - `usr_003`: Director Vikram Patel (`ADMIN`)
  - `usr_004`: Auditor Meera Nair (`AUDITOR`)

## Test Data Integrity Rules
1. **Zero Confidential Customer Data**: Production customer deeds are NEVER used as automated test fixtures. All test deeds use synthetic names (`Venkatappa`, `Krishnappa`) and mock Survey Numbers (`42/1`).
2. **Deterministic Seed State**: Reset DB fixture scripts ensure clean test setup before every integration test run.
