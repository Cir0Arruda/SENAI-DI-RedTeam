"""Read-only API diagnostics. No repeated precheck and no solver submission."""
from pathlib import Path
import json
from server import bridge,persist
O=Path(__file__).resolve().parents[2]/'desempenho/06_Engenharia/R05_CONFERENCIA_ORCA';O.mkdir(exist_ok=True)
out={}
for cls,pattern in [('adsk.sim.Study','material|isValid|mesh|valid|result|studyType'),('adsk.sim.MaterialAssignment','material|valid|error'),('adsk.sim.MaterialAssignments','material|valid|error')]:
 r=bridge.call('fusion_mcp_read',{'queryType':'apiDocumentation','apiCategory':'member','filter':cls,'searchPattern':pattern});out[cls]=r
(O/'FUSION_API_DIAGNOSTICO_LEITURA.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:[x.get('name') for x in v.get('members',[])] for k,v in out.items()}))
