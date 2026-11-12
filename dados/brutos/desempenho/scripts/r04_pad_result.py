from pathlib import Path
import zipfile,json
O=Path.cwd().parent/'desempenho';d=O/'05_Orca/Resultado_PAD'
print([(p.name,p.stat().st_size) for p in d.iterdir()])
p=d/'PADs_TPU95A40_FATIADO_TESTE.3mf'
with zipfile.ZipFile(p) as z:
 print(z.namelist()[:30]);s=z.read('Metadata/slice_info.config').decode() if 'Metadata/slice_info.config' in z.namelist() else 'NO SLICE INFO';print(s[:4500]);cfg=json.loads(z.read('Metadata/project_settings.config'));print({k:cfg.get(k) for k in ['wall_loops','sparse_infill_density','sparse_infill_pattern','filament_type','filament_density','nozzle_temperature','curr_bed_type']})
 for n in z.namelist():
  if n.endswith('.gcode'):
   data=z.read(n).decode('utf-8',errors='replace');(d/(Path(n).name+'.cabecalho.txt')).write_text('\n'.join(data.splitlines()[:100]),encoding='utf-8');print('GCODE',n,len(data),data[:1200])
