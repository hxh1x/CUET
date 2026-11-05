# CUET SCQP09 Data Validation Report

**Artifact:** `CUET_SCQP09_FINAL/DATA/question_bank_v2.json`  
**Date of Validation:** November 2026  
**Language Specification:** Strictly English-only (all Hindi/Devanagari scripts and multilingual OCR noise purged)  

---

## 1. Summary of Question Counts

| Metric | Target | Actual | Status |
|---|---|---|---|
| **Total Question Records** | 225 | 225 | **PASS** |
| **Year 2024 Count** | 75 | 75 | **PASS** |
| **Year 2025 Count** | 75 | 75 | **PASS** |
| **Year 2026 Count** | 75 | 75 | **PASS** |
| **Unique ID Count (YYYY_Qxxx)** | 225 | 225 | **PASS** |
| **Duplicate IDs** | 0 | 0 | **PASS** |

---

## 2. Quality & Extraction Assessment

| Assessment Category | Count | Percentage | Description / Handling |
|---|---|---|---|
| **Clean / Medium Confidence** | 192 | 85.3% | Auto-classified, clean text with no detectable OCR noise. |
| **Flagged for Manual Review (Low Confidence)** | 33 | 14.7% | Questions containing run-together words, double commas, or stripped bilingual noise in raw OCR. |
| **Options Successfully Structured** | 126 | 56% | Distinct 4-option array parsed and structured for learner assessment. |
| **Figure / Diagram Dependent** | 13 | 5.8% | Figure matrix, circuit diagram, or spatial reasoning questions referencing external visual diagrams in the source PDF. |
| **Language Conformity** | 225 | 100.0% | 100% strictly English. Zero Hindi/Devanagari characters remain in `question_text_clean`. |

---

## 3. Schema Fields Verification

All 225 records strictly adhere to the enhanced schema:
- `question_id`: Format `{year}_Q{qno:D3}` (e.g., `2024_Q001` through `2026_Q075`)
- `year`: Integer (2024, 2025, or 2026)
- `qno`: Integer (1 to 75)
- `subject`: Subject domain string
- `topic`: Topic area string
- `subtopic`: Granular subtopic string
- `question_text_clean`: Curated, normalized English text
- `question_text_original`: Raw OCR snapshot for provenance
- `options`: Array of 4 option strings or null
- `source_pdf`: Canonical source PDF file name
- `source_page`: `"unknown"`
- `figure_ref`: `"figure_in_source"` or null
- `extraction_confidence`: `"low"` or `"medium"`
- `review_status`: `"needs_manual_review"` or `"auto_classified"`
- `official_answer`: null (NTA official answer key not published in source data)
- `derived_answer`: null (reserved for mathematically verified solutions)
- `explanation`: null (reserved for curriculum module lessons)
- `concepts_tested`: `[subject, topic, subtopic]`
- `difficulty`: null (reserved for empirical assessment metrics)

---

## 4. Subject & Topic Coverage

| Subject | 2024 | 2025 | 2026 | Total | % of Exam |
|---|---|---|---|---|---|
| **Mathematics** | 30 | 20 | 20 | 70 | 31.1% |
| **Thinking & Decision Making** | 15 | 15 | 20 | 50 | 22.2% |
| **Data Structures & Algorithms** | 14 | 19 | 15 | 48 | 21.3% |
| **Operating Systems** | 10 | 11 | 9 | 30 | 13.3% |
| **Digital Fundamentals** | 5 | 10 | 11 | 26 | 11.6% |
| **Rare / Legacy CS (DBMS/CN)** | 1 | 0 | 0 | 1 | 0.4% |
| **Total** | **75** | **75** | **75** | **225** | **100.0%** |