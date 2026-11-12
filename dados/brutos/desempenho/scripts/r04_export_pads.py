import json
from pathlib import Path
from server import bridge,persist
O=Path.cwd().parent/'desempenho';raw=O/'02_STL_PAD/origem';raw.mkdir(exist_ok=True)
code='''import adsk.core,adsk.fusion,json

def run(_context: str):
 a=adsk.core.Application.get();src=next(x for x in a.documents if x.name=='SAMI - PAD95 SUPERIOR R02 - GARRA30 PAD40');sd=adsk.fusion.Design.cast(src.products.itemByProductType('DesignProductType'))
 name='SAMI R04 - PADs SEPARADOS - TPU95A40'
 assert not any(x.name==name for x in a.documents),'R04 PAD doc already exists; inspect before repeating'
 originals=[o for o in sd.rootComponent.allOccurrences if o.component.name.startswith('PAD95_R02_A')];assert len(originals)==8
 tm=adsk.fusion.TemporaryBRepManager.get();saved=[]
 for o in originals:
  t=tm.copy(o.component.bRepBodies.item(0));assert tm.transform(t,o.transform2);saved.append((o.component.name,t,o.component.bRepBodies.item(0).material,o.component.bRepBodies.item(0).appearance))
 doc=a.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType);doc.name=name;d=adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'));d.designType=adsk.fusion.DesignTypes.DirectDesignType
 m=d.materials.addByCopy(saved[0][2],'TPU95A_REFERENCIA_SOLIDA_PAD40_NO_FATIADOR');ap=d.appearances.addByCopy(saved[0][3],'PAD_LARANJA')
 rows=[]
 for stem,t,_,__ in saved:
  oc=d.rootComponent.occurrences.addNewComponent(adsk.core.Matrix3D.create());oc.component.name=stem;b=oc.component.bRepBodies.add(t);b.name=stem;b.material=m;b.appearance=ap
  p='''+repr(str(raw))+'''+'/'+stem+'.stl';opt=d.exportManager.createSTLExportOptions(b,p);opt.isBinaryFormat=True;assert d.exportManager.execute(opt)
  rows.append({'name':stem,'volume_cm3':b.volume,'solid':b.isSolid,'stl_raw':p})
 d.rootComponent.attributes.add('SAMI_R04','scope',json.dumps({'PAD_infill_percent':40,'material_reference':'PolyFlex TPU95A','CAD_envelope_only':True,'solver_results':False}))
 path='''+repr(str(O/'01_Fusion/PADs_R04_SEPARADOS.f3d'))+''';assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(path));assert d.exportManager.execute(d.exportManager.createSTEPExportOptions('''+repr(str(O/'01_Fusion/PADs_R04_SEPARADOS.step'))+'''))
 a.activeViewport.fit();assert a.activeViewport.saveAsImageFile('''+repr(str(O/'01_Fusion/PADs_R04_SEPARADOS.png'))+''',1600,1100)
 print(json.dumps({'document':name,'rows':rows,'archive':path,'simulation_solved':False}))
'''
r=bridge.script(code,False);(O/'02_STL_PAD/exportacao_Fusion.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');persist('r04_pad_export.json',r);print(json.dumps({'doc':r.get('document'),'pads':len(r.get('rows',[])),'archive':r.get('archive')}))
