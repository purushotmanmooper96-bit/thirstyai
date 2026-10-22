$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
python scripts/reproduce.py
if ($LASTEXITCODE -ne 0) { throw 'Reproduction failed. Review the output above.' }
