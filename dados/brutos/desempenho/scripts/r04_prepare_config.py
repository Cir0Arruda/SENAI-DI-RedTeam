from pathlib import Path
import httpx,json,zipfile,xml.etree.ElementTree as ET
O=Path.cwd().parent/'desempenho';P=O/'07_Referencias/perfis_originais';r=httpx.get('https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/resources/profiles/BBL/filament/fdm_filament_pa.json',timeout=20);r.raise_for_status();(P/'fdm_filament_pa.json').write_bytes(r.content)
with zipfile.ZipFile(O/'05_Orca/ORCA_ANTERIOR_MONTAGEM_ESCALADA.3mf') as z:
 root=ET.fromstring(z.read('3D/3dmodel.model'));print([(x.attrib,x.text) for x in root if x.tag.endswith('metadata')])
p=json.loads((O/'05_Orca/perfil_anterior_resolvido.json').read_text(encoding='utf-8'));print({k:p.get(k) for k in ['nozzle_temperature','filament_extruder_variant','filament_ids','compatible_printers','printable_area','printable_height','curr_bed_type','top_shell_layers','bottom_shell_layers','layer_height']})
