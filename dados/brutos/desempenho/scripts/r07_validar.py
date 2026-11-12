"""R07 - Validação do solver por voxels contra o Fusion (peça superior maciça, PA6-CF isotrópico).

Referência Fusion (2026-11-11, FUSION/preparacao_garra/comparacao_2026-11-11.json): corpo superior maciço,
E = 4430 MPa, nu = 0,39, 355,36 N em -Z nas 4 interfaces, engaste nos 6 furos da flange:
von Mises máx. 3,232 MPa, deslocamento máx. 0,08 mm.
"""
from __future__ import annotations
import json, sys
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__file__))
import r07_vfe as v  # noqa: E402

BC = json.loads(open(r'~/AppData/Local/Temp/claude/1707db6810405f3c/fadd520d-079e-4e12-a806-8e11880c5c52/scratchpad/bc_geom.json').read())
HOLES = np.array([h['o'][:2] for h in BC['holes']]) / 1.0
HOLES = HOLES / 1.0
BOSSES = {'R1': (-478.33, 218.0), 'R2': (-478.33, 348.0), 'L1': (-677.33, 218.0), 'L2': (-677.33, 348.0)}


def holes_xy():
    # bc_geom guarda coordenadas em décimos de mm? conferir escala pela flange (círculo 80 mm em torno do cubo)
    h = HOLES.copy()
    if np.abs(h).max() > 2000:
        h = h / 10
    return h


def fixed_fn_factory(m: v.Model, H):
    hx = holes_xy(); r_h = 4.2; zmax = m.mesh.bounds[1, 2]
    def fixed(X):
        d = np.min(np.linalg.norm(X[:, None, :2] - hx[None], axis=2), axis=1)
        return (d <= r_h + 0.8 * H) & (X[:, 2] >= zmax - 22)
    return fixed


def boss_nodes(X, keys, H, zmin):
    sel = np.zeros(len(X), bool)
    for k in keys:
        c = np.array(BOSSES[k]); r = np.linalg.norm(X[:, :2] - c, axis=1)
        sel |= (r >= 26.7 - 0.5 * H) & (r <= 31.0 + 0.5 * H) & (X[:, 2] <= zmin + 0.6 * H)
    return sel


def load_fn(keys, total_N, H, zmin):
    def f(X, nn):
        out = np.zeros(3 * nn)
        for k in keys:
            s = boss_nodes(X, [k], H, zmin); idx = np.where(s)[0]
            out[3 * idx + 2] -= total_N / len(keys) / len(idx)
        return out
    return f


if __name__ == '__main__':
    H = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
    m = v.Model(v.SRC / 'SUPERIOR_BASE_20.stl', H=H, FINE=H / 4)
    print('furos', holes_xy().round(1).tolist())
    zmin = m.mesh.bounds[0, 2]
    v.C_solid = lambda mat=v.MAT: v.C_iso(4430.0, 0.39)   # isotrópico, igual ao Fusion
    d = v.Design('MACICO', base_phi=1.0)
    lab = m.classify(d)
    print('massa maciça (g)', round(m.mass_g(lab)[0], 1))
    res = m.solve(lab, {'SYM_355': load_fn(list(BOSSES), 355.3596, H, zmin)}, fixed_fn_factory(m, H), tag='validacao')
    r = res['SYM_355']; U = r['U']
    eps, st = m.stresses(U)
    sig, frac = st[1.0]
    VM = v.vm(sig)
    disp = np.linalg.norm(U.reshape(-1, 3), axis=1)
    print('cg info', r['info'], 'iters', r['iters'], 'reação', r['reaction'].round(2))
    print(f'desl. máx {disp.max():.4f} mm | VM máx {VM.max():.3f} MPa | VM p99.9 {np.percentile(VM, 99.9):.3f} | p99 {np.percentile(VM, 99):.3f}')
