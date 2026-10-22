"""Build a typed CSV handoff for Power BI; never implies Desktop validation."""
from pathlib import Path
import csv
import hashlib
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
TABLES = {
    'Groundwater': ('data/processed/india_groundwater_2025.csv', {'year': 'Int64.Type', **{k: 'type number' for k in ('recharge_bcm', 'extractable_bcm', 'extraction_bcm', 'stage_pct')}}),
    'CompanyReports': ('data/processed/company_water_reports.csv', {'value': 'type number'}),
    'LocationContext': ('data/processed/location_stress_overlay.csv', {'value': 'type number', 'stress_score': 'type number'}),
    'Scenarios': ('outputs/scenarios.csv', {k: ('Int64.Type' if k == 'year' else 'type number') for k in ('year', 'demand_growth', 'efficiency_gain', 'it_mwh', 'facility_mwh', 'direct_l', 'indirect_l', 'total_l', 'carbon_kg', 'intensity_l_kwh_it')}),
    'Claims': ('dist/data/claims.csv', {'value': 'type number'}),
}


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


def evidence_status(path):
    rows = []
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.startswith('| '):
            continue
        cells = [s.strip() for s in line.strip().strip('|').split('|')]
        if len(cells) == 5 and cells[1].startswith(('Strong', 'Partial', 'Gap')):
            rows.append(dict(zip(('topic', 'level', 'source_locator', 'caveat', 'missing'), cells)))
    if len(rows) != 10:
        raise ValueError('Evidence status must contain exactly ten reviewed problem areas')
    return rows


def validate_table(name, rows, columns, types, source_ids):
    if len(columns) != len(set(columns)):
        raise ValueError(f'{name}: duplicate columns')
    keys = {'Groundwater': ('state', 'year'), 'CompanyReports': ('observation_id',),
            'LocationContext': ('location_id',), 'Scenarios': ('name', 'year'), 'Claims': ('id',)}[name]
    identities = [tuple(row[k] for k in keys) for row in rows]
    if len(identities) != len(set(identities)):
        raise ValueError(f'{name}: duplicate record key')
    for row in rows:
        for column in types:
            value = row[column]
            if value == '' and name == 'CompanyReports' and column == 'value':
                continue
            number = float(value)
            if not math.isfinite(number) or number < 0:
                raise ValueError(f'{name}.{column}: invalid numeric value')
            if types[column] == 'Int64.Type' and number != int(number):
                raise ValueError(f'{name}.{column}: non-integer')
        for column in ('source_id', 'stress_source_id'):
            if column in row and row[column] not in source_ids:
                raise ValueError(f'{name}: orphan {column}')
        if name == 'Scenarios' and (row['warning'] != 'ILLUSTRATIVE INPUTS - NOT MEASUREMENTS' or row['evidence_type'] != 'illustrative_scenario'):
            raise ValueError('Scenarios: missing illustrative warning')
        if name == 'CompanyReports' and any(not row[k] for k in ('unit', 'period', 'scope', 'water_metric', 'caveat')):
            raise ValueError('CompanyReports: missing comparability boundary')
        if name == 'LocationContext' and row['match_scale'] != 'STATE_PROXY_NOT_FACILITY_OR_BASIN':
            raise ValueError('LocationContext: unexpected match boundary')


def build(root=ROOT):
    destination = root / 'outputs/powerbi'
    destination.mkdir(parents=True, exist_ok=True)
    sources = json.loads((root / 'research/sources.json').read_text(encoding='utf-8'))
    source_ids = {s['id'] for s in sources}
    if len(sources) != len(source_ids):
        raise ValueError('Duplicate source key')
    tables = {}
    for name, (path, types) in TABLES.items():
        columns, rows = read_csv(root / path)
        validate_table(name, rows, columns, types, source_ids)
        tables[name] = (columns, rows, types)
    source_columns = ['source_id', 'title', 'publisher', 'url', 'locator', 'scope', 'licence']
    tables['Sources'] = (source_columns, [{'source_id': s['id'], **{k: s[k] for k in source_columns[1:]}} for s in sources], {})
    status = evidence_status(root / 'docs/evidence_status.md')
    tables['EvidenceStatus'] = (list(status[0]), status, {})
    manifest = {'status': 'DATA_HANDOFF_CHECKED_NOT_POWER_BI_DESKTOP_VALIDATED', 'tables': {}}
    expressions = []
    for name, (columns, rows, types) in tables.items():
        path = destination / (name + '.csv')
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=columns, lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
        manifest['tables'][name] = {'rows': len(rows), 'null_values': sum(r.get('value') == '' for r in rows), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'columns': {k: types.get(k, 'type text') for k in columns}}
        type_list = ', '.join('{"' + k + '", ' + types.get(k, 'type text') + '}' for k in columns)
        expressions.append(f'    {name} = Load("{name}.csv", {{{type_list}}})')
    (destination / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    query = '''// Create a Text parameter RepoRoot containing your checkout path, without a trailing slash.
// Read-only import. Null company values stay null. No unlike metric aggregation.
let
    Base = Text.TrimEnd(RepoRoot, {"/", "\\"}) & "/outputs/powerbi/",
    Load = (name as text, types as list) as table =>
        let
            Headers = Table.PromoteHeaders(Csv.Document(File.Contents(Base & name),
                [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
                [PromoteAllScalars=true]),
            EmptyAsNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue,
                List.Transform(types, each _{0}))
        in Table.TransformColumnTypes(EmptyAsNull, types, "en-US"),
''' + ',\n'.join(expressions) + '\nin\n    [' + ', '.join(n + '=' + n for n in tables) + ']\n'
    (root / 'bi/ThirstyAI_Data.m').write_text(query, encoding='utf-8')
    print('Power BI data handoff checked: ' + ', '.join(f'{k}={len(v[1])}' for k, v in tables.items()))
    return manifest


if __name__ == '__main__':
    build()
