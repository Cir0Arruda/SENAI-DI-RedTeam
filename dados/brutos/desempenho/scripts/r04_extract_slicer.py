from pathlib import Path
import re,json,math,csv,collections,zipfile,xml.etree.ElementTree as ET
O=Path.cwd().parent/'desempenho'
def parse_gcode(path,density):
 role='Custom';obj='SEM_OBJETO';relative=False;estate=0.;lengths=collections.defaultdict(float);byobj=collections.defaultdict(lambda:collections.defaultdict(float));moves=0
 reobj=re.compile(r'^; printing object (.+?) id:');param=re.compile(r'([XYZEFIJ])([-+0-9.eE]+)')
 with Path(path).open(encoding='utf-8',errors='replace') as f:
  for line in f:
   if line.startswith(('; FEATURE:',';TYPE:','; TYPE:')):role=line.split(':',1)[1].strip();continue
   m=reobj.match(line)
   if m:obj=m.group(1);continue
   if line.startswith('; stop printing object'):obj='SEM_OBJETO';continue
   code=line.split(';',1)[0].strip()
   if not code:continue
   tokens=code.split();cmd=tokens[0]
   if cmd=='M83':relative=True;continue
   if cmd=='M82':relative=False;continue
   # Machine macros may contain letters resembling numeric axis parameters.
   # Only motion and coordinate-reset commands have extrusion to parse.
   if cmd not in ['G0','G1','G2','G3','G92']:continue
   # Native G-code has whitespace-separated axis words. Parse only extrusion;
   # this also avoids repeatedly allocating all XYZ/F values for large TPMS files.
   eword=next((v[1:] for v in tokens[1:] if v.startswith('E')),None)
   if cmd=='G92':
    if eword is not None:estate=float(eword)
    continue
   if eword is None:continue
   ee=float(eword);delta=ee if relative else ee-estate;estate=estate+ee if relative else ee
   if delta>0 and any(v[0] in 'XYIJ' for v in tokens[1:]):lengths[role]+=delta;byobj[obj][role]+=delta;moves+=1
 area=math.pi*(1.75/2)**2
 rows=[{'role':k,'filament_mm':v,'volume_cm3':v*area/1000,'mass_g':v*area/1000*density} for k,v in sorted(lengths.items())]
 def cat(role):
  if 'support' in role.lower():return 'suporte'
  if role.lower() in ['skirt','brim','skirt/brim']:return 'adesao'
  if role.lower()=='custom':return 'custom_outros'
  return 'peca'
 totals=collections.defaultdict(float)
 for r in rows:totals[cat(r['role'])]+=r['mass_g']
 assert rows and not (len(rows)==1 and rows[0]['role']=='Custom'),'Feature comments absent: cannot separate object and supports'
 return {'roles':rows,'category_mass_g':dict(totals),'tracked_deposition_moves':moves,'method':'positive E during XY/arc moves, by native TYPE or FEATURE tags; retractions and E-only priming excluded','density_g_cm3':density,'filament_diameter_mm':1.75,'not_measured_mass':True,'object_role_mass_g':{k:{r:ell*area/1000*density for r,ell in rr.items()} for k,rr in byobj.items()}}

def extract(folder):
 folder=Path(folder);p=next(folder.glob('*FATIAD*.3mf'))
 with zipfile.ZipFile(p) as z:
  gnames=[n for n in z.namelist() if n.endswith('.gcode')];assert gnames,'No actual sliced Gcode in3MF'
  info=ET.fromstring(z.read('Metadata/slice_info.config'));plate=info.find('plate');meta={x.get('key'):x.get('value') for x in plate.findall('metadata')};assert meta.get('outside')=='false',meta
  cfg=json.loads(z.read('Metadata/project_settings.config'));rho=float(cfg['filament_density'][0]);gpath=folder/'plate_1.gcode'
  if not gpath.exists():gpath.write_bytes(z.read(gnames[0]))
  data=parse_gcode(gpath,rho);data['Orca_summary']={'prediction_s':int(meta['prediction']),'total_filament_mass_g':float(meta['weight']),'outside':meta['outside'],'support_used':meta.get('support_used'),'warnings':[x.attrib for x in plate.findall('warning')],'filament':plate.find('filament').attrib,'actual_Gcode_in_archive':True};data['effective_settings']={k:cfg.get(k) for k in ['printer_model','printer_settings_id','printable_area','wall_loops','sparse_infill_density','sparse_infill_pattern','filament_density','filament_type','layer_height','nozzle_temperature','curr_bed_type','textured_plate_temp']};data['tracked_mass_difference_from_Orca_g']=sum(data['category_mass_g'].values())-float(meta['weight'])
  # Export actual slicer native thumbnails, not deformation images.
  for n in ['Metadata/plate_1.png','Metadata/top_1.png']:
   if n in z.namelist():(folder/Path(n).name).write_bytes(z.read(n))
 (folder/'dados_fatiamento.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 with (folder/'material_por_funcao.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(data['roles'][0]));w.writeheader();w.writerows(data['roles'])
 print(json.dumps({'case':folder.name,'mass_categories_g':data['category_mass_g'],'Orca_mass_g':data['Orca_summary']['total_filament_mass_g'],'time_s':data['Orca_summary']['prediction_s'],'difference_g':data['tracked_mass_difference_from_Orca_g'],'warnings':data['Orca_summary']['warnings']},ensure_ascii=True),flush=True)
 return data
if __name__=='__main__':
 import sys
 for name in sys.argv[1:]:extract(O/'05_Orca'/name)
