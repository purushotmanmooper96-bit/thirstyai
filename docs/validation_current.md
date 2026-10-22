# Current validation and limits

This is the current status index. Historical QA files describe their named commits; they are not silently upgraded. The historical v0.1 limitations file remains intact.

| Component | Status | Evidence |
|---|---|---|
| Python / JavaScript / SQLite | Automated reproduction | `python scripts/reproduce.py`; semantic checks and cross-language parity |
| PostgreSQL | Actual PostgreSQL 16 execution in CI | Three views and five analysis queries compared with SQLite |
| Browser interactions | Automated Chrome regression suite | Invalid-input transitions, sharing, PNG/JSON downloads, filters, fallback, mobile layout and keyboard checks; see CI browser artifact |
| Source refresh | Candidate-only, explicit review promotion | Failed refresh preserves reviewed registry and processed snapshots; old captures archived |
| Excel Desktop | **UNCONFIRMED** | Verifier script and fixtures are prepared; CI self-test does not run Excel. Issue #5 requires native report, screenshots and author confirmation |
| Power BI Desktop | **Build pack only; no PBIX** | Native authoring, refresh, screenshots and author validation remain required |
| Facility / basin stress | **No verified exact joins** | State context is a proxy; no location, basin or missing value guessed |
| Environmental values | Attributed published evidence | No independent facility remeasurement, global AI water total, universal prompt factor or local causal-harm estimate |

Run Windows checks from the checkout:

```powershell
python scripts/reproduce.py
.\scripts\verify_excel.ps1
```

The second command requires Microsoft Excel Desktop and records actual results on a working copy. It does not mark this table confirmed automatically. See [Excel checklist](excel_validation.md).

For browser checks with Chrome installed:

```powershell
npm ci --prefix ci
$env:CHROME_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
node ci/browser-test.mjs
```

The launch readiness record is [implementation checklist](implementation_2026-10-22.md). Full WCAG certification, public-CDN load testing, native Excel and native Power BI verification are not implied by passing automated tests.
