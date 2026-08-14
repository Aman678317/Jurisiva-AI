# Chapter 9 — Validation Experiments Blueprint

## Overview
These 5 low-cost validation experiments test core assumptions before full backend engineering commitment.

---

## Experiment 1: Scanned Indic Deed OCR Accuracy Test
- **HYPOTHESIS**: Tesseract/PaddleOCR with Indic language models can achieve > 90% character accuracy on standard scanned Indian legal deeds (Hindi/Kannada/Marathi) after image binarization and deskewing.
- **USER**: Property Advocate / Internal QA.
- **TEST**: Process 20 real and synthetic scanned Indian land deed pages (150–200 DPI) through the open-source OCR preprocessing pipeline.
- **INPUT**: 20 scanned PDF/TIFF legal pages containing mixed English and regional Indic text.
- **EXPECTED RESULT**: Extracted text contains correct survey numbers, party names, and dates with minimal character error.
- **PASS THRESHOLD**: Character Error Rate (CER) <= 10.0% (Accuracy >= 90.0%) across test set.
- **FAIL THRESHOLD**: CER > 15.0% on standard 150 DPI scans.
- **TIME REQUIRED**: 3 days.
- **COST**: ₹0 (Open source tools on local dev machine).
- **NEXT ACTION**: If PASS -> Integrate PaddleOCR/Tesseract into ingestion pipeline; If FAIL -> Add specialized LLM vision OCR fallback (e.g. Qwen-VL / Claude Vision API).

---

## Experiment 2: Automated Title Flow Timeline Accuracy
- **HYPOTHESIS**: RAG + structured LLM extraction can construct an error-free chronological title chain from a 10-document property bundle with zero missing link deed hallucination.
- **USER**: Senior Property Advocate.
- **TEST**: Benchmark AI title flow timeline generation against 5 manually verified ground-truth property matter bundles.
- **INPUT**: 5 ground-truth legal matter bundles (total 75 documents).
- **EXPECTED RESULT**: AI correctly orders every transaction date, identifies executant/claimant pairs, and flags intentional missing link deeds.
- **PASS THRESHOLD**: 100% detection of missing link deeds; >= 95% accuracy on transaction dates and party pairings.
- **FAIL THRESHOLD**: < 90% date accuracy or any false negative on a missing link deed.
- **TIME REQUIRED**: 4 days.
- **COST**: ~₹300 (LLM API cost for evaluation runs).
- **NEXT ACTION**: If PASS -> Lock title flow timeline schema; If FAIL -> Refine Pydantic extraction prompts and few-shot legal examples.

---

## Experiment 3: Split-Screen Citation Trust & UX Perception Test
- **HYPOTHESIS**: Advocates will express high trust (> 4.5/5.0) in AI answers when presented with a split-screen viewer that automatically highlights the source bounding box on the original PDF upon clicking a citation badge.
- **USER**: 8 Independent Property Advocates.
- **TEST**: Interactive click-through prototype testing on synthetic legal matters. Advocate clicks citations to verify answers.
- **INPUT**: Interactive frontend wireframe / prototype with synthetic matter data.
- **EXPECTED RESULT**: Advocates navigate directly to highlighted source text and confirm verification speed.
- **PASS THRESHOLD**: Average Trust & UX Rating >= 4.2 / 5.0; 100% of participants confirm citation clicks are mandatory for daily work.
- **FAIL THRESHOLD**: Average Trust Rating < 3.5 / 5.0.
- **TIME REQUIRED**: 5 days (Interviews).
- **COST**: ₹0 (Direct founder interviews).
- **NEXT ACTION**: If PASS -> Standardize split-screen layout across all MVP views; If FAIL -> Modify highlight color, zoom padding, and bounding box interaction.

---

## Experiment 4: Per-Matter Pricing & Willingness-to-Pay (WTP) Validation
- **HYPOTHESIS**: Independent Advocates will agree to pay ₹150 – ₹300 per property matter processed rather than subscribing to expensive monthly seat licenses.
- **USER**: 12 Property Advocates / Small Legal Firms.
- **TEST**: Present 3 pricing options (Monthly Subscription ₹5,000/mo vs Per-Matter ₹200 vs Free Tier with paid exports) during user research interviews.
- **INPUT**: Pricing card sheet with feature breakdown.
- **EXPECTED RESULT**: Over 70% of Advocates select the Per-Matter or Pay-Per-Export option as their preferred model.
- **PASS THRESHOLD**: >= 65% preference for Per-Matter / Usage pricing; at least 5 Advocates request early pilot onboarding.
- **FAIL THRESHOLD**: Severe pushback against per-matter pricing (< 40% acceptance).
- **TIME REQUIRED**: 3 days (Integrated into research interviews).
- **COST**: ₹0.
- **NEXT ACTION**: If PASS -> Implement wallet/per-matter credit backend architecture; If FAIL -> Re-evaluate tier-based seat model.

---

## Experiment 5: Contradiction & Extent Discrepancy Detection Accuracy
- **HYPOTHESIS**: Automated cross-document prompt heuristics will reliably detect 100% of injected extent mismatches (e.g. Sale Deed 2400 sq.ft vs Pahani 2100 sq.ft) in test bundles.
- **USER**: QA / Test Harness.
- **TEST**: Run contradiction detection pipeline on 10 synthetic property bundles containing 15 seeded legal/extent discrepancies.
- **INPUT**: 10 synthetic matter bundles with known seeded contradictions.
- **EXPECTED RESULT**: System generates red-flag alerts for all 15 seeded contradictions with zero missed critical defects.
- **PASS THRESHOLD**: Recall = 100% on critical extent/boundary contradictions; Precision >= 80% (low false positives).
- **FAIL THRESHOLD**: Recall < 90% (missing a critical extent defect).
- **TIME REQUIRED**: 3 days.
- **COST**: ~₹200 (LLM API evaluation cost).
- **NEXT ACTION**: If PASS -> Lock contradiction detection rules; If FAIL -> Add explicit schema-level normalization before cross-checking.
