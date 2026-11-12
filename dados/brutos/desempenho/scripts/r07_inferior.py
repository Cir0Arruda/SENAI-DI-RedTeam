"""R07 - Esqueleto interno das peças INFERIORES (asas das ventosas). Mesmo método do r07_projeto.

Contorno: a asa é presa à peça superior nos dois ressaltos (anel de apoio no topo + 3 furos cada);
carga -Z nas 4 bases de ventosa (caixa(s) pendurada(s) na asa). Peça DIR; a ESQ é espelhada.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
import trimesh
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r07_vfe as v  # noqa: E402
import r07_projeto as p  # noqa: E402

H = 3.0
PART = 'INFERIOR_DIR'
CACHE = v.OUT / f'fine_{PART}_H{H}.npz'
BOSS = [(-478.33, 218.0), (-478.33, 348.0)]
FEET = [(-536.0, 155.0), (-536.0, 410.0), (-364.0, 155.0), (-364.0, 410.0)]
Z_IF = 267.4


def load_model():
    if CACHE.exists():
        m = v.Model.__new__(v.Model); z = np.load(CACHE)
        m.fine = z['fine']; m.dist = z['dist']; m.lo = z['lo']; m.shape = z['shape']; m.n = int(z['n'])
        m.H = H; m.FINE = H / m.n; m.g = (z['gx'], z['gy'], z['gz'])
        m.mesh = trimesh.load(v.SRC / f'{PART}_BASE_20.stl', force='mesh')
        return m
    m = v.Model(v.SRC / f'{PART}_BASE_20.stl', H=H, FINE=H / 4)
    np.savez_compressed(CACHE, fine=m.fine, dist=m.dist.astype(np.float32), lo=m.lo, shape=m.shape, n=m.n,
                        gx=m.g[0], gy=m.g[1], gz=m.g[2])
    return m


def boss_holes():
    pts = []
    for (cx, cy) in BOSS:
        for ang in ((90, 210, 330) if cy > 283 else (270, 150, 30)):
            a = np.deg2rad(ang); pts.append((cx + 22 * np.cos(a), cy + 22 * np.sin(a)))
    return pts


def fixed_fn(m):
    zmax = m.mesh.bounds[1, 2]; hx = np.array(boss_holes())
    def f(X):
        r = np.min([np.linalg.norm(X[:, :2] - np.array(b), axis=1) for b in BOSS], axis=0)
        top_ring = (r >= 26.7 - 0.5 * H) & (r <= 31.0 + 0.5 * H) & (X[:, 2] >= zmax - 0.6 * H)
        d = np.min(np.linalg.norm(X[:, None, :2] - hx[None], axis=2), axis=1)
        return top_ring | ((d <= 4.2 + 0.8 * H) & (X[:, 2] >= zmax - 15))
    return f


def foot_load(total_N, m):
    zmin = m.mesh.bounds[0, 2]
    def f(X, nn):
        out = np.zeros(3 * nn)
        for c in FEET:
            r = np.linalg.norm(X[:, :2] - np.array(c), axis=1)
            sel = np.where((r <= 22) & (r >= 6) & (X[:, 2] <= zmin + 0.6 * H))[0]
            if len(sel) == 0:  # base da ventosa pode não estar no fundo global: usa a camada mais baixa local
                near = np.where(r <= 22)[0]; zl = X[near, 2].min(); sel = near[X[near, 2] <= zl + 0.6 * H]
            out[3 * sel + 2] -= total_N / len(FEET) / len(sel)
        return out
    return f


def tree(spine=True, cross=False):
    paths = []
    for b in BOSS:
        for f in FEET:
            if (f[1] > 283) == (b[1] > 283):
                paths.append([b, f])
    if spine:
        paths.append([BOSS[0], BOSS[1]])
    if cross:
        paths += [[FEET[0], FEET[1]], [FEET[2], FEET[3]]]
    return paths


def design(tag, base=0.12, web_t=3.0, boss_phi=0.35, yellow_phi=0.20, tube_r=7.5, skeleton=True, spine=True, cross=False, foot_phi=0.35):
    solid = [p.cyl_any(boss_holes(), tube_r, Z_IF - 40, Z_IF + 10)]
    zones = [(p.cyl_any(BOSS, 31.5, Z_IF - 40, Z_IF + 10), boss_phi),
             (p.cyl_any(FEET, 24.0), foot_phi),
             (p.cyl_any(BOSS, 43.0, Z_IF - 20, Z_IF + 10), yellow_phi)]
    if not skeleton:
        return v.Design(tag, base_phi=base, wall_mm=2.25, zones=zones, solid_zones=solid)
    return v.Design(tag, base_phi=base, wall_mm=2.25, zones=zones, solid_zones=solid, web_paths=tree(spine, cross), web_t=web_t)


def r06():
    return v.Design('INF_R06', base_phi=0.20, wall_mm=2.0, zones=[
        (p.cyl_any(BOSS, 31.5, Z_IF - 30, Z_IF + 30), 0.70),
        (p.corridor(tree(True), 9.0), 0.50),
        (p.cyl_any(BOSS, 47.5, Z_IF - 30, Z_IF + 30), 0.30)])


VAR = {'INF_R06': r06,
       'INF_N1_COM': lambda: design('INF_N1_COM'),
       'INF_N1_SEM': lambda: design('INF_N1_SEM', skeleton=False),
       'INF_N2_COM': lambda: design('INF_N2_COM', base=0.10),
       'INF_N3_COM': lambda: design('INF_N3_COM', base=0.10, cross=True),
       'INF_F20_COM': lambda: design('INF_F20_COM', base=0.20),
       'INF_F20_SEM': lambda: design('INF_F20_SEM', base=0.20, skeleton=False),
       'INF_F20_SEM_ISO': lambda: design('INF_F20_SEM_ISO', base=0.225, skeleton=False)}


def evaluate(m, d, kg=24.0):
    lab = m.classify(d); mass, vs, vi = m.mass_g(lab)
    res = m.solve(lab, {'ONE_24': foot_load(kg * (p.G + p.A_EXTRA), m)}, fixed_fn(m), tag=d.name)
    r = res['ONE_24']; U = r['U']; eps, st = m.stresses(U)
    sig, fr = st[1.0]; has = fr > 0.05; fxy, fz = v.failure_indices(sig)
    inf = {}
    for c, (s, f) in st.items():
        if c < 0.999 and (f > 0.05).any():
            inf[str(c)] = round(float((v.vm(s[f > 0.05]) / v.infill_strength(c)).max()), 4)
    cen = m.lo + (m.last['ei'] + 0.5) * H
    i = np.argmax(np.where(has, np.maximum(fxy, fz), 0))
    out = {'design': d.name, 'mass_model_g': round(mass, 1), 'disp_max_mm': round(float(np.abs(U).max()), 4),
           'FI_xy': round(float(fxy[has].max()), 4), 'FI_z': round(float(fz[has].max()), 4), 'infill_FI': inf,
           'hot': cen[i].round(1).tolist(), 'reaction': r['reaction'].round(1).tolist()}
    (v.OUT / f'{d.name}.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out))
    return out


if __name__ == '__main__':
    m = load_model()
    for k in (sys.argv[1:] or VAR):
        evaluate(m, VAR[k]())
