import zipfile,json
from pathlib import Path
O=Path.cwd().parent/'desempenho';p=O/'05_Orca/ORCA_ANTERIOR_MONTAGEM_ESCALADA.3mf'
print({'saved':p.exists(),'bytes':p.stat().st_size if p.exists() else 0})
if p.exists():
 with zipfile.ZipFile(p) as z:
  print(z.namelist()[:22])
  q=json.loads(z.read('Metadata/project_settings.config'))
  for name in ['printer_model','printer_variant','printer_settings_id','print_settings_id','filament_settings_id','filament_type','filament_density','curr_bed_type','sparse_infill_pattern','sparse_infill_density','wall_loops']:
   print(name,q.get(name))
  (O/'05_Orca/perfil_anterior_resolvido.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
