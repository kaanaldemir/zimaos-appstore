"""Emit a ZIP source store for older ZimaOS/CasaOS clients."""
import json,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
output=root/'dist/store/main.zip';output.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
 for path in (root/'staging/Apps').rglob('*'):
  if not path.is_file():continue
  name=str(path.relative_to(root/'staging')).replace('\\','/')
  if path.name=='docker-compose.yml':
   compose=json.loads(path.read_text())
   for field in ['title','description','tagline']:
    value=compose['x-casaos'].get(field,{})
    compose['x-casaos'][field]={key.lower():text for key,text in value.items()}
   archive.writestr(name,json.dumps(compose,ensure_ascii=False,indent=2))
  else:archive.write(path,name)
 archive.write(root/'README.md','README.md')
