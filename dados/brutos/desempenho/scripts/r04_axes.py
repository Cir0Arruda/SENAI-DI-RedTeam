import json
from server import bridge,persist
r=bridge.script('''import adsk.core,adsk.fusion,json

def run(_context: str):
 a=adsk.core.Application.get();d=adsk.fusion.Design.cast(a.activeDocument.products.itemByProductType('DesignProductType'));rows=[]
 for o in d.rootComponent.allOccurrences:
  if o.component.name not in ('Suporte_Ventosas_S','Corpo Supor'):continue
  keys={}
  for f in o.component.bRepBodies.item(0).faces:
   g=f.geometry
   if g.objectType!='adsk::core::Cylinder' or abs(g.axis.z)<.999:continue
   if not (.3<g.radius<8):continue
   pt=g.origin.copy();pt.transformBy(o.transform2);key=(round(pt.x,3),round(pt.y,3));keys.setdefault(key,[]).append(round(g.radius,4))
  rows.append({'path':o.fullPathName,'axes':[{'xy_world_cm':list(k),'radii_cm':sorted(set(v))} for k,v in keys.items()]})
 print(json.dumps(rows))
''',True);persist('r04_axes.json',r);print(json.dumps(r,ensure_ascii=True))
for cls,pat in [('adsk.fusion.STLExportOptions','meshRefinement|surfaceDeviation|normalDeviation|maximumEdgeLength'),('adsk.fusion.TemporaryBRepManager','createBox|booleanOperation|createCylinderOrCone'),('adsk.fusion.Occurrence','isLightBulbOn')]:
 r=bridge.call('fusion_mcp_read',{'queryType':'apiDocumentation','apiCategory':'member','filter':cls,'searchPattern':pat});persist('r04_docs_'+cls.split('.')[-1]+'.json',r)
print('docs_cached')
