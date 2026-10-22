# Import the prepared Power BI data pack

The data handoff is checked by Python. The generated M query, DAX, layout and refresh still require Power BI Desktop execution; no PBIX or native validation is claimed.

## Prepare

```powershell
git pull --ff-only
python scripts/reproduce.py
Get-Content outputs/powerbi/manifest.json
```

This creates seven UTF-8 CSVs in `outputs/powerbi/`, with columns, row counts and SHA-256 digests in `manifest.json`. Values retain their original units, periods and boundaries. Missing company WUE values stay blank, not zero. The ten-topic evidence status comes directly from the reviewed Markdown table. Candidate research is excluded from Claims and Sources.

## Connect once, then create the tables

1. Open **Power BI Desktop → Blank report → Home → Transform data**.
2. In Power Query, click **Home → Manage Parameters → New Parameter**. Name **RepoRoot**, type **Text**, suggested values **Any value**. Set Current Value to the absolute checkout directory, for example `C:\Users\YourName\Projects\thirstyai`. Click **OK**. Keep credentials out of this parameter.
3. **Home → New Source → Blank Query**. Rename it **ThirstyAI_Data**. Click **Advanced Editor**, replace everything with the contents of [ThirstyAI_Data.m](ThirstyAI_Data.m), click **Done**. It returns a record; this query is an intermediate helper, not a report table. Right-click it and clear **Enable load** if that option is available.
4. For each name below, use **Home → New Source → Blank Query → Advanced Editor**, replace the editor with the matching expression, then rename the query exactly as shown. Do not expand the helper into one giant table.

| Query name | Complete expression | Expected rows in this release |
|---|---|---:|
| Groundwater | `let Data = ThirstyAI_Data[Groundwater] in Data` | 36 |
| CompanyReports | `let Data = ThirstyAI_Data[CompanyReports] in Data` | 16 |
| LocationContext | `let Data = ThirstyAI_Data[LocationContext] in Data` | 5 |
| Scenarios | `let Data = ThirstyAI_Data[Scenarios] in Data` | 33 |
| Claims | `let Data = ThirstyAI_Data[Claims] in Data` | 20 |
| Sources | `let Data = ThirstyAI_Data[Sources] in Data` | 19 |
| EvidenceStatus | `let Data = ThirstyAI_Data[EvidenceStatus] in Data` | 10 |

5. Inspect the data types. CompanyReports `value` is decimal and has two nulls. Scenarios `year` is whole number; warning is Text. Groundwater `stage_pct` is numeric percentage points. All identifiers, boundaries and periods are Text. The query converts empty cells to null before numeric conversion with `en-US` culture.
6. **Close & Apply → Home → Refresh**. If a privacy prompt appears, choose a suitable local-file privacy level; do not disable privacy protections globally. If refreshing fails, capture the error rather than declaring validation passed.
7. Continue [BUILD_WINDOWS.md](BUILD_WINDOWS.md), section 2, for relationships, measures, theme, five pages and accessibility. Page 5 can now use the imported EvidenceStatus table instead of manual Enter Data.
8. Save your own `ThirstyAI_v021.pbix`. Submit the evidence in [Desktop sign-off](../docs/desktop_signoff.md). Publishing to Power BI Service is optional and not part of local validation.

## When the source changes

Re-run `python scripts/reproduce.py`, inspect the manifest diff, then refresh Desktop. If columns or source definitions change, review them before accepting the refresh. The bundle is reproducible data preparation; it does not execute the M or DAX engine and does not certify the report visuals.
