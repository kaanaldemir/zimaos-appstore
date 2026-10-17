"""Prepare catalog input using anonymous registry reads; no server credentials."""
import hashlib,json,re,shutil,time,urllib.request,urllib.error
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE='https://kaanaldemir.github.io/zimaos-appstore'
ACCEPT=', '.join(['application/vnd.oci.image.index.v1+json','application/vnd.docker.distribution.manifest.list.v2+json','application/vnd.oci.image.manifest.v1+json','application/vnd.docker.distribution.manifest.v2+json'])
def manifest(image):
 repository,tag=image.rsplit(':',1)
 if repository.startswith('ghcr.io/'):
  registry='ghcr.io'; repository=repository.removeprefix('ghcr.io/')
  auth='https://ghcr.io/token?scope=repository:'+repository+':pull'
 else:
  registry='registry-1.docker.io'
  if '/' not in repository:repository='library/'+repository
  auth='https://auth.docker.io/token?service=registry.docker.io&scope=repository:'+repository+':pull'
 token=json.load(urllib.request.urlopen(auth,timeout=30))['token']
 request=urllib.request.Request('https://'+registry+'/v2/'+repository+'/manifests/'+tag,headers={'Authorization':'Bearer '+token,'Accept':ACCEPT})
 with urllib.request.urlopen(request,timeout=30) as response:
  payload=response.read();digest=response.headers.get('Docker-Content-Digest') or 'sha256:'+hashlib.sha256(payload).hexdigest()
 return image.rsplit(':',1)[0]+'@'+digest,digest

def main():
 stage=ROOT/'staging'
 if stage.exists():shutil.rmtree(stage)
 stage.mkdir()
 for filename in ['store-config.json','supported-languages.json','README.md']:
  shutil.copy2(ROOT/filename,stage/filename)
 try:previous=json.load(urllib.request.urlopen(BASE+'/image-state.json',timeout=20))
 except urllib.error.HTTPError as error:
  if error.code!=404:raise
  previous={}
 state={};skipped=[]
 for entry in json.loads((ROOT/'catalog.json').read_text()):
  source=ROOT/entry['source']; compose=json.loads((source/'docker-compose.yml').read_text())
  image_set={}
  try:
   for name,service in compose['services'].items():
    image,digest=manifest(service['image']);image_set[name]=digest;service['image']=image
  except urllib.error.HTTPError as error:
   if entry.get('optional') and error.code in [401,403,404]:
    skipped.append(entry['folder']);print('Pending public image:',entry['folder']);continue
   raise
  identity=hashlib.sha256(json.dumps({'source':compose,'images':image_set},sort_keys=True).encode()).hexdigest()
  old=previous.get(entry['id'],{})
  version=old.get('version') if old.get('identity')==identity else '1.0.'+str(int(time.time()))
  compose['x-casaos']['version']=version
  compose['x-casaos']['update_at']=time.strftime('%Y-%m-%d',time.gmtime()) if old.get('identity')!=identity else old['update_at']
  state[entry['id']]={'identity':identity,'version':version,'update_at':compose['x-casaos']['update_at'],'images':image_set}
  destination=stage/'Apps'/entry['folder'];shutil.copytree(source,destination)
  (destination/'docker-compose.yml').write_text(json.dumps(compose,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'out').mkdir(exist_ok=True)
 (ROOT/'out/image-state.json').write_text(json.dumps(state,indent=2)+'\n')
 (ROOT/'out/pending.json').write_text(json.dumps(skipped)+'\n')
 print('Prepared applications:',len(state))
if __name__=='__main__':main()
