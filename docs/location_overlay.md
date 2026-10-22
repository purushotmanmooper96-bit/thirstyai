# Locations with water disclosures and regional water-stress context

**Coverage: five curated location records link to three named US states. Exact facility/basin stress joins: zero.** This is deliberately a state-level context overlay, not a facility-risk map or a claim that the named campus draws from that state's average water source.

The company reports explicitly name the locations and their states. We join those state names to WRI Aqueduct 4.0's `province_baseline` sheet, indicator `bws`, total-demand weight `Tot`. The dataset documents a 1979–2019 baseline. It is not a measurement of 2024/2025 local conditions.

| Published location | Water evidence | Stress context matched |
|---|---|---|
| Google Henderson, Nevada | 2025 direct consumption; Google26 p.97 | Nevada administrative baseline |
| Google Mesa, Arizona | 2025 direct consumption; Google26 p.97 | Arizona administrative baseline |
| Microsoft Phoenix, Arizona | FY25 withdrawal; MS26DATA p.25; exclusions p.26 | Arizona administrative baseline |
| Meta Los Lunas, New Mexico | 2024 withdrawal; META25 p.9 | New Mexico administrative baseline |
| Meta Mesa, Arizona | 2024 withdrawal; META25 p.9 | Arizona administrative baseline |

Exact scores, labels and spreadsheet row locators are retained in `regional_water_stress.csv` and the combined `location_stress_overlay.csv`. No coordinates are supplied or guessed. Quilicura and Singapore remain unmatched in this deliberately small regional extraction, not “low risk”. High extraction confidence does not resolve the medium geographic confidence of a state proxy.

## What this does and does not answer

The table connects actual company water reporting to an openly licensed water-stress dataset at an explicitly coarse scale. It does not identify the water utility, groundwater assessment unit, inter-basin transfers, monthly scarcity or causal impact on another user. It must not be labeled “five high-risk facilities” or a comprehensive global hotspot ranking.

WRI: https://www.wri.org/data/aqueduct-40-country-rankings
Download: https://files.wri.org/aqueduct/aqueduct-4-0-country-rankings.zip
Licence: CC BY 4.0, https://github.com/wri/Aqueduct40/blob/master/README.md
Citation: Kuzma et al. (2023), Aqueduct 4.0, doi:10.46830/writn.23.00061. Source: WRI Aqueduct, accessed 22 October 2026. Only a small attributed extract is bundled; the full workbook is excluded.

## India connection

WRI India's 18 May 2026 analysis explicitly connects data-centre distribution and regional water stress. It names Maharashtra, Tamil Nadu, Karnataka, Telangana and Uttar Pradesh as the concentrated states and identifies its sources as DataCenterMap and WRI Aqueduct. We link that primary published analysis; we have not recreated its facility-level join or redistributed the commercial facility inventory. Our separate CGWB table remains all-use groundwater context, not AI water attribution.

https://wri-india.org/data/more-half-indias-data-centres-are-water-stressed-regions

Next research step: a legally reusable exact facility location and documented water supply, followed by a basin join and local verification. Until then the precise overlap count remains zero.
