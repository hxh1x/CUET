# CUET SCQP09 Automated Test Suite Runner (PowerShell)
# Architecture: Native Windows PowerShell Test Runner + Python Integration

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$pkgDir = Split-Path -Parent $scriptDir
Set-Location $pkgDir

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "       CUET SCQP09 Automated QA Test Suite Runner        " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$testResults = @()
$totalPassed = 0
$totalFailed = 0

function Assert-Test([string]$suite, [string]$name, [scriptblock]$condition) {
    try {
        $result = & $condition
        if ($result -eq $false) {
            throw "Condition evaluated to false."
        }
        $script:totalPassed++
        Write-Host "  [PASS] $suite :: $name" -ForegroundColor Green
        $script:testResults += [PSCustomObject]@{ Suite = $suite; Test = $name; Status = "PASS"; Message = "OK" }
    } catch {
        $script:totalFailed++
        Write-Host "  [FAIL] $suite :: $name - $($_.Exception.Message)" -ForegroundColor Red
        $script:testResults += [PSCustomObject]@{ Suite = $suite; Test = $name; Status = "FAIL"; Message = $_.Exception.Message }
    }
}

# -------------------------------------------------------------
# SUITE 1: DATA INTEGRITY TESTS
# -------------------------------------------------------------
Write-Host "`n--- Running Suite 1: Data Integrity ---" -ForegroundColor Yellow

$csvPath = Join-Path $pkgDir "02_QUESTION_BANK\SCQP09_Question_Bank_2024-2026.csv"
$jsonV2Path = Join-Path $pkgDir "DATA\question_bank_v2.json"
$taxCsvPath = Join-Path $pkgDir "01_MASTER_SYLLABUS\SCQP09_Master_Taxonomy.csv"

Assert-Test "DataIntegrity" "CSV File Exists" { Test-Path $csvPath }

$csvData = Import-Csv $csvPath
Assert-Test "DataIntegrity" "Total Question Count == 225" { $csvData.Count -eq 225 }

$yearCounts = $csvData | Group-Object year
Assert-Test "DataIntegrity" "Year 2024 has exactly 75 questions" { ($yearCounts | Where-Object { $_.Name -eq '2024' }).Count -eq 75 }
Assert-Test "DataIntegrity" "Year 2025 has exactly 75 questions" { ($yearCounts | Where-Object { $_.Name -eq '2025' }).Count -eq 75 }
Assert-Test "DataIntegrity" "Year 2026 has exactly 75 questions" { ($yearCounts | Where-Object { $_.Name -eq '2026' }).Count -eq 75 }

Assert-Test "DataIntegrity" "All 225 Year/Qno pairs are unique" {
    $set = [System.Collections.Generic.HashSet[string]]::new()
    $unique = $true
    foreach ($r in $csvData) {
        $key = "$($r.year)_$($r.qno)"
        if (-not $set.Add($key)) { $unique = $false; break }
    }
    return ($unique -and ($set.Count -eq 225))
}

Assert-Test "DataIntegrity" "question_bank_v2.json exists" { Test-Path $jsonV2Path }

$jsonV2Data = Get-Content $jsonV2Path -Raw -Encoding utf8 | ConvertFrom-Json
Assert-Test "DataIntegrity" "question_bank_v2.json has exactly 225 objects" { $jsonV2Data.Count -eq 225 }

Assert-Test "DataIntegrity" "question_bank_v2.json contains 0 Hindi/Devanagari characters in cleaned text" {
    $hindiCount = 0
    foreach ($q in $jsonV2Data) {
        if ($q.question_text_clean -match '[\u0900-\u097F]') { $hindiCount++ }
    }
    return ($hindiCount -eq 0)
}

Assert-Test "DataIntegrity" "Taxonomy has exactly 92 unique module IDs" {
    $taxData = Import-Csv $taxCsvPath
    $taxIds = $taxData | Select-Object -ExpandProperty id
    $uniqueIds = $taxIds | Select-Object -Unique
    return (($taxData.Count -eq 92) -and ($uniqueIds.Count -eq 92))
}

# -------------------------------------------------------------
# SUITE 2: CONTENT QUALITY TESTS (PILOT MODULE M1)
# -------------------------------------------------------------
Write-Host "`n--- Running Suite 2: Content Quality (Module M1) ---" -ForegroundColor Yellow

$m1Path = Join-Path $pkgDir "CURRICULUM\modules\M1_Sets_Venn_Inclusion_Exclusion.md"
Assert-Test "ContentQuality" "Pilot Module M1 File Exists" { Test-Path $m1Path }

$m1Text = [System.IO.File]::ReadAllText($m1Path, [System.Text.Encoding]::UTF8)

$required19Sections = @(
    "1. Module Identity & Overview",
    "2. Prerequisites",
    "3. Learning Objectives",
    "4. Required Prior Knowledge",
    "5. Detailed Concept Explanations",
    "6. Terminology & Formal Definitions",
    "7. Mathematical Foundations & Term-by-Term Formulas",
    "8. Visual Explanations (ASCII Venn Diagrams)",
    "9. Worked Examples (Step-by-Step with Full Computations)",
    "10. Common Misconceptions",
    "11. Common Mistakes & Exam Pitfalls",
    "12. Progressive Exercises (12 Structured Drills)",
    "13. Practical Assignment: University Course Enrollment Survey",
    "14. Knowledge-Check Questions (5 MCQs with Explanations)",
    "15. Independent Mastery Assessment (10 Exam-Level Questions)",
    "16. Assessment Rubric & Mastery Criteria",
    "17. Revision Material: Quick-Reference Formula Card",
    "18. Source References",
    "19. Source Category Labels"
)

foreach ($sec in $required19Sections) {
    $prefix = $sec.Substring(0, $sec.IndexOf('.'))
    Assert-Test "ContentQuality" "M1 contains Section $prefix" {
        $m1Text -match "##\s+$prefix\."
    }
}

Assert-Test "ContentQuality" "M1 contains all 5 Source PYQ references" {
    $pyqs = @("2024 Q26", "2025 Q17", "2025 Q19", "2026 Q21", "2026 Q39")
    $allPresent = $true
    foreach ($p in $pyqs) {
        if ($m1Text -notmatch [regex]::Escape($p)) { $allPresent = $false; break }
    }
    return $allPresent
}

Assert-Test "ContentQuality" "M1 contains category tags [SOURCE], [DERIVED], [SUPPLEMENTARY]" {
    return (($m1Text -match '\[SOURCE\]') -and ($m1Text -match '\[DERIVED\]') -and ($m1Text -match '\[SUPPLEMENTARY\]'))
}

# -------------------------------------------------------------
# SUITE 3: PIPELINE & SCRIPT INTEGRITY
# -------------------------------------------------------------
Write-Host "`n--- Running Suite 3: Pipeline & Scripts ---" -ForegroundColor Yellow

$buildPyPath = Join-Path $pkgDir "05_SOURCE\build_master_syllabus.py"
$taxPyPath = Join-Path $pkgDir "05_SOURCE\taxonomy_data.py"
$classifyPyPath = Join-Path $pkgDir "05_SOURCE\classify_recent.py"

Assert-Test "Pipeline" "build_master_syllabus.py exists and has WeasyPrint fallback" {
    $text = [System.IO.File]::ReadAllText($buildPyPath, [System.Text.Encoding]::UTF8)
    return ($text -match 'HAS_WEASYPRINT' -and $text -match 'assert len\(questions\) == 225')
}

Assert-Test "Pipeline" "taxonomy_data.py defines exactly 92 module rows" {
    $text = [System.IO.File]::ReadAllText($taxPyPath, [System.Text.Encoding]::UTF8)
    $m = [regex]::Matches($text, '(?s)dict\s*\(\s*id="([^"]+)"')
    return ($m.Count -eq 92)
}

Assert-Test "Pipeline" "classify_recent.py contains 225 question classifications" {
    $text = [System.IO.File]::ReadAllText($classifyPyPath, [System.Text.Encoding]::UTF8)
    $m = [regex]::Matches($text, '\d+:\s*\("([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\)')
    return ($m.Count -eq 225)
}

# -------------------------------------------------------------
# SUMMARY REPORT
# -------------------------------------------------------------
Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "                    TEST RUN RESULTS                      " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "TOTAL TESTS RUN : $($testResults.Count)"
Write-Host "TESTS PASSED    : $totalPassed" -ForegroundColor Green
Write-Host "TESTS FAILED    : $totalFailed" -ForegroundColor $(if ($totalFailed -eq 0) { "Green" } else { "Red" })
Write-Host "==========================================================" -ForegroundColor Cyan

if ($totalFailed -gt 0) {
    exit 1
} else {
    exit 0
}
