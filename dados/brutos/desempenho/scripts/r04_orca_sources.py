from pathlib import Path
import httpx,json
D=Path.cwd().parent/'desempenho';S=D/'07_Referencias/Orca_fonte';S.mkdir(exist_ok=True)
for name,path in [('bbs_3mf.cpp','src/libslic3r/Format/bbs_3mf.cpp'),('PrintConfig.cpp','src/libslic3r/PrintConfig.cpp')]:
 r=httpx.get('https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/'+path,timeout=40);r.raise_for_status();(S/name).write_text(r.text,encoding='utf-8')
print('Orca_sources_cached')
profile=Path('C:/Program Files/OrcaSlicer/resources/profiles')
print([str(p.relative_to(profile)) for p in profile.rglob('*.json') if ('PA6-CF' in p.name or ('Generic TPU' in p.name and 'BBL' in p.name) or 'Bambu Lab X1 0.4' in p.name)][:24])
