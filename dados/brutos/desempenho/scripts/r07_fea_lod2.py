"""R07 - Partição FEA LEVE (4 corpos) da peça SUPERIOR para o Fusion, quando os 98 corpos do r07_fea_lod travam
os contatos automáticos.

Corpos (cada um um único sólido; interfaces coincidentes = contato colado):
  FIXO     casca 5 paredes + tubos dos furos (100% nos dois casos)
  ALMAS    esqueleto em árvore (100% COM / giroide 32% SEM)
  COLAR    giroide 55%
  NUCLEO   rosa 35% + amarelo 20% + base 25% fundidos; material = média de Voigt por volume (E e densidade)
Saída: 04_Modificadores/R07/FEA_LOD2/SUPERIOR_<CORPO>.stl + fea_lod2.json (inclui o cartão NUCLEO_EQ)
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import trimesh
import manifold3d as mf
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r07_zonas as z  # noqa: E402
import r06_zonas_internas as z6  # noqa: E402

OUT = z.OUT / 'FEA_LOD2'
OUT.mkdir(exist_ok=True)
MAT = json.loads((z.ROOT / '06_Engenharia' / 'R07' / 'materiais_R07.json').read_text(encoding='utf-8'))


def main(nf_part=9000, nf_core=4000):
    part_t = trimesh.load(z.SRC / z.PARTS['SUPERIOR'], force='mesh')
    core_t = z6.core_of(part_t)
    part = z6.to_manifold(part_t.simplify_quadric_decimation(face_count=nf_part))
    core = z6.to_manifold(core_t.simplify_quadric_decimation(face_count=nf_core)) ^ part
    zmin, zmax = part_t.bounds[:, 2]
    paths = [[z.HUB, b] for b in z.BOSSES.values()] + [z.circle_path(z.HUB, 40.0, 24)] + z.spokes()
    tubes = z.union([z.cyl(c, z.TUBE_R, zmax - 25, zmax + 1, 20) for c in z.FLANGE_BOLTS] +
                    [z.cyl(c, z.TUBE_R, z.Z_IF - 30, z.Z_IF + 30, 20) for c in z.boss_holes(z.BOSSES)])
    webs = z.slab(paths, z.WEB_T, zmin - 1, zmax + 1)
    colar = z.ring(z.HUB, 26.0, 60.0, zmax - 35, zmax + 1)
    rosa = z.union([z.cyl(b, 31.5, z.Z_IF - 30, z.Z_IF + 30, 40) for b in z.BOSSES.values()])
    amar = z.union([z.cyl(b, 43.0, z.Z_IF - 30, z.Z_IF + 12, 40) for b in z.BOSSES.values()])
    t_core = core ^ tubes
    almas = (core ^ webs) - tubes
    col = (core ^ colar) - tubes - webs
    taken = tubes + webs + colar
    v_rosa = z6.vol((core ^ rosa) - taken); v_am = z6.vol((core ^ amar) - taken - rosa)
    nucleo = core - taken
    v_base = z6.vol(nucleo) - v_rosa - v_am
    fixo = (part - core) + t_core
    bodies = {'FIXO': fixo, 'ALMAS': almas, 'COLAR': col, 'NUCLEO': nucleo}
    c = MAT['cards']
    w = {'GIROIDE_35': v_rosa, 'GIROIDE_20': v_am, 'GIROIDE_25': v_base}
    W = sum(w.values())
    eq = {k: round(sum(c[n][k] * v for n, v in w.items()) / W, 1) for k in ('E_MPa', 'density_kg_m3', 'UTS_MPa')}
    eq['nu'] = 0.3
    rec = {'part_cm3': round(z6.vol(part), 2), 'NUCLEO_EQ': eq, 'nucleo_frac_cm3': {k: round(v, 2) for k, v in w.items()}, 'bodies': {}}
    for k, v in bodies.items():
        tm = z6.to_trimesh(v)
        tm.export(OUT / f'SUPERIOR_{k}.stl')
        rec['bodies'][k] = {'cm3': round(z6.vol(v), 2), 'faces': len(tm.faces), 'watertight': bool(tm.is_watertight),
                            'lumps': len(tm.split(only_watertight=False))}
    rec['sum_cm3'] = round(sum(r['cm3'] for r in rec['bodies'].values()), 2)
    (OUT / 'fea_lod2.json').write_text(json.dumps(rec, indent=2), encoding='utf-8')
    print(json.dumps(rec, indent=1))


if __name__ == '__main__':
    main()
