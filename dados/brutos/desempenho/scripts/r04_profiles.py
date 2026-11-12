import zipfile,json
from pathlib import Path
O=Path.cwd().parent/'desempenho';src=Path('~/AppData/Roaming/OrcaSlicer/system/BBL.opc');print({'opc_zip':zipfile.is_zipfile(src)})
if zipfile.is_zipfile(src):
 with zipfile.ZipFile(src) as z:
  names=[n for n in z.namelist() if n.endswith('.json') and any(s.lower() in n.lower() for s in ['PA6-CF','Generic PA-CF','Generic TPU','X1 0.4','Standard @BBL X1C'])]
  print(names[:30])
  (O/'07_Referencias/BBL_profile_names.json').write_text(json.dumps(z.namelist(),indent=2))
  for n in z.namelist():
   if not n.endswith('.json'):continue
   path=O/'07_Referencias/BBL_perfis'/n
   assert O in path.parents
   path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(z.read(n))
print('profiles_extracted_for_read')
