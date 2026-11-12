"""R07 - Geometria do ESQUELETO INTERNO em árvore + zonas de giroide, recortada por dentro da peça.

Exterior inalterado: tudo é recortado do núcleo (peça recuada WALL mm = 5 paredes x 0,45 mm).
Mesmas primitivas do projeto por voxels (r07_projeto / r07_inferior), para que massa e FEA batam.

Zonas (prioridade de cima para baixo; disjuntas por subtração):
  SOLIDO_100  almas de 3 mm em árvore (cubo->ressaltos, anel da flange, raios) + tubos nos furos
  COLAR_55    colarinho da flange do robô (peça superior)
  ROSA_35     ressaltos parafusados
  PES_35      bases das ventosas (peças inferiores)
  AMARELO_20  assento de transição em torno dos ressaltos
  base        giroide 10% (superior) / 12% (inferiores) = configuração global do Orca
Variante --sem: mesma coisa sem as almas (só tubos nos furos) -> contraprova "sem esqueleto".
Saídas: 04_Modificadores/R07/<PECA>[_SEM]_MOD_<ZONA>.stl, <PECA>_FEA_<ZONA>.stl, r07_zonas.json
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
import trimesh
import manifold3d as mf
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r06_zonas_internas as z6  # noqa: E402  (core_of, conversões)

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / '04_Modificadores' / 'origem'
OUT = ROOT / '04_Modificadores' / 'R07'
OUT.mkdir(parents=True, exist_ok=True)
z6.WALL = 2.25

HUB = (-577.8, 383.0)
BOSSES = {'R1': (-478.33, 218.0), 'R2': (-478.33, 348.0), 'L1': (-677.33, 218.0), 'L2': (-677.33, 348.0)}
FEET = {'INFERIOR_ESQ': [(-791.0, 155.0), (-791.0, 410.0), (-619.0, 155.0), (-619.0, 410.0)],
        'INFERIOR_DIR': [(-536.0, 155.0), (-536.0, 410.0), (-364.0, 155.0), (-364.0, 410.0)]}
OWN = {'INFERIOR_ESQ': ['L1', 'L2'], 'INFERIOR_DIR': ['R1', 'R2']}
FLANGE_BOLTS = [(-617.8, 383.0), (-597.8, 348.4), (-557.8, 348.4), (-537.8, 383.0), (-557.8, 417.6), (-597.8, 417.6)]
Z_IF = 267.4
WEB_T = 3.0
TUBE_R = 7.5
PARTS = {'SUPERIOR': 'SUPERIOR_BASE_20.stl', 'INFERIOR_ESQ': 'INFERIOR_ESQ_BASE_20.stl', 'INFERIOR_DIR': 'INFERIOR_DIR_BASE_20.stl'}
BASE = {'SUPERIOR': 10, 'INFERIOR_ESQ': 12, 'INFERIOR_DIR': 12}


def boss_holes(keys):
    pts = []
    for k in keys:
        cx, cy = BOSSES[k]
        for ang in ((90, 210, 330) if cy > 283 else (270, 150, 30)):
            a = np.deg2rad(ang); pts.append((cx + 22 * np.cos(a), cy + 22 * np.sin(a)))
    return pts


def cyl(c, r, z0, z1, seg=64):
    return mf.Manifold.cylinder(z1 - z0, r, r, seg).translate((c[0], c[1], z0))


def union(ms):
    ms = [m for m in ms if m is not None]
    return mf.Manifold.batch_boolean(ms, mf.OpType.Add) if ms else mf.Manifold()


def slab(paths, t, z0, z1):
    secs = []
    for path in paths:
        for a, b in zip(path[:-1], path[1:]):
            ca = mf.CrossSection.circle(t / 2, 16).translate(a); cb = mf.CrossSection.circle(t / 2, 16).translate(b)
            secs.append(mf.CrossSection.batch_hull([ca, cb]))
    return mf.CrossSection.batch_boolean(secs, mf.OpType.Add).extrude(z1 - z0).translate((0, 0, z0))


def circle_path(c, r, n=48):
    a = np.linspace(0, 2 * np.pi, n + 1)
    return [(c[0] + r * np.cos(t), c[1] + r * np.sin(t)) for t in a]


def spokes(r0=22.0, r1=72.0, n=6, a0=30.0):
    return [[(HUB[0] + r0 * np.cos(a), HUB[1] + r0 * np.sin(a)), (HUB[0] + r1 * np.cos(a), HUB[1] + r1 * np.sin(a))]
            for a in np.deg2rad(a0 + np.arange(n) * 360 / n)]


def ring(c, r0, r1, z0, z1):
    return cyl(c, r1, z0, z1, 96) - cyl(c, r0, z0 - 1, z1 + 1, 96)


def primitives(name, zmin, zmax, skeleton=True):
    if name == 'SUPERIOR':
        paths = [[HUB, b] for b in BOSSES.values()] + [circle_path(HUB, 40.0)] + spokes()
        tubes = union([cyl(c, TUBE_R, zmax - 25, zmax + 1) for c in FLANGE_BOLTS] +
                      [cyl(c, TUBE_R, Z_IF - 30, Z_IF + 30) for c in boss_holes(BOSSES)])
        zones = [('COLAR', 55, ring(HUB, 26.0, 60.0, zmax - 35, zmax + 1)),
                 ('ROSA', 35, union([cyl(b, 31.5, Z_IF - 30, Z_IF + 30) for b in BOSSES.values()])),
                 ('AMARELO', 20, union([cyl(b, 43.0, Z_IF - 30, Z_IF + 12) for b in BOSSES.values()]))]
    else:
        own = OWN[name]; feet = FEET[name]
        paths = [[BOSSES[k], f] for k in own for f in feet if (f[1] > 283) == (BOSSES[k][1] > 283)]
        paths.append([BOSSES[own[0]], BOSSES[own[1]]])
        tubes = union([cyl(c, TUBE_R, Z_IF - 40, Z_IF + 10) for c in boss_holes(own)])
        zones = [('ROSA', 35, union([cyl(BOSSES[k], 31.5, Z_IF - 40, Z_IF + 10) for k in own])),
                 ('PES', 35, union([cyl(f, 24.0, zmin - 1, zmax + 1) for f in feet])),
                 ('AMARELO', 20, union([cyl(BOSSES[k], 43.0, Z_IF - 20, Z_IF + 10) for k in own]))]
    solid = tubes + slab(paths, WEB_T, zmin - 1, zmax + 1) if skeleton else tubes
    return [('SOLIDO', 100, solid)] + zones, paths


def build(name, part_t, core_t, skeleton=True):
    part = z6.to_manifold(part_t)
    core = z6.to_manifold(core_t) ^ part
    zmin, zmax = part_t.bounds[:, 2]
    prims, paths = primitives(name, zmin, zmax, skeleton)
    taken = mf.Manifold(); zones = {}
    for zname, pct, prim in prims:
        zz = (core ^ prim) - taken
        zones[f'{zname}_{pct}'] = zz
        taken = taken + prim
    zones['BASE'] = core - taken
    zones['CASCA'] = part - core
    return part, zones, paths


def main(args):
    sem = '--sem' in args
    keys = [a for a in args if not a.startswith('--')] or list(PARTS)
    rep_path = OUT / 'r07_zonas.json'
    rep = json.loads(rep_path.read_text(encoding='utf-8')) if rep_path.exists() else {}
    for name in keys:
        part_t = trimesh.load(SRC / PARTS[name], force='mesh')
        core_t = z6.core_of(part_t)
        part, zones, paths = build(name, part_t, core_t, skeleton=not sem)
        tag = f'{name}_SEM' if sem else name
        rec = {'part_cm3': round(z6.vol(part), 2), 'base_infill_pct': BASE[name], 'skeleton': not sem,
               'zones_cm3': {k: round(z6.vol(v), 2) for k, v in zones.items()},
               'outside_part_cm3': {k: round(z6.vol(v - part), 4) for k, v in zones.items() if k not in ('CASCA',)},
               'web_paths_xy_mm': [[list(map(float, p)) for p in path] for path in paths] if not sem else []}
        rec['partition_error_pct'] = round(100 * abs(sum(rec['zones_cm3'].values()) - rec['part_cm3']) / rec['part_cm3'], 4)
        for k, v in zones.items():
            if v.is_empty():
                continue
            tm = z6.to_trimesh(v)
            if k not in ('BASE', 'CASCA'):
                tm.export(OUT / f'{tag}_MOD_{k}.stl')
            if not sem:
                tm.export(OUT / f'{tag}_FEA_{k}.stl')
        rep[tag] = rec
        print(tag, json.dumps(rec['zones_cm3']), 'fora', rec['outside_part_cm3'], 'err%', rec['partition_error_pct'], flush=True)
    rep_path.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main(sys.argv[1:])
