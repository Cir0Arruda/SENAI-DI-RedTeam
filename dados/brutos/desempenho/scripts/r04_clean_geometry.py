"""Native study geometry with original PA exteriors, separate PADs, NO modifier solids."""
from pathlib import Path
import json,zipfile
from server import bridge,persist
O=Path(__file__).resolve().parents[2]/'desempenho'
code='''import adsk.core,adsk.fusion,json
def run(_context: str):
 a=adsk.core.Application.get();name='SAMI R04 - ESTUDOS - EXTERIOR ORIGINAL SEM MASCARAS'
 assert not any(x.name==name for x in a.documents),'Study geometry already exists: inspect instead of duplicate'
 src=next(x for x in a.documents if x.name=='SAMI - PAD95 SUPERIOR R02 - GARRA30 PAD40');sd=adsk.fusion.Design.cast(src.products.itemByProductType('DesignProductType'))
 tm=adsk.fusion.TemporaryBRepManager.get();parts=[];lower=0
 for o in sd.rootComponent.allOccurrences:
  comp=o.component.name
  if comp not in ['Corpo Supor','Suporte_Ventosas_S'] and not comp.startswith('PAD95_R02_A'):continue
  if comp=='Corpo Supor':label='GARRA_SUPERIOR_EXTERIOR_ORIGINAL'
  elif comp=='Suporte_Ventosas_S':
   label='GARRA_INFERIOR_'+('ESQ' if lower==0 else 'DIR')+'_EXTERIOR_ORIGINAL';lower+=1
  else:label=comp
  b=o.component.bRepBodies.item(0);t=tm.copy(b);assert tm.transform(t,o.transform2)
  parts.append((label,t,b.material,b.appearance,o.fullPathName,b.volume))
 assert len(parts)==11 and lower==2
 doc=a.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name=name;d=adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'));d.designType=adsk.fusion.DesignTypes.DirectDesignType
 mats={};rows=[]
 for label,t,mat,ap,source,volume in parts:
  if mat.id not in mats:mats[mat.id]=d.materials.addByCopy(mat,mat.name+'_SOLID_REFERENCE_ONLY_R04')
  oc=d.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create());oc.component.name=label;b=oc.component.bRepBodies.add(t);b.name=label;b.material=mats[mat.id]
  pad=label.startswith('PAD');b.attributes.add('SAMI_R04','scope',json.dumps({'source_occurrence':source,'source_volume_cm3':volume,'outer_geometry_must_not_change':not pad,'infill':{'percent':40,'pattern':'gyroid'} if pad else {'base':20,'yellow':30,'blue':50,'pink':70,'pattern':'tpmsd','wall_loops':5},'solid_reference_NOT_homogenized_effective_material':True,'not_ready_to_solve_as_solid':True}))
  assert abs(b.volume-volume)<.000001
  rows.append({'name':label,'source':source,'volume_cm3':b.volume,'material_reference':b.material.name,'is_PAD':pad,'geometry_unchanged':True})
 d.rootComponent.attributes.add('SAMI_R04','mandatory_rule','NO EXTERNAL CHANGES TO GRIPPER. No modifier bodies in this study geometry. Infill is not explicitly meshed. Do not solve as homogeneous solid and call it zonal infill. PADs remain separate components.')
 p='''+repr(str(O/'01_Fusion/GARRA_R04_EXTERIOR_ORIGINAL_PREPARACAO'))+'''
 assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(p+'.f3d'))
 assert d.exportManager.execute(d.exportManager.createSTEPExportOptions(p+'.step'))
 a.activeViewport.fit();assert a.activeViewport.saveAsImageFile(p+'.png',1600,1100)
 print(json.dumps({'document':name,'bodies':rows,'modifier_body_count':0,'jobs_submitted':0,'mesh_generated':False,'simulation_status':'prepared_geometry_only; zonal effective laws and PAD contact/dissipation missing','archive':p+'.f3d'}))
'''
r=bridge.script(code,False);persist('r04_clean_study_geometry.json',r)
(O/'06_Engenharia/FUSION_GEOMETRIA_ESTUDOS.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
with zipfile.ZipFile(r['archive']) as z:assert z.testzip() is None
print(json.dumps({'document':r['document'],'PA_bodies':sum(not x['is_PAD'] for x in r['bodies']),'PAD_halves':sum(x['is_PAD'] for x in r['bodies']),'modifier_solids':0,'source_volume_equality':'passed','new_jobs':0}))
