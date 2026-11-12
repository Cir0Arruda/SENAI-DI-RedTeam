from pathlib import Path
import json,httpx
import r04_orca_project as op
O=op.O;P=O/'07_Referencias/K1Max_perfis';seen={}
def load(name):
 if name in seen:return seen[name]
 f=P/('process__'+name+'.json')
 if not f.exists():
  r=httpx.get('https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/resources/profiles/Creality/process/'+name+'.json',timeout=30);r.raise_for_status();f.write_bytes(r.content)
 d=json.loads(f.read_text(encoding='utf-8'));q=load(d['inherits']).copy() if d.get('inherits') else {};q.update(d);seen[name]=q;return q
proc=load('0.20mm Standard @Creality K1Max (0.4 nozzle)');(P/'PROCESSO_K1MAX_RESOLVIDO.json').write_text(json.dumps(proc,ensure_ascii=False,indent=2),encoding='utf-8');mach=json.loads((P/'MAQUINA_K1MAX_RESOLVIDA.json').read_text(encoding='utf-8'));original=op.settings

def k1_settings(tpu=False):
 q=original(tpu);custom={k:v for k,v in q.items() if k in ['wall_loops','sparse_infill_density','sparse_infill_pattern','layer_height','initial_layer_print_height','top_shell_layers','bottom_shell_layers','top_shell_thickness','bottom_shell_thickness','enable_support','support_on_build_plate_only','filament_settings_id','filament_density','filament_colour','print_settings_id'] or 'line_width' in k}
 for k in q:
  if k.endswith('_gcode') and k!='high_precision_gcode':q[k]=[''] if isinstance(q[k],list) else ''
 for source in [mach,proc]:
  for k,v in source.items():
   if k in q and k not in ['name','type','inherits','compatible_printers','print_settings_id']:q[k]=v
 q.update(custom);q['print_compatible_printers']=proc.get('compatible_printers',[mach['name']]);q['upward_compatible_machine']=mach.get('upward_compatible_machine',[]);q.update({'printer_settings_id':mach['name'],'printer_model':'Creality K1 Max','printer_variant':'0.4','curr_bed_type':'Textured PEI Plate','brim_width':'3','filament_start_gcode':[''],'filament_end_gcode':[''],'enable_support':'1','support_on_build_plate_only':'0'})
 if 'support_brim_width' in q:q['support_brim_width']='3'
 if tpu:
  for k in ['hot_plate_temp','hot_plate_temp_initial_layer','textured_plate_temp','textured_plate_temp_initial_layer','eng_plate_temp','eng_plate_temp_initial_layer']:q[k]=['35']
 return q
op.settings=k1_settings
if __name__=='__main__':
 F=O/'05_Orca'
 for key in ['SUPERIOR','INFERIOR_ESQ','INFERIOR_DIR']:
  parts=[{'file':O/f'03_STL_Garra/GARRA_{key}_BASE20.stl','name':'GARRA_'+key+'_CONTINUA_BASE20'}]
  for col,pct in [('AMARELO',30),('AZUL',50),('ROSA',70)]:parts.append({'file':O/f'04_Modificadores/{key}/MOD_{col}_{pct}.stl','name':f'MOD_{col}_{pct}_NAO_IMPRIMIVEL','modifier':True,'percent':pct})
  print(op.build(F/f'GARRA_{key}_TPMSD_K1MAX_ESCALA_REAL.3mf',[{'name':f'GARRA_{key}_R04_ESCALA_REAL','xy':(150,150),'parts':parts}],False))
 objs=[]
 for i,p in enumerate(sorted((O/'02_STL_PAD').glob('PAD95_R02_*.stl'))):objs.append({'name':p.stem,'xy':(65+i%3*82,65+i//3*82),'parts':[{'file':p,'name':p.stem}]})
 print(op.build(F/'PADs_TPU95A40_K1MAX_ESCALA_REAL.3mf',objs,True))
 (F/'configuracao_referencia_K1MAX.json').write_text(json.dumps({'machine':mach['name'],'bed_mm':[300,300,300],'source_process':proc['name'],'scale':1,'orientation':'source Z up; no tilted X1 geometry used','PAD_bed_C':35,'PAD_nozzle_C':230,'PA_density_g_cm3':1.09,'TPU_density_g_cm3':1.22,'printing_not_qualified':True,'purpose':'material and path estimate, no sending to printer'},ensure_ascii=False,indent=2),encoding='utf-8')
 print('K1MAX_REAL_SCALE_READY')
