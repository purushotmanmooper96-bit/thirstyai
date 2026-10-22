import { calculate, compare, DEFAULTS } from "./model.mjs";
export const MODEL_VERSION = "0.2.1";
export const WARNING = "ILLUSTRATIVE INPUTS — NOT MEASUREMENTS";
export const INPUT_KEYS = Object.keys(DEFAULTS);
export function validWorkload(value) {
  const n = Number(value);
  return (
    String(value).trim() !== "" && Number.isFinite(n) && n >= 1 && n <= 1e9
  );
}
export function scenarioPayload(b, a) {
  compare(b, a);
  const inputs = (x) =>
    Object.fromEntries(INPUT_KEYS.map((key) => [key, x[key]]));
  return { v: 1, model: MODEL_VERSION, b: inputs(b), a: inputs(a) };
}
export function encodeScenario(b, a) {
  return btoa(JSON.stringify(scenarioPayload(b, a)));
}
export function decodeScenario(raw) {
  if (raw.length > 5000) throw new Error("Scenario link too long");
  const s = JSON.parse(atob(raw));
  if (s.v !== undefined && (s.v !== 1 || s.model !== MODEL_VERSION))
    throw new Error("Unsupported scenario version");
  compare(s.b, s.a);
  for (const x of [s.b, s.a])
    if (
      !validWorkload(x.it_mwh) ||
      x.pue > 2.5 ||
      x.wue > 3 ||
      x.grid_l_kwh > 6 ||
      x.carbon_kg_kwh > 1.2
    )
      throw new Error("Outside UI bounds");
  return scenarioPayload(s.b, s.a);
}
export function futureCsvRows(rows, state) {
  const fields = [
    "warning",
    "model_version",
    "year",
    "trajectory",
    "water_l",
    "it_mwh",
    "facility_mwh",
    "demand_growth",
    "efficiency_gain",
    "baseline_it_mwh",
    "pue",
    "wue",
    "grid_l_kwh",
    "carbon_kg_kwh",
    "water_metric",
    "wue_denominator",
    "includes_indirect",
    "evidence_type",
    "boundary",
  ];
  return [
    fields,
    ...rows.flatMap((r) =>
      ["chosen", "demand", "slower"].map((k) => [
        WARNING,
        MODEL_VERSION,
        r.year,
        k,
        r[k].total_l,
        r[k].it_mwh,
        r[k].facility_mwh,
        k === "slower" ? state.growth / 200 : state.growth / 100,
        k === "demand" ? 0 : state.efficiency / 100,
        state.b.it_mwh,
        state.b.pue,
        state.b.wue,
        state.b.grid_l_kwh,
        state.b.carbon_kg_kwh,
        state.b.water_metric,
        state.b.wue_denominator,
        state.b.includes_indirect,
        "illustrative_scenario",
        r[k].boundary,
      ]),
    ),
  ];
}
export function receiptLines(b, a) {
  const r = compare(b, a);
  const n = (x) =>
    new Intl.NumberFormat("en", { maximumFractionDigits: 2 }).format(x);
  return [
    "SHOW YOUR ASSUMPTIONS",
    WARNING,
    `Same IT workload: ${n(b.it_mwh)} MWh`,
    `Baseline total: ${n(r.baseline.total_l)} L | Alternative: ${n(r.alternative.total_l)} L`,
    `Direct water: ${n(r.baseline.direct_l)} → ${n(r.alternative.direct_l)} L`,
    `Electricity-related water: ${n(r.baseline.indirect_l)} → ${n(r.alternative.indirect_l)} L`,
    `Facility electricity: ${n(r.baseline.facility_mwh)} → ${n(r.alternative.facility_mwh)} MWh`,
    `Operational carbon: ${n(r.baseline.carbon_kg)} → ${n(r.alternative.carbon_kg)} kg CO2e`,
    `Baseline: PUE ${b.pue}; WUE ${b.wue}; grid water ${b.grid_l_kwh}; grid carbon ${b.carbon_kg_kwh}`,
    `Alternative: PUE ${a.pue}; WUE ${a.wue}; grid water ${a.grid_l_kwh}; grid carbon ${a.carbon_kg_kwh}`,
    "WUE: L/IT kWh. Grid water: L/facility kWh. Carbon: kg/facility kWh.",
    "Operational consumption only; manufacturing and local scarcity impacts excluded.",
    "Not a measured facility, feasible technology specification or achieved saving.",
    `ThirstyAI model ${MODEL_VERSION} | purushotmanmooper96-bit.github.io/thirstyai/`,
  ];
}
