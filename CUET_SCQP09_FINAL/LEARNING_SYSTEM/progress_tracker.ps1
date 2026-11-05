param(
    [string]$Command = "summary",
    [string]$ProfilePath = "learner_progress.json",
    [string]$Id = "STU_001",
    [string]$Name = "Learner",
    [string]$Module = "M1",
    [string]$Status = "in_progress",
    [int]$Tier = 1,
    [int]$Level = 3,
    [int]$Score = 8,
    [int]$Total = 10,
    [int]$Speed = 60
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not [System.IO.Path]::IsPathRooted($ProfilePath)) {
    $ProfilePath = Join-Path $scriptDir $ProfilePath
}

function Load-Profile([string]$path) {
    if (-not (Test-Path $path)) { return $null }
    return Get-Content $path -Raw -Encoding utf8 | ConvertFrom-Json
}

function Save-Profile([string]$path, $data) {
    $data.last_active = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    $json = ConvertTo-Json -InputObject $data -Depth 10
    [System.IO.File]::WriteAllText($path, $json, [System.Text.Encoding]::UTF8)
}

if ($Command -eq "init") {
    $now = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    $profile = [ordered]@{
        learner_id = $Id
        name = $Name
        created_at = $now
        last_active = $now
        target_exam_date = "2027-03-15"
        target_score_percentile = 99.0
        overall_completion_pct = 0.0
        module_records = [ordered]@{}
        assessment_history = @()
    }
    Save-Profile $ProfilePath $profile
    Write-Host "[OK] Initialized learner profile for $Name ($Id) at $ProfilePath" -ForegroundColor Green
}
elseif ($Command -eq "summary") {
    $profile = Load-Profile $ProfilePath
    if (-not $profile) {
        Write-Warning "Profile not found at $ProfilePath. Initializing demo profile..."
        $examplePath = Join-Path $scriptDir "progress_example.json"
        if (Test-Path $examplePath) {
            $profile = Load-Profile $examplePath
        } else {
            Write-Error "No profile found."
            return
        }
    }
    Write-Host "`n============================================================" -ForegroundColor Cyan
    Write-Host "  CUET SCQP09 Progress Summary: $($profile.name) ($($profile.learner_id))" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "Overall Progress: $($profile.overall_completion_pct)% of 92 modules mastered/competent"
    Write-Host "Total Assessments Recorded: $($profile.assessment_history.Count)"

    Write-Host "`nActive Modules in Profile:"
    foreach ($prop in $profile.module_records.PSObject.Properties) {
        $m = $prop.Value
        Write-Host "  [$($m.module_id)] Status: $($m.status.ToUpper()), Tier: $($m.mastery_tier)/5, Best Score: $($m.best_score_pct)%"
    }
    Write-Host "============================================================`n" -ForegroundColor Cyan
}
