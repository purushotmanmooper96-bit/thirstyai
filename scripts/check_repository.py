"""Check packaging/version consistency, documentation targets and notebook execution."""
from pathlib import Path
import ast,json,re,subprocess,sys
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from thirstyai import __version__
def main():
 versions=[__version__,json.loads((ROOT/'package.json').read_text(encoding='utf-8'))['version']]
 for name in ('pyproject.toml','CITATION.cff'):
  text=(ROOT/name).read_text(encoding='utf-8')
  match=re.search(r'^version\s*[:=]\s*["\']?([0-9.]+)',text,re.M)
  if not match:raise ValueError('Missing version in '+name)
  versions.append(match.group(1))
 if len(set(versions))!=1:raise ValueError('Package / citation versions differ: '+str(versions))
 model_text=(ROOT/'dist/scenario.mjs').read_text(encoding='utf-8')
 if __version__ not in model_text:raise ValueError('Browser share model version differs')
 for folder in ('scripts','src','tests'):
  for path in (ROOT/folder).rglob('*.py'):ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
 for path in ROOT.rglob('*.md'):
  if any(part in ('.git','node_modules','.ci-tools') for part in path.parts):continue
  for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
   if target.startswith(('http:','https:','mailto:','#','<')):continue
   relative=unquote(target.split('#')[0])
   if relative and not (path.parent/relative).exists():raise ValueError(f'Broken local link in {path.relative_to(ROOT)}: {target}')
 for filename in [str(p.relative_to(ROOT)) for p in (ROOT/'dist').glob('*.mjs')]+['scripts/build_workbook.mjs']:
  subprocess.run(['node','--check',filename],cwd=ROOT,check=True,timeout=15)
 for path in (ROOT/'notebooks').glob('*.ipynb'):
  notebook=json.loads(path.read_text(encoding='utf-8'));namespace={'__name__':'__main__'}
  for cell in notebook['cells']:
   if cell['cell_type']=='code':exec(compile(''.join(cell['source']),str(path),'exec'),namespace)
 print('Repository checks passed: versions, Python/JS syntax, local documentation links and notebook cells. Optional workbook authoring and native desktop applications require their own environments.')
if __name__=='__main__':main()
