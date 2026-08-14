# Standardized Error Classification Taxonomy

## Production Error Categories

| Error Class | Code | Severity | Operator Action | User-Facing Message |
| :--- | :---: | :---: | :--- | :--- |
| **VALIDATION_ERROR** | `ERR_400` | LOW | None (Invalid input) | "Invalid document parameters provided." |
| **AUTH_ERROR** | `ERR_401` | MEDIUM | Audit login attempt | "Authentication session expired." |
| **DEPENDENCY_TIMEOUT**| `ERR_504` | HIGH | Check circuit breaker | "External source connection timed out." |
| **DATA_CORRUPTION** | `ERR_500` | CRITICAL | Quarantine record | "Data validation fault; review queued." |
