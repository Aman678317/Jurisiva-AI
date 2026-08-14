# Temporal Knowledge Graph & Relationship Provenance Schema

## Controlled Relationship Vocabulary

| Relationship Type | Source Entity | Target Entity | Temporal Attributes | Provenance Required |
| :--- | :--- | :--- | :---: | :---: |
| **`OWNS`** | Party (Person/Org) | Property | `valid_from`, `valid_to` | Deed Document ID & Page |
| **`ENCUMBERS`** | Financial Institution | Property | `valid_from`, `valid_to` | Mortgage Deed ID |
| **`CITES`** | Court Judgment | Precedent Case | `observed_at` | Page & Paragraph Locator |
| **`PARTICIPATES_IN`**| Advocate / Party | Legal Matter | `valid_from` | Wakalatnama / Filing ID |

Knowledge graph queries strictly enforce tenant boundaries (`org_id` & `matter_id`).
