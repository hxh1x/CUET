# CUET SCQP09 Automated Test Suite

**Location:** `CUET_SCQP09_FINAL/TESTS/`  
**Purpose:** Regression testing, empirical data integrity validation, and content quality auditing for the CUET-PG SCQP09 package.

---

## 1. Test Suite Structure

The test suite is organized into three distinct verification domains:

1. **`test_data_integrity.py`:**
   - Validates that source question bank has exactly 225 records.
   - Validates that each of the three years (2024, 2025, 2026) contains exactly 75 questions.
   - Validates uniqueness of all 225 `(year, qno)` pairs.
   - Validates that `DATA/question_bank_v2.json` contains 225 objects, conforms to schema, and contains zero Hindi/Devanagari characters.
   - Validates that the taxonomy contains exactly 92 unique module IDs.

2. **`test_content_quality.py`:**
   - Validates that the pilot module (`M1_Sets_Venn_Inclusion_Exclusion.md`) exists.
   - Validates that all 19 required curriculum sections are present and non-empty.
   - Validates the presence of official PYQ source references (2024 Q26, 2025 Q17, 2025 Q19, 2026 Q21, 2026 Q39).
   - Validates standard source classification tags (`[SOURCE]`, `[DERIVED]`, `[SUPPLEMENTARY]`).

3. **`test_pipeline.py`:**
   - Validates that `05_SOURCE/taxonomy_data.py` contains exactly 92 entries in `ROWS`.
   - Validates that `05_SOURCE/classify_recent.py` contains 225 question entries across 2024, 2025, and 2026.
   - Validates syntax compilation and graceful fallback in `05_SOURCE/build_master_syllabus.py`.

---

## 2. How to Run the Tests

### Option A: Via PowerShell (Recommended for Windows)
No Python runtime or external pip packages are required. Native PowerShell handles all assertions:
```powershell
# Navigate to the package root
cd C:\Users\HXH1X\Downloads\new\new\CUET\CUET_SCQP09_FINAL

# Run all test suites
powershell -NoProfile -ExecutionPolicy Bypass -File TESTS/run_tests.ps1
```

### Option B: Via Python (pytest or unittest)
If Python 3.10+ is installed on Windows or Linux/WSL:
```bash
# Run all tests via unittest
python -m unittest discover TESTS -p "test_*.py" -v
```
