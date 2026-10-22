# Data dictionary

## india_groundwater_2025.csv

Grain: one Indian state or union territory, assessment year 2025.

| Field | Type / meaning |
|---|---|
| state | Official source label for state/UT; no facility inference |
| recharge_bcm | Annual groundwater recharge, billion cubic meters, rounded in source |
| extractable_bcm | Annual extractable groundwater resource, billion cubic meters |
| extraction_bcm | Annual groundwater extraction, all uses, billion cubic meters |
| stage_pct | Published annual extraction / annual extractable resource × 100 |
| year | Assessment year, integer |
| source_id | Foreign key to `research/sources.json` |
| evidence_type | `government_reported` |
| scope | `state_or_UT_all_uses` |
| locator | Annexure I and row number |

Numeric zeros retain their source rounding. None are inferred missing values. State ratios are nonadditive. State/UT volumes can be summed for a coarse check subject to source rounding; use published national totals for national claims.

## sources.json

One record per source document/version: `id`, `title`, `publisher`, `url`, `locator`, `scope`, `licence` and drift-check `anchor`. The source licence string documents current evidence, not a blanket redistribution grant.

## claims.json

One headline fact: `id`, `title`, `value`, `unit`, `period`, `geography`, `scope`, `evidence_type`, `source_id`, `locator`, `caveat`. Values with different units and populations must not be summed. C01–C02 are the same IEA vintage but different years and evidence types. C04 includes facility energy overhead; C05 is direct cooling water allocation.

## provenance.json

One retrieval attempt per source: source ID, canonical URL, UTC retrieval time, SHA-256 of raw bytes, byte count, status and reviewer note. Failed downloads are explicit; the build requires successful headline-source retrieval records. Raw files are ignored by Git.

## scenarios.csv and engine output

`name`, `year`, `demand_growth`, `efficiency_gain` identify conditional assumptions. `it_mwh`, `facility_mwh`, `direct_l`, `indirect_l`, `total_l`, `carbon_kg` carry explicit units. `intensity_l_kwh_it` is total operational consumption per IT kWh; `evidence_type` is illustrative_scenario; `boundary` excludes manufacturing. These fields are not actual observations.

## v0.2 company and location tables

`company_water_reports.csv`: one company/metric/scope/period record. `value` is nullable; absence is never zero. `water_metric` and `energy_denominator` retain unresolved definitions. `confidence` concerns extraction; `assurance` records source-level assurance, not independent ThirstyAI measurement. `source_id` resolves to the direct source URL; `locator` is record-specific. SQL `vw_company_reporting` adds a comparison warning, not a performance rank.

`location_water.csv`: seven curated official location/campus aggregates, not a complete inventory. Water values keep original units and periods. `regional_water_stress.csv`: three Aqueduct administrative baseline scores, with indicator/weight and spreadsheet row. `location_stress_overlay.csv`: five exact named-state matches; `match_scale` is STATE_PROXY_NOT_FACILITY_OR_BASIN; geographic confidence is Medium. No inferred coordinates, supply basin or causal effect.

`scenarios.csv` includes a warning column; `evidence.json` includes `scenario_warning`. Evidence records remain reported evidence. Targets in `company_targets.json` are goals with their own boundaries, never deducted from consumption.
