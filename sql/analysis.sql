-- 1. Observations above annual extractable resource. Not facility impact rankings.
SELECT state, year, stage_pct, source_id FROM vw_india_context
WHERE stage_pct>100 ORDER BY stage_pct DESC;

-- 2. A selected state/UT comparison. NCR is not one state.
SELECT state,stage_pct,extraction_bcm,extractable_bcm FROM groundwater
WHERE state IN ('Maharashtra','Tamil Nadu','Karnataka','Telangana','Delhi','Haryana','Uttar Pradesh')
ORDER BY stage_pct DESC;

-- 3. Explicit denominator and component audit for illustrative scenarios.
SELECT scenario_id,water_metric,denominator,direct_l,indirect_l,total_l,facility_mwh
FROM vw_scenarios;

-- 4. Scope coverage, not an unweighted mean of state extraction ratios.
SELECT year,COUNT(*) AS state_ut_records,COUNT(DISTINCT source_id) AS groundwater_sources
FROM groundwater GROUP BY year;

-- 5. Duplicate-grain check. An empty result is expected.
SELECT state,year,COUNT(*) FROM groundwater GROUP BY state,year HAVING COUNT(*)>1;
