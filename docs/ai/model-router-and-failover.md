# Multi-Model AI Router & Key Failover Mesh

Jurisiva AI has been equipped with a **Multi-Model AI Router** featuring native support for **NVIDIA NIM**, **DeepSeek-R1 & V3**, **GLM-4 & GLM-2**, alongside OpenAI, Anthropic, Google, and Sovereign Local inference, backed by an **automatic multi-key rotation and provider failover mesh**.

---

## 🏛️ Multi-LLM Architecture & Cascading Failover

```
                           AI Task Ingestion
                                  │
                                  ▼
                   ┌──────────────────────────────┐
                   │    Governed ModelRouter      │
                   │ (Task / Risk / Latency / CoT)│
                   └──────────────┬───────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
[ DEEP LEGAL REASONING ]  [ FAST CLASSIFICATION ]  [ HIGH-RISK COURT DRAFT ]
   1. DeepSeek-R1 (CoT)      1. GLM-4 / GLM-2         1. Claude 3.5 Sonnet
   2. NVIDIA Nemotron-70B    2. GLM-4-Flash           2. DeepSeek-R1
   3. GPT-4o / o1            3. GPT-4o-mini           3. NVIDIA Llama 3.1 70B
   4. Claude 3.5 Sonnet      4. Gemini 1.5 Flash      4. GPT-4o
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                                  ▼
                     ┌──────────────────────────┐
                     │     KeyPool Manager      │
                     │ (Multi-Key Rate-Limit    │
                     │  Rotation & Cooldown)    │
                     └────────────┬─────────────┘
                                  │
                  429 / Quota / Error Encountered?
                                  │
               ┌──────────────────┴──────────────────┐
               │ YES                                 │ NO
               ▼                                     ▼
   Rotate to Next Key in Pool                Execute & Return
   If All Keys Exhausted ➔ Failover          Verified Statutory
   to Next LLM in Chain Seamlessly           Legal Output
```

---

## ⚡ Added AI Providers & Models

| Provider | Supported Models | Primary Specialization |
| :--- | :--- | :--- |
| **NVIDIA NIM** | `nvidia/llama-3.1-nemotron-70b-instruct`, `meta/llama-3.1-405b-instruct`, `deepseek-ai/deepseek-r1` | High-throughput statutory property reasoning, root-of-title verification |
| **DeepSeek** | `deepseek-reasoner` (R1 with Chain of Thought), `deepseek-chat` (V3) | Deep statutory contradictions, Akarband vs deed reconciliation, apex case synthesis |
| **GLM / Zhipu AI** | `glm-4`, `glm-4-plus`, `glm-4-flash`, `glm-2` (ChatGLM) | Rapid entity extraction, classification, multilingual Indic translation |
| **Anthropic** | `claude-3-5-sonnet-20241022` | Certified Title Opinions, Court Pleadings, High-risk draft covenants |
| **OpenAI** | `gpt-4o`, `gpt-4o-mini`, `o1`, `text-embedding-3-large` | General legal copilot and 1536-dim semantic embeddings |
| **Google** | `gemini-1.5-pro`, `gemini-1.5-flash` | Multimodal deed inspection and Kannada/Hindi handwritten OCR |
| **Local Sovereign** | `local-llama3-legal-8b`, `local-florence-2` | Air-gapped chambers and emergency fallback |

---

## 🔄 Multi-Key Rate Limit & Quota Failover (`KeyPool`)

Each provider is backed by a `KeyPool`:
1. Supports multiple comma-separated keys:
   - `NVIDIA_API_KEYS="key1,key2,key3"`
   - `DEEPSEEK_API_KEYS="key1,key2"`
   - `GLM_API_KEYS="key1,key2"`
2. If **Key 1** hits `429 Too Many Requests` or quota limits, `KeyPool` automatically places it in cooldown and rotates to **Key 2** instantly.
3. If all keys for a provider are exhausted, `ModelRouter.execute_with_failover()` smoothly cascades to the next capable LLM in the chain (e.g. DeepSeek $\rightarrow$ NVIDIA $\rightarrow$ OpenAI $\rightarrow$ Claude $\rightarrow$ GLM), ensuring **zero request interruption or user-facing downtime**.
