# Power BI Desktop build pack

Status: reusable files and instructions. No PBIX has been authored/opened in this environment.

1. Open Power BI Desktop. Create a text parameter `ProjectRoot` pointing to the cloned project directory, without a trailing slash. Use Windows backslashes as normal Power Query string characters.
2. Import `data/processed/india_groundwater_2025.csv` and `outputs/scenarios.csv`; set state/source/name/type fields to Text, year to Whole Number and numeric measures to Decimal Number. Do not summarize `stage_pct`.
3. Import `dist/data/claims.csv` with Text fields for unit/period/scope and Decimal Number for value. Disable summarization of `value`; it mixes units. Keep this table separate from scenario facts.
4. Use `queries.pq` as an example query and `measures.dax` for measures. Create a Sources table from the supplied source CSV export if desired; relationship source_id → sources.id is many-to-one, single-direction. The scenario table is independent from groundwater. Never join solely on year across these populations.
5. Import `theme.json` and build the pages below. Each page must label evidence type and unit and link its source or assumptions.

Pages:
- Overview: separate IEA electricity endpoints and coverage counts; do not invent a global water KPI.
- India: state table and bar chart of published extraction stage, with 2025/source note; no unsupported facility map.
- Evidence: claim title/value/unit, geography, period, locator and caveat table.
- Futures: water trajectory by year and selected scenario. Use the guarded measure for cards.
- Solutions: baseline trade-offs from the web calculator, with explicit assumptions and scope; do not invent liters saved per dollar.

Verify one scenario slice against `outputs/scenarios.csv` and Python: baseline 2025 = 2,200,000 L under the illustrative defaults. Select exactly one year and one trajectory for scalar cards. Never sum ratios or different scenarios into a total. Screenshots and Desktop rendering remain a task for a Windows environment.

PostgreSQL alternative: execute `sql/postgresql_schema.sql`, `sql/sources_seed.sql` and `sql/seed.sql` in that order with psql. Connect Desktop to the resulting views. A separate PostgreSQL schema uses CREATE OR REPLACE VIEW and DOUBLE PRECISION. PostgreSQL execution has not been verified here.
