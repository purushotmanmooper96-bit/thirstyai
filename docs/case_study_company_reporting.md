# Three operators, different reporting boundaries

Company disclosures now provide real water observations. They do **not** establish AI-only water use, or a fair environmental league table.

| Operator and reporting period | What is published | Why comparisons need care |
|---|---|---|
| Google, calendar 2025 | Global withdrawal 14,689 and consumption 10,869 million gallons; owned and fully leased data-centre withdrawal 13,562 and consumption 10,523 million gallons. PUE 1.09. | Corporate and data-centre boundaries differ. Source uses gallons, while the other two use ML. No compatible fleet WUE value was extracted from this annual report. |
| Microsoft, FY25 ending 30 June 2025 | Enterprise withdrawal 13,266 ML and consumption 8,170 ML. Global-average PUE 1.17. Owned-datacentre WUE 0.27 L/kWh. | Enterprise totals include owned/leased offices, datacentres and labs. Inspected WUE endnote does not explicitly resolve consumption vs withdrawal and energy denominator, so it is barred from the consumptive model. |
| Meta, calendar 2024 in its current 2025 report/index | Operational withdrawal 5,637 ML and consumption 3,123 ML; data-centre withdrawal 4,145 ML and consumption 2,974 ML. PUE 1.08. | Different year. Construction water is reported separately and excluded from the operational withdrawal total. WUE methodology is withdrawal per IT kWh; a numeric fleet WUE was not located in the inspected report/index. |

These are extracted company-reported quantities, not independently remeasured by ThirstyAI. A blanket “unaudited” label would also be misleading: the reports identify third-party limited assurance for selected metrics. Limited assurance is not independent monitoring of every site or a full scientific validation. Our `assurance` field preserves that distinction.

## Find the original tables

- Google 2026 Environmental Report: PDF p.96 Water tables; p.97 location table; PUE p.15. https://sustainability.google/files/google-2026-environmental-report.pdf
- Microsoft 2026 Environmental Data Fact Sheet: Table 8 p.7, location Table 15 pp.25–26. https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2026-Microsoft-Environmental-Data-Fact-Sheet-PDF.pdf
- Microsoft 2026 Environmental Sustainability Report: pp.23–24, WUE endnote 12 p.64. https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/2026-Microsoft-Environmental-Sustainability-Report-PDF.pdf
- Meta 2025 Environmental Data Index: PDF pp.8–11; definitions p.18. https://sustainability.atmeta.com/asset/2025-environmental-data-index/
- Meta selected-metric review, linked from that reporting page: https://sustainability.atmeta.com/asset/2025-independent-accountants-review-report/

The report pages/indexes were opened and downloaded on 22 October 2026. Hashes and retrieval times are in research/provenance.json. High confidence means a number was extracted and located carefully, not that ThirstyAI independently measured it. Null WUE stays null.

## What should readers ask for?

Ask for the same reporting period, included/excluded fleet, direct withdrawal and consumption separately, source water types, seasonal peaks, exact WUE numerator and denominator, geographic supply sources, indirect electricity water and the specific assurance scope. Do not subtract replenishment from local consumption as if it reverses an impact in the same place and time.

`company_water_reports.csv` preserves each metric as a separate observation. `vw_company_reporting` displays its source and flags mismatched periods, units, scopes or definitions. Its purpose is to compare **reporting**, not rank companies by one misleading total.
