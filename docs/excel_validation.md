# Microsoft Excel Desktop validation checklist

The workbook is a v0.1 snapshot of the calculator and original source register, not the expanded v0.2 evidence database. Use CSV/JSON and SQL for the new company data. No claim of Excel Desktop validation is made until the author confirms it.

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
