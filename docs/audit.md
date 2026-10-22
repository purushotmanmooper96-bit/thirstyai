# v0.1 validation record

Date: 22 October 2026. This records executed checks, not independent environmental assurance.

## Completed

- Downloaded six official/research source documents via HTTPS. Saved UTC retrieval timestamps, byte lengths and SHA-256 hashes. Checked expected source anchors and manually inspected relevant claim locators.
- Parsed the first matching government groundwater table (the page repeats it). Required 36 unique state/UT rows. Kept source values and published stage ratios; no facility data were invented.
- Executed 19 Python unittest tests and 5 Node tests covering valid accounting, incompatible metrics, wrong denominators, double counting, missing/nonfinite values, zeros, workload mismatch, negative savings, break-even, futures and evidence grain.
- Built and integrity-checked a SQLite database. Executed source joins and accounting views, rejected an incompatible SQL scenario metric, and compared two SQL outputs to Python.
- Compared 30 deterministic generated Python/JavaScript parameter cases across direct water, indirect water, total water, energy and carbon.
- Executed five notebook code cells sequentially with saved outputs in the local Python environment. This is recorded execution, not a claim of a separate Jupyter-kernel test.
- Built the Excel audit workbook using the spreadsheet authoring runtime; checked default result parity, input-change recalculation and missing-input behavior; scanned formula errors and rendered all three sheets.
- Browser preview: inspected overview and decision-lab layout. Changed workload from 1,000 to 2,000 MWh and observed results double correctly; reset to defaults; searched India for Tamil Nadu and observed one matching source row.

## Remaining environment checks

- PostgreSQL server execution and native Power BI Desktop/PBIX authoring are not available here.
- Microsoft Excel Desktop recalculation was not separately tested. The generated workbook's authoring engine checks passed.
- Remote CI results must be checked after the GitHub push; configured Windows/Linux jobs are not preclaimed as passed.
- Real facility calibration, supply-source geospatial joins, worldwide coverage and probabilistic forecasts are outside this release.

UI checks completed later in the release are appended below rather than implied by the existence of a feature.

## Additional browser checks

- India above-100% filter returned Punjab, Rajasthan and Haryana, matching the source and SQL analysis.
- Setting demand growth to zero changed the future trajectory and held the demand-only line constant.
- Future CSV export generated a browser download. Evidence search for Gemini returned the energy and scoped direct-water claims.
