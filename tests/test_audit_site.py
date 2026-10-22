import unittest,sys,signal,os
from pathlib import Path
from io import BytesIO
from unittest.mock import Mock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_site import wait_ready,lighthouse_command,stop_chrome
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

 @unittest.skipUnless(os.name=="posix", "POSIX process groups are unavailable on Windows")
 def test_cleanup_stops_children_even_when_parent_has_exited(self):
  process=Mock();process.pid=123;process.poll.return_value=0
  with patch('audit_site.os.name','posix'),patch('audit_site.os.killpg') as kill:
   stop_chrome(process)
  self.assertEqual(kill.call_args_list, [unittest.mock.call(123,signal.SIGTERM),unittest.mock.call(123,signal.SIGKILL)])
  process.wait.assert_called_once_with(timeout=5)
 @unittest.skipUnless(os.name=="posix", "POSIX process groups are unavailable on Windows")
 def test_cleanup_accepts_already_stopped_group(self):
  process=Mock();process.pid=123
  with patch('audit_site.os.name','posix'),patch('audit_site.os.killpg',side_effect=ProcessLookupError):
   stop_chrome(process)
  process.wait.assert_called_once_with(timeout=5)

 def test_windows_cleanup_waits_for_termination(self):
  process=Mock();process.poll.return_value=None
  with patch('audit_site.os.name','nt'):stop_chrome(process)
  process.terminate.assert_called_once_with()
  process.wait.assert_called_once_with(timeout=10)
