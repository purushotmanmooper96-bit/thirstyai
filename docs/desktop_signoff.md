# Finish the native Desktop checks

These checks require your installed Windows applications. There is no Excel or Power BI Desktop engine in the execution environment used for this repository work. Automated tests, formula caches and prepared files cannot establish that these applications recalculated or rendered correctly.

## Excel — issue #5

```powershell
git pull --ff-only
python scripts/reproduce.py
.\scripts\verify_excel.ps1
```

Use [the Excel checklist](excel_validation.md) for the three expected numeric cases and invalid-input cases. Review the generated `outputs/excel-validation/<run>/report.json`, confirm the visual/India checks, and attach the report and Calculator screenshots to [issue #5](https://github.com/purushotmanmooper96-bit/thirstyai/issues/5). Do not substitute the CI `-SelfTest` result.

## PostgreSQL on your Windows laptop

The PostgreSQL 16 CI server has passed, but that does not test your pgAdmin installation. Follow [the database guide](verify_postgres_windows.md), load `thirstyai_db` and run the verifier using environment variables. Record the server version and each view/query result. Do not share a password or connection string containing one.

## Power BI

Use [the prepared import pack](../bi/IMPORT_WINDOWS.md), then [the five-page build guide](../bi/BUILD_WINDOWS.md). Record Desktop version, seven query row counts, refresh success, two blank company WUE values, model relationships and the single-year/single-scenario DAX behavior. Include five report pages, tooltip, reset bookmark, keyboard/tab order and mobile-layout screenshots. Report any step that fails. A screenshot of a table alone does not validate all five pages.

## Evidence to return

Copy this checklist into your issue response after running the checks. Fill in actual results; leave anything untested as UNTESTED.

```text
Commit tested:
Windows version:
Excel version/build:
Excel verifier result and attached report:
Baseline / double / alternative / invalid / zero cases:
Save-reopen-recalculate and visual/India checks:
PostgreSQL version and verifier results:
Power BI version:
Refresh result and row counts:
Blank WUE / relationships / scenario measures:
Five pages / tooltips / bookmarks / keyboard / mobile:
Attachments:
Failures or untested steps:
I confirm the stated PASS items were run in the named applications:
```

Only after reviewing this evidence and your explicit confirmation should current validation and historical limitations be updated. Keep issue #5 open while native Excel evidence is missing. A prepared PBIX, if later supplied, must still be opened and refreshed; its filename is not proof of successful validation.
