-- SQLite audit schema. Grain: one state/UT and assessment year.
CREATE TABLE IF NOT EXISTS sources (
 source_id TEXT PRIMARY KEY, title TEXT NOT NULL, url TEXT NOT NULL,
 scope TEXT NOT NULL, locator TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS groundwater (
 state TEXT NOT NULL, year INTEGER NOT NULL,
 recharge_bcm REAL NOT NULL CHECK(recharge_bcm >= 0),
 extractable_bcm REAL NOT NULL CHECK(extractable_bcm >= 0),
 extraction_bcm REAL NOT NULL CHECK(extraction_bcm >= 0),
 stage_pct REAL NOT NULL CHECK(stage_pct >= 0),
 source_id TEXT NOT NULL REFERENCES sources(source_id),
 PRIMARY KEY(state, year)
);
CREATE TABLE IF NOT EXISTS scenario_inputs (
 scenario_id TEXT PRIMARY KEY, it_mwh REAL NOT NULL CHECK(it_mwh >= 0),
 pue REAL NOT NULL CHECK(pue >= 1), wue REAL NOT NULL CHECK(wue >= 0),
 grid_l_kwh REAL NOT NULL CHECK(grid_l_kwh >= 0),
 carbon_kg_kwh REAL NOT NULL CHECK(carbon_kg_kwh >= 0),
 water_metric TEXT NOT NULL CHECK(water_metric = 'consumption'),
 denominator TEXT NOT NULL CHECK(denominator = 'IT_kWh'),
 evidence_type TEXT NOT NULL CHECK(evidence_type = 'illustrative_scenario')
);
CREATE VIEW IF NOT EXISTS vw_india_context AS
 SELECT g.*,s.url,s.locator AS source_locator,
 CASE WHEN stage_pct>100 THEN 1 ELSE 0 END AS annual_extraction_above_resource,
 extractable_bcm-extraction_bcm AS assessed_annual_flow_difference_bcm
 FROM groundwater g JOIN sources s ON g.source_id=s.source_id;
CREATE VIEW IF NOT EXISTS vw_scenarios AS
 SELECT *,it_mwh*pue AS facility_mwh,
 it_mwh*1000*wue AS direct_l,
 it_mwh*1000*pue*grid_l_kwh AS indirect_l,
 it_mwh*1000*(wue+pue*grid_l_kwh) AS total_l,
 it_mwh*1000*pue*carbon_kg_kwh AS carbon_kg
 FROM scenario_inputs;
CREATE INDEX IF NOT EXISTS idx_groundwater_year_stage ON groundwater(year,stage_pct);

CREATE TABLE IF NOT EXISTS company_water_reports (
 observation_id TEXT PRIMARY KEY, company TEXT NOT NULL, metric TEXT NOT NULL,
 value REAL CHECK(value >= 0), unit TEXT NOT NULL, period TEXT NOT NULL,
 geography TEXT NOT NULL, scope TEXT NOT NULL, water_metric TEXT NOT NULL,
 energy_denominator TEXT NOT NULL, evidence_type TEXT NOT NULL,
 source_id TEXT NOT NULL REFERENCES sources(source_id), locator TEXT NOT NULL,
 confidence TEXT NOT NULL CHECK(confidence IN ('High','Medium','Low')),
 confidence_basis TEXT NOT NULL, assurance TEXT NOT NULL, caveat TEXT NOT NULL
);
CREATE VIEW IF NOT EXISTS vw_company_reporting AS
 SELECT c.*,s.url,
 CASE WHEN EXISTS (
 SELECT 1 FROM company_water_reports other WHERE other.metric=c.metric AND
 (other.unit<>c.unit OR other.period<>c.period OR other.scope<>c.scope OR
 other.water_metric<>c.water_metric OR other.energy_denominator<>c.energy_denominator))
 THEN 'DEFINITIONS_PERIODS_OR_SCOPES_DIFFER' ELSE 'CHECK_FLEET_AND_ASSURANCE' END AS comparison_flag
 FROM company_water_reports c JOIN sources s ON c.source_id=s.source_id;
