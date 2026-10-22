<div align="center">

# ThirstyAI

**AI has a water footprint. The useful question is: where, when, and which water?**

[Open the evidence atlas](https://purushotmanmooper96-bit.github.io/thirstyai/) · [Company case study](docs/case_study_company_reporting.md) · [Evidence gaps](docs/evidence_status.md) · [தமிழ் அறிமுகம்](docs/translations/README.ta.md) · [Audit](docs/audit.md)

[![Reproducibility](https://github.com/purushotmanmooper96-bit/thirstyai/actions/workflows/checks.yml/badge.svg)](https://github.com/purushotmanmooper96-bit/thirstyai/actions/workflows/checks.yml)
[![MIT code licence](https://img.shields.io/badge/code-MIT-blue)](LICENSE)
![Python 3.12](https://img.shields.io/badge/Python-3.12-blue)

</div>

## The problem in 60 seconds

AI runs on computers in buildings, connected to power grids and water systems. Some cooling systems evaporate water. Some power stations also consume water to make electricity. Making chips has a separate water footprint.

That does not mean every AI question uses the same amount of water, or that every data centre causes a shortage. **The risk depends on the water source, season, local supply and other users.** A global average can hide a local problem. A dramatic “water per prompt” headline can hide the accounting choices.

ThirstyAI lets you inspect company disclosures, explore regional context and test conditional cooling choices. It shows its sources and the questions it cannot yet answer.

## Why it happens: heat → cooling → water

Computers turn electricity into heat. The building must move that heat somewhere. Evaporating water can help reject heat, while dry cooling can use less direct water and require more electricity under some conditions. Liquid cooling moves heat away from chips; it does not, by itself, tell you how the building finally rejects that heat. [Microsoft design disclosure, energy trade-offs section](https://www.microsoft.com/en-us/microsoft-cloud/blog/2024/12/09/sustainable-by-design-next-generation-datacenters-consume-zero-water-for-cooling/).

## How AI uses water, in plain words

- **At the building:** cooling and other site operations. Taking water and consuming it are different quantities.
- **At the power station:** electricity production can consume water somewhere else. Its cooling system and location matter. [NREL review, abstract](https://research-hub.nlr.gov/en/publications/operational-water-consumption-and-withdrawal-factors-for-electric-4/).
- **Before operation:** chip manufacturing and construction. This calculator excludes them; it does not pretend that exclusion makes them zero. [TSMC reporting](https://esg.tsmc.com/en-US/articles/414).

## What the evidence says

These are different questions and boundaries, **not a company ranking**. High confidence below means confidence in extraction and attribution, not independent measurement of the underlying operations.

| Finding | Year / geography | Boundary and type | Source / exact locator | Confidence |
|---|---|---|---|---|
| **485 TWh/year** estimated; **950 TWh/year** projected | 2025 / 2030, global | Electricity for all data centres, not AI alone; estimate / conditional projection | [IEA 2026 executive summary, demand outlook](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary), C01–C02 | High / Medium |
| **10,523 million gallons** | 2025, Google global owned and fully leased data centres | Company-reported consumption; excludes seawater/brackish water, may include estimates; not AI-only | [Google 2026 report p.96, Water](https://sustainability.google/files/google-2026-environmental-report.pdf), CORP04 | High |
| **8,170 ML** | FY25 ending June 2025, Microsoft global enterprise | Company-reported consumption across offices, labs and data centres; not a DC-only total | [Microsoft 2026 fact sheet p.7, Table 8](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2026-Microsoft-Environmental-Data-Fact-Sheet-PDF.pdf), CORP08 | High |
| **2,974 ML** | 2024, Meta global data centres | Company-reported operational water consumption, not AI-only | [Meta 2025 index p.11](https://sustainability.atmeta.com/asset/2025-environmental-data-index/), CORP14 | High |

ML means million litres. Google reports gallons; the source unit is retained. Reports describe limited external assurance for selected metrics; ThirstyAI has not independently audited or remeasured the company values. [Full comparison, WUE/PUE definitions and omissions](docs/case_study_company_reporting.md).

We do not manufacture a common uncertainty range from unlike reports. There is **no verified global AI water total here**. The Google serving study's prompt allocation is documented in the claim register, with its narrow boundary; it is never generalized to all AI.

## Where we do and do not know

| Included in v0.2 | What that does not establish |
|---|---|
| Three operators; 16 metric records, including two missing numeric WUE values | A representative global sample or a performance ranking |
| Seven curated official location water records | Independently metered facilities or complete fleet coverage |
| Five location records matched to three US states' WRI context | Exact basin stress: **zero verified facility/basin joins**; no hotspot ranking |
| 36 Indian state/UT groundwater rows, 2025 | AI's share of extraction, local supply or groundwater storage depletion |
| Source links, SHA-256 captures, timestamps and reviewed locators | Independent assurance of the underlying source |
| Python, browser and SQLite calculation checks; PostgreSQL verifier and CI | A validated PBIX or Microsoft Excel Desktop confirmation |

Coverage counts describe this curated release, not the world. WRI's administrative stress context uses a **1979–2019 modeled baseline**, not a reading of current site conditions. [Overlay, row locators and licence](docs/location_overlay.md).

India's groundwater table is all-user context. A separate [WRI India analysis](https://wri-india.org/data/more-half-indias-data-centres-are-water-stressed-regions) explicitly examines data-centre siting and water stress; we attribute that analysis without redistributing its commercial facility inventory or inventing AI extraction shares. The title describes a research question, not a demonstrated local causal effect.

## What could happen by 2030–2035

Demand growth can increase total resource use even when each task becomes more efficient. Electricity supply, cooling design, climate, regulation and where new capacity is built can change the water outcome. IEA's projection above is conditional, and covers all data centres.

The site's future lab explores assumed demand growth and efficiency through 2035. **ILLUSTRATIVE INPUTS — NOT MEASUREMENTS.** It starts with a hypothetical workload, holds cooling/grid assumptions fixed, and applies selected rates. It is not a forecast of global AI water, technology adoption, droughts or savings achieved. We provide no unsupported future water range. [Scenario method](docs/methodology.md).

## What can be done

These are practical questions and actions, not certified engineering advice or promised savings. “Partial” means supporting mechanism/context exists, but outcomes need local measurement.

| Who acts | Action | Evidence and limit |
|---|---|---|
| Companies | Report withdrawal and consumption separately, with period, water source, fleet and WUE denominator | Strong evidence of definition differences: [company case study](docs/case_study_company_reporting.md); reporting alone saves no water |
| Companies | Compare dry, evaporative and hybrid options using both direct water and electricity | Partial: [MS24 design discussion](https://www.microsoft.com/en-us/microsoft-cloud/blog/2024/12/09/sustainable-by-design-next-generation-datacenters-consume-zero-water-for-cooling/); site performance must be tested |
| Companies | Reduce energy per useful result with suitable models, caching and efficient serving; track total demand too | Partial: [Google study, methods / Table 2](https://arxiv.org/html/2508.15734v1); company-specific, no universal savings factor |
| Companies | Assess supplying generators, not only building water; keep replenishment in a separate ledger | Partial: [NREL abstract](https://research-hub.nlr.gov/en/publications/operational-water-consumption-and-withdrawal-factors-for-electric-4/) and [Meta benefits method p.5](https://sustainability.atmeta.com/asset/2024-volumetric-water-benefits/); time, place and additionality matter |
| Governments | Require local supply, seasonal demand and drought-contingency evidence for proposed projects | Partial / policy proposal: [WRI screening limits](https://www.wri.org/research/aqueduct-40-updated-decision-relevant-global-water-risk-indicators); regional scores cannot replace local review |
| Governments | Require discharge-quality monitoring and clear permits alongside volume reporting | Partial: [TSMC supplier programme](https://esg.tsmc.com.tw/en-US/articles/413); programme disclosure is not proof of local effluent safety |
| Communities | Ask utilities/operators about the actual supply basin, dry-season demand and other users; request accessible records | Partial: [Meta Prineville context p.9](https://sustainability.atmeta.com/asset/2024-volumetric-water-benefits/); no causal estimate of community harm here |
| Individuals / developers | Choose an adequate tool, avoid unnecessary repeat computation, and evaluate quality alongside resource use | Weak quantified evidence for individual water savings; no personal litres-saved counter is offered |
| Everyone maintaining this project | Verify a source, correct a definition, refresh evidence and disclose gaps | Process recommendation; inspect [provenance](research/provenance.json), tests and [contributing guide](CONTRIBUTING.md) |

## What you can do

Open the [decision lab](https://purushotmanmooper96-bit.github.io/thirstyai/#lab), compare equal workloads, then inspect a source before sharing its number. In the company view, ask why two values have different boundaries. Submit a sourced correction or help close one clearly defined gap. Share the evidence and its limitation together.

## How ThirstyAI differs from other tools

[Thirst](https://pypi.org/project/thirst/) is an existing India-focused NVIDIA GPU command-line project. Its maintainer describes scheduling/power controls, GPU energy measurement and modeled water/carbon receipts. We reviewed its published description, not its performance. ThirstyAI is a separate, unaffiliated public evidence atlas and reporting-comparison lab; it does not control GPU jobs or measure your hardware. Both can be useful for different questions. Similar names do not imply partnership or interchangeable results.

## How to use / reproduce

Core dependencies: Python 3.12 and Node 22+ for the full checks. No API key or paid account. PostgreSQL's driver is optional. Browser app has no build-time package install.

**Windows / PowerShell**

```powershell
git clone https://github.com/purushotmanmooper96-bit/thirstyai.git
Set-Location thirstyai
python scripts/reproduce.py
python -m http.server 8000 --directory dist
```

**Linux / macOS**

```bash
git clone https://github.com/purushotmanmooper96-bit/thirstyai.git
cd thirstyai
python3 scripts/reproduce.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. Stop with Ctrl+C. Use HTTP rather than double-clicking the HTML file. The offline rebuild uses attributed processed snapshots, rebuilds SQL/browser exports, and checks semantic constraints and Python/JavaScript/SQLite parity. It does not re-fetch sources or validate desktop applications.

[PostgreSQL / pgAdmin steps](docs/verify_postgres_windows.md) · [Power BI click-by-click build](bi/BUILD_WINDOWS.md) · [Excel validation cases](docs/excel_validation.md) · [Current validation record](docs/validation_v02.md).

For a deliberate source refresh: `python scripts/ingest.py --refresh`, review changed source locators and definitions, then rebuild. Raw downloads stay outside Git. A changed manually reviewed document must not silently inherit approval. See [methodology](docs/methodology.md), [licensing](docs/data_licensing.md) and the [ten-topic evidence status](docs/evidence_status.md).

## Small glossary

- **WUE:** water use effectiveness, often litres per energy unit. Always ask which water quantity and which energy denominator.
- **PUE:** total facility electricity divided by IT electricity. It is an energy ratio, not a water score.
- **Withdrawal:** water taken from a source.
- **Consumption:** withdrawn water not returned within the stated boundary, often through evaporation.
- **Stage of groundwater extraction:** annual extraction divided by annual extractable groundwater, expressed as a percentage. It is not a percentage of stored groundwater emptied.
- **Projection / allocation:** a conditional future result / a share assigned using an accounting method; neither is a universal measurement.

## Cite

Purushotman Mooper. *ThirstyAI: evidence atlas and decision lab*, v0.2. See [CITATION.cff](CITATION.cff). Cite original sources for environmental claims and retain their boundary, period and caveat. Independent portfolio work; no endorsement by source organisations or the author's former employer is implied.

Original code: [MIT](LICENSE). Third-party data and documents retain their own terms. [Contribute a correction](CONTRIBUTING.md) · [Release notes](docs/CHANGELOG.md).
