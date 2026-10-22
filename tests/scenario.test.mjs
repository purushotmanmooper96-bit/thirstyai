import test from "node:test";
import assert from "node:assert/strict";
import { DEFAULTS, ALTERNATIVE, project } from "../dist/model.mjs";
import {
  encodeScenario,
  decodeScenario,
  validWorkload,
  futureCsvRows,
  receiptLines,
  MODEL_VERSION,
} from "../dist/scenario.mjs";
import { displayedWater } from "../dist/disclosures.mjs";
import { CHALLENGES } from "../dist/challenge.mjs";
import fs from "node:fs";
test("versioned share links round-trip all inputs; unsupported models fail closed", () => {
  const b = { ...DEFAULTS, it_mwh: 2345.6 },
    a = { ...ALTERNATIVE, it_mwh: 2345.6 };
  const s = decodeScenario(encodeScenario(b, a));
  assert.deepEqual(s.b, b);
  assert.deepEqual(s.a, a);
  assert.equal(s.model, MODEL_VERSION);
  assert.throws(() =>
    decodeScenario(btoa(JSON.stringify({ ...s, model: "999" }))),
  );
  assert.throws(() =>
    decodeScenario(btoa(JSON.stringify({ ...s, a: { ...a, it_mwh: 5 } }))),
  );
  assert.throws(() => decodeScenario("x".repeat(5001)));
});
test("invalid visible workloads cannot be accepted as numeric zero or infinity", () => {
  for (const v of ["", " ", 0, -1, "text", "Infinity", 1e10])
    assert.equal(validWorkload(v), false);
  assert.equal(validWorkload("1000"), true);
});
test("future export reconstructs every trajectory from complete original inputs", () => {
  const state = {
    b: { ...DEFAULTS, wue: 1.7, grid_l_kwh: 2.3 },
    growth: 17,
    efficiency: 7,
  };
  const year = 2035;
  const rows = [
    {
      year,
      chosen: project(state.b, 0.17, 0.07, year),
      demand: project(state.b, 0.17, 0, year),
      slower: project(state.b, 0.085, 0.07, year),
    },
  ];
  const [header, ...records] = futureCsvRows(rows, state);
  for (const record of records) {
    const r = Object.fromEntries(header.map((h, i) => [h, record[i]]));
    const b = { ...state.b, it_mwh: r.baseline_it_mwh };
    assert.equal(
      project(b, r.demand_growth, r.efficiency_gain, r.year).total_l,
      r.water_l,
    );
    assert.equal(r.wue, 1.7);
    assert.equal(r.grid_l_kwh, 2.3);
    assert.equal(r.model_version, MODEL_VERSION);
    assert.match(r.warning, /NOT MEASUREMENTS/);
  }
});
test("receipt carries scope and all critical assumptions", () => {
  const text = receiptLines(DEFAULTS, ALTERNATIVE).join("\n");
  for (const value of [
    "NOT MEASUREMENTS",
    "PUE",
    "WUE",
    "grid water",
    "grid carbon",
    "manufacturing",
    "Not a measured facility",
    MODEL_VERSION,
  ])
    assert.ok(text.includes(value));
});
test("challenge records exist and preserve genuinely different metrics and scopes", () => {
  const data = JSON.parse(
    fs.readFileSync(
      new URL("../dist/data/evidence.json", import.meta.url),
      "utf8",
    ),
  );
  for (const q of CHALLENGES)
    for (const id of q.ids)
      assert.ok(data.companies.some((c) => c.observation_id === id));
  assert.equal(CHALLENGES[0].answer, false);
  assert.equal(CHALLENGES[2].answer, true);
});
test("unit conversion retains missing values and does not guess gallon definitions", () => {
  assert.equal(
    displayedWater({ value: null, unit: "ML" }, "litres", String),
    "Not extracted",
  );
  assert.equal(
    displayedWater({ value: 2, unit: "ML" }, "litres", String),
    "2000000 L (source: 2 ML)",
  );
  assert.equal(
    displayedWater(
      { value: 2, unit: "million gallons (as reported)" },
      "litres",
      String,
    ),
    "2 million gallons (as reported)",
  );
});
