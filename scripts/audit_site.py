"""Run pinned Lighthouse against dist with bounded Chrome startup and cleanup.
CI has Chrome installed; no browser download, ignored failures or score fabrication.
"""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import argparse,json,os,shutil,socket,subprocess,tempfile,threading,time,urllib.request
ROOT=Path(__file__).resolve().parents[1]
def free_port():
 with socket.socket() as sock:
  sock.bind(('127.0.0.1',0));return sock.getsockname()[1]
def wait_ready(url,process,timeout=30):
 deadline=time.monotonic()+timeout
 while time.monotonic()<deadline:
  if process.poll() is not None:raise RuntimeError('Chrome exited before readiness; inspect lighthouse-chrome.log')
  try:
   with urllib.request.urlopen(url,timeout=1) as response:payload=json.load(response)
   if payload.get('webSocketDebuggerUrl'):return
  except (OSError,ValueError):pass
  time.sleep(.2)
 raise TimeoutError('Chrome debugging endpoint did not become ready within the startup limit')
def lighthouse_command(cli,url,port,profile,output):
 command=['node',str(cli),url,f'--port={port}','--hostname=127.0.0.1','--output=json','--output=html',f'--output-path={output}','--no-enable-error-reporting','--quiet']
 if profile=='desktop':command.append('--preset=desktop')
 return command
class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--lighthouse-cli',type=Path,required=True)
 args=parser.parse_args();cli=args.lighthouse_cli.resolve()
 if not cli.is_file():raise SystemExit('Install pinned Lighthouse and supply its cli/index.js path')
 chrome=os.environ.get('CHROME_PATH') or shutil.which('google-chrome') or shutil.which('chromium')
 if not chrome:raise SystemExit('Chrome is required; set CHROME_PATH to the installed executable')
 out=ROOT/'outputs';out.mkdir(exist_ok=True)
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT/'dist')))
 worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
 process=None
 try:
  url=f'http://127.0.0.1:{server.server_port}/';port=free_port()
  with tempfile.TemporaryDirectory(prefix='thirstyai-chrome-') as profile_dir,(out/'lighthouse-chrome.log').open('w',encoding='utf-8') as log:
   try:
    process=subprocess.Popen([chrome,'--headless=new','--no-sandbox','--disable-dev-shm-usage',f'--remote-debugging-port={port}','--remote-debugging-address=127.0.0.1',f'--user-data-dir={profile_dir}','--no-first-run','--no-default-browser-check','about:blank'],stdout=log,stderr=subprocess.STDOUT)
    wait_ready(f'http://127.0.0.1:{port}/json/version',process)
    for profile in ('mobile','desktop'):
     subprocess.run(lighthouse_command(cli,url,port,profile,out/f'lighthouse-{profile}'),cwd=ROOT,check=True,timeout=180)
     report=json.loads((out/f'lighthouse-{profile}.report.json').read_text(encoding='utf-8'))
     if report.get('runtimeError'):raise RuntimeError(f'{profile} Lighthouse runtime error')
     if not all(report.get('categories',{}).get(key,{}).get('score') is not None for key in ('performance','accessibility','best-practices','seo')):
      raise RuntimeError(f'{profile} incomplete Lighthouse report')
     print(profile,{key:round(value['score']*100) for key,value in report['categories'].items()},flush=True)
   finally:
    if process is not None and process.poll() is None:
     process.terminate()
     try:process.wait(timeout=10)
     except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)
 finally:server.shutdown();server.server_close();worker.join(timeout=5)
if __name__=='__main__':main()
