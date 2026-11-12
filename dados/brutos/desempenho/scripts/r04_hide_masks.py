"""Hide tooling envelopes in native CAD; preserve all printable/source geometry."""
import json
from pathlib import Path
from server import bridge,persist
O=Path(__file__).resolve().parents[2]/'desempenho'
code='''import adsk.core,adsk.fusion,json
def run(_context: str):
 a=adsk.core.Application.get();rows=[]
 for key in ['SUPERIOR','INFERIOR_ESQ','INFERIOR_DIR']:
  name='SAMI R04 - '+key+' - MODIFICADORES TPMSD'
  doc=next(x for x in a.documents if x.name==name);doc.activate();d=adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'))
  before={o.component.name:sum(b.volume for b in o.component.bRepBodies) for o in d.rootComponent.occurrences}
  for o in d.rootComponent.occurrences:
   o.isLightBulbOn='_BASE_20' in o.component.name
  after={o.component.name:sum(b.volume for b in o.component.bRepBodies) for o in d.rootComponent.occurrences};assert before==after
  d.rootComponent.attributes.add('SAMI_R04','NO_EXTERNAL_CHANGE','Mandatory user rule: colored masks only control internal sparse infill; never join them to envelope or treat as physical simulation bodies.')
  f='''+repr(str(O/'01_Fusion'))+'''+'/GARRA_'+key+'_ZONAS_R04.f3d'
  assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(f))
  a.activeViewport.fit();assert a.activeViewport.saveAsImageFile(f.replace('.f3d','_EXTERIOR_INALTERADO.png'),1600,1100)
  rows.append({'document':name,'visible_printable_envelopes':1,'nonprinting_masks_hidden':3,'body_volumes_unchanged':before==after,'archive':f})
 print(json.dumps({'rows':rows,'new_simulation_jobs':0}))
'''
r=bridge.script(code,False);persist('r04_masks_hidden.json',r)
(O/'06_Engenharia/FUSION_EXTERIOR_INALTERADO.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'native_documents_updated':len(r['rows']),'body_volumes_unchanged':all(x['body_volumes_unchanged'] for x in r['rows']),'simulation_submissions':0}))
