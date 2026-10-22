"""Offline rebuild and checks. Refresh evidence separately with ingest.py --refresh."""
from pathlib import Path
import subprocess,sys,os
root=Path(__file__).resolve().parents[1];env=os.environ.copy();env['PYTHONPATH']=str(root/'src')
for args in [[sys.executable,'scripts/build.py'],[sys.executable,'scripts/database.py'],[sys.executable,'-m','unittest','discover','-s','tests','-v'],['node','--test','tests/model.test.mjs'],[sys.executable,'scripts/check.py']]:
 subprocess.run(args,cwd=root,env=env,check=True)
print('Rebuild complete. Start the app: python -m http.server 8000 --directory dist')
