# Website verification, 22 October 2026

Canonical public URL: https://purushotmanmooper96-bit.github.io/thirstyai/

The old `/thirstyai/site/#lab` was opened in the connected browser and redirected to `/thirstyai/#lab`, with the illustrative warning visible. A query string is also preserved by the redirect code. No-JavaScript users receive a plain link to the canonical page. The canonical page contains real source-linked HTML findings, company disclosures, source tables, limitations and section anchors before JavaScript runs. Automated tests inspect that output; it no longer starts with only “Loading…”.

## Executed checks

- Desktop preview: company disclosure table rendered; null WUE says “Not extracted”; periods and boundaries visible. Scenario workload changed to 2000 MWh, keyboard ArrowRight changed baseline PUE from 1.20 to 1.21; outputs became 4.42 ML baseline and 3.00 ML alternative, as calculated. These are hypothetical operational consumption, not observed savings.
- Mobile public page, explicit viewport 390 × 844: document width 375 CSS pixels (scrollbar excluded), no page-wide horizontal overflow; company table scrolls inside its region. Navigation scrolls horizontally. Temporary viewport was reset. This is browser emulation, not a physical-phone test.
- Visible focus styles, native labeled sliders and inputs; wide new tables are keyboard-focusable regions. A complete screen-reader / keyboard audit remains open.
- Sampled text contrast ratios: muted `#acbbc4` on panel `#111c26` **8.75:1**; label `#a7bac5` on background `#0c131b` **9.31:1**; link `#8ce2da` on background **12.45:1**; primary text `#e8f0f2` on warning background `#24241e` **13.50:1**. These exceed 4.5:1, but a sample is not full WCAG AA certification. Inline links are underlined and body mobile text was enlarged.
- Custom social card is 1200 × 630 PNG, 34,060 bytes. Open Graph and Twitter large-image metadata point to it. Setting GitHub's repository-specific social preview is a separate settings action.
- Scenario JSON includes a warning field; future CSV has the warning as its first column and in every row. Evidence JSON contains a scenario-warning field while real disclosures remain explicitly reported evidence. The India/claims CSVs contain actual evidence, not hypothetical calculator inputs.

## Lighthouse: actual CI measurements

[Lighthouse run 39758457275](https://github.com/purushotmanmooper96-bit/thirstyai/actions/runs/39758457275), commit `882b7209b87cc2aa73ef4cf8248c4bb067290bca`. Lighthouse 12.8.2, CI's Chrome, served `dist/` over localhost. These are lab scores, **not** public-CDN performance or real-user field measurements. Raw JSON/HTML are retained in the run's `lighthouse-reports` artifact; compact results are in `outputs/lighthouse_summary.json`.

| Profile | Performance | Accessibility | Best practices | SEO | LCP | CLS |
|---|---:|---:|---:|---:|---:|---:|
| Mobile | 89 | 100 | 100 | 100 | 2225 ms | 0 |
| Desktop | 100 | 100 | 100 | 100 | 494 ms | 0 |

The earlier audit found inline-link distinction, small fonts and a redundant brand accessible-name mismatch. Links/fonts were fixed. Although the later score was 100, one unweighted desktop label advisory persisted; the redundant brand aria-label was then removed so its visible text supplies its accessible name. Subsequent CI audits accompany later commits; scores above describe only the stated commit, never an assumed future result.

Uncompressed initial asset total at that checkpoint: **162,441 bytes** across HTML, CSS, application/model scripts, icon and evidence JSON, calculated from local file sizes (`outputs/site_weight.json`). Social card is not part of initial rendering. External font requests were removed. This is not gzip/Brotli transfer size, and hosting caches differ from the CI server. Remaining performance work includes render-blocking CSS and deployment cache policy; no unsupported hosting-header control is claimed.

## Re-run on Windows

```powershell
python scripts/reproduce.py
python -m http.server 8000 --directory dist
```

In another PowerShell window, with Node and Chrome installed:

```powershell
npx --yes lighthouse@12.8.2 http://localhost:8000/ --output=html --output-path=./outputs/lighthouse-mobile.html
npx --yes lighthouse@12.8.2 http://localhost:8000/ --preset=desktop --output=html --output-path=./outputs/lighthouse-desktop.html
```

Use Chrome DevTools device mode for 390 × 844, keyboard navigation and JavaScript-disabled reading. Report version, URL, profile and date with results. Do not compare a single variable-speed Lighthouse run as a stable benchmark.
