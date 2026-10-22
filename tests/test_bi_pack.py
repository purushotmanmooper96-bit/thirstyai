import importlib.util
import unittest
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bi_pack', ROOT / 'scripts/build_bi_pack.py')
pack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pack)


class PowerBIHandoff(unittest.TestCase):
    def test_complete_handoff_is_deterministic(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for path, _ in pack.TABLES.values():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, target)
            for path in ('research/sources.json', 'docs/evidence_status.md'):
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, target)
            (root / 'bi').mkdir()
            first = pack.build(root)
            query = (root / 'bi/ThirstyAI_Data.m').read_bytes()
            self.assertEqual(first, pack.build(root))
            self.assertEqual(query, (root / 'bi/ThirstyAI_Data.m').read_bytes())
            self.assertEqual(first['tables']['CompanyReports']['null_values'], 2)
            self.assertEqual(first['tables']['EvidenceStatus']['rows'], 10)
            self.assertEqual(len(first['tables']), 7)

    def test_missing_company_values_are_not_zero(self):
        columns, rows = pack.read_csv(ROOT / pack.TABLES['CompanyReports'][0])
        self.assertEqual(sum(r['value'] == '' for r in rows), 2)
        ids = {r['source_id'] for r in rows}
        pack.validate_table('CompanyReports', rows, columns, {'value': 'type number'}, ids)

    def test_orphan_and_erased_boundaries_fail(self):
        columns, rows = pack.read_csv(ROOT / pack.TABLES['CompanyReports'][0])
        with self.assertRaisesRegex(ValueError, 'orphan'):
            pack.validate_table('CompanyReports', rows, columns, {'value': 'type number'}, set())
        row = dict(rows[0], scope='')
        with self.assertRaisesRegex(ValueError, 'boundary'):
            pack.validate_table('CompanyReports', [row], columns, {'value': 'type number'}, {row['source_id']})

    def test_scenarios_cannot_lose_warning(self):
        columns, rows = pack.read_csv(ROOT / pack.TABLES['Scenarios'][0])
        row = dict(rows[0], warning='Measured savings')
        with self.assertRaisesRegex(ValueError, 'illustrative'):
            pack.validate_table('Scenarios', [row], columns, pack.TABLES['Scenarios'][1], set())

    def test_duplicate_scenario_cannot_double_totals(self):
        columns, rows = pack.read_csv(ROOT / pack.TABLES['Scenarios'][0])
        with self.assertRaisesRegex(ValueError, 'duplicate record'):
            pack.validate_table('Scenarios', [rows[0], rows[0]], columns, pack.TABLES['Scenarios'][1], set())

    def test_regional_proxy_cannot_be_called_facility_risk(self):
        columns, rows = pack.read_csv(ROOT / pack.TABLES['LocationContext'][0])
        row = dict(rows[0], match_scale='FACILITY')
        with self.assertRaisesRegex(ValueError, 'match boundary'):
            pack.validate_table('LocationContext', [row], columns, {}, {row['source_id'], row['stress_source_id']})

    def test_all_ten_evidence_areas_retained(self):
        self.assertEqual(len(pack.evidence_status(ROOT / 'docs/evidence_status.md')), 10)
