"""R06 - Projetos Orca (K1 Max, escala 1:1) com as zonas INTERNAS e fatiamento pela CLI.

Corrige o R04: modificadores agora ficam inteiramente dentro da peça (0 cm³ fora do contorno)
e os três (amarelo, azul, rosa) estão presentes em cada peça. Perfil de impressora/processo
herdado do projeto K1 Max já importado pelo usuário (sem envio à impressora).
Uso (cwd = FUSION): python ../desempenho/scripts/r06_orca.py
"""
from __future__ import annotations
import datetime, json, subprocess, sys, zipfile
from pathlib import Path
import numpy as np
import trimesh

DESK = Path(__file__).resolve().parents[2]
O = DESK / 'desempenho'
sys.path.insert(0, str(DESK / 'FUSION' / 'fusion_mcp_compact'))
import r04_orca_project as proj           # noqa: E402  (reaproveita o gerador de 3MF do R04)
import r04_extract_slicer as ext          # noqa: E402

ORCA = 'C:/Program Files/OrcaSlicer/orca-slicer.exe'
SRC = O / '04_Modificadores' / 'origem'
ZON = O / '04_Modificadores' / 'R06'
OUT = O / '05_Orca' / 'R06'
OUT.mkdir(parents=True, exist_ok=True)
K1 = json.loads(zipfile.ZipFile(O / '05_Orca' / 'GARRA_SUPERIOR_TPMSD_K1MAX_ESCALA_REAL.3mf')
                .read('Metadata/project_settings.config'))
K1.update({'sparse_infill_density': '20%', 'sparse_infill_pattern': 'tpmsd', 'wall_loops': '5',
           'print_settings_id': 'SAMI_R06_TPMSD20_30_50_70_5paredes_ZONAS_INTERNAS'})
proj.settings = lambda tpu=False: json.loads(json.dumps(K1))   # perfil K1 Max do usuário

PARTS = {'SUPERIOR': 'SUPERIOR_BASE_20.stl', 'INFERIOR_ESQ': 'INFERIOR_ESQ_BASE_20.stl',
         'INFERIOR_DIR': 'INFERIOR_DIR_BASE_20.stl'}
ZONES = [('AMARELO', 30), ('AZUL', 50), ('ROSA', 70)]


def write_local(src: Path, dst: Path, shift: np.ndarray) -> Path:
    m = trimesh.load(src, force='mesh')
    m.apply_translation(-shift)
    m.export(dst)
    return dst


def build(key: str) -> Path:
    part = trimesh.load(SRC / PARTS[key], force='mesh')
    lo, hi = part.bounds
    shift = np.array([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2]])  # centro XY, base em Z=0
    tmp = OUT / 'stl_local'
    tmp.mkdir(exist_ok=True)
    parts = [{'file': write_local(SRC / PARTS[key], tmp / f'{key}_PECA.stl', shift),
              'name': f'GARRA_{key}_EXTERIOR_ORIGINAL_BASE20'}]
    for color, pct in ZONES:
        f = write_local(ZON / f'{key}_MOD_{color}_{pct}.stl', tmp / f'{key}_MOD_{color}_{pct}.stl', shift)
        parts.append({'file': f, 'name': f'MOD_{color}_{pct}_INTERNO', 'modifier': True, 'percent': pct})
    dst = OUT / f'GARRA_{key}_R06_ZONAS_INTERNAS_K1MAX.3mf'
    proj.build(dst, [{'name': f'GARRA_{key}_R06', 'xy': (150, 150), 'parts': parts}], False)
    return dst


def slice_(key: str, inp: Path) -> dict:
    folder = OUT / f'Resultado_{key}'
    folder.mkdir(exist_ok=True)
    out = folder / f'{key}_R06_FATIADO.3mf'
    state = {'case': key, 'start_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'input': str(inp), 'printer': 'Creality K1 Max 300 mm, bico 0,4 mm', 'scale': 1,
             'sent_to_printer': False}
    args = [ORCA, str(inp), '--slice', '0', '--outputdir', str(folder), '--export-3mf', out.name]
    with (folder / 'Orca_fatiamento.log').open('wb') as f:
        r = subprocess.run(args, stdout=f, stderr=subprocess.STDOUT, timeout=1800, cwd=folder)
    state.update({'returncode': r.returncode, 'ok': r.returncode == 0 and out.exists(),
                  'end_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat()})
    (folder / 'status.json').write_text(json.dumps(state, indent=2), encoding='utf-8')
    if state['ok']:
        data = ext.extract(folder)
        state['mass_g'] = data['category_mass_g']
        state['orca_total_g'] = data['Orca_summary']['total_filament_mass_g']
        state['time_s'] = data['Orca_summary']['prediction_s']
    print(json.dumps(state, ensure_ascii=True), flush=True)
    return state


if __name__ == '__main__':
    keys = sys.argv[1:] or list(PARTS)
    res = {k: slice_(k, build(k)) for k in keys}
    (OUT / 'r06_fatiamento_resumo.json').write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
