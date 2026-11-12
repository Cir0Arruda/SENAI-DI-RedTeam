from pathlib import Path
import httpx,concurrent.futures,json
O=Path.cwd().parent/'desempenho';base='https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/resources/profiles/BBL/filament/'
names=['Generic TPU @base.json','Generic TPU.json','Generic TPU @BBL X1C.json','Bambu PA6-CF @BBL X1C.json']
def get(n):
 r=httpx.get(base+n,timeout=20)
 if r.status_code==200:
  p=O/'07_Referencias/perfis_originais'/n;p.parent.mkdir(exist_ok=True);p.write_bytes(r.content);return [n,r.status_code,json.loads(r.content).get('inherits')]
 return [n,r.status_code]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:print(list(ex.map(get,names)))
