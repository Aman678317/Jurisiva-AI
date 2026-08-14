# Vendor Register & Subprocessor Risk Matrix

| Vendor / Provider | Category | Purpose | Data Handled | Security / Contract Status |
| :--- | :--- | :--- | :--- | :--- |
| **AWS / Azure / GCP** | Cloud Hosting | PostgreSQL, Object Storage, Redis | Encrypted tenant documents & DB | ISO 27001 / SOC 2 Type II Certified |
| **OpenAI / Anthropic (via LiteLLM)** | AI Provider | RAG completion & summarization | Temporary prompt text (Zero Data Retention agreement) | DPA with Zero Training Guarantee |
| **eCourts / Kaveri Public Portals** | Public Data | Case metadata & land record verification | Public search queries | Official Government Interfaces |
