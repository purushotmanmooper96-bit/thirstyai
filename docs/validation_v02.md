# v0.2 validation record

This document supplements the historical v0.1 limitations file; that file is not silently upgraded before author confirmation.

| Component | Status | Evidence / next check |
|---|---|---|
| Python / SQLite / JavaScript | Executed in development | `python scripts/reproduce.py`; unit tests, semantic rejection and cross-language parity |
| PostgreSQL | Verifier and PostgreSQL 16 CI job added; execution pending | `python scripts/verify_postgres.py --load`; record CI run and author's Windows result separately |
| Power BI Desktop | Build pack only; no PBIX | Follow `bi/BUILD_WINDOWS.md`, send screenshots + refresh results |
| Microsoft Excel Desktop | Unconfirmed | Three expected cases and invalid-input checks in `docs/excel_validation.md` |
| Existing workbook | v0.1 snapshot | Calculator and original sources; expanded company evidence lives in CSV/JSON/SQL |

Never use a passing SQLite run as evidence that PostgreSQL passed, or cached spreadsheet values as Excel Desktop recalculation evidence.
