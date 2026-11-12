import zipfile,json,httpx
from pathlib import Path
O=Path.cwd().parent/'desempenho'
with zipfile.ZipFile(O/'05_Orca/ORCA_ANTERIOR_MONTAGEM_ESCALADA.3mf') as z:
 text=z.read('Metadata/model_settings.config').decode();(O/'07_Referencias/model_settings_exemplo.config').write_text(text);print(text[:2600])
for name,url in [('Model.cpp','https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/src/libslic3r/Model.cpp'),('OrcaSlicer.cpp','https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/src/OrcaSlicer.cpp')]:
 r=httpx.get(url,timeout=40);r.raise_for_status();(O/'07_Referencias/Orca_fonte'/name).write_text(r.text,encoding='utf-8')
print('source_members_saved')
