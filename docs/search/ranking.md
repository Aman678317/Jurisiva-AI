# Reciprocal Rank Fusion (RRF) Ranking Strategy

## RRF Merging Formula
When combining lexical BM25 search candidates and vector cosine similarity search candidates:

$$RRF\_Score(d) = \frac{1}{k + Rank_{lexical}(d)} + \frac{1}{k + Rank_{semantic}(d)}$$

Where $k = 60$ (standard smoothing constant).

---

## Ranking & Diversity Rules
1. **Identifier Precision Overboost**: If a query contains an exact Survey Number or Registration Number, candidate chunks containing that exact token receive a $+0.25$ score boost.
2. **Page Diversity Penalty**: To prevent 10 nearly identical chunks from page 1 dominating the top-5 results, subsequent chunks from the same page receive a $0.85\times$ penalty factor, ensuring candidate diversity across deeds.
