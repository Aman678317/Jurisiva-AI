# Chapter 3 — India Opportunity Map & Ranking Matrix

## Evaluation Methodology & Scoring Criteria
Each candidate opportunity is scored from 1 (Lowest / Least Favorable) to 5 (Highest / Most Favorable) across 9 dimensions:
1. **PAIN**: Severity of user frustration and financial/time loss.
2. **FREQUENCY**: How often the workflow occurs in standard practice.
3. **WILLINGNESS TO PAY**: User budget availability and economic ROI.
4. **DATA AVAILABILITY**: Ease of user uploading required document bundles.
5. **TECHNICAL FEASIBILITY**: Viability using current OCR, RAG, and NLP models.
6. **LOW COMPETITION**: Absence of direct, dominant dedicated products (5 = minimal competition).
7. **LOW REGULATORY RISK**: Freedom from unauthorized practice of law barriers (5 = safe assistant model).
8. **AI ADVANTAGE**: Magnitude of efficiency gain from LLM + RAG automation.
9. **FAST TIME TO MVP**: Rapid execution speed for initial prototype (5 = fast).

---

## Opportunity Scoring Matrix

| Opportunity Domain | Pain | Freq | Pay | Data | Tech | Comp | RegRisk | AI Adv | MVP Speed | **Total Score (out of 45)** | Rank |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Property Title Due Diligence & Search** | 5 | 5 | 5 | 4 | 4 | 5 | 4 | 5 | 4 | **41** | **#1 (Primary MVP)** |
| **2. Litigation Case Bundle Fact Extraction** | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | **38** | **#2 (Secondary)** |
| **3. Commercial Lease & Agreement Abstraction**| 4 | 4 | 4 | 4 | 5 | 2 | 5 | 4 | 5 | **37** | **#3 (Later)** |
| **4. Regulatory Compliance Monitoring** | 3 | 3 | 3 | 3 | 4 | 3 | 3 | 3 | 3 | **28** | **#4 (Later)** |
| **5. Automated e-Courts Filing & Scraping** | 4 | 4 | 2 | 2 | 2 | 4 | 1 | 3 | 1 | **23** | **#5 (DO NOT BUILD YET)** |

---

## Detailed Rationale for Top 3 Opportunities

### #1 Primary MVP Candidate: Property Title Due Diligence & Search (Score: 41/45)
- **Why it wins**: Severe pain (8+ hours of manual deed reading per property transaction); very high frequency (millions of property transactions and home loans in India annually); high willingness to pay (lawyers charge ₹5,000 – ₹25,000 per title search report); direct data provided by client/bank; minimal specialized competition in India; clear AI advantage in entity extraction, chronological timeline building, and cross-deed extent contradiction detection.

### #2 Secondary Candidate: Litigation Case Bundle Fact & Timeline Extraction (Score: 38/45)
- **Why it follows**: High pain during trial preparation and written statement drafting; Advocates manage hundreds of pages of affidavits and cross-examinations. Serves as a natural expansion module once the core document viewer, OCR, and citation RAG pipeline are established.

### #3 Later Candidate: Commercial Lease & Agreement Abstraction (Score: 37/45)
- **Why deferred**: Well-served by corporate CLM tools (SpotDraft, SirionLabs) for large enterprises. Lower differentiation compared to property diligence and litigation bundles.

### Disqualified Candidate: Automated e-Courts Filing & Scraping (Score: 23/45)
- **Why disqualified**: Extremely high regulatory risk, CAPTCHA challenges, fragile government web portals, high technical failure rate, and zero control over upstream uptime. Violates key project principle: "Never invent APIs or rely on fragile web-scraping."
