# v0.2 validation record

This document supplements the historical v0.1 limitations file; that file is not silently upgraded before author confirmation.

| Component | Status | Evidence / next check |
|---|---|---|
| Python / SQLite / JavaScript | Executed in development | `python scripts/reproduce.py`; unit tests, semantic rejection and cross-language parity |
| PostgreSQL | Executed on PostgreSQL 16 in CI; author’s Windows confirmation pending | All three views PASS in runs 39758080419 and 39758457275; `python scripts/verify_postgres.py --load` for author’s Windows check |
| Power BI Desktop | Build pack only; no PBIX | Follow `bi/BUILD_WINDOWS.md`, send screenshots + refresh results |
| Microsoft Excel Desktop | Unconfirmed | Three expected cases and invalid-input checks in `docs/excel_validation.md` |
| Existing workbook | v0.1 snapshot | Calculator and original sources; expanded company evidence lives in CSV/JSON/SQL |

Never use a passing SQLite run as evidence that PostgreSQL passed, or cached spreadsheet values as Excel Desktop recalculation evidence.

Reproduction CI on commit `882b7209b87cc2aa73ef4cf8248c4bb067290bca` passed on ubuntu-latest and windows-latest (run 39758457275). UTF-8 file handling fixed a failure in the first Windows run. Lighthouse and mobile results: [site QA](site_qa.md).

## Follow-up prompted by the failure email

[CI and complete-checkout recheck](ci_recheck.md) records the Chrome startup failure, robustness fixes, expanded 48-Python / six-JavaScript suite, seed-file verification, notebook/syntax/link checks and byte-stable rebuild. Historical red runs remain visible. Five open contribution issues are deliberately unfinished tasks, not proof of five broken features.
