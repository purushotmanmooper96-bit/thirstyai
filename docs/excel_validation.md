# Microsoft Excel Desktop validation checklist

The workbook is a v0.1 snapshot of the calculator and original source register, not the expanded v0.2 evidence database. Use CSV/JSON and SQL for the new company data. No claim of Excel Desktop validation is made until the author confirms it.

## Run the checks automatically in Excel Desktop

From your Windows checkout, with Microsoft Excel Desktop installed and activated:

```powershell
git pull --ff-only
python scripts/reproduce.py
.\scripts\verify_excel.ps1
```

The script starts a separate Excel instance, opens a working copy, sets automatic calculation and calls [CalculateFullRebuild](https://learn.microsoft.com/en-us/office/vba/api/excel.application.calculatefullrebuild). It runs the three cases below plus blank, text, invalid PUE, negative intensity and valid zero cases. It restores baseline, saves, reopens and recalculates, then writes `outputs/excel-validation/<UTC-run>/report.json` with Excel version/build, actual outputs and the original workbook's SHA-256. It does not upload anything, update limitations or close the issue. The original workbook is not edited. Macros and external-link updates are disabled in the test instance.

`PASS` means these machine checks passed in the installed Excel engine. Review the JSON, perform the remaining visual/India checks below, capture Calculator screenshots without personal data, and confirm the results in issue #5. `BLOCKED_OR_ERROR` or `FAIL` is not validation. Share the report if a discrepancy occurs.

CI runs ` .\scripts\verify_excel.ps1 -SelfTest` to check verifier logic **without Excel**. Python tests compare its fixture expectations to the Python engine and confirm shipped outputs contain formulas. Neither substitutes for the native run. The verifier's native COM path remains unverified until run on a machine with Excel Desktop.

## Manual checklist and visual confirmation

1. Open `excel/ThirstyAI_Audit.xlsx` in Microsoft Excel Desktop. Save a working copy.
2. **Formulas → Calculation Options → Automatic**. Press **Ctrl+Alt+F9** to recalculate all formulas. Do not merely inspect cached results.
3. On **Calculator**, enter each row below in B7:B11. Compare F7:F11 to the expected outputs. All are **ILLUSTRATIVE INPUTS — NOT MEASUREMENTS**; water means operational consumption, excludes manufacturing and may occur in different basins.

| Case | B7 IT MWh | B8 PUE | B9 WUE L/IT kWh | B10 grid L/facility kWh | B11 kg/facility kWh | F7 MWh | F8 direct L | F9 indirect L | F10 total L | F11 kg CO2e |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 1000 | 1.2 | 1 | 1 | 0.4 | 1200 | 1000000 | 1200000 | 2200000 | 480000 |
| Double work | 2000 | 1.2 | 1 | 1 | 0.4 | 2400 | 2000000 | 2400000 | 4400000 | 960000 |
| Alternative | 1000 | 1.4 | 0.1 | 1 | 0.4 | 1400 | 100000 | 1400000 | 1500000 | 560000 |

4. Clear B9: every output must say **Invalid input**. Restore it. Set PUE below 1 or a negative intensity: invalid. Zero workload is allowed and yields zero. Test a text cell; invalid. Check for `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?` using **Home → Find & Select → Find → Options → Look in: Values → Within: Workbook**.
5. Verify India has 36 state/UT rows. Stage (%) is already percentage points; do not use Excel Percentage formatting that multiplies by 100. It is all-use groundwater context, not AI extraction.
6. Restore baseline, save, close, reopen, recalculate. Record Excel version (**File → Account → About Excel**), date, all results and screenshots. Confirm each item to update the limitations record.

Python reference: `python scripts/reproduce.py`. Do not substitute withdrawal WUE, including Meta's published definition, for the consumptive model input.
