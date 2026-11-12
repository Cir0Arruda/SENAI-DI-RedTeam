"""R07 - Camadas reais do G-code (Orca K1 Max, 1:1) da peça SUPERIOR com o contorno do esqueleto e das zonas.

Prova visual de que o esqueleto (almas 100%) e as zonas de giroide ficam só DENTRO da peça. Não é FEA.
Reaproveita o leitor de G-code do r06_camadas.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r06_camadas as c6  # noqa: E402

O = Path(__file__).resolve().parents[1]
ZON = O / '04_Modificadores' / 'R07'
DEST = O / '06_Engenharia' / 'R07'
ZCOL = {'SOLIDO_100': '#1f5fbf', 'COLAR_55': '#7a3fc2', 'ROSA_35': '#e0569b', 'PES_35': '#f29ad0', 'AMARELO_20': '#e8b400'}
NOME = {'SOLIDO_100': 'esqueleto 100%', 'COLAR_55': 'colar 55%', 'ROSA_35': 'rosa 35%', 'PES_35': 'pés 35%', 'AMARELO_20': 'amarelo 20%'}
# variantes: (peça, G-code, pasta dos modificadores, saída, camadas, rótulo do 100%)
VAR = {
    'SUPERIOR': ('SUPERIOR', 'Resultado_SUPERIOR_B25', ZON, 'CAMADAS_R07_SUPERIOR', (8, 40, 74), None),
    'SUPERIOR_SEM': ('SUPERIOR', 'COMPARATIVO/Resultado_R07_SEM_SUPERIOR', ZON / 'SEM_ALMAS_SUPERIOR', 'CAMADAS_R07_SUPERIOR_SEM', (8, 40, 74), 'tubos 100%'),
    'INFERIOR': ('INFERIOR_DIR', 'Resultado_INFERIOR_DIR_B20', ZON, 'CAMADAS_R07_INFERIOR', (20, 52, 70), None),
}


def main(var='SUPERIOR'):
    key, res, zdir, outname, layers, lab100 = VAR[var]
    seg = c6.read_layers(O / '05_Orca' / 'R07' / res / 'plate_1.gcode', layers)
    part = trimesh.load(c6.SRC / f'{key}_BASE_20.stl', force='mesh')
    zones = {k: trimesh.load(zdir / f'{key}_MOD_{k}.stl', force='mesh') for k in ZCOL if (zdir / f'{key}_MOD_{k}.stl').exists()}
    nome = dict(NOME, **({'SOLIDO_100': lab100} if lab100 else {}))
    z0 = part.bounds[0, 2]
    fig, axes = plt.subplots(1, len(seg), figsize=(6 * len(seg), 5.4), layout='constrained')
    rec = {}
    for ax, zl in zip(np.atleast_1d(axes), sorted(seg)):
        s = seg[zl]
        walls = np.array([p for sgm in s['wall'] for p in sgm])
        zw = z0 + zl - 0.1
        sec = part.section(plane_origin=(0, 0, zw), plane_normal=(0, 0, 1))
        pb = sec.bounds[:, :2]
        off = (walls.min(0) + walls.max(0)) / 2 - (pb[0] + pb[1]) / 2
        for cat, col, lw in [('skin', '#c9d1d8', .3), ('infill', '#3c4650', .35), ('wall', '#101820', .55)]:
            if s[cat]:
                ax.add_collection(LineCollection(s[cat], colors=col, linewidths=lw))
        present = []
        for k, m in zones.items():
            zs = m.section(plane_origin=(0, 0, zw), plane_normal=(0, 0, 1))
            if zs is None:
                continue
            present.append(nome[k])
            for e in zs.discrete:
                ax.plot(e[:, 0] + off[0], e[:, 1] + off[1], color=ZCOL[k], lw=1.3)
        ax.autoscale(); ax.set_aspect('equal'); ax.axis('off')
        ax.set_title(f'camada Z = {zl:.1f} mm\n{", ".join(present) or "só base"}', fontsize=10)
        rec[f'{zl:.2f}'] = {'zones': present, 'segments': {c: len(v) for c, v in s.items()}}
    out = DEST / f'{outname}.png'
    fig.savefig(out, dpi=150, facecolor='white'); plt.close(fig)
    jf = DEST / 'camadas_r07.json'
    allr = json.loads(jf.read_text(encoding='utf-8')) if jf.exists() else {}
    allr[var] = rec
    jf.write_text(json.dumps(allr, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out, json.dumps(rec, ensure_ascii=False))


if __name__ == '__main__':
    for v in (sys.argv[1:] or ['SUPERIOR']):
        main(v)
