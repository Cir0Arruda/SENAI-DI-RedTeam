from pathlib import Path
import httpx,json
O=Path.cwd().parent/'desempenho';url='https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/resources/profiles/Creality/machine/Creality K1 Max 0.4 nozzle.json';r=httpx.get(url,timeout=25);print({'status':r.status_code})
if r.status_code==200:
 p=O/'07_Referencias/perfis_originais/Creality K1 Max 0.4 nozzle.json';p.write_bytes(r.content);d=r.json();print({k:d.get(k) for k in ['name','inherits','include','printer_model','printable_area','printable_height','machine_start_gcode']})
