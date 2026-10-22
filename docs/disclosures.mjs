export function displayedWater(c, unitMode, fmt) {
  if (c.value === null) return "Not extracted";
  if (unitMode === "litres" && c.unit === "ML")
    return `${fmt(c.value * 1e6)} L (source: ${fmt(c.value)} ML)`;
  return `${fmt(c.value, Number.isInteger(c.value) ? 0 : 2)} ${c.unit}`;
}
export function createDisclosures({ data, pagehead, esc, fmt, link }) {
  let company = "all",
    metric = "all",
    units = "original";
  function matching() {
    return data.companies.filter(
      (c) =>
        (company === "all" || c.company === company) &&
        (metric === "all" || c.metric === metric),
    );
  }
  function row(c) {
    return `<tr><td>${esc(c.company)}<br>${esc(c.metric)}</td><td>${esc(displayedWater(c, units, fmt))}</td><td>${esc(c.period)}<br>${esc(c.geography)}<br>${esc(c.scope)}</td><td>${esc(c.water_metric)}<br>${esc(c.energy_denominator)}<br>Extraction: ${esc(c.confidence)}</td><td>${link(c.source_id)}<br>${esc(c.locator)}<br>${esc(c.caveat)}<br><strong>Definitions / periods / fleets differ.</strong></td></tr>`;
  }
  function cards() {
    return (
      matching()
        .map(
          (c) =>
            `<details class="disclosure-card"><summary>${esc(c.company)} · ${esc(c.metric)} · ${esc(displayedWater(c, units, fmt))}</summary><p>${esc(c.period)} · ${esc(c.scope)}</p><p>${esc(c.water_metric)} · ${esc(c.energy_denominator)} · extraction confidence ${esc(c.confidence)}</p><p>${link(c.source_id)} · ${esc(c.locator)}</p><p>${esc(c.caveat)}</p><p>${esc(c.assurance)}</p></details>`,
        )
        .join("") || "<p>No records match these filters.</p>"
    );
  }
  function companies() {
    return `${pagehead("Company reporting", "Same word. Different water accounts.", "Compare reporting definitions, not company performance. Pick a company or metric, then open its scope and original locator.")}<div class="callout warning"><strong>Company self-reported; not independently remeasured by ThirstyAI.</strong> Selected metrics have limited external assurance. Missing numeric WUE does not mean zero.</div><div class="company-filters"><label class="filter-label">Company <select id="company-filter"><option value="all">All companies</option>${[...new Set(data.companies.map((c) => c.company))].map((x) => `<option ${company === x ? "selected" : ""}>${esc(x)}</option>`).join("")}</select></label><label class="filter-label">Metric <select id="metric-filter"><option value="all">All metrics</option>${["withdrawal", "consumption", "WUE", "PUE"].map((x) => `<option ${metric === x ? "selected" : ""}>${x}</option>`).join("")}</select></label><label class="filter-label">Display units <select id="unit-filter"><option value="original">Original source units</option><option value="litres" ${units === "litres" ? "selected" : ""}>Convert ML to litres</option></select></label></div><p class="conversion">ML = million litres. Gallons remain as reported; no unverified gallon definition is assumed. Unit conversion never makes unlike fleets, periods or water definitions equivalent.</p><p id="company-count" aria-live="polite"></p><div id="company-cards">${cards()}</div><details><summary>Inspect the full comparison table</summary><div class="table-wrap" tabindex="0" role="region" aria-label="Company reporting comparison"><table><thead><tr><th>Company / metric</th><th>Value and unit</th><th>Period / scope</th><th>Definition / confidence</th><th>Source / locator / caveat</th></tr></thead><tbody id="company-rows">${matching().map(row).join("")}</tbody></table></div></details><div class="toolbar"><a href="data/company_water_reports.csv" download class="btn ghost small">Download disclosures ↓</a><a href="#locations" class="btn ghost small">Inspect location context ↗</a></div><h2>Ask for the missing denominator.</h2><p>Ask for monthly withdrawal and consumption, water source, WUE definition, supply basin and assurance scope. Replenishment belongs in a separate ledger; it does not erase consumption in the same place and season.</p>`;
  }
  function bindCompanies() {
    const update = () => {
      company = document.querySelector("#company-filter").value;
      metric = document.querySelector("#metric-filter").value;
      units = document.querySelector("#unit-filter").value;
      document.querySelector("#company-cards").innerHTML = cards();
      document.querySelector("#company-rows").innerHTML = matching()
        .map(row)
        .join("");
      document.querySelector("#company-count").textContent =
        `${matching().length} of ${data.companies.length} metric records shown. Missing values remain missing.`;
    };
    for (const id of ["company-filter", "metric-filter", "unit-filter"])
      document.getElementById(id).onchange = update;
    update();
  }
  function locations() {
    return `${pagehead("Location context", "A regional warning is not a site diagnosis.", "All curated officially named locations appear below. Unmatched regional context stays unknown. No coordinates or supplying basins are guessed.")}<div class="metric-grid"><article class="card"><div class="number">${data.locations.length}</div>published location records</article><article class="card"><div class="number">${data.overlay.length}</div>state-context matches</article><article class="card"><div class="number">0</div>verified exact facility/basin joins</article></div><div class="callout warning"><strong>STATE PROXY — NOT FACILITY OR BASIN STRESS.</strong> WRI baseline: 1979–2019, model release 2023. Not current site conditions or causal harm.</div><div class="table-wrap" tabindex="0" role="region" aria-label="Locations with regional context"><table><thead><tr><th>Published location</th><th>Reported water / boundary</th><th>Regional context</th><th>Source trail</th></tr></thead><tbody>${data.locations
      .map((r) => {
        const context = data.overlay.find(
          (x) => x.location_id === r.location_id,
        );
        return `<tr><td>${esc(r.company)}<br>${esc(r.location)}</td><td>${esc(r.value)} ${esc(r.unit)}<br>${esc(r.water_metric)} · ${esc(r.period)}<br>${esc(r.scope)}<br>Extraction: ${esc(r.confidence)}<br>${esc(r.caveat)}</td><td>${context ? `${esc(context.stress_region)}<br>${esc(context.stress_label)}<br>Score ${esc(context.stress_score)} (dimensionless)<br>${esc(context.stress_period)}<br>Geographic match: ${esc(context.match_confidence)}` : "Unknown — no verified regional match in this release"}</td><td>${link(r.source_id)}: ${esc(r.locator)}${context ? `<br>${link(context.stress_source_id)}: ${esc(context.stress_locator)}` : ""}</td></tr>`;
      })
      .join(
        "",
      )}</tbody></table></div><p>WRI Aqueduct extract: CC BY 4.0. No scarcity-weighted footprint is calculated.</p><div class="buttons"><a href="data/location_water.csv" download class="btn ghost">Download all location records ↓</a><a href="data/location_stress_overlay.csv" download class="btn ghost">Download matched context ↓</a></div><h2>India is a separate context study</h2><p>${link("WRIINDIA26", "WRI India’s siting analysis")} connects data centres and regional stress. Our CGWB table covers all water users and does not estimate AI extraction.</p><a href="#india" class="btn ghost">Inspect all-user groundwater context ↗</a>`;
  }
  return { companies, bindCompanies, locations };
}
