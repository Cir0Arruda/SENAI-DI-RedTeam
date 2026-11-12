from pathlib import Path
import httpx,json
O=Path.cwd().parent/'desempenho';P=O/'07_Referencias/K1Max_perfis';P.mkdir(exist_ok=True)
base='https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/resources/profiles/Creality/machine/'
for name in ['Creality K1 Max (0.4 nozzle)','Creality K1 Max']:
 r=httpx.get(base+name+'.json',timeout=25);r.raise_for_status();(P/(name+'.json')).write_bytes(r.content);d=r.json();print(name,{k:d.get(k) for k in ['inherits','include','printer_model','printable_area','printable_height','gcode_flavor','nozzle_diameter','machine_start_gcode']})
