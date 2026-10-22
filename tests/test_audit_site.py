import unittest,sys
from pathlib import Path
from io import BytesIO
from unittest.mock import Mock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_site import wait_ready,lighthouse_command
class AuditStartup(unittest.TestCase):
 def test_waits_for_real_debugging_endpoint(self):
  process=Mock();process.poll.return_value=None
  with patch('audit_site.urllib.request.urlopen',return_value=BytesIO(b'{"webSocketDebuggerUrl":"ws://127.0.0.1/devtools/browser/test"}')):
   wait_ready('http://127.0.0.1/json/version',process,timeout=1)
 def test_exited_browser_fails_immediately(self):
  process=Mock();process.poll.return_value=1
  with self.assertRaises(RuntimeError):wait_ready('http://127.0.0.1/json/version',process)
 def test_startup_has_a_deadline(self):
  process=Mock();process.poll.return_value=None
  with self.assertRaises(TimeoutError):wait_ready('http://127.0.0.1/json/version',process,timeout=0)
 def test_audits_attach_to_explicit_port(self):
  mobile=lighthouse_command(Path('cli/index.js'),'http://127.0.0.1:8765/',9222,'mobile',Path('out'))
  desktop=lighthouse_command(Path('cli/index.js'),'http://127.0.0.1:8765/',9222,'desktop',Path('out'))
  self.assertIn('--port=9222',mobile);self.assertNotIn('--preset=desktop',mobile)
  self.assertIn('--preset=desktop',desktop);self.assertIn('--no-enable-error-reporting',desktop)
