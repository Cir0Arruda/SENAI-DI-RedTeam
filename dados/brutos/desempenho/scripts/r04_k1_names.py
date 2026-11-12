from pathlib import Path
import httpx,json
O=Path.cwd().parent/'desempenho';u='https://api.github.com/repos/OrcaSlicer/OrcaSlicer/contents/resources/profiles/Creality/machine';r=httpx.get(u,timeout=25);print({'status':r.status_code});d=r.json()
if isinstance(d,list):
 names=[{'name':x['name'],'url':x['download_url']} for x in d if 'K1' in x['name']];print(json.dumps(names,ensure_ascii=True));(O/'07_Referencias/K1_perfis.json').write_text(json.dumps(names,indent=2),encoding='utf-8')
# Preserve interrupted test as obsolete instead of leaving an active job marker.
for p in (O/'05_Orca').glob('Resultado_*_X1_REF/status.json'):
 q=json.loads(p.read_text());
 if q['status']=='running':q['status']='cancelled_reference_changed_by_user';q['reason']='User authorized larger printer to retain source orientation and scale1';p.write_text(json.dumps(q,indent=2),encoding='utf-8')
