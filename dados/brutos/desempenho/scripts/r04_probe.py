import json
from pathlib import Path
from server import bridge,persist
r=bridge.script('''import adsk.core,adsk.fusion,json

def run(_context: str):
 a=adsk.core.Application.get();doc=a.activeDocument;d=adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'));rows=[]
 for o in d.rootComponent.allOccurrences:
  if o.component.name in ('Corpo Supor','Suporte_Ventosas_S') or o.component.name.startswith('PAD95_R02_'):
   rows.append({'path':o.fullPathName,'component':o.component.name,'transform':o.transform2.asArray(),'bbox_min_cm':o.boundingBox.minPoint.asArray(),'bbox_max_cm':o.boundingBox.maxPoint.asArray(),'bodies':[{'name':b.name,'volume_cm3':b.volume,'faces':b.faces.count,'solid':b.isSolid} for b in o.component.bRepBodies]})
 print(json.dumps({'active':doc.name,'documents':[x.name for x in a.documents],'command':a.userInterface.activeCommand,'rows':rows}))
''',True)
persist('r04_live_inventory.json',r);print(json.dumps(r,ensure_ascii=True))
