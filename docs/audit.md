# Sceptical review of ThirstyAI v0.2.1

Reviewed 22 October 2026. This is a critical self-review in peer-reviewer and hiring-reviewer roles, not an external endorsement, environmental audit, hiring prediction or guarantee of reach. Historical v0.1 results are preserved in audit_v01.md.

## Verdict

The project is now a useful reporting-comparison atlas and a reproducible teaching lab. It is not a global AI water inventory, local impact assessment or calibrated engineering tool. Its strongest evidence is the original source trail and explicit rejection of incompatible definitions. The remaining research gap is local, seasonal, independently corroborated evidence.

## Every numerical headline

High confidence describes extraction/attribution, not independent remeasurement. “Projection” and “allocation” remain distinct from company-reported figures. Direct source URLs, years, geography, exact locators and boundaries are listed below.

| ID / finding | Value / unit | Period / geography | Boundary / type / confidence | Source and locator | Caveat |
|---|---|---|---|---|---|
| C01 / Data-centre electricity demand, 2025 | 485 TWh/year | 2025 / Global | All data centres, not AI alone / not_applicable / IEA estimate / High | [International Energy Agency / IEA26](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary) / Executive summary, updated demand outlook paragraph | Electricity, not water; report vintage 2026. |
| C02 / Data-centre electricity demand, 2030 | 950 TWh/year | 2030 / Global | All data centres, not AI alone / not_applicable / IEA projection / Medium | [International Energy Agency / IEA26](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary) / Executive summary, updated demand outlook paragraph | Conditional central projection; not a measured future outcome. |
| C03 / India groundwater stage of extraction | 60.63 % | 2025 / India | Annual extraction divided by annual extractable groundwater; all uses / not_applicable / Government reported / High | [Ministry of Jal Shakti / PIB / CGWB25](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2206073&lang=1&reg=3) / Main text and Annexure I, Grand Total | Not the percentage of stored groundwater depleted. Does not attribute extraction to AI. |
| C04 / Median Gemini Apps text-prompt serving energy | 0.24 Wh/prompt | May 2025 / Google serving fleet | Company-authored serving methodology, including facility overhead / not_applicable / Production study / High | [Elsworth et al. / Google / GOOGLE25](https://arxiv.org/html/2508.15734v1) / Table 2, comprehensive approach | Not every prompt or model; do not apply PUE again to facility-energy metric. |
| C05 / Median Gemini Apps text-prompt cooling water | 0.26 mL/prompt | May 2025 / Google serving fleet | Allocated direct consumptive cooling water; previous-year WUE / consumption / Company-modeled allocation / Medium | [Elsworth et al. / Google / GOOGLE25](https://arxiv.org/html/2508.15734v1) / Section 3.3 and Table 2 | Not electricity-related or full lifecycle water. Cannot be generalized to all AI tasks. |
| C06 / US data-centre electricity reference case | 649 TWh/year | 2030 / United States | All US data centres; 2025 Update published June 2026 / not_applicable / LBNL projection / Medium | [Lawrence Berkeley National Laboratory / LBNL26](https://bies.lbl.gov/publications/united-states-data-center-energy-2025) / Official publication abstract, Reference Case | Different model from IEA; not a water total. Do not combine projections as observations. |
| CORP01 / Google withdrawal | 14689 million gallons (as reported) | 2025-01-01/2025-12-31 / Global | Global operations / withdrawal / company_reported / High | [Google / GOOGLE26](https://sustainability.google/files/google-2026-environmental-report.pdf) / PDF p.96, Water / water use by data centers and offices, 2025 | Not AI-only; reporting periods, fleets and water definitions differ. |
| CORP02 / Google consumption | 10869 million gallons (as reported) | 2025-01-01/2025-12-31 / Global | Global operations / consumption / company_reported / High | [Google / GOOGLE26](https://sustainability.google/files/google-2026-environmental-report.pdf) / PDF p.96, Water / water use by data centers and offices, 2025 | Not AI-only; reporting periods, fleets and water definitions differ. |
| CORP03 / Google withdrawal | 13562 million gallons (as reported) | 2025-01-01/2025-12-31 / Global | Operational data centers: owned and fully leased / withdrawal / company_reported / High | [Google / GOOGLE26](https://sustainability.google/files/google-2026-environmental-report.pdf) / PDF p.96, Water / water use by data centers and offices, 2025 | Not AI-only; reporting periods, fleets and water definitions differ. |
| CORP04 / Google consumption | 10523 million gallons (as reported) | 2025-01-01/2025-12-31 / Global | Operational data centers: owned and fully leased / consumption / company_reported / High | [Google / GOOGLE26](https://sustainability.google/files/google-2026-environmental-report.pdf) / PDF p.96, Water / water use by data centers and offices, 2025 | Not AI-only; reporting periods, fleets and water definitions differ. |
| CORP05 / Google PUE | 1.09 facility kWh / IT kWh | 2025-01-01/2025-12-31 / Global | Data-center fleet / not_applicable / company_reported / High | [Google / GOOGLE26](https://sustainability.google/files/google-2026-environmental-report.pdf) / PDF p.15, fleet-wide average PUE | Not AI-only; reporting periods, fleets and water definitions differ. |
| CORP07 / Microsoft withdrawal | 13266 ML | FY2025 ended 2025-06-30 / Global | Enterprise offices, owned/leased datacenters and labs / withdrawal / company_reported / High | [Microsoft / MS26DATA](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2026-Microsoft-Environmental-Data-Fact-Sheet-PDF.pdf) / PDF p.7, Table 8, FY25 | Not AI-only; reporting periods, fleets and water definitions differ. |
| CORP08 / Microsoft consumption | 8170 ML | FY2025 ended 2025-06-30 / Global | Enterprise offices, owned/leased datacenters and labs / consumption / company_reported / High | [Microsoft / MS26DATA](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2026-Microsoft-Environmental-Data-Fact-Sheet-PDF.pdf) / PDF p.7, Table 8, FY25 | Not AI-only; reporting periods, fleets and water definitions differ. |
| CORP09 / Microsoft PUE | 1.17 facility kWh / IT kWh | FY2025 ended 2025-06-30 / Global | Data-center global average / not_applicable / company_reported / High | [Microsoft / MS26REPORT](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2026-Microsoft-Environmental-Sustainability-Report-PDF.pdf) / PDF p.23, Datacenters energy | Not AI-only; reporting periods, fleets and water definitions differ. |
| CORP10 / Microsoft WUE | 0.27 L/kWh (publisher definition) | FY2025 ended 2025-06-30 / Global | Owned datacenters / water_use_unspecified / company_reported / High | [Microsoft / MS26REPORT](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2026-Microsoft-Environmental-Sustainability-Report-PDF.pdf) / PDF p.24; definition endnote 12 p.64 | Inspected 2026 definition says cooling/humidification water use divided by energy, without explicitly resolving withdrawal vs consumption and IT denominator. Not accepted as consumptive WUE by the calculator. |
| CORP11 / Meta withdrawal | 5637 ML | 2024-01-01/2024-12-31 / Global | Operations excluding separately disclosed construction / withdrawal / company_reported / High | [Meta / META25](https://sustainability.atmeta.com/asset/2025-environmental-data-index/) / PDF p.9, section 3.1, 2024 column | Not AI-only; reporting periods, fleets and water definitions differ. |
| CORP12 / Meta consumption | 3123 ML | 2024-01-01/2024-12-31 / Global | Operations / consumption / company_reported / High | [Meta / META25](https://sustainability.atmeta.com/asset/2025-environmental-data-index/) / PDF p.11, section 3.2, 2024 column | Not AI-only; reporting periods, fleets and water definitions differ. |
| CORP13 / Meta withdrawal | 4145 ML | 2024-01-01/2024-12-31 / Global | Data centers / withdrawal / company_reported / High | [Meta / META25](https://sustainability.atmeta.com/asset/2025-environmental-data-index/) / PDF p.9, section 3.1, 2024 column | Not AI-only; reporting periods, fleets and water definitions differ. |
| CORP14 / Meta consumption | 2974 ML | 2024-01-01/2024-12-31 / Global | Data centers / consumption / company_reported / High | [Meta / META25](https://sustainability.atmeta.com/asset/2025-environmental-data-index/) / PDF p.11, section 3.2, 2024 column | Not AI-only; reporting periods, fleets and water definitions differ. |
| CORP15 / Meta PUE | 1.08 facility kWh / IT kWh | 2024-01-01/2024-12-31 / Global | Data centers / not_applicable / company_reported / High | [Meta / META25](https://sustainability.atmeta.com/asset/2025-environmental-data-index/) / PDF p.8, section 2.4, 2024 column | Not AI-only; reporting periods, fleets and water definitions differ. |

The displayed 1.96× electricity ratio is derived as C02/C01 (950/485), all data centres, 2030 projection versus 2025 estimate, global. It is not an AI-only growth measurement or water multiplier.

## Published location values

| Location | Value / unit / period | Boundary / confidence | Direct source / exact locator |
|---|---|---|---|
| Google / Henderson, Nevada | 239.4 million gallons (as reported) / 2025 | consumption / Published location/campus aggregate; not AI-only / extraction High | [Google / GOOGLE26](https://sustainability.google/files/google-2026-environmental-report.pdf) / PDF p.97 Water use by data center location, Henderson NV |
| Google / Quilicura, Chile | 143 million gallons (as reported) / 2025 | consumption / Published location/campus aggregate; not AI-only / extraction High | [Google / GOOGLE26](https://sustainability.google/files/google-2026-environmental-report.pdf) / PDF p.97 Water use by data center location, Quilicura |
| Google / Mesa, Arizona | 9.7 million gallons (as reported) / 2025 | consumption / Published location/campus aggregate; not AI-only / extraction High | [Google / GOOGLE26](https://sustainability.google/files/google-2026-environmental-report.pdf) / PDF p.97 Water use by data center location, Mesa AZ |
| Microsoft / Phoenix, Arizona | 981 ML / FY2025 ended 2025-06-30 | withdrawal / Published location/campus aggregate; not AI-only / extraction High | [Microsoft / MS26DATA](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2026-Microsoft-Environmental-Data-Fact-Sheet-PDF.pdf) / PDF p.25 Table 15 Phoenix AZ; exclusions p.26 |
| Microsoft / Singapore | 423 ML / FY2025 ended 2025-06-30 | withdrawal / Published location/campus aggregate; not AI-only / extraction High | [Microsoft / MS26DATA](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2026-Microsoft-Environmental-Data-Fact-Sheet-PDF.pdf) / PDF p.25 Table 15 Singapore; 99% non-potable; exclusions p.26 |
| Meta / Los Lunas, New Mexico | 252 ML / 2024 | withdrawal / Published location/campus aggregate; not AI-only / extraction High | [Meta / META25](https://sustainability.atmeta.com/asset/2025-environmental-data-index/) / PDF p.9 Water withdrawal by facility, Los Lunas NM |
| Meta / Mesa, Arizona | 57 ML / 2024 | withdrawal / Published location/campus aggregate; not AI-only / extraction High | [Meta / META25](https://sustainability.atmeta.com/asset/2025-environmental-data-index/) / PDF p.9 Water withdrawal by facility, Mesa AZ |

All location rows are company-reported operational aggregates, not AI-only observations or independent measurements. No coordinates or supply basins were guessed.

## Regional scores

| Region | Score / category | Period / boundary / confidence | Source / locator |
|---|---|---|---|
| Arizona | 4.392122413 / Extremely High (>80%) | 1979–2019 modeled baseline; dimensionless Aqueduct 4.0 demand-weighted administrative bws/Tot; geographic proxy confidence Medium | [World Resources Institute / WRIADMIN](https://files.wri.org/aqueduct/aqueduct-4-0-country-rankings.zip) / province_baseline row 2284; name_1=Arizona, indicator_name=bws, weight=Tot |
| New Mexico | 4.324930145 / Extremely High (>80%) | 1979–2019 modeled baseline; dimensionless Aqueduct 4.0 demand-weighted administrative bws/Tot; geographic proxy confidence Medium | [World Resources Institute / WRIADMIN](https://files.wri.org/aqueduct/aqueduct-4-0-country-rankings.zip) / province_baseline row 2437; name_1=New Mexico, indicator_name=bws, weight=Tot |
| Nevada | 3.569639288 / High (40-80%) | 1979–2019 modeled baseline; dimensionless Aqueduct 4.0 demand-weighted administrative bws/Tot; geographic proxy confidence Medium | [World Resources Institute / WRIADMIN](https://files.wri.org/aqueduct/aqueduct-4-0-country-rankings.zip) / province_baseline row 6456; name_1=Nevada, indicator_name=bws, weight=Tot |

## Coverage, targets and illustrative numbers

- Coverage is counted from checked-in records: 19 registered documents (includes licence and assurance), 20 numerical claims, 16 company metric records (14 values and two absent numeric WUE values), three operators, seven curated location records, five state-context joins, three state scores, 36 India state/UT rows and zero verified exact facility/basin joins. Counts describe this curated release, not the world.
- The India map/table values are all-use annual groundwater flows (BCM/year) and published extraction stage (%), assessment year 2025, CGWB/PIB Annexure I. Every row retains its row locator; the source URL resolves through CGWB25. These are not AI extraction shares or stored-water depletion fractions.
- Company replenishment/positive-water targets are separate goals, not observations or offsets against reported consumption. Their direct sources, target years and boundaries are in research/company_targets.json. They are not treated as completed local benefits.
- Default scenario inputs (1000 IT MWh, PUE 1.2/1.4, consumptive WUE 1/0.1 L/IT kWh, grid consumption 1 L/facility kWh and carbon 0.4 kg/facility kWh) are author-selected hypothetical assumptions. Baseline 2.2 ML, alternative 1.5 ML, 31.8% modeled reduction, 200 MWh extra energy and 4.5 L/kWh shared-grid break-even are calculated examples, not company results, forecasts or savings achieved. Manufacturing/local scarcity impacts excluded.
- Future rates and dates to 2035 are conditional scenario controls, not empirical trend estimates. There is no supported global future AI-water range. Tests and export warnings keep this explicit.

## Current verification (supersedes the historical v0.2 test counts)

- Release v0.2.1 is published at commit `e415ebe556592d02fe3eb4527c8276257d1a41c5`; the application was deployed and checked live. [Verification record](verification_v021.md) links the actual CI and Pages runs.
- That release passed 58 Python tests, 13 JavaScript tests, seven Chrome interaction groups, 30 Python/JS parity cases, SQLite checks, PostgreSQL 16 comparisons for three views and five queries, notebook execution and repository checks. The current follow-up passes 65 Python tests locally (including seven Power BI handoff regressions), 13 JavaScript tests, the same parity checks, notebook execution and documentation checks. Its GitHub CI results belong to its own commit, not retroactively to the release.
- CI Lighthouse 12.8.2: mobile performance 97, accessibility/best practices/SEO 100; desktop 100 in all four categories. These are lab scores, not field measurements or full WCAG certification.
- Source refresh stages candidates, preserves reviewed data on failure and requires explicit exact-hash review promotion. Share links preserve assumptions and version; invalid input blocks results and export. PNG/JSON exports and source-fetch fallback have Chrome coverage.
- Current Power BI handoff checks numeric types, source references, warnings, missing values and boundary fields. It does not execute Power Query, DAX or the Desktop renderer. The workbook remains its documented v0.1 calculator/source snapshot.

## Unverified or incomplete

1. Native Excel Desktop, the author's PostgreSQL/pgAdmin Windows setup, and a built/refreshed Power BI report. [Desktop sign-off](desktop_signoff.md) identifies the exact evidence needed. Issue #5 remains open for native Excel. Historical limitations remain unchanged pending author confirmation.
2. Independent underlying company measurements, harmonized reporting years/fleets, unambiguous compatible annual WUE for all operators and full assurance scope evaluation.
3. Actual water supply basins, seasonal facility peaks, local competition/causal effects, discharge monitoring and AI chip lifecycle allocation. State proxies must remain proxies.
4. A measured global AI water inventory and a validated worldwide hotspot ranking. A [published global scenario candidate](global_water_estimates.md) is captured separately, **human review pending and headline-ineligible**; it does not close the inventory gap.
5. Physical-device/assistive-technology testing, full manual accessibility review and public-CDN field/load measurements. Automated Chrome and Lighthouse checks do not certify these.
6. GitHub repository social-preview upload is not confirmed. The website has its own social card. Maintainer path: Settings → General → Social preview → Edit → Upload `dist/social-preview.png`.
7. Social launch execution and user feedback remain separate from prepared distribution materials. No social posts were sent. There is no evidence of virality, external endorsement or hiring outcomes.

## Weaknesses a critic should raise

- Selection bias: three large operators and a curated small location sample cannot describe the industry. Report availability and language bias the selection.
- Confidence is not uncertainty quantification. Accurate copying does not establish measurement validity; company-commissioned context can omit local perspectives.
- The administrative join is reproducible but coarse. Historical demand weighting and water transfers can make a state proxy a poor description of a particular supply source.
- Annual volume alone misses seasonality, scarcity, quality and opportunity cost. Withdrawal, consumption and restoration benefits are not interchangeable.
- The model is intentionally simple: no cost, feasibility, time-varying marginal grid, lifecycle or probabilistic uncertainty model. Users can construct physically infeasible bundles.
- Hashes prove byte identity, not truth. Refresh requires human locator/definition review. Source links can move; raw reports are excluded for licensing and repository size.
- Cross-tool agreement tests accounting implementation; agreement is not real-world calibration. The workbook is a v0.1 snapshot, not a synchronized copy of the expanded evidence database.

## Scorecard out of ten

These are subjective review scores with stated reasons, not externally measured quality or a probability of getting hired.

| Dimension | Score | Reason |
|---|---:|---|
| Credibility | 8 | Source trails, boundaries and gaps visible; relies on self-reporting and a small curated sample. |
| Usefulness | 7 | Helps readers inspect disclosures and trade-offs; local engineering decisions still need supply and seasonal evidence. |
| Clarity | 8 | Plain-language story and static evidence; long technical comparison tables still require attention. |
| Reproducibility | 8 | Cross-language checks, Windows/Linux and PostgreSQL server CI; native BI/Excel and independent data remeasurement incomplete. |
| Originality | 7 | The disclosure-comparison and India-context combination adds value; neither the basic accounting nor risk datasets are novel research. |
| Shareability | 7 | Usable demo, social card, clear hook and contribution tasks; audience response has not been measured and virality cannot be promised. |

From a hiring reviewer’s perspective, the strongest signal is the author explaining a definition mismatch, tracing a value to its source and showing a failing test caught a real issue. More dashboards alone do not replace that understanding. Keep this independent portfolio work separate from employment accomplishments.

## Top five remaining fixes

1. Run the native [Desktop checks](desktop_signoff.md) and return actual reports and screenshots; never close a validation item from a self-test alone.
2. Obtain an independently corroborated local case with documented supply, seasonal water quantities and local stakeholder evidence.
3. Replace a regional proxy only when a legally reusable, validated supply-basin mapping is available; a campus coordinate alone is insufficient.
4. Human-review the new global scenario candidate and assess its assumptions before any headline promotion; broaden sampling before industry generalization.
5. Complete assistive-technology/physical-device checks and repository social-preview upload, then execute the community-appropriate [launch playbook](product_growth_audit_2026-10-22.md). Evaluate actual source contributions and successful reproductions.

## Reproduce on Windows

```powershell
git pull --ff-only
python scripts/reproduce.py
Get-Content outputs/powerbi/manifest.json
```

Use [PostgreSQL Windows instructions](verify_postgres_windows.md) for environment-variable setup. The current request-by-request status is [scope_completion.md](scope_completion.md); [validation_current.md](validation_current.md) is the current validation index. Earlier issue-fix details remain in [ci_recheck.md](ci_recheck.md); its historical counts and issue states are not current status.
