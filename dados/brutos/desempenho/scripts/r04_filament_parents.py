import json,httpx,concurrent.futures
from pathlib import Path
O=Path.cwd().parent/'desempenho';P=O/'07_Referencias/perfis_originais';names=['fdm_filament_tpu.json','fdm_filament_common.json','Bambu PA6-CF @base.json','Generic PA-CF @base.json']
def get(n):
 r=httpx.get('https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/resources/profiles/BBL/filament/'+n,timeout=20)
 if r.status_code==200:(P/n).write_bytes(r.content)
 return[n,r.status_code]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:print(list(ex.map(get,names)))
for path in P.glob('*.json'):
 p=json.loads(path.read_text());print(path.name,{k:p.get(k) for k in ['inherits','filament_type','filament_density','nozzle_temperature','hot_plate_temp','textured_plate_temp','filament_max_volumetric_speed'] if k in p})
