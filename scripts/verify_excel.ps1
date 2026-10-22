# Requires Windows and a licensed, working Microsoft Excel Desktop installation.
# -SelfTest checks the verifier without opening Excel; it is NOT native validation.
[CmdletBinding()]
param([switch]$SelfTest)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$root = Split-Path $PSScriptRoot -Parent
$cases = @(Get-Content (Join-Path $root 'tests/fixtures/excel_cases.json') -Raw | ConvertFrom-Json)

function Test-Outputs($Actual, $Expected) {
    if (@($Actual).Count -ne @($Expected).Count) { return $false }
    for ($i = 0; $i -lt @($Expected).Count; $i++) {
        $a = $Actual[$i]; $e = $Expected[$i]
        if ($e -is [string]) {
            if ($a -isnot [string] -or $a -cne $e) { return $false }
        } else {
            if ($null -eq $a -or $a -is [string] -or $a -is [bool]) { return $false }
            $v = [double]$a
            if ([double]::IsNaN($v) -or [double]::IsInfinity($v)) { return $false }
            if ([Math]::Abs($v - [double]$e) -gt 0.000001) { return $false }
        }
    }
    return $true
}
if ($SelfTest) {
    foreach ($case in $cases) {
        if (@($case.inputs).Count -ne 5 -or @($case.expected).Count -ne 5) { throw 'Invalid fixture dimensions' }
        if (-not (Test-Outputs $case.expected $case.expected)) { throw 'Valid result rejected' }
    }
    if (Test-Outputs @(0, 0, 0, 0, 0) $cases[0].expected) { throw 'Wrong results accepted' }
    foreach ($bad in @($null, '2200000', $true, [double]::NaN, [double]::PositiveInfinity)) {
        if (Test-Outputs @($bad) @(2200000)) { throw 'Nonnumeric/error output accepted' }
    }
    Write-Host 'Verifier self-test PASS. Excel Desktop was NOT run.'
    exit 0
}

$source = Join-Path $root 'excel/ThirstyAI_Audit.xlsx'
$stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')
$out = Join-Path $root "outputs/excel-validation/$stamp"
[void](New-Item -ItemType Directory -Path $out -Force)
$copy = Join-Path $out 'working-copy.xlsx'
Copy-Item $source $copy
$report = [ordered]@{
    status = 'NOT_RUN'; engine = 'Microsoft Excel Desktop COM'; utc = [DateTime]::UtcNow.ToString('o')
    workbook_sha256 = (Get-FileHash $source -Algorithm SHA256).Hash.ToLowerInvariant()
    os_version = [Environment]::OSVersion.VersionString
    excel_version = $null; excel_build = $null; automatic_calculation = $false
    cases = @(); reopened_baseline = $false; original_unchanged = $false
    author_confirmation = 'PENDING'; screenshots = 'PENDING'; error = $null
}
$excel = $null; $book = $null; $sheet = $null
$exitCode = 1
function Read-Outputs($Sheet) {
    $result = @()
    for ($row = 7; $row -le 11; $row++) {
        $cell = $Sheet.Range("F$row")
        try { $result += $cell.Value2 }
        finally { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($cell) }
    }
    return ,$result
}
function Recalculate($Excel) {
    $Excel.CalculateFullRebuild()
    $deadline = [DateTime]::UtcNow.AddSeconds(30)
    while ($Excel.CalculationState -ne 0) {
        if ([DateTime]::UtcNow -gt $deadline) { throw 'Calculation did not finish in 30 seconds' }
        Start-Sleep -Milliseconds 100
    }
}
function Set-Inputs($Sheet, $Values) {
    for ($i = 0; $i -lt 5; $i++) {
        $cell = $Sheet.Range("B$($i + 7)")
        if ($null -eq $Values[$i]) { [void]$cell.ClearContents() }
        elseif ($Values[$i] -is [string]) { $cell.Value2 = [string]$Values[$i] }
        else { $cell.Value2 = [double]$Values[$i] }
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($cell)
    }
}
try {
    if ($env:OS -ne 'Windows_NT') { throw 'Windows with Excel Desktop is required' }
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $excel.AutomationSecurity = 3 # Force-disable macros in this new test instance.
    $excel.EnableEvents = $false
    $book = $excel.Workbooks.Open($copy, 0, $false) # Do not update external links.
    $excel.Calculation = -4105 # xlCalculationAutomatic
    $report.automatic_calculation = ($excel.Calculation -eq -4105)
    $report.excel_version = [string]$excel.Version
    $report.excel_build = [string]$excel.Build
    $sheet = $book.Worksheets.Item('Calculator')
    for ($row = 7; $row -le 11; $row++) {
        if (-not $sheet.Range("F$row").HasFormula) { throw "F$row is not a formula" }
    }
    foreach ($case in $cases) {
        Set-Inputs $sheet $case.inputs
        Recalculate $excel
        $actual = Read-Outputs $sheet
        $pass = Test-Outputs $actual $case.expected
        $report.cases += [ordered]@{ name = $case.name; inputs = @($case.inputs); expected = @($case.expected); actual = @($actual); pass = $pass }
        Write-Host "$($case.name): $(if ($pass) { 'PASS' } else { 'FAIL' })"
    }
    Set-Inputs $sheet $cases[0].inputs
    Recalculate $excel
    $book.Save()
    [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($sheet); $sheet = $null
    $book.Close($false)
    [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($book); $book = $null
    $book = $excel.Workbooks.Open($copy, 0, $false)
    $sheet = $book.Worksheets.Item('Calculator')
    Recalculate $excel
    $report.reopened_baseline = Test-Outputs (Read-Outputs $sheet) $cases[0].expected
    $report.original_unchanged = ((Get-FileHash $source -Algorithm SHA256).Hash.ToLowerInvariant() -eq $report.workbook_sha256)
    $failed = @($report.cases | Where-Object { -not $_.pass })
    if ($failed.Count -eq 0 -and $report.reopened_baseline -and $report.original_unchanged -and $report.automatic_calculation) {
        $report.status = 'PASS'; $exitCode = 0
    } else { $report.status = 'FAIL' }
} catch {
    $report.status = 'BLOCKED_OR_ERROR'
    $report.error = $_.Exception.Message
    Write-Warning $report.error
} finally {
    if ($null -ne $sheet) { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($sheet) }
    if ($null -ne $book) {
        try { $book.Close($false) } finally { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($book) }
    }
    if ($null -ne $excel) {
        try { $excel.Quit() } finally { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($excel) }
    }
    [GC]::Collect(); [GC]::WaitForPendingFinalizers()
    $report | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $out 'report.json') -Encoding UTF8
    Write-Host "Evidence: $out/report.json"
    Write-Host 'Author confirmation and screenshots remain required before issue #5 closes.'
}
exit $exitCode
