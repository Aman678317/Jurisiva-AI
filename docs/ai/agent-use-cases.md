# Agentic Use Case Inventory & Decision Matrix

## Agent Classification Matrix

| Workflow | Classification | Deterministic Code Sufficient? | Human Approval Required? | Tool Permissions |
| :--- | :--- | :---: | :---: | :--- |
| **Title Deed Document Classification** | `NO_AGENT_REQUIRED` | YES | NO | N/A |
| **Encumbrance Search & Evidence Match** | `CONTROLLED_AGENT` | NO | NO | READ ONLY (`search_index`, `get_document_page`) |
| **Title Search Report Drafting** | `HUMAN_APPROVED_AGENT` | NO | YES | READ + PROPOSE DRAFT (`draft_report_section`) |
| **Document Deletion / Tenant Changes** | `AUTOMATION` (Non-AI) | YES | MANDATORY | DELETE (Human-Only API) |

Unconstrained autonomous loops are strictly forbidden. All legal workflows default to `HUMAN_APPROVED_AGENT`.
