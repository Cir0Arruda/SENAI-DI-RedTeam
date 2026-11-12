"""R07 - Variantes de comparação para a decisão COM x SEM esqueleto (fatiamento real, K1 Max, 1:1).

Parte dos 3MF R07 (mesmo perfil do usuário, 5 paredes, exterior original) e gera:
  UNI_<PADRAO><PCT>  preenchimento UNIFORME na peça inteira (sem esqueleto, sem zonas):
                     todos os modificadores recebem o mesmo padrão e a mesma densidade da peça.
                     giroide 30/35/40 (pedido do usuário), 3D honeycomb 30 (projeto atual citado no documento)
                     e TPMS-D 40 (proposta citada no documento).
  R07_SEM            superior com as mesmas zonas R07, mas sem as almas (SUPERIOR_SEM_MOD_*: só os tubos ficam 100%).
Inferior direita = espelho da esquerda (as fatias anteriores diferiram < 0,02 g); só a esquerda é fatiada.
Nada é enviado à impressora.
Uso: python r07_comparativo.py [CASO ...]   (sem argumentos: todos)
"""
from __future__ import annotations
import json, re, sys, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r06_orca_patch as P  # noqa: E402
import r07_orca as R  # noqa: E402

OUT = R.OUT / 'COMPARATIVO'
OUT.mkdir(exist_ok=True)
SRC = {'SUPERIOR': R.OUT / 'GARRA_SUPERIOR_R07_ESQUELETO_GIROIDE25_K1MAX.3mf',
       'INFERIOR_ESQ': R.OUT / 'GARRA_INFERIOR_ESQ_R07_ESQUELETO_GIROIDE20_K1MAX.3mf'}
UNI = [('gyroid', 30), ('gyroid', 35), ('gyroid', 40), ('3dhoneycomb', 30), ('tpmsd', 40), ('gyroid', 15), ('gyroid', 22)]
TAG = {'gyroid': 'GIROIDE', '3dhoneycomb': 'HONEYCOMB3D', 'tpmsd': 'TPMSD'}


def uniform(key: str, pat: str, pct: int) -> Path:
    dst = OUT / f'GARRA_{key}_UNI_{TAG[pat]}{pct}_K1MAX.3mf'
    with zipfile.ZipFile(SRC[key]) as zin, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'Metadata/project_settings.config':
                ps = json.loads(data)
                ps['sparse_infill_pattern'] = pat; ps['sparse_infill_density'] = f'{pct}%'
                ps['print_settings_id'] = f'SAMI_UNIFORME_{TAG[pat]}{pct}_5paredes'
                data = json.dumps(ps, indent=4, ensure_ascii=False)
            elif item.filename == 'Metadata/model_settings.config':
                cfg = data.decode('utf-8')
                cfg = re.sub(r'(key="sparse_infill_density" value=")\d+%', rf'\g<1>{pct}%', cfg)
                cfg = re.sub(r'(key="sparse_infill_pattern" value=")[a-z0-9]+', rf'\g<1>{pat}', cfg)
                data = cfg
            zout.writestr(item, data)
    return dst


def r07_sem_superior() -> Path:
    """Mesmo build do r07_orca (base 25%), mas com os modificadores SEM almas e saída separada."""
    d = R.ZON / 'SEM_ALMAS_SUPERIOR'; d.mkdir(exist_ok=True)
    import shutil
    for f in R.ZON.glob('SUPERIOR_SEM_MOD_*.stl'):
        shutil.copy(f, d / f.name.replace('_SEM_MOD_', '_MOD_'))
    keep = R.OUT / 'GARRA_SUPERIOR_R07_ESQUELETO_GIROIDE25_K1MAX.3mf'
    bak = keep.with_suffix('.bak')
    shutil.copy(keep, bak)                      # build() grava no mesmo nome: preserva o COM
    P.ZON = d
    try:
        tmp = R.build('SUPERIOR', 25)
        dst = OUT / 'GARRA_SUPERIOR_R07_SEM_ESQUELETO_GIROIDE25_K1MAX.3mf'
        shutil.move(tmp, dst)
    finally:
        shutil.move(bak, keep); P.ZON = R.ZON
    return dst


def cases():
    c = {'R07_SEM_SUPERIOR': r07_sem_superior}
    for pat, pct in UNI:
        for key in SRC:
            c[f'UNI_{TAG[pat]}{pct}_{key}'] = (lambda k=key, p=pat, q=pct: uniform(k, p, q))
    return c


if __name__ == '__main__':
    P.OUT = OUT
    allc = cases()
    want = sys.argv[1:] or list(allc)
    resf = OUT / 'r07_comparativo_fatiamento.json'
    res = json.loads(resf.read_text(encoding='utf-8')) if resf.exists() else {}
    for k in want:
        if k in res and res[k].get('ok'):
            continue
        inp = allc[k]()
        res[k] = P.slice_(k, inp)
        resf.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
        print(k, res[k].get('ok'), res[k].get('mass_g'), flush=True)
