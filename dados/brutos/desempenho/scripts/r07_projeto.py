"""R07 - Projeto do esqueleto interno (almas em árvore) da peça superior: varredura de variantes.

Casos de carga (força vertical -Z nas interfaces de uma asa = as duas caixas presas em um lado):
  ONE_24 : 24 kg x (g + 5 m/s²) em uma asa (erro da seladora, mesma aceleração do estudo Fusion)
  ONE_30 : 30 kg x (g + 5 m/s²) em uma asa
  SYM_24 : 24 kg x (g + 5 m/s²) dividido nas duas asas (operação normal)
Saída: 06_Engenharia/R07/<variante>.json e mapas PNG.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r07_vfe as v  # noqa: E402
import r07_validar as val  # noqa: E402

G = 9.80665; A_EXTRA = 5.0
H = 3.0
CACHE = v.OUT / f'fine_SUPERIOR_H{H}.npz'
HUB = (-577.8, 383.0)
B = val.BOSSES
HOLE_R = 4.2


def bolt_holes():
    """3 furos por ressalto (lidos da planta): raio ~22 mm; y=348 -> 90/210/330°, y=218 -> 270/150/30°."""
    pts = []
    for (cx, cy) in B.values():
        angs = (90, 210, 330) if cy > 283 else (270, 150, 30)
        for ang in angs:
            a = np.deg2rad(ang); pts.append((cx + 22.0 * np.cos(a), cy + 22.0 * np.sin(a)))
    return pts


def load_model():
    m = v.Model.__new__(v.Model)
    if CACHE.exists():
        z = np.load(CACHE)
        m.fine = z['fine']; m.dist = z['dist']; m.lo = z['lo']; m.shape = z['shape']; m.n = int(z['n'])
        m.H = H; m.FINE = H / m.n; m.g = (z['gx'], z['gy'], z['gz'])
        import trimesh; m.mesh = trimesh.load(v.SRC / 'SUPERIOR_BASE_20.stl', force='mesh')
    else:
        m = v.Model(v.SRC / 'SUPERIOR_BASE_20.stl', H=H, FINE=H / 4)
        np.savez_compressed(CACHE, fine=m.fine, dist=m.dist.astype(np.float32), lo=m.lo, shape=m.shape, n=m.n,
                            gx=m.g[0], gy=m.g[1], gz=m.g[2])
    return m


def cyl(c, r, z0=-1e9, z1=1e9):
    return lambda X, Y, Z: ((X - c[0]) ** 2 + (Y - c[1]) ** 2 <= r * r) & (Z >= z0) & (Z <= z1)


def ring(c, r0, r1, z0=-1e9, z1=1e9):
    return lambda X, Y, Z: ((X - c[0]) ** 2 + (Y - c[1]) ** 2 <= r1 * r1) & ((X - c[0]) ** 2 + (Y - c[1]) ** 2 >= r0 * r0) & (Z >= z0) & (Z <= z1)


def corridor(paths, half):
    def f(X, Y, Z):
        m = v.polyline_mask(X[..., 0], Y[..., 0], paths, half)[..., None]
        return np.broadcast_to(m, np.broadcast_shapes(X.shape, Z.shape))
    return f


Z_IF = 267.4


def designs():
    D = {}
    # R06 equivalente (TPMS-D -> mesma regra de rigidez): rosa R31,5 70%, amarelo +16 mm 30%, azul 18 mm 50%, base 20%
    D['R06'] = v.Design('R06', base_phi=0.20, wall_mm=2.0, zones=[
        (cyl_any(list(B.values()), 31.5, Z_IF - 30, Z_IF + 30), 0.70),
        (corridor([[HUB, b] for b in B.values()], 9.0), 0.50),
        (cyl_any(list(B.values()), 47.5, Z_IF - 30, Z_IF + 30), 0.30)])
    for tag, kw in VARIANTS.items():
        D[tag] = novo(tag, **kw)
    return D


FLANGE_BOLTS = [(-617.8, 383.0), (-597.8, 348.4), (-557.8, 348.4), (-537.8, 383.0), (-557.8, 417.6), (-597.8, 417.6)]


def circle_path(c, r, n=48):
    a = np.linspace(0, 2 * np.pi, n + 1)
    return [(c[0] + r * np.cos(t), c[1] + r * np.sin(t)) for t in a]


def tree_paths(ring_r=40.0, wing_spine=True):
    p = [[HUB, b] for b in B.values()]
    if ring_r:
        p.append(circle_path(HUB, ring_r))
    if wing_spine:
        p += [[B['R1'], B['R2']], [B['L1'], B['L2']]]
    return p


def spokes(r0=22.0, r1=70.0, n=6, a0=0.0):
    return [[(HUB[0] + r0 * np.cos(a), HUB[1] + r0 * np.sin(a)), (HUB[0] + r1 * np.cos(a), HUB[1] + r1 * np.sin(a))]
            for a in np.deg2rad(a0 + np.arange(n) * 360 / n)]


def novo(tag, base=0.15, web_t=3.0, ring_r=40.0, spine=True, tube_r=7.5, collar_phi=0.45, boss_phi=0.40,
         yellow_phi=0.25, skeleton=True, collar=(28.0, 52.0, 25.0), extra_paths=(), collar_solid=None):
    """Esqueleto em árvore: almas sólidas (web_t) cubo->ressaltos + anel da flange + espinha da asa;
    tubos sólidos nos furos (flange e ressaltos); colarinho da flange; ressaltos e assento amarelo."""
    zmax_flange = 349.9
    solid = [cyl_any(FLANGE_BOLTS, 4.2 + tube_r - 4.2 if tube_r > 4.2 else 0, zmax_flange - 25, 1e9),
             cyl_any(bolt_holes(), tube_r, Z_IF - 30, Z_IF + 30)] if tube_r else []
    zones = [(cyl_any(list(B.values()), 31.5, Z_IF - 30, Z_IF + 30), boss_phi),
             (ring(HUB, collar[0], collar[1], zmax_flange - collar[2], 1e9), collar_phi),
             (cyl_any(list(B.values()), 43.0, Z_IF - 30, Z_IF + 12), yellow_phi)]
    if collar_solid:
        solid.append(ring(HUB, collar_solid[0], collar_solid[1], zmax_flange - collar_solid[2], 1e9))
    if not skeleton:
        return v.Design(tag, base_phi=base, wall_mm=2.25, zones=zones, solid_zones=solid)
    return v.Design(tag, base_phi=base, wall_mm=2.25, zones=zones, solid_zones=solid,
                    web_paths=tree_paths(ring_r, spine) + [list(p) for p in extra_paths], web_t=web_t)


VARIANTS = {
    'N1_COM': dict(base=0.15, web_t=3.0),
    'N1_SEM': dict(base=0.15, skeleton=False),
    'N2_COM': dict(base=0.12, web_t=3.0),
    'N3_COM': dict(base=0.15, web_t=4.0),
    'N4_COM': dict(base=0.18, web_t=3.0, collar_phi=0.55),
    'N5_COM': dict(base=0.12, web_t=3.0, collar_phi=0.55, extra_paths=spokes(22, 72, 6, 30)),
    'N6_COM': dict(base=0.12, web_t=3.0, collar_phi=0.45, collar_solid=(34.0, 47.0, 14.0)),
    'N7_COM': dict(base=0.12, web_t=3.0, collar_phi=0.55, collar=(26.0, 60.0, 35.0), extra_paths=spokes(22, 72, 6, 30)),
    'N8_COM': dict(base=0.10, web_t=3.0, collar_phi=0.55, collar=(26.0, 60.0, 35.0), extra_paths=spokes(22, 72, 6, 30)),
    'N9_COM': dict(base=0.12, web_t=3.0, collar_phi=0.55, collar=(26.0, 60.0, 35.0), extra_paths=spokes(22, 72, 6, 30), spine=False),
    'N10_COM': dict(base=0.12, web_t=3.0, collar_phi=0.45, collar=(26.0, 60.0, 35.0), extra_paths=spokes(22, 72, 6, 30), boss_phi=0.35, yellow_phi=0.20),
}
# Projeto final R07 (peça superior) e contraprovas
FINAL = dict(base=0.10, web_t=3.0, collar_phi=0.55, collar=(26.0, 60.0, 35.0), extra_paths=spokes(22, 72, 6, 30),
             spine=False, boss_phi=0.35, yellow_phi=0.20)
VARIANTS['F_COM'] = FINAL
VARIANTS['F_SEM'] = {**FINAL, 'skeleton': False}
VARIANTS['F_SEM_ISO'] = {**FINAL, 'skeleton': False, 'base': 0.155}   # sem almas, mesma massa (giroide mais denso)


def cyl_any(cs, r, z0=-1e9, z1=1e9):
    def f(X, Y, Z):
        m = np.zeros(np.broadcast_shapes(X.shape, Z.shape), bool)
        for c in cs:
            m |= cyl(c, r, z0, z1)(X, Y, Z)
        return m
    return f


def loads(m):
    zmin = m.mesh.bounds[0, 2]
    W = lambda kg: kg * (G + A_EXTRA)
    return {'ONE_24': val.load_fn(['R1', 'R2'], W(24), H, zmin),
            'ONE_30': val.load_fn(['R1', 'R2'], W(30), H, zmin),
            'SYM_24': val.load_fn(list(B), W(24), H, zmin)}


def evaluate(m, d: v.Design, cases=None, plot=True):
    lab = m.classify(d)
    mass, vs, vi = m.mass_g(lab)
    L = loads(m)
    if cases:
        L = {k: L[k] for k in cases}
    res = m.solve(lab, L, val.fixed_fn_factory(m, H), tag=d.name)
    out = {'design': d.name, 'mass_model_g': round(mass, 1), 'solid_cm3': round(vs, 1), 'infill_cm3': round(vi, 1),
           'base_phi': d.base_phi, 'web_t': d.web_t, 'cases': {}}
    L_ = m.last
    cen = m.lo + (L_['ei'] + 0.5) * H
    for k, r in res.items():
        U = r['U']; eps, st = m.stresses(U)
        disp = np.linalg.norm(U.reshape(-1, 3), axis=1)
        rec = {'disp_max_mm': round(float(disp.max()), 4), 'iters': r['iters'], 'reaction_N': r['reaction'].round(2).tolist()}
        sig, fr = st[1.0]
        has = fr > 0.05
        fxy, fz = v.failure_indices(sig)
        rec['solid_vm_max_MPa'] = round(float(v.vm(sig[has]).max()), 3)
        rec['solid_FI_xy_max'] = round(float(fxy[has].max()), 4)
        rec['solid_FI_z_max'] = round(float(fz[has].max()), 4)
        worst = []
        for c, (s, f) in st.items():
            if c >= 0.999:
                continue
            hasc = f > 0.05
            if hasc.any():
                fi = v.vm(s[hasc]) / v.infill_strength(c)
                worst.append((c, float(fi.max())))
        rec['infill_FI_max'] = {str(c): round(x, 4) for c, x in worst}
        i = np.argmax(np.where(has, np.maximum(fxy, fz), 0)); rec['hot_xyz'] = cen[i].round(1).tolist()
        out['cases'][k] = rec
        if plot:
            fi = np.where(has, np.maximum(fxy, fz), 0)
            fig, ax = plt.subplots(figsize=(8, 7), layout='constrained')
            order = np.argsort(fi)
            sc = ax.scatter(cen[order, 0], cen[order, 1], c=fi[order], s=4, cmap='inferno')
            plt.colorbar(sc, label='índice de falha do sólido (máx XY, Z)')
            for b in B.values():
                ax.plot(*b, 'c+')
            ax.set_aspect('equal'); ax.set_title(f'{d.name} {k}: desl {rec["disp_max_mm"]} mm')
            fig.savefig(v.OUT / f'mapa_{d.name}_{k}.png', dpi=90); plt.close(fig)
    (v.OUT / f'{d.name}.json').write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False))
    return out


VARIANTS['F20_COM'] = {**FINAL, 'base': 0.20}
VARIANTS['F20_SEM'] = {**FINAL, 'base': 0.20, 'skeleton': False}
VARIANTS['F20_SEM_ISO'] = {**FINAL, 'base': 0.273, 'skeleton': False}


VARIANTS['F25_COM'] = {**FINAL, 'base': 0.25}
VARIANTS['F25_SEM'] = {**FINAL, 'base': 0.25, 'skeleton': False}
VARIANTS['F25_SEM_ISO'] = {**FINAL, 'base': 0.323, 'skeleton': False}


if __name__ == '__main__':
    m = load_model()
    D = designs()
    keys = [a for a in sys.argv[1:] if not a.startswith('--')] or list(D)
    cases = ['ONE_24'] if '--rapido' in sys.argv else None
    for k in keys:
        evaluate(m, D[k], cases=cases)
