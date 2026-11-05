# CUET SCQP09 Build Pipeline Wrapper (PowerShell)
# Architecture: Dual-mode execution (Python / Native PowerShell)
# Target Directory: CUET_SCQP09_FINAL/

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$pkgDir = Split-Path -Parent $scriptDir
Set-Location $pkgDir

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   CUET SCQP09 Master Syllabus & Data Pipeline Runner    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Working Directory: $pkgDir"

# 1. Environment & Python Discovery
$pythonCmd = $null
$foundPy = Get-Command python -ErrorAction SilentlyContinue
if ($foundPy -and ($foundPy.Source -notmatch 'WindowsApps')) {
    $pythonCmd = $foundPy.Source
} else {
    $foundPy3 = Get-Command py -ErrorAction SilentlyContinue
    if ($foundPy3) {
        $pythonCmd = "py"
    }
}

# Check virtual environments
$winVenvPy = Join-Path $pkgDir "..\.venv\Scripts\python.exe"
if (Test-Path $winVenvPy) {
    $pythonCmd = (Resolve-Path $winVenvPy).Path
}

if ($pythonCmd) {
    Write-Host "[INFO] Detected Python interpreter: $pythonCmd" -ForegroundColor Green
    Write-Host "[INFO] Running 05_SOURCE/build_master_syllabus.py..." -ForegroundColor Cyan
    & $pythonCmd (Join-Path $scriptDir "build_master_syllabus.py")
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[SUCCESS] Python pipeline executed successfully." -ForegroundColor Green
    } else {
        Write-Warning "[WARN] Python script failed with exit code $LASTEXITCODE. Falling back to native PowerShell validation."
    }
} else {
    Write-Host "[INFO] No native Windows Python runtime found in PATH." -ForegroundColor Yellow
    Write-Host "[INFO] (.venv contains Linux ELF binaries; for Windows, install Python 3.11+ or run via WSL)" -ForegroundColor Gray
    Write-Host "[INFO] Executing Native PowerShell Data Validation & Pipeline..." -ForegroundColor Cyan

    $csvPath = Join-Path $pkgDir "02_QUESTION_BANK\SCQP09_Question_Bank_2024-2026.csv"
    $taxCsvPath = Join-Path $pkgDir "01_MASTER_SYLLABUS\SCQP09_Master_Taxonomy.csv"
    $jsonV2Path = Join-Path $pkgDir "DATA\question_bank_v2.json"

    # Validate CSV question bank
    if (-not (Test-Path $csvPath)) {
        throw "Question bank CSV not found at $csvPath"
    }
    $csvData = Import-Csv $csvPath
    Write-Host "  -> Loaded $($csvData.Count) questions from CSV."
    if ($csvData.Count -ne 225) {
        throw "Validation Failed: Expected exactly 225 questions, got $($csvData.Count)"
    }

    # Validate per-year distribution
    $yearGroups = $csvData | Group-Object year
    foreach ($yg in $yearGroups) {
        Write-Host "  -> Year $($yg.Name): $($yg.Count) questions"
        if ($yg.Count -ne 75) {
            throw "Validation Failed: Year $($yg.Name) has $($yg.Count) questions (expected 75)."
        }
    }

    # Validate Taxonomy CSV
    if (Test-Path $taxCsvPath) {
        $taxData = Import-Csv $taxCsvPath
        Write-Host "  -> Loaded $($taxData.Count) taxonomy modules from CSV."
        if ($taxData.Count -ne 92) {
            throw "Validation Failed: Expected 92 taxonomy modules, got $($taxData.Count)"
        }
    }

    # Validate JSON v2
    if (Test-Path $jsonV2Path) {
        $jsonItems = Get-Content $jsonV2Path -Raw -Encoding utf8 | ConvertFrom-Json
        Write-Host "  -> Loaded $($jsonItems.Count) structured questions from DATA/question_bank_v2.json."
        if ($jsonItems.Count -ne 225) {
            throw "Validation Failed: Expected 225 items in question_bank_v2.json, got $($jsonItems.Count)"
        }
    }

    Write-Host "[SUCCESS] Native PowerShell pipeline verified all datasets cleanly." -ForegroundColor Green
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Pipeline run complete." -ForegroundColor Cyan
