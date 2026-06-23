#Requires -Version 5.1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -q -r requirements_lock.txt
}
$env:PYTHONPATH = "$Root\src\python"
$py = ".\.venv\Scripts\python.exe"
& $py tools\fetch_hydrogen_data.py --demo
& $py tools\verify_audit.py
Write-Host "=== EGS-NLRF PIPELINE COMPLETE ==="
