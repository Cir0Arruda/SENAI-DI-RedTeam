from pathlib import Path
import httpx,json
O=Path.cwd().parent/'desempenho';P=O/'07_Referencias/K1Max_perfis';seen={}
def load(name):
 if name in seen:return seen[name]
 path=P/(name+'.json')
 if not path.exists():
  r=httpx.get('https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/resources/profiles/Creality/machine/'+name+'.json',timeout=30);r.raise_for_status();path.write_bytes(r.content)
 d=json.loads(path.read_text(encoding='utf-8'));q=load(d['inherits']).copy() if d.get('inherits') else {};q.update(d);seen[name]=q;return q
q=load('Creality K1 Max (0.4 nozzle)');(P/'MAQUINA_K1MAX_RESOLVIDA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8');print({'machine':q['name'],'bed':q['printable_area'],'flavor':q['gcode_flavor'],'parents':list(seen)})
r=httpx.get('https://api.github.com/repos/OrcaSlicer/OrcaSlicer/contents/resources/profiles/Creality/process',timeout=30);r.raise_for_status();names=[{'name':x['name'],'url':x['download_url']} for x in r.json() if 'K1 Max' in x['name'] and ('Standard' in x['name'] or '0.20' in x['name'])];print(names[:8]);(P/'processos_encontrados.json').write_text(json.dumps(names,indent=2))
