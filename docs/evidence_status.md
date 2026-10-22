# What the evidence can and cannot answer

Reviewed 22 October 2026. “Strong” means the stated narrow question has a direct published record, not that every company or causal effect is known. Company disclosures are self-reported; selected metrics may have limited external assurance. No independent remeasurement is performed here.

| Problem area | Level | Best source / exact locator | Key caveat | Still missing |
|---|---|---|---|---|
| Direct cooling water | Strong for published company totals | GOOGLE26 pp.96–97; META25 pp.9,11 | Operational water totals are not necessarily cooling alone or AI alone | Comparable monthly cooling-only consumption across operators |
| Electricity-related water | Partial | NREL12 abstract, DOI 10.1088/1748-9326/7/4/045802 | US literature synthesis from 2012; technologies and cooling systems differ | Current local grid consumption factors, time and supply boundaries |
| Chip manufacturing water | Partial | TSMC26 Water Positive section | Manufacturer commitment; no workload allocation | AI chip lifecycle inventory and allocation method |
| Siting in stressed regions | Partial | WRIADMIN province_baseline, bws/Tot; WRIINDIA26 main text | Our join is a state proxy, not a basin match; India analysis is attributed, not recreated | Verified supply basins, coordinates, permits and seasonal context |
| Heat-wave / drought peaks | Partial | METAVWB24 pp.9,25 | City seasonal demand and basin drought context are not data-centre peak measurements | Monthly / peak facility demand during heat waves and droughts |
| Competition with local users | Partial | METAVWB24 pp.17,25 | Shared basin and restoration context do not prove displacement or causation | Independent local water balances, rights and household/agricultural effects |
| Water quality and discharge | Partial | TSMCWATER26 “Identifying Risks via Three Key Indicators” | Supplier programme reporting, not independently sampled effluent | Facility discharge temperature, pollutants, permit and monitoring results |
| Reporting transparency | Strong for definition differences | MS26DATA Tables 8,15; META25 p.18; GOOGLE26 pp.87–88 | Years, fleets, definitions and assurance differ | Common annual + seasonal disclosure standard |
| Growth of AI demand | Partial | IEA26 executive summary; LBNL26 abstract | All data centres, not AI-only; projections conditional | Realised future demand and consistent AI share |
| Energy–water–carbon trade-offs | Partial | NREL12 abstract; MS24 “Mitigating energy impacts” | Technology-specific; lower direct cooling water can increase energy | Site-specific performance, cost and marginal grid impacts |

Source names, direct URLs, licence notes, locators, hashes and retrieval times: [source register](../research/sources.json) and [provenance](../research/provenance.json). Additional sources in this task: NREL12, TSMC26, TSMCWATER26, METAVWB24. No numbers from these four were promoted to headline claims.

## The global-total gap

This release does **not** establish a global AI water total or an uncertainty range for one. Electricity totals cannot become water totals without defensible local factors, workload shares and boundaries. The 2024 LBNL US report was opened during review, but its PDF download was blocked in this environment. It is not added as a hashed headline source. A US estimate would still not answer the global question.

## India: connected context, no invented attribution

WRI India publishes an analysis of data-centre siting and water stress. The CGWB state table describes all-user groundwater flows. They answer different questions. We do not infer the AI share of extraction, or call a state extraction ratio a facility stress rating. See [location overlay](location_overlay.md).

## Maintenance

Refresh sources deliberately; record SHA-256 and UTC retrieval time; inspect changed definitions and exact locators before promoting facts. Keep reported evidence, estimates, allocations and projections distinct. Revisit missing seasonal and basin data before adding hotspot or causal-impact claims.

## Seasonal source candidate

[Issue 2 review](issue_resolutions/2_seasonal_source_search.md) records one operator-published monthly chart and its supply/consumption caveat. It is source discovery, not an added monthly numeric dataset or evidence of drought harm.
