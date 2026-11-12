"""Audit unchanged printable envelopes and nonprinting 3MF modifiers."""
from pathlib import Path
import json,zipfile,xml.etree.ElementTree as ET,numpy as np,hashlib
from r04_mesh_package import read,clean
O=Path(__file__).resolve().parents[2]/'desempenho'
rows=[]
for key in ['SUPERIOR','INFERIOR_ESQ','INFERIOR_DIR']:
 rec=json.loads((O/f'04_Modificadores/{key}_regioes.json').read_text(encoding='utf-8'))
 val=json.loads((O/f'04_Modificadores/{key}_validacao_STL.json').read_text(encoding='utf-8'))[0]
 raw=next(r for r in rec['regions'] if r['label']=='BASE')['stl_raw']
 expected,_=clean(read(raw),rec['scope']['source_volume_cm3'])
 expected-=np.array(val['shift_world_mm']);public=read(O/val['file'])
 assert expected.shape==public.shape
 err=float(np.max(np.abs(expected-public)));assert err<.0001,(key,err)
 files=[O/f'05_Orca/GARRA_{key}_TPMSD_K1MAX_ESCALA_REAL.3mf']
 sliced=O/f'05_Orca/Resultado_{key}_K1MAX/{key}_K1MAX_FATIADO_REFERENCIA.3mf'
 if sliced.exists():files.append(sliced)
 checks=[]
 for file in files:
  with zipfile.ZipFile(file) as z:
   root=ET.fromstring(z.read('Metadata/model_settings.config'))
   parts=[]
   for p in root.findall('./object/part'):
    meta={a.get('key'):a.get('value') for a in p.findall('metadata')}
    parts.append({'subtype':p.get('subtype'),'name':meta.get('name'),'density':meta.get('sparse_infill_density'),'pattern':meta.get('sparse_infill_pattern')})
   normals=[p for p in parts if p['subtype']=='normal_part'];mods=[p for p in parts if p['subtype']=='modifier_part']
   assert len(normals)==1 and len(mods)==3,(file,parts)
   assert sorted(p['density'] for p in mods)==['30%','50%','70%']
   assert all(p['pattern']=='tpmsd' for p in mods)
   cfg=json.loads(z.read('Metadata/project_settings.config'))
   assert cfg['wall_loops']=='5' and cfg['sparse_infill_density']=='20%' and cfg['sparse_infill_pattern']=='tpmsd'
   checks.append({'file':str(file.relative_to(O)),'normal_printed_envelopes':len(normals),'internal_density_modifiers':mods,'wall_loops':5,'base_infill':'20% TPMS-D','modifiers_are_not_printed_bodies':True})
 rows.append({'part':key,'public_STL_vertex_difference_from_native_envelope_mm':err,'exterior_changed':False,'translation_only':True,'scale':1,'source_BRep_volume_cm3':rec['scope']['source_volume_cm3'],'project_checks':checks})
data={'revision':'R04','user_rule':'ALTERACOES EXTERNAS PROIBIDAS; cores somente no preenchimento interno. PAD separado, sem alterar a garra.','status':'passed','scope':'Printable envelope identity and actual Orca modifier classifications; not a mechanical simulation or per-layer containment test.','parts':rows}
(O/'06_Engenharia/AUDITORIA_EXTERIOR_INALTERADO.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'passed','parts':len(rows),'external_geometry_changed':False,'modifier_subtype':'modifier_part','max_vertex_difference_mm':max(x['public_STL_vertex_difference_from_native_envelope_mm'] for x in rows)}))
