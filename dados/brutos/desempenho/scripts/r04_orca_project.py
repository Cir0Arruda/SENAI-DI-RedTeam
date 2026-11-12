from pathlib import Path
import json,zipfile,xml.etree.ElementTree as ET,numpy as np
from r04_mesh_package import read
O=Path.cwd().parent/'desempenho';F=O/'05_Orca';P=O/'07_Referencias/perfis_originais';base=json.loads((F/'perfil_anterior_resolvido.json').read_text(encoding='utf-8'));NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',NS)

def material(name,seen=None):
 d=json.loads((P/(name+'.json')).read_text(encoding='utf-8'));out=material(d['inherits']) if d.get('inherits') else {};out.update(d);return out

def settings(tpu=False):
 q=json.loads(json.dumps(base));mat=material('Generic TPU' if tpu else 'Bambu PA6-CF @BBL X1C')
 for k,val in mat.items():
  if k not in q or k in ['name','type','inherits','compatible_printers']:continue
  if isinstance(val,list) and len(val)>1 and isinstance(q[k],list) and len(q[k])==1:val=val[:1] # selected Direct Drive Standard variant
  q[k]=val
 for k in list(q):
  if any(x in k.lower() for x in ['password','apikey','api_key','token','print_host','printhost_user','printhost_cafile']):q[k]='' if isinstance(q[k],str) else []
 q.update({'curr_bed_type':'Textured PEI Plate','wall_loops':'3' if tpu else '5','sparse_infill_density':'40%' if tpu else '20%','sparse_infill_pattern':'gyroid' if tpu else 'tpmsd','layer_height':'0.2','initial_layer_print_height':'0.2','top_shell_layers':'6','bottom_shell_layers':'6','top_shell_thickness':'1.2','bottom_shell_thickness':'1.2','enable_support':'1','support_on_build_plate_only':'0','brim_type':'auto_brim','filament_settings_id':['Generic TPU' if tpu else 'Bambu PA6-CF @BBL X1C'],'filament_density':['1.22' if tpu else '1.09'],'filament_colour':['#F27A20' if tpu else '#50565E'],'print_settings_id':'SAMI_R04_PAD40_3paredes' if tpu else 'SAMI_R04_TPMSD20_30_50_70_5paredes'})
 for k in ['line_width','outer_wall_line_width','inner_wall_line_width','sparse_infill_line_width','internal_solid_infill_line_width','top_surface_line_width','initial_layer_line_width','support_line_width']:
  if k in q:q[k]='0.4'
 if tpu:
  for k in ['nozzle_temperature','nozzle_temperature_initial_layer']:q[k]=['230']
  for k in ['hot_plate_temp','hot_plate_temp_initial_layer','textured_plate_temp','textured_plate_temp_initial_layer','eng_plate_temp','eng_plate_temp_initial_layer']:q[k]=['50']
  q['filament_max_volumetric_speed']=['3.2']
 return q

def build(dst,objects,tpu=False):
 model=ET.Element('{'+NS+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'pt-BR'});
 for name,value in [('Application','BambuStudio-02.08.01.55'),('OrcaSlicer','2.5.0'),('BambuStudio:3mfVersion','1'),('Title','SAMI R04 - PREPARACAO NAO VALIDADA')]:ET.SubElement(model,'{'+NS+'}metadata',{'name':name}).text=value
 res=ET.SubElement(model,'{'+NS+'}resources');buildnode=ET.SubElement(model,'{'+NS+'}build');cfg=ET.Element('config');plate=ET.Element('plate');ET.SubElement(plate,'metadata',{'key':'plater_id','value':'1'});ET.SubElement(plate,'metadata',{'key':'plater_name','value':dst.stem});ET.SubElement(plate,'metadata',{'key':'locked','value':'false'});ET.SubElement(plate,'metadata',{'key':'filament_maps','value':'1'});nid=1
 for oi,obj in enumerate(objects):
  ids=[]
  for part in obj['parts']:
   vv=read(part['file']);verts,ix=np.unique(np.round(vv.reshape(-1,3),6),axis=0,return_inverse=True);tris=ix.reshape(-1,3);objnode=ET.SubElement(res,'{'+NS+'}object',{'id':str(nid),'type':'model','name':part['name']});mesh=ET.SubElement(objnode,'{'+NS+'}mesh');vs=ET.SubElement(mesh,'{'+NS+'}vertices');ts=ET.SubElement(mesh,'{'+NS+'}triangles')
   for pt in verts:ET.SubElement(vs,'{'+NS+'}vertex',dict(zip(['x','y','z'],[format(float(x),'.6f') for x in pt])))
   for tri in tris:ET.SubElement(ts,'{'+NS+'}triangle',dict(zip(['v1','v2','v3'],map(str,tri))))
   ids.append((nid,part));nid+=1
  groupid=nid;nid+=1;parent=ET.SubElement(res,'{'+NS+'}object',{'id':str(groupid),'type':'model','name':obj['name']});comps=ET.SubElement(parent,'{'+NS+'}components')
  for ident,part in ids:ET.SubElement(comps,'{'+NS+'}component',{'objectid':str(ident)})
  x,y=obj.get('xy',(128,128));trans=f'1 0 0 0 1 0 0 0 1 {x} {y} 0';ET.SubElement(buildnode,'{'+NS+'}item',{'objectid':str(groupid),'transform':trans,'printable':'1'})
  oc=ET.SubElement(cfg,'object',{'id':str(groupid),'auto_drop':'1'})
  for k,val in {'name':obj['name'],'extruder':'1','sparse_infill_pattern':'gyroid' if tpu else 'tpmsd','sparse_infill_density':'40%' if tpu else '20%','wall_loops':'3' if tpu else '5'}.items():ET.SubElement(oc,'metadata',{'key':k,'value':val})
  for ident,part in ids:
   pn=ET.SubElement(oc,'part',{'id':str(ident),'subtype':'modifier_part' if part.get('modifier') else 'normal_part'});ET.SubElement(pn,'metadata',{'key':'name','value':part['name']});ET.SubElement(pn,'metadata',{'key':'matrix','value':'1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1'})
   if part.get('modifier'):
    ET.SubElement(pn,'metadata',{'key':'sparse_infill_density','value':str(part['percent'])+'%'});ET.SubElement(pn,'metadata',{'key':'sparse_infill_pattern','value':'tpmsd'})
  mi=ET.SubElement(plate,'model_instance')
  for k,val in [('object_id',str(groupid)),('instance_id','0'),('identify_id',str(100+oi))]:ET.SubElement(mi,'metadata',{'key':k,'value':val})
 cfg.append(plate);types=b'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/><Default Extension="config" ContentType="application/octet-stream"/></Types>';rels=b'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'
 with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('[Content_Types].xml',types);z.writestr('_rels/.rels',rels);z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True));z.writestr('Metadata/model_settings.config',ET.tostring(cfg,encoding='utf-8',xml_declaration=True));z.writestr('Metadata/project_settings.config',json.dumps(settings(tpu),ensure_ascii=False,indent=2))
 return str(dst)

if __name__=='__main__':
 objs=[]
 for i,path in enumerate(sorted((O/'02_STL_PAD').glob('PAD95_R02_*.stl'))):objs.append({'name':path.stem,'xy':(42+i%3*82,42+i//3*82),'parts':[{'file':path,'name':path.stem}]})
 print(build(F/'PADs_TPU95A40_PREPARADO.3mf',objs,True))
 for key in ['SUPERIOR','INFERIOR_ESQ','INFERIOR_DIR']:
  parts=[{'file':O/f'03_STL_Garra/GARRA_{key}_BASE20.stl','name':'GARRA_'+key+'_CONTINUA_BASE20'}]
  for color,pct in [('AMARELO',30),('AZUL',50),('ROSA',70)]:parts.append({'file':O/f'04_Modificadores/{key}/MOD_{color}_{pct}.stl','name':f'MOD_{color}_{pct}_NAO_IMPRIMIVEL','modifier':True,'percent':pct})
  print(build(F/f'GARRA_{key}_TPMSD_ZONAL_ESCALA1.3mf',[{'name':f'GARRA_{key}_R04_ESCALA1','parts':parts}],False))
