# India Public Data Mapping & Source Inventory

## 1. Official & Public Data Domains

| Domain / Portal | Authority Level | Access Method | API Availability | Terms & Restrictions | Freshness |
| :--- | :---: | :--- | :---: | :--- | :--- |
| **eCourts Services** | Level 1 (Primary) | Official Web Portal / Public Search | Limited Official API | Permitted public case status lookup only | Real-time |
| **Kaveri 2.0 (Karnataka Land Records)** | Level 1 (Primary) | State Government Portal | Web Portal / Mock Adapter | Public property search & EC verification | Daily |
| **MahaBhulekh (Maharashtra Land Records)** | Level 1 (Primary) | State Government Portal | Web Portal / Mock Adapter | 7/12 extract & mutation entry search | Daily |
| **MahaRERA / RERA Karnataka** | Level 2 (Govt) | State RERA Portal | Web Portal / Mock Adapter | Approved project registration & orders | Weekly |
| **MCA21 (Ministry of Corporate Affairs)** | Level 2 (Govt) | Public Portal | Official Web Portal | Company master data & charge search | Real-time |
| **Official Gazette of India** | Level 1 (Primary) | eGazette Portal | Public PDF Repository | Public notification repository | Monthly |

---

## 2. Integration Safety & Compliance Policy
1. **No Unrestricted Scraping**: Scraping arbitrary commercial websites or bypassing CAPTCHAs/paywalls is strictly forbidden.
2. **Mock-First Architecture**: Development and automated testing utilize mock adapters (`MockCourtAdapter`, `MockPropertyAdapter`) to guarantee deterministic execution at zero API cost.
3. **Source Verification Gate**: Public data is never assumed 100% current or authoritative; every external item is tagged with a `VerificationStatus` (`VERIFIED`, `SOURCE_RETRIEVED`, `UNVERIFIED`, `OUTDATED`).
