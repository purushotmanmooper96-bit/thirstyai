# Build ThirstyAI in Power BI Desktop

This is a reproducible build specification, **not a delivered or validated PBIX**. Save as `ThirstyAI_v02.pbix`; send screenshots and refresh results for review. Defaults and futures are **ILLUSTRATIVE INPUTS — NOT MEASUREMENTS**. Do not create a company league table or sum unlike company metrics.

## 1. Prepare and connect

Recommended CSV route: use [IMPORT_WINDOWS.md](IMPORT_WINDOWS.md) to import all seven prepared tables with explicit types, null handling and manifest row counts, then continue at section 2 below. The manual connections below remain an alternative; do not import duplicate copies. The generated M query has not been executed in Desktop here.

1. In PowerShell at repo root, run `python scripts/reproduce.py`. For PostgreSQL, complete [database verification](../docs/verify_postgres_windows.md) first.
2. Open **Power BI Desktop → Blank report**. **File → Options and settings → Options → Current File → Regional Settings → English (United States)** for dot-decimal CSV parsing. Click **OK**.
3. **Home → Get data → Text/CSV → Browse**. Select `data/processed/india_groundwater_2025.csv`; encoding **65001 UTF-8**, delimiter comma. Click **Transform Data**. Rename query **Groundwater**.
4. Repeat for `data/processed/company_water_reports.csv` as **CompanyReports**, `data/processed/location_stress_overlay.csv` as **LocationContext**, `outputs/scenarios.csv` as **Scenarios** and `dist/data/claims.csv` as **Claims**.
5. For the source dimension: **Home → New Source → JSON**, select `research/sources.json`. In Power Query click **To Table → OK**; expand the record column, select `id,title,publisher,url,locator,scope,licence`, uncheck **Use original column name as prefix**. Rename **Sources**, rename `id` to `source_id`.
6. For an optional PostgreSQL connection instead of the Groundwater and CompanyReports CSVs: **Home → Get Data → More → Database → PostgreSQL database → Connect**. Server `localhost:5432`, database `thirstyai_db`, **Import → OK**. Choose **Database** authentication, enter role/password in the credential dialog. In Navigator select `public.vw_india_context` and `public.vw_company_reporting`, click **Transform Data**; rename to Groundwater / CompanyReports. Do not also import their CSV versions. A gateway will be needed for scheduled online refresh; this pack does not provision one.
7. In **Transform Data**, set text columns to **Text**; numeric company `value` to **Decimal Number** (blank stays null); `year` to **Whole Number**; groundwater amounts and `stage_pct` to **Decimal Number**. In Scenarios set `year` Whole Number and numeric calculation columns Decimal Number; `evidence_type` and warning columns Text. For LocationContext, keep identifiers, category, scale, baseline period and caveats as Text; score and water value Decimal Number. Do not enable automatic summation of ratios.
8. Click **Close & Apply**. **Home → Refresh**. Confirm 36 Groundwater rows, 16 CompanyReports rows including two blank WUE values, 5 LocationContext rows and 33 Scenarios rows. These are curated coverage counts, not the global population.

## 2. Model, measures and theme

1. Click **Model view**. Remove any automatically created fact-to-fact relationships. Drag `Sources[source_id]` to `Groundwater[source_id]`, `CompanyReports[source_id]`, `Claims[source_id]`: **One to many, Single direction, Active**. Keep LocationContext disconnected: its water and stress sources are separate and a single misleading relationship would hide one boundary. Keep Scenarios disconnected; there is no source dimension for hypothetical inputs.
2. Select each `Sources[url]` / Claims URL if imported: **Column tools → Data category → Web URL**. Select ratios / raw values: **Default summarization → Don't summarize**.
3. **Report view → Modeling → New measure**. Paste one measure at a time from `bi/measures.dax` (comments describe context). Create additional measures:

```dax
Company Figure = SELECTEDVALUE(CompanyReports[value])
Company Unit = SELECTEDVALUE(CompanyReports[unit], "Select one unit")
Company Boundary = SELECTEDVALUE(CompanyReports[scope], "Multiple boundaries: do not combine")
Company Record Count = COUNTROWS(CompanyReports)
Location Context Rows = COUNTROWS(LocationContext)
```

4. `Reported Stage Pct`: format as **Custom `0.00"%"`** if supported; otherwise decimal number and label axis **Stage (%) — percentage points**. Do not use Percentage format on existing percentage points. Water ML measures divide L by 1,000,000. WUE and PUE are ratios; never sum them.
5. **View → Themes → Browse for themes**, choose `bi/theme.json`. **View → Page view → Fit to width**. Choose a readable sans-serif font and at least 12 pt body labels; retain units and definitions when space is tight.

## 3. Five pages

Use **+** at the bottom, double-click page tabs to rename. Insert a text box with the page limitation before adding visuals. Select a visual then fill fields from the Data pane.

**Page 1 — Start here**
- **Insert → Text box**: “AI needs cooling and electricity. Water impacts depend on place, time and accounting boundary. No universal water-per-prompt figure.”
- Add **Table** with Claims `title,value,unit,period,geography,scope,evidence_type,locator,source_id`. Add slicers `source_id` and `evidence_type`. Avoid total rows: **Format visual → Totals → Off**.
- Add **Card** with `State UT Records` and explanatory label “All-use groundwater context”. Link the source register via a button Web URL action to the GitHub research directory.

**Page 2 — Company disclosures**
- Text: “Company self-reported. Selected metrics may have limited external assurance. Years and boundaries differ; this is not a performance ranking.”
- Add slicers CompanyReports `company,metric,period,unit`. Add **Table** with `company,metric,value,unit,period,scope,water_metric,energy_denominator,locator,assurance,caveat`. Turn totals off. Add `comparison_flag` if using PostgreSQL view; CSV users display a permanent warning that periods/scopes/definitions differ.
- Add a small table filtered `value is blank`: shows absent numeric WUE disclosures without displaying zero. Do not combine company values in a bar chart.

**Page 3 — Locations and India**
- Text: “5 US state-context matches, 0 verified exact facility/basin joins. 1979–2019 modeled baseline. Regional context is not local impact. India groundwater is all users, not AI extraction.”
- Add **Table** with LocationContext official location name, company, reported water value/unit/period, regional category, match scale, source IDs and caveat (use the actual CSV column names).
- Add Groundwater **Clustered bar chart**: state on Y, stage_pct on X; sort descending. Add state slicer; title includes **2025, all uses**. Do not shade countries or plot guessed facility pins. Add table with source locator and all three annual groundwater flows.

**Page 4 — Conditional futures**
- Text at top: **ILLUSTRATIVE INPUTS — NOT MEASUREMENTS. Not a global forecast or savings achieved.**
- Add **Line chart**: Scenarios year X-axis, `Scenario Water ML` Y-axis, name Legend. Add slicer year and name. For a card, select exactly one year and trajectory, otherwise the measure must remain blank. Add table of `demand_growth,efficiency_gain,it_mwh,facility_mwh,total_l,evidence_type` and warning. Growth and efficiency are assumptions, not fitted trends.
- Add a text box with formula `IT kWh × [consumptive WUE + PUE × grid consumption factor]`; list manufacturing exclusions. This page reads the scenarios export; it is not a full interactive cooling engineering simulator.

**Page 5 — Actions and evidence limits**
- Add text boxes with company, government, community and individual actions from README. Include source IDs and evidence levels. Add ten-topic status table using **Home → Enter data** from `docs/evidence_status.md` (avoid changing partial into strong).
- Add source and methodology URL buttons. Explain the missing global total, state proxies, unconfirmed native checks and update process. Author credit: **Purushotman Mooper — independent portfolio research**.

## 4. Tooltips, bookmarks and accessibility

1. Add a tooltip page via **+**. Rename **Definition tooltip**. Click blank canvas → **Format page → Page information → Tooltip On**; **Canvas settings → Type Tooltip**. Add text explaining withdrawal vs consumption, source year and state proxy. For each visual **Format visual → General → Tooltips → Type Report page → Page Definition tooltip**. Keep the essential caveat visible on the main page too.
2. **View → Selection** and **Bookmarks**. On Company page set one company/metric; click **Add**, rename **Example disclosure**. In bookmark options enable **Data** and **Current page**. Create **Reset company filters** with slicers cleared. **Insert → Buttons → Blank → Action On → Bookmark → Reset company filters**. Test with Ctrl+click in Desktop. Do not hide the boundary disclaimer in a bookmark.
3. **View → Selection → Tab order**: put page title first, then slicers, data table, source button. Hide decorative objects from tab order. For each visual **Format → General → Alt text** describe what it shows and the boundary. Test keyboard Tab / Shift+Tab, Enter and high contrast mode. Use labels as well as colours; target contrast 4.5:1 for body text and 3:1 for large text/UI.
4. Keep no reliance on hover for essential units. **View → Mobile layout**: arrange disclaimer, slicers and tables in a single column. Test horizontal table navigation.
5. **File → Save**. Refresh from original files, test every page/filter/bookmark and inspect blank WUE values. Send screenshots of all five pages, Model view, row counts, source tooltip, mobile layout and refresh status. Until reviewed, this remains an unvalidated build pack. Avoid publishing credentials or local paths in screenshots.
