# Data Classification & Handling Rules

## Classification Categories

| Classification | Description | Examples | Handling Rules |
| :--- | :--- | :--- | :--- |
| **PUBLIC** | Freely accessible public legal records | eCourts judgment text, Gazette notifications | Unrestricted public view |
| **INTERNAL** | System logs, telemetry, app build artifacts | Application performance metrics, anonymized logs | Restricted to SRE & internal team |
| **CONFIDENTIAL** | Advocate matter metadata & title reports | Matter titles, party names, title deed extracts | Scoped strictly by Organization RBAC |
| **HIGHLY_SENSITIVE** | Original PDF title deeds & authentication keys | Uploaded property title deeds, JWT keys | AES-256 encrypted, strict tenant isolation |
