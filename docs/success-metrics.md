# Quantitative Success Metrics

## Core Performance & Accuracy Targets

| Metric | Target / Benchmark | Measurement Methodology |
| :--- | :--- | :--- |
| **Document Processing Success** | > 99.0% | Percentage of uploaded document bundles processed without system error |
| **OCR Accuracy (English/Indic)** | > 95.0% Character Accuracy | Character error rate (CER) test suite against benchmark ground-truth legal scans |
| **Retrieval Accuracy (Recall@k=5)** | > 90.0% | Evaluation dataset of legal queries mapped to ground-truth document passages |
| **Citation Correctness** | 100.0% Verifiable | Zero citations pointing to non-existent or inaccurate source page/snippet |
| **Hallucination Rate** | < 1.0% | Faithfulness benchmark evaluated on RAG evaluation test set (Ragas/TruLens framework) |
| **Time Saved per Title Report** | > 60% Reduction | Baseline manual review (~8 hrs) vs AI-assisted review (~2.5 hrs including human review) |
| **Human Correction Rate** | < 15% of Extracted Fields | Percentage of AI entity extractions modified by human reviewer during verification |
| **Workflow Completion Rate** | > 85.0% | Percentage of created matters that proceed to final exported report |
| **Repeat Usage / Retention** | > 70.0% Weekly Active Advocates | Active matter creation and Q&A interactions week-over-week |
| **Cost per Matter Processed** | < ₹150 (~$1.80 USD) | Total LLM API + OCR processing infrastructure cost per 100-page bundle |
