# Property Due Diligence Workspace & Checklist

## Due Diligence Checklist
| Item | Required Document | Verification Rule | Review Status |
| :--- | :--- | :--- | :--- |
| **Mother Deed (30-yr)** | Sale Deed (1985 or earlier) | Complete chain of title without gap > 3 years | Verified |
| **Encumbrance Cert (EC)** | Form 15 / Form 16 EC | Nil encumbrance or matching mortgage discharge | Pending Review |
| **Khata Certificate** | A-Khata / BBMP e-Khata | PID / Khata matches current owner name | Verified |
| **Tax Paid Receipts** | Latest Property Tax Receipt | Payment date within current financial year | Verified |
| **Pahani / RTC** | RTC / Mutation Register | Column 9 (Owner) & Column 10 (Extent) match deed | Verified |

## Missing Document Detection Rule
If the timeline gap between Deed $N$ (Buyer: Person B) and Deed $N+1$ (Seller: Person C) exceeds 3 years without a connecting succession or sale deed, the workspace tags `"MISSING_LINK_IN_TITLE"`.
