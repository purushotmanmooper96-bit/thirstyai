"""Operational consumption accounting. Factors are inputs, never site measurements."""
from dataclasses import asdict, dataclass
import math


def number(value, name, lower=0, upper=None):
    try:
        valid = not isinstance(value, bool) and isinstance(value, (float, int)) and math.isfinite(value)
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError(f'{name} must be a finite number, not missing')
    if value < lower or (upper is not None and value > upper):
        raise ValueError(f'{name} outside [{lower}, {upper}]')
    return float(value)


@dataclass(frozen=True)
class Inputs:
    it_mwh: float = 1000
    pue: float = 1.2
    wue: float = 1.0
    grid_l_kwh: float = 1.0
    carbon_kg_kwh: float = 0.4
    water_metric: str = 'consumption'
    wue_denominator: str = 'IT_kWh'
    includes_indirect: bool = False

    def validate(self):
        number(self.it_mwh, 'IT MWh')
        number(self.pue, 'PUE', 1)
        for k in ('wue', 'grid_l_kwh', 'carbon_kg_kwh'):
            number(getattr(self, k), k)
        if self.water_metric != 'consumption':
            raise ValueError('Withdrawal WUE cannot enter a consumption calculation')
        if self.wue_denominator != 'IT_kWh':
            raise ValueError('This engine requires WUE per IT kWh')
        if self.includes_indirect is not False:
            raise ValueError('WUE must exclude electricity-related water')


def calculate(inputs: Inputs):
    inputs.validate()
    it_kwh = inputs.it_mwh * 1000
    facility = it_kwh * inputs.pue
    direct = it_kwh * inputs.wue
    indirect = facility * inputs.grid_l_kwh
    result = {
        'it_mwh': inputs.it_mwh,
        'facility_mwh': facility / 1000,
        'direct_l': direct,
        'indirect_l': indirect,
        'total_l': direct + indirect,
        'carbon_kg': facility * inputs.carbon_kg_kwh,
        'intensity_l_kwh_it': inputs.wue + inputs.pue * inputs.grid_l_kwh,
        'evidence_type': 'illustrative_scenario',
        'boundary': 'operational consumption; manufacturing excluded',
    }
    for key, value in result.items():
        if isinstance(value, (int, float)):
            number(value, key)
    return result


def compare(baseline: Inputs, alternative: Inputs):
    if baseline.it_mwh != alternative.it_mwh:
        raise ValueError('Use the same IT workload for cooling comparisons')
    b, a = calculate(baseline), calculate(alternative)
    result = {'baseline': b, 'alternative': a,
            'water_saved_l': b['total_l'] - a['total_l'],
            'water_saved_pct': None if b['total_l'] == 0 else 100 * (1 - a['total_l'] / b['total_l']),
            'energy_change_mwh': a['facility_mwh'] - b['facility_mwh']}
    for key in ('water_saved_l','water_saved_pct','energy_change_mwh'):
        if result[key] is not None: number(result[key], key, lower=-float('inf'))
    return result


def break_even_grid(baseline: Inputs, alternative: Inputs):
    calculate(baseline); calculate(alternative)
    delta = alternative.pue - baseline.pue
    return None if delta == 0 else number((baseline.wue - alternative.wue) / delta, 'break-even factor', lower=-float('inf'))


def capacity_energy(it_mw, utilization, hours):
    return number(number(it_mw, 'IT MW') * number(utilization, 'utilization', 0, 1) * number(hours, 'hours'), 'capacity energy')


def project(inputs, demand_growth, efficiency_gain, target_year, base_year=2025):
    """Conditional constant-rate extrapolation. Not a forecast or confidence interval."""
    calculate(inputs)
    number(demand_growth, 'demand growth', 0, 1)
    number(efficiency_gain, 'efficiency gain', 0, 1)
    if type(base_year) is not int or type(target_year) is not int or target_year < base_year:
        raise ValueError('Invalid target year')
    try:
        factor = ((1 + demand_growth) * (1 - efficiency_gain)) ** (target_year - base_year)
    except OverflowError as exc:
        raise ValueError('Projection exceeds finite numeric range') from exc
    return calculate(Inputs(**(asdict(inputs) | {'it_mwh': inputs.it_mwh * factor})))
