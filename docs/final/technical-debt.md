# Technical Debt Register & Remediation Schedule

## Active Technical Debt Inventory

| Debt ID | System Area | Debt Description | Severity | Impact | Target Remediation |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **DEBT-01** | OCR Engine | OCR fallback relies on Tesseract binary when AWS Textract is unavailable | MEDIUM | Slower processing speed for degraded scans | Q4 2026 |
| **DEBT-02** | Search Cache | Redis query cache TTL set to static 3600 seconds | LOW | Potential cache invalidation lag on document updates | Q4 2026 |
| **DEBT-03** | Frontend Build | Legacy CSS bundle size optimization needed for low-bandwidth mobile devices | LOW | Slightly higher initial page load time on 3G networks | Q1 2027 |
