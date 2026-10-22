# ThirstyAI

**See what AI water headlines leave out.**

Explore published data-centre water disclosures and test how cooling choices shift water, energy and carbon.

**[Open the live demo](https://purushotmanmooper96-bit.github.io/thirstyai/)** · [Compare company reports](https://purushotmanmooper96-bit.github.io/thirstyai/#companies) · [Try the cooling lab](https://purushotmanmooper96-bit.github.io/thirstyai/#lab) · [தமிழ்](docs/translations/README.ta.md)

[![Reproducibility](https://github.com/purushotmanmooper96-bit/thirstyai/actions/workflows/checks.yml/badge.svg)](https://github.com/purushotmanmooper96-bit/thirstyai/actions/workflows/checks.yml)
[![MIT code](https://img.shields.io/badge/code-MIT-blue)](LICENSE)
![Python 3.12](https://img.shields.io/badge/Python-3.12-blue)

Free to try. No account or API key. Calculations run in your browser.

[Background, solutions and future outlook](docs/public_guide.md) · [Current validation](docs/validation_current.md)

## Try this first

Open **Company reporting**. Pick a withdrawal figure and a consumption figure. Inspect their periods and reporting scopes before comparing them.

Then open **Decision lab**. Keep the workload fixed and change a cooling assumption. Watch direct water and electricity-related water move separately. Copy a versioned scenario link or download a PNG result card to share the same assumptions.

**Lab inputs are illustrative, not measurements. A modelled reduction is not water saved in the real world.**

## Why this matters

AI runs in buildings that need electricity and cooling. Water can be used at the building, at power stations, and during chip manufacturing. The amount, timing and local significance depend on the system.

A company-wide total cannot tell you the water cost of your prompt. A regional stress score cannot tell you the actual supply conditions of a particular facility. ThirstyAI helps you see those distinctions.

## What you can explore

| View | What it does |
|---|---|
| Company reporting | Shows reported water, PUE/WUE definitions, periods, sources and caveats |
| Location context | Pairs officially named locations with limited regional context |
| Decision lab | Compares hypothetical operational water, electricity and carbon |
| India observatory | Explores government-reported all-user groundwater context |
| Future scenarios | Tests assumed demand and efficiency changes; not a global forecast |
| Evidence and solutions | Traces claims and explains practical questions and trade-offs |

**Coverage in this snapshot:** three operators, seven curated published location-water records and 36 Indian state/UT groundwater rows. These counts describe the curated release, not the world. [Coverage and evidence gaps](docs/evidence_status.md).

## What makes it useful

- Each registered source has a download hash, retrieval time and reviewed locator.
- Reported evidence, estimates, allocations and projections remain distinguishable.
- The model rejects withdrawal-based WUE in a consumption calculation and incompatible energy denominators.
- Python, JavaScript and SQLite outputs are checked against each other. PostgreSQL 16 is checked in CI.
- Evidence is downloadable as CSV/JSON. Third-party documents retain their original licences.

A hash identifies downloaded bytes; it does not independently verify the underlying environmental measurement. [Methodology](docs/methodology.md) · [Company case study](docs/case_study_company_reporting.md).

## Limits you should know

There is no verified global AI water total, universal litres-per-prompt number, company performance league table or verified exact facility/basin join here. The current regional overlay is a state-level proxy. India groundwater figures do not measure AI's share of extraction.

Company observations are self-reported; some selected metrics have limited external assurance. The lab excludes manufacturing and does not establish engineering feasibility or local scarcity impact.

Power BI is a build pack, not a validated PBIX. The Excel workbook is an earlier calculator/source snapshot; native Excel confirmation is not established by its cached values or by a closed issue. [Current validation record](docs/validation_v02.md) · [Excel checks](docs/excel_validation.md).

## Run locally

Install Python 3.12 and Node 22+ for the full checks. Core Python calculations use the standard library.

### Windows PowerShell

```powershell
git clone https://github.com/purushotmanmooper96-bit/thirstyai.git
Set-Location thirstyai
python scripts/reproduce.py
python -m http.server 8000 --directory dist
```

### Linux / macOS

```bash
git clone https://github.com/purushotmanmooper96-bit/thirstyai.git
cd thirstyai
python3 scripts/reproduce.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. The offline rebuild uses checked-in snapshots; it does not fetch fresh sources or validate desktop software.

[PostgreSQL and pgAdmin](docs/verify_postgres_windows.md) · [Power BI build](bi/BUILD_WINDOWS.md) · [Excel verifier](docs/excel_validation.md).

## Understand the repository

| Path | Purpose |
|---|---|
| `src/thirstyai/` | Python calculation engine |
| `research/` | Source metadata, provenance, claims and review notes |
| `data/processed/` | Attributed snapshots |
| `dist/` | Browser app and exports |
| `docs/` | Documentation and generated GitHub Pages copy |
| `sql/`, `bi/`, `excel/` | SQL, Power BI build pack and workbook |
| `tests/`, `scripts/` | Reproduction and verification |

ThirstyAI is separate from [Thirst](https://pypi.org/project/thirst/), an India-focused GPU command-line project. ThirstyAI does not control GPU jobs or measure your hardware.

The claim challenge asks three short source-backed questions and can export an explanation card. These test definitions, not company ethics.

## Help improve the evidence

Verify one locator, contribute a qualifying primary source, or reproduce a result. For corrections, include the original link, exact page/table, period, water definition and reporting boundary. Do not upload third-party PDFs without permission.

[Contributing guide](CONTRIBUTING.md) · [Issues](https://github.com/purushotmanmooper96-bit/thirstyai/issues).

If you want to follow future evidence updates, star the repository.

## Glossary and citation

**Withdrawal:** water taken from a source. **Consumption:** water not returned within the stated boundary. **PUE:** facility electricity divided by IT electricity. **WUE:** water per energy unit; always check both definitions. **Groundwater extraction stage:** annual extraction relative to annual extractable resources, not stored water emptied.

Built by **Purushotman Mooper** as independent portfolio work. Cite [CITATION.cff](CITATION.cff) and the original sources for environmental claims. Code: [MIT](LICENSE). Data/documents: [source-specific terms](docs/data_licensing.md).
