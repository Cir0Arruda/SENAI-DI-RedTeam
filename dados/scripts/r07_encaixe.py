"""R07 - Corte vertical da garra MONTADA (superior + inferior direita) no plano dos anéis da asa direita.

Mostra o esqueleto (almas/tubos 100%) do superior descendo até a base da asa e o da inferior subindo até o
anel do encaixe. Geometria dos modificadores do Orca (os mesmos que geraram os G-codes); não é FEA.
Saída: 06_Engenharia/R07/ENCAIXE_R07_{COM,SEM}.png
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r07_camadas as rc  # noqa: E402

SRC, ZON, DEST = rc.c6.SRC, rc.ZON, rc.DEST
X_CUT = -478.3   # plano x dos centros dos anéis da asa direita (bc_geom: ressaltos em x = -478,3)


def polys(mesh, x):
    s = mesh.section(plane_origin=(x, 0, 0), plane_normal=(1, 0, 0))
    if s is None:
        return []
    return [e[:, [1, 2]] for e in s.discrete]


def draw(ax, mesh, x, fc, ec, lw=.8, alpha=1, z=1):
    for p in polys(mesh, x):
        ax.add_patch(Polygon(p, closed=True, fc=fc, ec=ec, lw=lw, alpha=alpha, zorder=z))


def main(var='COM'):
    sup = trimesh.load(SRC / 'SUPERIOR_BASE_20.stl', force='mesh')
    inf = trimesh.load(SRC / 'INFERIOR_DIR_BASE_20.stl', force='mesh')
    dirs = {'SUPERIOR': ZON / 'SEM_ALMAS_SUPERIOR', 'INFERIOR_DIR': ZON / 'SEM_ALMAS'} if var == 'SEM' else {'SUPERIOR': ZON, 'INFERIOR_DIR': ZON}
    fig, ax = plt.subplots(figsize=(10, 5.2), layout='constrained')
    PFILL = {'superior': '#e8eaf3', 'inferior direita': '#f5efe3'}
    for m, lab in [(sup, 'superior'), (inf, 'inferior direita')]:
        draw(ax, m, X_CUT, PFILL[lab], 'none', z=1)
    order = ['AMARELO_20', 'PES_35', 'ROSA_35', 'COLAR_55', 'SOLIDO_100']
    lab100 = 'tubos 100%' if var == 'SEM' else 'esqueleto 100%'
    seen = {}
    for k in order:
        for key, d in dirs.items():
            f = d / f'{key}_MOD_{k}.stl'
            if f.exists():
                m = trimesh.load(f, force='mesh')
                if polys(m, X_CUT):
                    draw(ax, m, X_CUT, rc.ZCOL[k], rc.ZCOL[k], lw=.5, alpha=.9 if k == 'SOLIDO_100' else .4, z=3 if k == 'SOLIDO_100' else 2)
                    seen[k] = lab100 if k == 'SOLIDO_100' else rc.NOME[k]
    for m, ec in [(sup, '#2b2f6b'), (inf, '#6b4f1d')]:
        for p_ in polys(m, X_CUT):
            ax.add_patch(Polygon(p_, closed=True, fc='none', ec=ec, lw=1.3, zorder=5))
    zj = sup.bounds[0, 2]
    ax.axhline(zj, color='#c2410c', lw=1, ls='--', zorder=6)
    ax.autoscale(); ax.set_aspect('equal')
    x1 = ax.get_xlim()[1]
    ax.text(x1, zj + 1.5, 'encaixe', color='#9a3412', fontsize=9, ha='right', va='bottom')
    ax.text(x1, 300, 'superior', color='#2b2f6b', fontsize=10, ha='right', fontweight='bold')
    ax.text(x1, 226, 'inferior direita', color='#6b4f1d', fontsize=10, ha='right', fontweight='bold')
    ax.set_xlabel('y (mm)'); ax.set_ylabel('z (mm)')
    for s_ in ('top', 'right'):
        ax.spines[s_].set_visible(False)
    ks = [k for k in order[::-1] if k in seen]
    hs = [plt.Rectangle((0, 0), 1, 1, fc=rc.ZCOL[k], alpha=.9 if k == 'SOLIDO_100' else .5) for k in ks]
    ax.legend(hs, [seen[k] for k in ks], loc='upper left', frameon=False, fontsize=9, ncol=len(ks), bbox_to_anchor=(0, 1.02))
    out = DEST / f'ENCAIXE_R07_{var}.png'
    fig.savefig(out, dpi=150, facecolor='white'); plt.close(fig)
    print(out, seen)


if __name__ == '__main__':
    for v in (sys.argv[1:] or ['COM', 'SEM']):
        main(v)
