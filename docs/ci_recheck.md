# Repository and CI recheck — 22 October 2026

The failure email was real. Run [39771985828](https://github.com/purushotmanmooper96-bit/thirstyai/actions/runs/39771985828), commit f5310a1, failed in Lighthouse with `waiting for dynamic debugging port in chrome-err.log`. Windows, Linux and PostgreSQL passed in that same run. The later [39772227762](https://github.com/purushotmanmooper96-bit/thirstyai/actions/runs/39772227762) passed all four jobs, but that did not eliminate the intermittent startup weakness. Historical failed runs and their emails are retained; a new fix does not rewrite them.

## Changes after the complete checkout review

- Lighthouse now uses an explicit loopback debugging port and waits for Chrome's real JSON readiness endpoint. It has startup/job/subprocess deadlines, a temporary browser profile and guaranteed server/browser cleanup. The pinned CLI is installed once. JSON/HTML reports and Chrome logs are uploaded even on failure. No `continue-on-error` or fake success was added.
- Finite input values can still overflow during multiplication or growth. Python/JavaScript now reject nonfinite results, validate the original scenario before projection, and agree on integer-year checks. Regression cases cover extreme inputs and invalid original inputs hidden by zero future workload.
- Generated CSVs use explicit UTF-8/LF; manifest paths use forward slashes. `.gitattributes` standardises text checkout. CI now fails if a rebuild changes committed data/site/SQL snapshots.
- Source review guards now cover the entire displayed register and regional overlay, not only numerical headline claims. Invalid hashes, UTC timestamps, source links and nonfinite/negative fact values fail closed. The capture helper requires an explicit human-review acknowledgement and note.
- PostgreSQL loading now executes the actual source, groundwater, scenario and company SQL seed files documented for pgAdmin. All views and five analysis queries are compared with SQLite. Comparison handles repeated first-column values without assuming row order.
- Python's package version now agrees with package.json, pyproject.toml and CITATION.cff. The optional workbook-authoring source range grows with the source register; the shipped workbook remains the documented older snapshot. Native Excel/Power BI validation is still not claimed.
- Reproduction now also checks version consistency, Python/JavaScript syntax, local documentation links and sequential notebook code cells. A repeated local build produced no byte differences in generated research/data/site/SQL exports.

## The five open issues

Issues [#1](https://github.com/purushotmanmooper96-bit/thirstyai/issues/1)–[#5](https://github.com/purushotmanmooper96-bit/thirstyai/issues/5) are intentionally scoped `good first issue` contribution/validation tasks: independent point review, a seasonal source, Tamil translation, manual keyboard review and native Excel checks. They are not five confirmed software crashes. They remain open because closing incomplete tasks would conceal the work still needed.

## What is and is not verified

The new local suite passes 48 Python tests, six JavaScript tests, 30 deterministic Python/JavaScript parity cases, SQLite integrity/semantics, repository checks and notebook cells. The fixed workflow's actual Windows/Linux, PostgreSQL seed/query and Chrome audit execution must be read from its associated Actions run; configuration alone is not proof. See the current [Reproducibility runs](https://github.com/purushotmanmooper96-bit/thirstyai/actions/workflows/checks.yml).

This pass checks the implementation and source lineage; it does not independently remeasure company water, refresh every external document, establish global/basin causal claims, certify all accessibility, or execute the author's desktop applications. These limitations are still explicit, and docs/limitations.md remains unchanged pending author confirmation.

## Windows

```powershell
git pull --ff-only origin main
python scripts/reproduce.py
```

For PostgreSQL use docs/verify_postgres_windows.md. For a failed audit, download `lighthouse-reports` from that run and inspect the Chrome log and runtime error; do not infer the data model failed from the workflow's overall red icon.
