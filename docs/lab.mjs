import { compare, breakEvenGrid, DEFAULTS, ALTERNATIVE } from "./model.mjs";
import {
  validWorkload,
  encodeScenario,
  receiptLines,
  MODEL_VERSION,
} from "./scenario.mjs";
import { downloadReceipt } from "./sharing.mjs";
export function createLab(
  state,
  { fmt, volume, tag, pagehead, download, toast, rerender },
) {
  function allInputsValid() {
    return (
      validWorkload(document.querySelector("#workload").value) &&
      [...document.querySelectorAll("input[data-key]")].every(
        (x) => x.value !== "" && x.checkValidity(),
      )
    );
  }
  function setLabValidity(valid) {
    const status = document.querySelector("#lab-status");
    status.textContent = valid
      ? ""
      : "Results unavailable: enter valid inputs before sharing or exporting.";
    document.querySelector("#lab-results").hidden = !valid;
    for (const id of ["share", "receipt", "export-scenario"]) {
      const el = document.getElementById(id);
      if (el) el.disabled = !valid;
    }
    document.querySelector("#receipt-text").textContent = valid
      ? receiptLines(state.b, state.a).join("\n")
      : "Results unavailable while inputs are invalid.";
  }
  function slider(group, key, label, min, max, step, unit) {
    const v = state[group][key];
    return `<div class="field"><div class="field-top"><label for="${group}-${key}">${label}</label><output id="${group}-${key}-out" for="${group}-${key}">${fmt(v, step < 1 ? 2 : 0)} ${unit}</output></div><input aria-describedby="${group}-${key}-out" id="${group}-${key}" data-group="${group}" data-key="${key}" type="range" min="${min}" max="${max}" step="${step}" value="${v}"><label class="exact-label" for="${group}-${key}-exact">Exact ${label}</label><input id="${group}-${key}-exact" class="exact-value" data-group="${group}" data-key="${key}" type="number" min="${min}" max="${max}" step="${step}" value="${v}"></div>`;
  }

  function scenarioCard(group, title) {
    return `<article class="card scenario-card ${group === "a" ? "alt" : ""}"><div class="sectionhead"><h3>${title}</h3>${tag("ILLUSTRATIVE INPUTS", "amber")}</div>${slider(group, "pue", "Facility energy / IT energy (PUE)", 1, 2.5, 0.01, "×")}${slider(group, "wue", "Direct consumption WUE", 0, 3, 0.05, "L/kWh IT")}${slider(group, "grid_l_kwh", "Electricity water intensity", 0, 6, 0.05, "L/kWh facility")}${slider(group, "carbon_kg_kwh", "Electricity carbon intensity", 0, 1.2, 0.01, "kg CO₂e/kWh")}<p class="source-note">User-controlled assumptions. This bundle is not a measured facility or a validated technology specification.</p></article>`;
  }

  function lab() {
    return `${pagehead("Decision lab", "A better choice depends on the boundary.", "Hold IT work constant. Change cooling and electricity assumptions. See the direct water, electricity-related water, energy and carbon trade-offs together.")}<div class="toolbar"><label for="workload">IT workload (MWh)</label><input type="number" id="workload" min="1" max="1000000000" step="any" value="${state.b.it_mwh}" style="flex:0;width:150px;min-width:140px"><button class="btn ghost small" id="reset">Reset example</button><button class="btn ghost small" id="share">Copy scenario link ↗</button><button class="btn ghost small" id="receipt">Download result card ↓</button></div><div class="callout warning"><strong>ILLUSTRATIVE INPUTS — NOT MEASUREMENTS.</strong> Default values are hypothetical, not empirical averages. WUE here is direct <em>consumption</em> per IT kWh. Manufacturing, water stress and withdrawal are outside this calculation. Controls can create physically infeasible bundles; use validated engineering inputs before making decisions.</div><p class="guided-example">Try the example: the alternative assumes lower direct water use and higher electricity overhead. Reveal the controls to change one assumption.</p><div id="lab-status" role="status"></div><div id="lab-results" aria-live="polite"></div><details class="advanced-controls"><summary>Adjust cooling and electricity assumptions</summary><div class="pair">${scenarioCard("b", "Baseline")}${scenarioCard("a", "Alternative")}</div></details><details><summary>Inspect the formula and boundary</summary><pre>Facility energy (kWh) = IT energy × PUE
Direct consumption (L) = IT energy × consumptive WUE
Indirect consumption (L) = facility energy × grid water factor
Operational consumption (L) = direct + indirect
Carbon (kg CO₂e) = facility energy × assumed grid carbon factor</pre><p>Water volumes can arise in different basins. Adding them is physical accounting, not a claim that their local impacts are equivalent. Lower carbon does not automatically mean lower water. Renewable procurement alone does not establish local grid water intensity.</p></details><details><summary>Accessible result-card text</summary><pre id="receipt-text"></pre></details>`;
  }

  function updateLab() {
    const r = compare(state.b, state.a),
      max = Math.max(r.baseline.total_l, r.alternative.total_l, 1),
      delta = r.water_saved_pct;
    document.querySelector("#lab-results").innerHTML =
      `<div class="metric-grid"><article class="card"><div class="label">BASELINE CONSUMPTION</div><div class="number">${volume(r.baseline.total_l)}</div><span class="mini muted">${fmt(r.baseline.facility_mwh)} MWh facility energy</span></article><article class="card"><div class="label">ALTERNATIVE CONSUMPTION</div><div class="number">${volume(r.alternative.total_l)}</div><span class="mini muted">${fmt(r.alternative.facility_mwh)} MWh facility energy</span></article><article class="card"><div class="label">WATER REDUCTION VS BASELINE</div><div class="number ${r.water_saved_l >= 0 ? "positive" : "negative"}">${delta === null ? "N/A" : fmt(delta, 1) + "%"}</div><span class="mini muted">${volume(r.water_saved_l)} less (negative = more)</span></article><article class="card"><div class="label">FACILITY ENERGY CHANGE</div><div class="number ${r.energy_change_mwh <= 0 ? "positive" : "negative"}">${r.energy_change_mwh > 0 ? "+" : ""}${fmt(r.energy_change_mwh)} <small>MWh</small></div><span class="mini muted">Same IT work; overhead changes</span></article></div><details class="result-details"><summary>Inspect water pathways, carbon and sensitivity</summary><article class="card"><div class="sectionhead"><div><h2>Follow both water pathways.</h2><p>Direct and electricity-related operational consumption</p></div><button class="btn ghost small" id="export-scenario">Export result ↓</button></div>${[
        ["Baseline", r.baseline],
        ["Alternative", r.alternative],
      ]
        .map(
          ([name, x]) =>
            `<div class="barrow"><span>${name}</span><div class="stack" role="img" aria-label="${name}: ${volume(x.direct_l)} direct, ${volume(x.indirect_l)} indirect"><div class="direct" style="width:${(100 * x.direct_l) / max}%"></div><div class="indirect" style="width:${(100 * x.indirect_l) / max}%"></div></div><strong>${volume(x.total_l)}</strong></div>`,
        )
        .join(
          "",
        )}<div class="legend"><span><i></i>Direct cooling consumption</span><span><i class="blue"></i>Electricity-related consumption</span></div><div class="table-wrap"><table><thead><tr><th>Metric</th><th class="num">Baseline</th><th class="num">Alternative</th></tr></thead><tbody>${[
        [
          "Direct water",
          volume(r.baseline.direct_l),
          volume(r.alternative.direct_l),
        ],
        [
          "Indirect water",
          volume(r.baseline.indirect_l),
          volume(r.alternative.indirect_l),
        ],
        [
          "Facility energy",
          fmt(r.baseline.facility_mwh) + " MWh",
          fmt(r.alternative.facility_mwh) + " MWh",
        ],
        [
          "Operational carbon",
          fmt(r.baseline.carbon_kg / 1000, 2) + " t CO₂e",
          fmt(r.alternative.carbon_kg / 1000, 2) + " t CO₂e",
        ],
      ]
        .map(
          (row) =>
            `<tr><td>${row[0]}</td><td class="num">${row[1]}</td><td class="num">${row[2]}</td></tr>`,
        )
        .join(
          "",
        )}</tbody></table></div><div class="insight">${r.water_saved_l >= 0 ? "The alternative reduces modeled water consumption under these inputs." : "The alternative increases modeled water consumption under these inputs."} ${r.energy_change_mwh > 0 ? "It also needs more facility electricity." : "Check electricity and carbon alongside water."} This is a conditional comparison, not real-world savings achieved.</div><p class="source-note">${breakEvenExplanation()} <br>ML = million liters. kL = thousand liters. All outputs inherit user-selected assumptions.</p></article><article class="card" style="margin-top:20px"><h3>Sensitivity: what if the electricity water factor changes?</h3><p class="subtle">Both cases use the same grid factor below. Other inputs remain as selected.</p><div class="table-wrap"><table><thead><tr><th>Grid factor (L/kWh)</th><th class="num">Baseline water</th><th class="num">Alternative water</th><th class="num">Water reduction</th></tr></thead><tbody>${[
        0, 0.5, 1, 2, 4, 6,
      ]
        .map((g) => {
          const c = compare(
            { ...state.b, grid_l_kwh: g },
            { ...state.a, grid_l_kwh: g },
          );
          return `<tr><td>${g}</td><td class="num">${volume(c.baseline.total_l)}</td><td class="num">${volume(c.alternative.total_l)}</td><td class="num ${c.water_saved_l >= 0 ? "positive" : "negative"}">${c.water_saved_pct === null ? "N/A" : fmt(c.water_saved_pct, 1) + "%"}</td></tr>`;
        })
        .join("")}</tbody></table></div></article></details>`;
    document.querySelector("#export-scenario").onclick = () => {
      if (!allInputsValid()) return;
      const obj = {
        warning: "ILLUSTRATIVE INPUTS — NOT MEASUREMENTS",
        release: MODEL_VERSION,
        model_version: MODEL_VERSION,
        generated_at: new Date().toISOString(),
        evidence_type: "illustrative_scenario",
        inputs: { baseline: state.b, alternative: state.a },
        results: r,
        limitations: [
          "Not a facility measurement",
          "Manufacturing excluded",
          "No local scarcity impact allocation",
        ],
      };
      download(
        "thirstyai-scenario.json",
        JSON.stringify(obj, null, 2),
        "application/json",
      );
      toast("Result and assumptions exported");
    };
    document.querySelector("#receipt-text").textContent = receiptLines(
      state.b,
      state.a,
    ).join("\n");
  }

  function breakEvenExplanation() {
    if (state.b.grid_l_kwh !== state.a.grid_l_kwh)
      return "Break-even grid analysis requires the same grid factor in both cases.";
    const t = breakEvenGrid(state.b, state.a);
    if (t === null)
      return "Equal PUE: water differences depend on direct WUE under a shared grid.";
    if (t < 0)
      return "No non-negative break-even grid factor for these PUE/WUE settings.";
    return `At a shared grid intensity of ${fmt(t, 2)} L/kWh, these cooling inputs have equal total water consumption. The sensitivity table shows which option wins either side.`;
  }

  function bindLab() {
    document.querySelectorAll("input[data-key]").forEach(
      (input) =>
        (input.oninput = () => {
          const { group, key } = input.dataset;
          if (input.value === "" || !input.checkValidity()) {
            setLabValidity(false);
            return;
          }
          state[group][key] = Number(input.value);
          for (const peer of document.querySelectorAll(
            `input[data-group="${group}"][data-key="${key}"]`,
          ))
            peer.value = input.value;
          document.querySelector(`#${group}-${key}-out`).textContent =
            fmt(Number(input.value), 2) +
            (key === "pue"
              ? " ×"
              : key === "carbon_kg_kwh"
                ? " kg CO₂e/kWh"
                : key === "wue"
                  ? " L/kWh IT"
                  : " L/kWh facility");
          const valid = allInputsValid();
          setLabValidity(valid);
          if (valid) updateLab();
        }),
    );
    document.querySelector("#workload").oninput = (e) => {
      const n = Number(e.target.value);
      if (!validWorkload(e.target.value)) {
        e.target.setCustomValidity("Enter 1 to 1,000,000,000 MWh");
        setLabValidity(false);
        return;
      }
      e.target.setCustomValidity("");
      state.b.it_mwh = state.a.it_mwh = n;
      setLabValidity(allInputsValid());
      if (allInputsValid()) updateLab();
    };
    document.querySelector("#reset").onclick = () => {
      state.b = { ...DEFAULTS };
      state.a = { ...ALTERNATIVE };
      history.replaceState(null, "", location.pathname + "#lab");
      rerender();
      toast("Example restored");
    };
    document.querySelector("#share").onclick = async () => {
      if (!allInputsValid()) return;
      const url = new URL(location.href);
      url.searchParams.set("scenario", encodeScenario(state.b, state.a));
      url.hash = "lab";
      try {
        await navigator.clipboard.writeText(url.href);
        toast("Scenario link copied");
      } catch {
        download(
          "thirstyai-scenario-link.txt",
          "ILLUSTRATIVE INPUTS - NOT MEASUREMENTS\n" + url.href,
          "text/plain",
        );
        toast("Scenario link downloaded");
      }
    };
    document.querySelector("#receipt").onclick = async () => {
      if (!allInputsValid()) return;
      try {
        await downloadReceipt(state.b, state.a);
        toast("Illustrative result card downloaded");
      } catch {
        toast("Card unavailable; use the text or JSON export.");
      }
    };
    updateLab();
  }
  return { lab, bindLab };
}
