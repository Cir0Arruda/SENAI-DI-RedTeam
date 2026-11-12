"""R06 - Variantes de preenchimento uniforme do corpo superior para a otimização multiobjetivo.

Parte do projeto R06 (perfil K1 Max do usuário, 5 perímetros, TPMS-D) e só troca a densidade:
base e os três modificadores recebem o mesmo valor => preenchimento uniforme X%.
Fatiamento local pela CLI do Orca; nada é enviado à impressora.
Uso: python r06_orca_variantes.py [20 30 50 70]
"""
from __future__ import annotations
import json, re, sys, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r06_orca_patch as p  # noqa: E402

SRC = p.OUT / 'GARRA_SUPERIOR_R06_ZONAS_INTERNAS_K1MAX.3mf'


def variant(pct: int) -> Path:
    dst = p.OUT / f'GARRA_SUPERIOR_UNIFORME_{pct}_K1MAX.3mf'
    zin = zipfile.ZipFile(SRC)
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'Metadata/project_settings.config':
                ps = json.loads(data)
                ps['sparse_infill_density'] = f'{pct}%'
                data = json.dumps(ps, indent=4, ensure_ascii=False)
            elif item.filename == 'Metadata/model_settings.config':
                data = re.sub(r'(key="sparse_infill_density" value=")\d+%', rf'\g<1>{pct}%', data.decode('utf-8'))
            zout.writestr(item, data)
    return dst


if __name__ == '__main__':
    res = {}
    for pct in [int(x) for x in (sys.argv[1:] or ['20', '30', '50', '70'])]:
        key = f'SUPERIOR_UNIFORME_{pct}'
        inp = variant(pct)
        folder = p.OUT / f'Resultado_{key}'
        st = p.slice_.__wrapped__(key, inp) if hasattr(p.slice_, '__wrapped__') else p.slice_(key, inp)
        res[key] = st
        (p.OUT / 'r06_variantes_resumo.json').write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
