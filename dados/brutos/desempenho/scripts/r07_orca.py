"""R07 - Projetos Orca K1 Max com o ESQUELETO INTERNO (almas sólidas) e giroide, fatiados pela CLI.

Parte dos mesmos 3MF K1 Max do usuário (exterior original, perfil K1 Max, 5 paredes) e troca:
  * preenchimento global: giroide BASE% (padrão 20%)
  * modificadores R07 (todos internos): SOLIDO 100% (almas de 3 mm + tubos dos furos), COLAR 55%,
    ROSA 35% (+ bases das ventosas nas inferiores), AMARELO 20%.
Nada é enviado à impressora. Uso: python r07_orca.py [--base 20] [SUPERIOR INFERIOR_ESQ INFERIOR_DIR]
"""
from __future__ import annotations
import json, re, sys, zipfile
from pathlib import Path
import trimesh
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r06_orca_patch as P  # noqa: E402

O = P.O
ZON = O / '04_Modificadores' / 'R07'
OUT = O / '05_Orca' / 'R07'
OUT.mkdir(parents=True, exist_ok=True)
P.ZON = ZON
P.OUT = OUT
ZSETS = {'SUPERIOR': [('SOLIDO', 100), ('COLAR', 55), ('ROSA', 35), ('AMARELO', 20)],
         'INFERIOR_ESQ': [('AMARELO', 20), ('SOLIDO', 100), ('ROSAPES', 35)],   # ordem = partes 2,3,4 do 3MF original
         'INFERIOR_DIR': [('AMARELO', 20), ('SOLIDO', 100), ('ROSAPES', 35)]}


def prepare_lower(key):
    ZON = P.ZON
    a = trimesh.load(ZON / f'{key}_MOD_ROSA_35.stl', force='mesh'); b = trimesh.load(ZON / f'{key}_MOD_PES_35.stl', force='mesh')
    trimesh.util.concatenate([a, b]).export(ZON / f'{key}_MOD_ROSAPES_35.stl')  # zonas disjuntas, mesma densidade


def build(key, base):
    if key != 'SUPERIOR':
        prepare_lower(key)
    P.ZONES = ZSETS[key]
    src = P.patch(key)                      # gera GARRA_<key>_R06_ZONAS_INTERNAS... dentro de OUT
    dst = OUT / f'GARRA_{key}_R07_ESQUELETO_GIROIDE{base}_K1MAX.3mf'
    zin = zipfile.ZipFile(src)  # fechado antes de apagar
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            n = item.filename; data = zin.read(n)
            if n == 'Metadata/project_settings.config':
                ps = json.loads(data)
                ps['sparse_infill_pattern'] = 'gyroid'; ps['sparse_infill_density'] = f'{base}%'
                ps['print_settings_id'] = f'SAMI_R07_ESQUELETO_GIROIDE{base}_5paredes'
                if ps['printer_settings_id'] not in ps.get('print_compatible_printers', []):
                    ps['print_compatible_printers'] = ps.get('print_compatible_printers', []) + [ps['printer_settings_id']]
                data = json.dumps(ps, indent=4, ensure_ascii=False)
            elif n == 'Metadata/model_settings.config':
                cfg = data.decode('utf-8').replace('tpmsd', 'gyroid').replace('R06', 'R07')
                # densidade do objeto (global da peça) = base
                cfg = re.sub(r'(<object id="\d+"[^>]*>.*?key="sparse_infill_density" value=")\d+%', rf'\g<1>{base}%', cfg, count=1, flags=re.S)
                for pid, (zname, pct) in enumerate(ZSETS[key], start=2):
                    blk = re.search(rf'<part id="{pid}" subtype="modifier_part">.*?</part>', cfg, re.S).group(0)
                    nb = re.sub(r'(key="sparse_infill_density" value=")\d+%', rf'\g<1>{pct}%', blk)
                    nb = re.sub(r'(key="name" value=")[^"]+', rf'\g<1>MOD_{zname}_{pct}_INTERNO_R07', nb)
                    cfg = cfg.replace(blk, nb)
                data = cfg
            zout.writestr(item, data)
    zin.close(); src.unlink()
    return dst


if __name__ == '__main__':
    args = sys.argv[1:]; base = 20
    if '--base' in args:
        i = args.index('--base'); base = int(args[i + 1]); del args[i:i + 2]
    sem = '--sem' in args
    args = [a for a in args if a != '--sem']
    keys = args or ['SUPERIOR', 'INFERIOR_ESQ', 'INFERIOR_DIR']
    if sem:  # inferiores sem almas: usa <PECA>_SEM_MOD_* com os mesmos nomes de arquivo
        import shutil
        d = ZON / 'SEM_ALMAS'; d.mkdir(exist_ok=True)
        for k in keys:
            for f in ZON.glob(f'{k}_SEM_MOD_*.stl'):
                shutil.copy(f, d / f.name.replace('_SEM_MOD_', '_MOD_'))
        ZON = d; P.ZON = d
    resf = OUT / f'r07_fatiamento_base{base}.json'
    res = json.loads(resf.read_text(encoding='utf-8')) if resf.exists() else {}
    for k in keys:
        inp = build(k, base)
        res[k] = P.slice_(f'{k}_B{base}', inp)
        resf.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
