# Issue 5: Microsoft Excel Desktop confirmation

Status: **open — requires the author's Microsoft Excel Desktop run**. This environment cannot operate that application. No native version/date/screenshots or successful Desktop recalculation are invented. The shipped workbook is still the documented older snapshot; authoring-runtime checks and Python parity do not satisfy this issue.

The concrete work is prepared in [excel_validation.md](../excel_validation.md): exact input cells, three expected output sets, full recalculation, invalid/blank/text inputs, save/reopen checks and the version/date evidence to report. Do not upload passwords or unrelated personal data. No change is made to the historical limitations record without the author's confirmation.

PowerShell from the public checkout:

```powershell
python scripts/reproduce.py
.\scripts\verify_excel.ps1
Start-Process .\excel\ThirstyAI_Audit.xlsx
```

In Excel choose Formulas → Calculation Options → Automatic, then press Ctrl+Alt+F9. Follow the three cases and invalid-input checks in the linked checklist. Reply to issue #5 with Excel version/date, observed outputs and screenshots; discrepancies should be fixed before marking it complete.

The new verifier automates native cases and save/reopen on a working copy and writes actual engine results to JSON. Its fixture/comparison tests run in CI, including Windows PowerShell. This prepares the native check; it does not establish that native Excel has run. See the linked checklist for report location and remaining visual/author confirmation.
