# Production Deployment Architecture

## System Topography

```mermaid
graph TD
    Client[Browser / Advocate Workstation] --> TLS[TLS 1.3 Reverse Proxy / Nginx]
    TLS --> WebApp[apps/web React SPA UI]
    TLS --> API[services/api FastAPI Server]
    
    subgraph Private VPC Network
        API --> DB[(PostgreSQL 16 + pgvector)]
        API --> Redis[(Redis 7 Queue / Cache)]
        API --> S3[(MinIO / S3 Sealed Storage)]
        
        Redis --> Worker[Document Ingestion Worker]
        Worker --> DB
        Worker --> S3
    end
    
    API --> AIGateway[LiteLLM AI Provider Gateway]
    AIGateway --> OpenAI[OpenAI / Anthropic APIs]
```

---

## Data Boundary Isolation
- **Public Boundary**: HTTPS Port 443 only.
- **Private Subnet**: PostgreSQL (Port 5432), Redis (Port 6379), S3 Storage (Port 9000). Direct public internet exposure is strictly blocked.
