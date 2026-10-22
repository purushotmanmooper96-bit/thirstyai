import { createLab } from "./lab.mjs";
import { createOverview } from "./overview.mjs";
import { createDisclosures } from "./disclosures.mjs";
import { decodeScenario, futureCsvRows } from "./scenario.mjs";
import { showEvidenceFallback } from "./sharing.mjs";
import { createChallenge } from "./challenge.mjs";
import { bindSkipLink } from "./navigation.mjs";
import {
  calculate,
  compare,
  breakEvenGrid,
  project,
  DEFAULTS,
  ALTERNATIVE,
} from "./model.mjs";
const main = document.querySelector("main"),
  nav = document.querySelector("#nav");
bindSkipLink(document.querySelector(".skip"), main);
const icons = {
  overview: "M3 3h7v7H3z M14 3h7v7h-7z M3 14h7v7H3z M14 14h7v7h-7z",
  lab: "M9 3v6l-5 10a1 1 0 0 0 1 2h14a1 1 0 0 0 1-2L15 9V3 M7 3h10 M7 15h10",
  india:
    "M12 3c-4 0-7 3-7 7 0 5 7 11 7 11s7-6 7-11c0-4-3-7-7-7Z M9 10a3 3 0 1 0 6 0 3 3 0 1 0-6 0",
  futures: "M3 19V5 M3 19h18 M6 15l5-5 4 3 6-8",
  evidence: "M5 3h11l4 4v14H5z M15 3v5h5 M8 12h9 M8 16h6",
  solutions:
    "M12 3v3 M4 6l2 2 M20 6l-2 2 M9 18h6 M10 21h4 M8 14a6 6 0 1 1 8 0c-1 1-1 2-1 4H9c0-2 0-3-1-4",
};
const pages = [
  ["overview", "Overview"],
  ["lab", "Decision lab"],
  ["companies", "Company reporting"],
  ["locations", "Location context"],
  ["india", "India observatory"],
  ["futures", "Future scenarios"],
  ["evidence", "Evidence & methods"],
  ["solutions", "Solutions playbook"],
  ["challenge", "Claim challenge"],
];
nav.innerHTML = pages
  .map(
    ([id, t]) =>
      `<a href="#${id}" data-page="${id}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="${icons[id] ?? icons.evidence}"/></svg>${t}${id === "india" ? '<span class="nav-count">36</span>' : ""}</a>`,
  )
  .join("");
const state = {
  b: { ...DEFAULTS },
  a: { ...ALTERNATIVE },
  growth: 10,
  efficiency: 5,
};
const fmt = (n, d = 0) =>
  new Intl.NumberFormat("en", {
    maximumFractionDigits: d,
    minimumFractionDigits: d,
  }).format(n);
const volume = (n) =>
  Math.abs(n) >= 1e6
    ? `${fmt(n / 1e6, 2)} ML`
    : Math.abs(n) >= 1000
      ? `${fmt(n / 1000, 1)} kL`
      : `${fmt(n)} L`;
const esc = (s) =>
  String(s).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const tag = (text, type = "") =>
  `<span class="tag ${type}">${esc(text)}</span>`;
const download = (name, text, type = "text/csv") => {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 5000);
};
const csv = (rows) =>
  rows
    .map((r) =>
      r.map((v) => `"${String(v ?? "").replace(/"/g, '""')}"`).join(","),
    )
    .join("\r\n");
function toast(text) {
  const el = document.querySelector("#toast");
  el.textContent = text;
  el.classList.add("show");
  setTimeout(() => el.classList.remove("show"), 3000);
}
let data;
try {
  const r = await fetch("./data/evidence.json");
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  data = await r.json();
} catch (e) {
  showEvidenceFallback(main, e.message);
}
const source = (id) => data.sources.find((s) => s.id === id);
const link = (id, label) =>
  `<a href="${esc(source(id).url)}" target="_blank" rel="noopener noreferrer">${esc(label ?? source(id).publisher)} ↗</a>`;
const overview = () => createOverview({ data, tag, link, fmt })();
const { lab, bindLab } = createLab(state, {
  fmt,
  volume,
  tag,
  pagehead: (...x) => pagehead(...x),
  download,
  toast,
  rerender: () => render(),
});
const { companies, bindCompanies, locations } = createDisclosures({
  data,
  pagehead: (...x) => pagehead(...x),
  esc,
  fmt,
  link,
});
const { challenge, bindChallenge } = createChallenge({
  data,
  esc,
  link,
  download,
  toast,
});
const pagehead = (k, t, p) =>
  `<div class="pagehead"><div class="eyebrow">${k}</div><h1>${t}</h1><p>${p}</p></div>`;

function india() {
  return `${pagehead("India observatory", "One country. Very different water contexts.", "Explore the 2025 reported groundwater assessment across 36 states and union territories. These annual, all-use indicators do not measure AI water use or establish local data-centre impact.")}<div class="kpis"><article class="card kpi"><div class="label">NATIONAL STAGE OF EXTRACTION</div><div class="number">60.63<small>%</small></div><div class="note">Reported national value · C03</div></article><article class="card kpi"><div class="label">GEOGRAPHIC COVERAGE</div><div class="number">36 <small>states / UTs</small></div><div class="note">Annexure I · one observation per state/UT</div></article><article class="card kpi"><div class="label">INDIA FACILITY / SUPPLY JOINS</div><div class="number">0</div><div class="note">No India facility supply joins inferred</div></article></div><div class="callout warning"><strong>Read the ratio correctly.</strong> Stage of extraction = annual extraction ÷ annual extractable groundwater resource. A value above 100% means annual extraction exceeds that assessed resource; it is not “more than 100% of groundwater already gone.” State averages can hide local variation.</div><article class="card"><div class="sectionhead"><div><h2>Groundwater, in context.</h2><p>Reported values retained; volumes are rounded by the source.</p></div><a href="data/india_groundwater_2025.csv" download class="btn ghost small">Download data ↓</a></div><div class="toolbar"><input id="india-search" type="search" aria-label="Search state or UT" placeholder="Search a state or union territory…"><select id="india-sort" aria-label="Sort states"><option value="stage">Extraction stage: high → low</option><option value="name">State / UT: A → Z</option><option value="extraction">Annual extraction: high → low</option></select><label class="checkbox"><input id="india-over" type="checkbox"> Above 100% only</label></div><div id="india-result"></div><p class="source-note">${link("CGWB25")} · Annexure I · Assessment year 2025 · BCM = billion cubic meters. Do not recompute published stage values from rounded volume columns; this can materially distort small jurisdictions.</p></article><div class="cols"><article class="card"><h3>For India's data-centre hubs</h3><p class="subtle">Mumbai/Navi Mumbai and Pune sit within Maharashtra; Chennai within Tamil Nadu; Bengaluru within Karnataka; Hyderabad within Telangana. Delhi NCR spans multiple jurisdictions including Delhi, Haryana and Uttar Pradesh.</p><div class="insight">Next evidence needed: exact facility water source, assessment unit or basin, cooling configuration, operating load and monthly demand. A state ratio cannot answer those questions.</div></article><article class="card"><h3>Ask before making a siting claim</h3><div class="steps"><p>Where does the facility actually source water?</p><p>What happens in the dry season?</p><p>Which local users share that source?</p></div></article></div>`;
}
function updateIndia() {
  const q = document.querySelector("#india-search").value.toLowerCase(),
    sort = document.querySelector("#india-sort").value,
    over = document.querySelector("#india-over").checked;
  let rows = data.india.filter(
    (r) => r.state.toLowerCase().includes(q) && (!over || r.stage_pct > 100),
  );
  rows.sort((a, b) =>
    sort === "name"
      ? a.state.localeCompare(b.state)
      : sort === "extraction"
        ? b.extraction_bcm - a.extraction_bcm
        : b.stage_pct - a.stage_pct,
  );
  document.querySelector("#india-result").innerHTML =
    `<p class="countline">Showing ${rows.length} of 36 state/UT observations · government reported · 2025</p><div class="table-wrap"><table><thead><tr><th>State / Union territory</th><th class="num">Recharge<br>BCM/year</th><th class="num">Extractable<br>BCM/year</th><th class="num">Extraction<br>BCM/year</th><th class="num">Stage of extraction</th></tr></thead><tbody>${rows.map((r) => `<tr><td>${esc(r.state)}</td><td class="num">${fmt(r.recharge_bcm, 2)}</td><td class="num">${fmt(r.extractable_bcm, 2)}</td><td class="num">${fmt(r.extraction_bcm, 2)}</td><td class="num"><span class="stage"><span class="stage-track"><i class="${r.stage_pct > 100 ? "over" : ""}" style="width:${Math.min((r.stage_pct / 160) * 100, 100)}%"></i></span>${fmt(r.stage_pct, 2)}%</span></td></tr>`).join("") || '<tr><td colspan="5">No states match these filters. Clear the search or change the threshold filter.</td></tr>'}</tbody></table></div>`;
}
function futures() {
  return `${pagehead("Future scenarios", "The future is a set of choices.", "Explore what demand growth and energy efficiency could mean for the same hypothetical workload. These are project scenarios, not IEA forecasts or probability bands.")}<div class="callout warning"><strong>Illustrative starting point:</strong> the baseline from the decision lab (${fmt(state.b.it_mwh)} MWh IT energy in a hypothetical 2025 baseline). Cooling and grid factors are held constant. Efficiency reduces energy per unit of useful work; demand increases the amount of work.</div><article class="card"><div class="future-inputs"><div class="field"><div class="field-top"><label for="growth">Annual useful-work demand growth</label><output id="growth-out">${state.growth}%</output></div><input id="growth" type="range" min="0" max="35" step="1" value="${state.growth}"></div><div class="field"><div class="field-top"><label for="efficiency">Annual energy-per-work efficiency gain</label><output id="efficiency-out">${state.efficiency}%</output></div><input id="efficiency" type="range" min="0" max="25" step="1" value="${state.efficiency}"></div></div><div id="future-result" aria-live="polite"></div></article><div class="cols"><article class="card"><h3>What the scenario includes</h3><p class="subtle">Energy multiplier = [(1 + demand growth) × (1 − efficiency gain)] ^ years. The water model then uses the selected PUE, consumptive WUE and electricity factors.</p><p class="subtle">Demand and efficiency are chosen independently for exploration; they are not calibrated distributions. Differences between trajectories are not confidence intervals.</p></article><article class="card"><h3>What could change the outcome?</h3><p class="subtle">Task mix, model size, cooling adoption, climate, grid changes, construction delays and rebound effects. This simple model does not claim to predict those processes.</p><a class="small-link" href="#solutions">Explore choices and monitoring ↗</a></article></div>`;
}
function futureRows() {
  return Array.from({ length: 11 }, (_, i) => {
    const year = 2025 + i;
    return {
      year,
      chosen: project(
        state.b,
        state.growth / 100,
        state.efficiency / 100,
        year,
      ),
      demand: project(state.b, state.growth / 100, 0, year),
      slower: project(
        state.b,
        state.growth / 200,
        state.efficiency / 100,
        year,
      ),
    };
  });
}
function updateFutures() {
  const rows = futureRows(),
    max = Math.max(
      ...rows.flatMap((r) => [
        r.chosen.total_l,
        r.demand.total_l,
        r.slower.total_l,
      ]),
      1,
    ),
    x = (i) => 55 + i * 65,
    y = (v) => 260 - (v / max) * 210,
    path = (key) =>
      rows
        .map((r, i) => `${i ? "L" : "M"}${x(i)},${y(r[key].total_l)}`)
        .join(" ");
  const end = rows.at(-1);
  document.querySelector("#future-result").innerHTML =
    `<div class="sectionhead" style="margin-top:25px"><div><h2>Conditional water trajectories to 2035</h2><p>Operational consumption · million liters per year</p></div><button class="btn ghost small" id="export-future">Export scenarios ↓</button></div><svg class="chart" viewBox="0 0 760 320" role="img" aria-label="Conditional scenario chart. In 2035, selected trajectory is ${volume(end.chosen.total_l)}, demand only ${volume(end.demand.total_l)}, half demand growth ${volume(end.slower.total_l)}.">${[0, 0.5, 1].map((f) => `<path class="gridline" d="M55 ${y(max * f)}H705"/><text fill="#7f99a8" font-size="10" x="7" y="${y(max * f) + 4}">${fmt((max * f) / 1e6, 1)}</text>`).join("")}<path class="line-amber" d="${path("demand")}"/><path class="line-blue" d="${path("slower")}"/><path class="line-mint" d="${path("chosen")}"/>${[0, 5, 10].map((i) => `<text fill="#8ea8b6" font-size="11" text-anchor="middle" x="${x(i)}" y="289">${2025 + i}</text>`).join("")}</svg><div class="legend"><span><i></i>Selected growth + efficiency</span><span><i style="background:var(--amber)"></i>Demand growth only</span><span><i class="blue"></i>Half demand growth + efficiency</span></div><div class="metric-grid"><article class="card"><div class="label">YOUR SCENARIO · 2030</div><div class="number">${volume(rows[5].chosen.total_l)}</div></article><article class="card"><div class="label">YOUR SCENARIO · 2035</div><div class="number">${volume(end.chosen.total_l)}</div></article><article class="card"><div class="label">DEMAND ONLY · 2035</div><div class="number">${volume(end.demand.total_l)}</div></article><article class="card"><div class="label">HALF DEMAND GROWTH · 2035</div><div class="number">${volume(end.slower.total_l)}</div></article></div><div class="table-wrap"><table><thead><tr><th>Year</th><th class="num">Selected trajectory</th><th class="num">Demand only</th><th class="num">Half demand growth</th></tr></thead><tbody>${[rows[0], rows[5], rows[10]].map((r) => `<tr><td>${r.year}</td><td class="num">${volume(r.chosen.total_l)}</td><td class="num">${volume(r.demand.total_l)}</td><td class="num">${volume(r.slower.total_l)}</td></tr>`).join("")}</tbody></table></div><p class="source-note">These trajectories are calculated from your assumptions. They are not global AI water estimates. “Half demand growth” means half the selected annual growth rate, with the same efficiency gain.</p>`;
  document.querySelector("#export-future").onclick = () =>
    download(
      "thirstyai-conditional-futures.csv",
      csv(futureCsvRows(rows, state)),
    );
}

function evidence() {
  return `${pagehead("Evidence & methods", "A claim should come with a trail.", "Inspect the observation period, scope, source locator and limitation behind every headline. Estimates, company allocations and projections are labeled separately.")}<div class="data-coverage"><span><strong>${data.sources.length}</strong> registered documents (includes licence / assurance)</span><span><strong>${data.claims.length}</strong> numerical claims</span><span><strong>36</strong> groundwater rows</span><span><strong>${data.locations.length}</strong> company-reported location records</span></div><div class="toolbar"><input type="search" id="claim-search" aria-label="Search headline claims" placeholder="Search a claim, publisher or scope…"><a href="data/claims.csv" download class="btn ghost small">Download claims ↓</a><a href="data/evidence.json" download class="btn ghost small">Download evidence JSON ↓</a></div><div class="evidence-cards" id="claims-list"></div><article class="card" style="margin-top:22px"><h2>Source register</h2><div class="table-wrap"><table><thead><tr><th>ID / Publisher</th><th>Source & locator</th><th>Access status</th></tr></thead><tbody>${data.sources.map((s) => `<tr><td>${esc(s.id)}<br><span class="muted">${esc(s.publisher)}</span></td><td>${link(s.id, s.title)}<br><span class="muted">${esc(s.locator)}</span></td><td>Downloaded, hashed<br><span class="muted">Manual locator review</span></td></tr>`).join("")}</tbody></table></div><p class="source-note">The ingestion pipeline saves raw hashes and checks anchors. Those checks detect source drift; they do not replace human review or independent assurance. Raw third-party documents are excluded from source distribution.</p></article><h2 style="margin-top:30px">What you need to know</h2><details open><summary>Withdrawal and consumption are different metrics.</summary><p>Withdrawal is water taken from a source. Consumption is the portion not returned within the accounting boundary, often through evaporation. Recycled circulation is not a new withdrawal every time around. This calculator uses consumption; a withdrawal-based WUE must not be substituted.</p></details><details><summary>A liter is a volume, not a complete impact measure.</summary><p>Timing, source, basin conditions and other users matter. Direct and power-generation water may occur in different locations. This release does not calculate scarcity-weighted impacts or make facility-level causal claims.</p></details><details><summary>How the calculation works</summary><pre>Total operational water = IT kWh × [WUE + PUE × grid water intensity]</pre><p>Only valid when WUE is direct consumptive water per IT kWh and the grid factor excludes the direct cooling component. Manufacturing, construction, networks and end-user devices are outside the model.</p></details><details><summary>Confidence and limitations</summary><p>Source retrieval and correct attribution are checked. There are no independent facility measurements in this release. Official projections are uncertain; company studies use particular allocation methods; state indicators hide local variation. High confidence labels describe extraction and attribution, not independent remeasurement or resolved local uncertainty.</p></details><details><summary>Data licences and attribution</summary><p>Original code is MIT licensed. Third-party documents retain their terms. IEA and the Google article identify CC BY 4.0; The small WRI administrative extract is attributed under CC BY 4.0; state context is not a facility rating. Indian government facts are attributed to PIB/CGWB; no blanket licence is asserted. Raw HTML/PDF documents are excluded.</p></details>`;
}
function updateClaims() {
  const q = document.querySelector("#claim-search").value.toLowerCase(),
    rows = data.claims.filter((c) =>
      JSON.stringify(c).toLowerCase().includes(q),
    );
  document.querySelector("#claims-list").innerHTML =
    rows
      .map(
        (c) =>
          `<article class="card"><div class="sectionhead">${tag(c.evidence_type, /projection/.test(c.evidence_type) ? "blue" : "")}<span class="mini muted">${c.id}</span></div><h3>${esc(c.title)}</h3><div class="number">${fmt(c.value, Number.isInteger(c.value) ? 0 : 2)} <small>${esc(c.unit)}</small></div><dl><dt>Period</dt><dd>${esc(c.period)}</dd><dt>Geography</dt><dd>${esc(c.geography)}</dd><dt>Scope / water boundary</dt><dd>${esc(c.scope)} · ${esc(c.water_metric)}</dd><dt>Confidence in extraction</dt><dd>${esc(c.confidence)}</dd><dt>Locator</dt><dd>${esc(c.locator)}</dd></dl><div class="callout" style="margin:12px 0 0">${esc(c.caveat)}</div><div class="source-link">${link(c.source_id)}</div></article>`,
      )
      .join("") ||
    '<div class="callout">No claims match. Try another term.</div>';
}
function solutions() {
  const items = [
    [
      "01 / COOLING",
      "Match heat rejection to the setting.",
      "Evaluate dry, evaporative and hybrid heat rejection against local climate, energy demand and water constraints. Liquid cooling describes heat transport at the chip or rack; it does not by itself identify the final heat rejection system.",
      "Less evaporative consumption can require more power. Test the whole operational boundary before recommending a design.",
      "MS24",
    ],
    [
      "02 / ELECTRICITY",
      "Follow water beyond the facility.",
      "Ask how the supplying generators are cooled and where they operate. Use a documented grid factor and distinguish annual accounting from the marginal effects of a change.",
      "Clean-energy procurement claims are not a direct measurement of local water use. Lower carbon is not automatically lower water.",
      "WRI23",
    ],
    [
      "03 / GOVERNANCE",
      "Make disclosure comparable.",
      "Publish withdrawal and consumption separately, water sources, relevant reporting periods, the WUE denominator, operating boundaries and dry-season data where available.",
      "More transparent reporting improves evaluation; it does not itself reduce consumption. Missing reporting is not evidence of misconduct.",
      "MS24",
    ],
    [
      "04 / LOCAL CONTEXT",
      "Look below the state average.",
      "Before siting or expanding a facility, investigate actual supply, basin or groundwater assessment unit, drought contingencies and competing users.",
      "A regional indicator is useful context, not proof that a specific data centre caused a local shortage.",
      "CGWB25",
    ],
    [
      "05 / EFFICIENCY",
      "Reduce energy per useful result.",
      "Evaluate smaller suitable models, caching, batching and efficient serving against quality and latency needs. Track total work and total energy, not efficiency alone.",
      "Efficiency gains can coexist with growing total demand. A company-specific text-serving result is not every AI workload.",
      "GOOGLE25",
    ],
    [
      "06 / MAINTENANCE",
      "Keep the evidence alive.",
      "Refresh source versions, preserve hashes, review changed definitions and track coverage. For operators, monitor water source, WUE definition, PUE, seasonal consumption and drought response.",
      "A portfolio model is not operational telemetry. Replenishment projects should remain a separate, location-aware ledger.",
      "WRI23",
    ],
  ];
  return `${pagehead("Solutions playbook", "Turn evidence into better questions.", "There is no universal best cooling technology or city. Start with the local constraint, compare feasible alternatives, then monitor what actually changes.")}<div class="solutions">${items.map(([k, t, p, c, s]) => `<article class="card"><div class="kicker">${k}</div><h2>${t}</h2><p style="margin-top:13px">${p}</p><div class="tradeoff"><strong>Trade-off / limitation</strong><br>${c}</div><span class="source-link">Context: ${link(s)}</span></article>`).join("")}</div><article class="card" style="margin-top:22px"><h2>A prevention and monitoring loop</h2><div class="steps"><p><span><strong>Define the boundary.</strong><br>Separate IT work, facility energy, direct water and electricity-related water.</span></p><p><span><strong>Investigate local constraints.</strong><br>Confirm source, seasonality, other users, and feasible cooling/power options.</span></p><p><span><strong>Compare alternatives.</strong><br>Show baseline, uncertainty, trade-offs, costs when known and break-even conditions.</span></p><p><span><strong>Measure and update.</strong><br>Track real outcomes; document discrepancies, source updates and corrections.</span></p></div><p class="source-note">No liters-saved-per-dollar league table is published: comparable intervention cost and lifetime evidence is not available in this release.</p></article><div class="buttons"><a class="btn" href="#lab">Test a conditional comparison ↗</a><a class="btn ghost" href="#evidence">Check the sources</a></div>`;
}
try {
  const raw = new URL(location.href).searchParams.get("scenario");
  if (raw) {
    const decoded = decodeScenario(raw);
    state.b = decoded.b;
    state.a = decoded.a;
  }
} catch {
  toast("Unsupported or invalid scenario link ignored. Using defaults.");
  state.b = { ...DEFAULTS };
  state.a = { ...ALTERNATIVE };
}

function render() {
  const key = pages.some(([id]) => id === location.hash.slice(1))
    ? location.hash.slice(1)
    : "overview";
  document.querySelectorAll("nav a").forEach((a) => {
    const active = a.dataset.page === key;
    a.classList.toggle("active", active);
    if (active) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  });
  document.querySelector("#crumb").textContent = pages.find(
    ([id]) => id === key,
  )[1];
  main.innerHTML = {
    overview,
    lab,
    companies,
    locations,
    india,
    futures,
    evidence,
    solutions,
    challenge,
  }[key]();
  if (key === "lab") bindLab();
  if (key === "companies") bindCompanies();
  if (key === "challenge") bindChallenge();
  if (key === "india") {
    ["india-search", "india-sort", "india-over"].forEach(
      (id) => (document.getElementById(id).oninput = updateIndia),
    );
    updateIndia();
  }
  if (key === "evidence") {
    document.querySelector("#claim-search").oninput = updateClaims;
    updateClaims();
  }
  if (key === "futures") {
    ["growth", "efficiency"].forEach(
      (id) =>
        (document.getElementById(id).oninput = (e) => {
          state[id] = Number(e.target.value);
          document.getElementById(id + "-out").textContent =
            e.target.value + "%";
          updateFutures();
        }),
    );
    updateFutures();
  }
  document.title = `${pages.find(([id]) => id === key)[1]} · ThirstyAI`;
}
if (data) {
  window.addEventListener("hashchange", () => {
    render();
    window.scrollTo(0, 0);
  });
  render();
}
