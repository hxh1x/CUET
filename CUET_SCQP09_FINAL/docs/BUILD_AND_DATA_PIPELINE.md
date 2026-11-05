# CUET SCQP09 Build & Data Pipeline Documentation

**Location:** `CUET_SCQP09_FINAL/docs/BUILD_AND_DATA_PIPELINE.md`  
**Target Package:** CUET-PG SCQP09 (Computer Science / MCA)  
**Maintained Under:** Canonical directory `CUET_SCQP09_FINAL/`  

---

## 1. Overview & System Architecture

The CUET SCQP09 preparation system processes 225 official NTA examination questions from the 2024, 2025, and 2026 test cycles (75 questions per year). The pipeline links these questions to a 92-module learning-ordered taxonomy and compiles:
1. `SCQP09_Master_Syllabus.html` (Full structured HTML document)
2. `SCQP09_Master_Syllabus_2024-2026.pdf` (50-page printable syllabus via WeasyPrint)
3. `SCQP09_Master_Taxonomy.csv` (92-row taxonomy with 2024–2026 question frequency counts)
4. `DATA/question_bank_v2.json` (Strictly English cleaned and structured question repository)

---

## 2. Legacy Directory Status Notice

> [!NOTE]
> The top-level folder `SCQP09_MASTER_SYLLABUS/` is a historical, legacy duplicate of `CUET_SCQP09_FINAL/01_MASTER_SYLLABUS` and `CUET_SCQP09_FINAL/05_SOURCE`. It is retained strictly for provenance and must **not** be used for ongoing development, generation, or editing. All production data, curriculum materials, and scripts reside in `CUET_SCQP09_FINAL/`.

---

## 3. Environment Prerequisites

The pipeline supports both **Python (Windows/Linux/WSL)** and **Native Windows PowerShell (PowerShell 5.1 / 7+)**:

### Option A: Running via PowerShell (Zero External Dependencies)
If Python is not installed or when running on standard Windows workstations:
```powershell
# Navigate to the canonical directory
cd C:\Users\HXH1X\Downloads\new\new\CUET\CUET_SCQP09_FINAL

# Execute the self-contained pipeline runner
powershell -NoProfile -ExecutionPolicy Bypass -File 05_SOURCE/run_pipeline.ps1
```

### Option B: Running via Python 3.10+
If Python 3.10+ is available on Windows or in WSL:
```bash
# 1. Ensure Python dependencies are installed
pip install weasyprint

# 2. Run the syllabus builder
python 05_SOURCE/build_master_syllabus.py
```

*Note on WeasyPrint Fallback:* `05_SOURCE/build_master_syllabus.py` has been updated with graceful degradation. If WeasyPrint or Cairo/Pango system libraries are absent, the script successfully builds the complete HTML syllabus and CSV taxonomy without raising an `ImportError`.

---

## 4. Pipeline Execution Steps & Commands

### Step 1: Data Cleaning & Normalization (English-Only Purification)
Purges OCR debris, removes all Devanagari/Hindi characters from question stems and options, resolves run-together words, extracts structured 4-option arrays, and produces `DATA/question_bank_v2.json`:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ../.gemini/antigravity/brain/9bb73bde-cbac-41b1-b3e3-3973186c14b6/scratch/generate_qb_v2.ps1
```

### Step 2: Taxonomy Integrity Verification
Validates that all 92 modules are defined, no duplicate IDs exist, all 225 questions are classified, and exactly zero orphan mappings exist:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ../.gemini/antigravity/brain/9bb73bde-cbac-41b1-b3e3-3973186c14b6/scratch/verify_tax_clean.ps1
```

### Step 3: Master Syllabus Generation
Runs the generator to produce `01_MASTER_SYLLABUS/SCQP09_Master_Syllabus.html` and `01_MASTER_SYLLABUS/SCQP09_Master_Taxonomy.csv`:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File 05_SOURCE/run_pipeline.ps1
```

### Step 4: Automated Testing
Executes comprehensive integrity and quality tests:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File TESTS/run_tests.ps1
```

---

## 5. Artifact Directory Mapping

| Source File | Destination Artifact | Verification Rule |
|---|---|---|
| `02_QUESTION_BANK/SCQP09_Question_Bank_2024-2026.csv` | Input to `build_master_syllabus.py` | Must have 225 rows, exactly 75 per year |
| `05_SOURCE/taxonomy_data.py` | `01_MASTER_SYLLABUS/SCQP09_Master_Taxonomy.csv` | Exactly 92 modules with priority codes |
| `05_SOURCE/build_master_syllabus.py` | `01_MASTER_SYLLABUS/SCQP09_Master_Syllabus.html` | Generated valid HTML5 document |
| `02_QUESTION_BANK/*.csv`, `*.json` | `DATA/question_bank_v2.json` | 225 JSON objects, strictly English |
