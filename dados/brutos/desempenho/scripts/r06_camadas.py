"""R06 - Camadas reais do G-code do Orca com contorno das zonas internas sobreposto.

Prova visual: o preenchimento varia só DENTRO da peça (rosa 70 / azul 50 / amarelo 30 / base 20),
as paredes externas (5 perímetros) seguem o contorno original. Não é resultado de FEA.
Alinhamento: translação XY que casa o bbox das paredes da camada com o bbox da seção da peça.
Uso: python r06_camadas.py [SUPERIOR INFERIOR_ESQ INFERIOR_DIR]
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

O = Path(__file__).resolve().parents[1]
ZON = O / '04_Modificadores' / 'R06'
SRC = O / '04_Modificadores' / 'origem'
RES = O / '05_Orca' / 'R06'
DEST = O / '06_Engenharia' / 'R06'
DEST.mkdir(parents=True, exist_ok=True)
LAYERS = {'SUPERIOR': [6, 22, 55], 'INFERIOR_ESQ': [20, 52, 68], 'INFERIOR_DIR': [20, 52, 68]}
ZCOL = {'ROSA70': '#e0569b', 'AZUL50': '#2f7fe0', 'AMARELO30': '#e8b400'}


def read_layers(gcode: Path, targets):
    zs = []
    with gcode.open(encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith(';Z:'):
                zs.append(float(line[3:]))
    pick = {min(zs, key=lambda z: abs(z - t)) for t in targets}
    seg = {z: {'wall': [], 'infill': [], 'skin': []} for z in pick}
    cur = None; role = ''; x = y = None
    with gcode.open(encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith(';Z:'):
                z = float(line[3:]); cur = z if z in seg else None; x = y = None; continue
            if cur is None:
                continue
            if line.startswith((';TYPE:', '; FEATURE:')):
                role = line.split(':', 1)[1].strip().lower(); continue
            if not line.startswith(('G0 ', 'G1 ', 'G2 ', 'G3 ')):
                continue
            vals = {t[0]: float(t[1:]) for t in line.split(';', 1)[0].split()[1:] if t[0] in 'XYE'}
            xx = vals.get('X', x); yy = vals.get('Y', y)
            if vals.get('E', 0) > 0 and None not in (x, y, xx, yy) and 'support' not in role and role not in ('brim', 'skirt', 'custom', ''):
                cat = 'wall' if 'wall' in role or 'perimeter' in role else ('infill' if 'sparse' in role else 'skin')
                seg[cur][cat].append([(x, y), (xx, yy)])
            x, y = xx, yy
    return seg


def main(keys):
    rep = {}
    for key in keys:
        folder = RES / f'Resultado_{key}'
        seg = read_layers(folder / 'plate_1.gcode', LAYERS[key])
        part = trimesh.load(SRC / f'{key}_BASE_20.stl', force='mesh')
        zones = {k: trimesh.load(ZON / f'{key}_MOD_{k[:-2]}_{k[-2:]}.stl', force='mesh') for k in ZCOL}
        z0 = part.bounds[0, 2]
        fig, axes = plt.subplots(1, len(seg), figsize=(6 * len(seg), 5.6), layout='constrained')
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
                present.append(k)
                for e in zs.discrete:
                    ax.plot(e[:, 0] + off[0], e[:, 1] + off[1], color=ZCOL[k], lw=1.4)
            ax.autoscale(); ax.set_aspect('equal'); ax.grid(alpha=.12)
            ax.set_title(f'{key} | camada Z = {zl:.2f} mm\nzonas na camada: {", ".join(present) or "só base 20%"}', fontsize=10)
            ax.set_xlabel('X (mm)'); ax.set_ylabel('Y (mm)')
            rec[f'{zl:.2f}'] = {'zones': present, 'segments': {c: len(v) for c, v in s.items()},
                               'align_offset_xy_mm': off.round(2).tolist()}
        fig.suptitle('Trajetórias REAIS do Orca (K1 Max, 1:1) + contorno das zonas internas R06\n'
                     'rosa 70% | azul 50% | amarelo 30% | restante 20% TPMS-D — paredes externas inalteradas (5 perímetros)', fontsize=11)
        out = DEST / f'CAMADAS_R06_{key}.png'
        fig.savefig(out, dpi=150); plt.close(fig)
        rep[key] = {'figure': str(out), 'layers': rec}
        print(key, json.dumps(rec, ensure_ascii=True))
    (DEST / 'camadas_r06.json').write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main(sys.argv[1:] or ['INFERIOR_ESQ', 'INFERIOR_DIR'])
