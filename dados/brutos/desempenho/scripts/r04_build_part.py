import json,sys
from pathlib import Path
from server import bridge,persist
O=Path.cwd().parent/'desempenho';key=sys.argv[1] if len(sys.argv)>1 else 'SUPERIOR';assert key in ['SUPERIOR','INFERIOR_ESQ','INFERIOR_DIR'];raw=O/'03_STL_Garra/origem';raw.mkdir(exist_ok=True);mr=O/'04_Modificadores/origem';mr.mkdir(exist_ok=True)
code='''import adsk.core,adsk.fusion,json,math

def run(_context: str):
 a=adsk.core.Application.get();src=next(x for x in a.documents if x.name=='SAMI - PAD95 SUPERIOR R02 - GARRA30 PAD40');src.activate();sd=adsk.fusion.Design.cast(src.products.itemByProductType('DesignProductType'))
 key='''+repr(key)+''';name='SAMI R04 - '+key+' - MODIFICADORES TPMSD';assert not any(x.name==name for x in a.documents),'R04 part already exists; inspect rather than repeat'
 occs=[o for o in sd.rootComponent.allOccurrences if o.component.name=='Suporte_Ventosas_S'];source=next(o for o in sd.rootComponent.allOccurrences if o.component.name=='Corpo Supor') if key=='SUPERIOR' else occs[0 if key=='INFERIOR_ESQ' else 1]
 tm=adsk.fusion.TemporaryBRepManager.get();P=adsk.core.Point3D.create;V=adsk.core.Vector3D.create;U=adsk.fusion.BooleanTypes.UnionBooleanType;I=adsk.fusion.BooleanTypes.IntersectionBooleanType;D=adsk.fusion.BooleanTypes.DifferenceBooleanType
 body=tm.copy(source.component.bRepBodies.item(0));assert tm.transform(body,source.transform2);original_volume=body.volume
 # Export actual occurrence at source scale, without hardware or the PAD.
 rawpath='''+repr(str(raw))+'''+'/GARRA_'+key+'_ENVELOPE.stl';opt=sd.exportManager.createSTLExportOptions(source,rawpath);opt.isBinaryFormat=True;assert sd.exportManager.execute(opt)
 joints=[(-67.73338307306587,21.800055418372644),(-67.73338307306582,34.800055418330146),(-47.83338307306283,34.800055418330085),(-47.833383073062866,21.800055418372594)]
 def cyl(x,y,r,z0,z1):return tm.createCylinderOrCone(P(x,y,z0),r,P(x,y,z1),r)
 def union(items):
  out=tm.copy(items[0])
  for t in items[1:]:assert tm.booleanOperation(out,t,U),'mask union failed'
  return out
 def corridor(points,width,z0,z1):
  boxes=[]
  for aa,bb in zip(points,points[1:]):
   dx=bb[0]-aa[0];dy=bb[1]-aa[1];ll=math.hypot(dx,dy);assert ll>.001
   box=adsk.core.OrientedBoundingBox3D.create(P((aa[0]+bb[0])/2,(aa[1]+bb[1])/2,(z0+z1)/2),V(dx/ll,dy/ll,0),V(-dy/ll,dx/ll,0),ll+width,width,z1-z0);boxes.append(tm.createBox(box))
  return union(boxes)
 local_joints=joints if key=='SUPERIOR' else ([joints[0],joints[1]] if key=='INFERIOR_ESQ' else [joints[3],joints[2]])
 pink=union([cyl(x,y,3.15,26.4,29.3) for x,y in local_joints]);yellow=union([cyl(x,y,4.6,23.0,31.0) for x,y in local_joints])
 paths=[]
 if key=='SUPERIOR':
  paths=[[joints[0],(-65.1,27.5),(-62.0,33.6)], [joints[3],(-50.5,27.5),(-53.5,33.6)], [joints[1],(-64.0,36.4),(-62.4,38.3)], [joints[2],(-51.6,36.4),(-53.1,38.3)], [(-65.1,27.5),(-62.4,31.5),(-57.783383,33.2),(-53.2,31.5),(-50.5,27.5)]]
  items=[corridor(path,1.8,26.0,34.0) for path in paths]
  ring=cyl(-57.783383,38.300055,5.1,27.0,33.6);assert tm.booleanOperation(ring,cyl(-57.783383,38.300055,4.1,26.9,33.7),D);items.append(ring);blue=union(items)
 else:
  left=key=='INFERIOR_ESQ';js=[joints[0],joints[1]] if left else [joints[3],joints[2]];xs=[-78.683383,-62.383383] if left else [-53.183383,-36.883383]
  for j,yy in zip(js,[15.900055,40.700055]):
   for xx in xs:paths.append([j,((j[0]+xx)/2,(j[1]+yy)/2),(xx,yy)])
  paths.append([js[0],((js[0][0]+js[1][0])/2,(js[0][1]+js[1][1])/2),js[1]])
  blue=union([corridor(path,1.6,19.0,27.5) for path in paths])
 # Modifier primitives are clipped by the slicer. No fragile boolean against source NURBS.
 assert tm.booleanOperation(blue,pink,D),'blue minus pink'
 assert tm.booleanOperation(yellow,pink,D),'yellow minus pink'
 assert tm.booleanOperation(yellow,blue,D),'yellow minus blue'
 parts=[('ROSA',70,pink,(238,35,219)),('AZUL',50,blue,(0,145,206)),('AMARELO',30,yellow,(249,220,10)),('BASE',20,body,(180,188,196))]
 total=None
 doc=a.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name=name;d=adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'));d.designType=adsk.fusion.DesignTypes.DirectDesignType
 mat=d.materials.addByCopy(source.component.bRepBodies.item(0).material,'PA6CF_SOLIDO_REFERENCIA_NAO_HOMOGENEIZADO')
 rows=[]
 for label,pct,t,col in parts:
  oc=d.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create());oc.component.name=key+'_'+label+'_'+str(pct);b=oc.component.bRepBodies.add(t);b.name=oc.component.name;b.material=mat
  ap=d.appearances.addByCopy(mat.appearance,'COR_'+label)
  for cp in ap.appearanceProperties:
   if cp.objectType=='adsk::core::ColorProperty':cp.value=adsk.core.Color.create(*col,255)
  b.appearance=ap
  b.attributes.add('SAMI_R04','region',json.dumps({'density_percent':pct,'sparse_pattern':'tpmsd','CAD_envelope_not_explicit_lattice':True,'modifier_only_for_slicing':label!='BASE','no_effective_solver_law':True}))
  path='''+repr(str(mr))+'''+'/'+key+'_'+label+'_'+str(pct)+'.stl';opt=d.exportManager.createSTLExportOptions(b,path);opt.isBinaryFormat=True;assert d.exportManager.execute(opt)
  rows.append({'label':label,'percent':pct,'modifier_envelope_volume_cm3_not_printed_region_volume':b.volume,'lumps':b.lumps.count,'stl_raw':path})
 scope={'part':key,'source_occurrence':source.fullPathName,'source_volume_cm3':original_volume,'partition_total_cm3':total,'partition_difference_cm3':None,'geometry_mode':'whole PA envelope plus nonprinting modifier masks; not disjoint source partitions','source_trim_failure':'ASM_EDGECOIN_PROBLEM; no repeat of source intersection','priority':[70,50,30,20],'paths_world_cm':paths,'pink_cylinder_radius_mm':31.5,'pink_z_mm':[264,293],'yellow_cylinder_radius_mm':46,'yellow_z_mm':[230,310],'blue_corridor_width_mm':18 if key=='SUPERIOR' else 16,'zones_are_dimensional_hypotheses_from_2D_image':True,'field_simulation_solved':False}
 d.rootComponent.attributes.add('SAMI_R04','scope',json.dumps(scope))
 f='''+repr(str(O/'01_Fusion'))+'''+'/GARRA_'+key+'_ZONAS_R04.f3d';assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(f));assert d.exportManager.execute(d.exportManager.createSTEPExportOptions(f.replace('.f3d','.step')))
 a.activeViewport.fit();assert a.activeViewport.saveAsImageFile(f.replace('.f3d','.png'),1600,1100)
 print(json.dumps({'document':name,'source_transform':source.transform2.asArray(),'main_stl_raw':rawpath,'source_material':source.component.bRepBodies.item(0).material.name,'scope':scope,'regions':rows,'archive':f}))
'''
r=bridge.script(code,False);(O/f'04_Modificadores/{key}_regioes.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');persist('r04_'+key.lower()+'.json',r);print(json.dumps({'part':key,'doc':r.get('document'),'volumes':[(x['label'],round(x['modifier_envelope_volume_cm3_not_printed_region_volume'],3)) for x in r.get('regions',[])],'source_volume':r.get('scope',{}).get('source_volume_cm3')}))
