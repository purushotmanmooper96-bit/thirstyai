# Methodology

## Question and boundary

Which accounting assumptions change operational water consumption for the same IT work? The v0.1 engine accounts for direct consumption at a data centre and electricity-related consumption. It does not allocate manufacturing, construction, network or end-user impacts. It does not turn liters into a local damage score.

## Measurement semantics

- Withdrawal: water abstracted from a source.
- Consumption: water not returned within the accounting boundary.
- WUE in this engine: direct consumed liters per IT kWh.
- PUE: facility energy divided by IT energy for the same period.
- Grid intensity: consumed liters per facility kWh delivered, with boundary specified by the input provider.

Microsoft's inspected 2024 cooling article references withdrawal WUE. It is not loaded as consumptive WUE. Google's May 2025 serving result includes facility energy overhead; applying PUE again to that energy would be double counting. Its direct water allocation uses IT energy and annual consumptive WUE, not the complete electricity-related water pathway.

## Equations

Let E be IT kWh, p be PUE, w be consumptive WUE, i be grid consumption intensity and c be grid carbon factor. Facility energy = E p; direct liters = E w; indirect liters = E p i; operational liters = E(w+p i); carbon kg = E p c. IT MWh is multiplied by 1000 to obtain kWh.

The code rejects negative, nonfinite, boolean or missing numerical inputs, PUE below one, incompatible water metrics, wrong WUE denominators and WUE already including indirect water. The interface bounds its sliders but is not an engineering feasibility solver. Do not treat adjustable bounds as empirically justified parameter ranges.

For alternatives with equal E and a shared i, water break-even is i = (w_baseline − w_alternative)/(p_alternative − p_baseline), when the denominator is nonzero. A negative result is not a non-negative physical threshold. Compare the actual sign either side rather than assuming which option wins.

## Futures

IT energy multiplier = [(1+annual demand growth)(1−annual energy-per-work efficiency gain)] ^ years. This is constant-rate conditional arithmetic, not a fitted or probabilistic forecast. Cooling/grid factors remain fixed. Source-native IEA projections remain separate from project scenarios. No 2035 water-scarcity map is interpolated from Aqueduct horizons.

## India extraction

The pipeline downloads the PIB release, identifies the groundwater table by header, parses the first matching copy, requires 36 unique state/UT records, and retains the published ratio. Duplicate copies on the webpage are not combined. Stage = annual extraction / annual extractable groundwater; published volumes are rounded and cannot always reproduce stage, especially small UTs. A zero rounded extraction volume with a positive ratio is preserved and explained, not “fixed”. National stage is the published national ratio, never a mean of state ratios.

## Evidence and uncertainty

A claim stores source ID, period, geography, scope, evidence type, locator and caveat. Raw retrievals record hash and timestamp, and anchor checks detect obvious source drift. Manual locator review establishes the cited fact. Neither method independently audits corporate measurements. Missing data remains missing. We publish no confidence score without a defensible rubric and no statistical intervals from arbitrary parameter ranges.

## Geography and causality

State context is not a site's water source. No facility/basin mapping, supply-network tracing or causal estimate is implemented in v0.1. Indirect water could occur elsewhere. Aqueduct is a screening resource; its technical note calls for local investigation. Replenishment is not subtracted from local consumption.

## SQL engines

The runnable audit uses SQLite. A separate PostgreSQL schema adapts view creation and floating-point types for that engine. PostgreSQL execution is not claimed in this environment.
