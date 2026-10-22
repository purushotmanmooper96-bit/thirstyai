$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
python -m http.server 8000 --directory dist
