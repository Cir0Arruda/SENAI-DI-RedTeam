"""R07 - Partição FEA (resolução reduzida) da peça SUPERIOR para o Fusion: um corpo por zona.

Mesma geometria do r07_zonas, mas peça e núcleo simplificados ANTES das booleanas (interfaces
coincidentes = contato colado) e o sólido separado em ALMAS (esqueleto) e TUBOS (furos), para que
"com" e "sem esqueleto" sejam o MESMO modelo com materiais trocados no estudo do Fusion.
Saída: 04_Modificadores/R07/FEA_LOD/SUPERIOR_<ZONA>.stl + fea_lod.json
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import trimesh
import manifold3d as mf
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r07_zonas as z  # noqa: E402
import r06_zonas_internas as z6  # noqa: E402

OUT = z.OUT / 'FEA_LOD'
OUT.mkdir(exist_ok=True)


def main(nf_part=16000, nf_core=7000):
    name = 'SUPERIOR'
    part_t = trimesh.load(z.SRC / z.PARTS[name], force='mesh')
    core_t = z6.core_of(part_t)
    part = z6.to_manifold(part_t.simplify_quadric_decimation(face_count=nf_part))
    core = z6.to_manifold(core_t.simplify_quadric_decimation(face_count=nf_core)) ^ part
    zmin, zmax = part_t.bounds[:, 2]
    paths = [[z.HUB, b] for b in z.BOSSES.values()] + [z.circle_path(z.HUB, 40.0, 32)] + z.spokes()
    tubes = z.union([z.cyl(c, z.TUBE_R, zmax - 25, zmax + 1, 24) for c in z.FLANGE_BOLTS] +
                    [z.cyl(c, z.TUBE_R, z.Z_IF - 30, z.Z_IF + 30, 24) for c in z.boss_holes(z.BOSSES)])
    webs = z.slab(paths, z.WEB_T, zmin - 1, zmax + 1)
    prims = [('TUBOS', tubes), ('ALMAS', webs),
             ('COLAR', z.ring(z.HUB, 26.0, 60.0, zmax - 35, zmax + 1)),
             ('ROSA', z.union([z.cyl(b, 31.5, z.Z_IF - 30, z.Z_IF + 30, 48) for b in z.BOSSES.values()])),
             ('AMARELO', z.union([z.cyl(b, 43.0, z.Z_IF - 30, z.Z_IF + 12, 48) for b in z.BOSSES.values()]))]
    taken = mf.Manifold(); zones = {}
    for k, p in prims:
        zones[k] = (core ^ p) - taken; taken = taken + p
    zones['BASE'] = core - taken
    zones['CASCA'] = part - core
    rec = {'part_cm3': round(z6.vol(part), 2), 'part_original_cm3': round(part_t.volume / 1000, 2), 'zones': {}}
    for k, v in zones.items():
        tm = z6.to_trimesh(v)
        tm.export(OUT / f'{name}_{k}.stl')
        rec['zones'][k] = {'cm3': round(z6.vol(v), 2), 'faces': len(tm.faces), 'watertight': bool(tm.is_watertight),
                           'lumps': len(tm.split(only_watertight=False))}
    rec['sum_cm3'] = round(sum(r['cm3'] for r in rec['zones'].values()), 2)
    (OUT / 'fea_lod.json').write_text(json.dumps(rec, indent=2), encoding='utf-8')
    print(json.dumps(rec, indent=1))


if __name__ == '__main__':
    main()
