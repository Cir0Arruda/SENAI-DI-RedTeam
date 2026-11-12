"""R06 - Partição FEA em resolução reduzida para conversão em corpos sólidos no Fusion.

Mesmo método do r06_zonas_internas.py, mas a peça e o núcleo são simplificados ANTES das
booleanas: as interfaces entre casca e zonas continuam coincidentes (contato colado exato),
com menos triângulos para o MeshConvert do Fusion.
Saída: desempenho/04_Modificadores/R06/FEA_LOD/<PECA>_<ZONA>.stl + fea_lod.json
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import trimesh
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r06_zonas_internas as z  # noqa: E402

OUT = z.OUT / 'FEA_LOD'
OUT.mkdir(exist_ok=True)
FACES = {'SUPERIOR': (24000, 9000), 'INFERIOR_ESQ': (14000, 6000), 'INFERIOR_DIR': (14000, 6000)}


def main(keys):
    rep = {}
    for name in keys:
        part_t = trimesh.load(z.SRC / z.PARTS[name], force='mesh')
        core_t = z.core_of(part_t)
        nf_part, nf_core = FACES[name]
        part_lod = part_t.simplify_quadric_decimation(face_count=nf_part)
        core_lod = core_t.simplify_quadric_decimation(face_count=nf_core)
        part = z.to_manifold(part_lod)
        core = z.to_manifold(core_lod) ^ part
        seg = 48
        pink_p = z.mf.Manifold.batch_boolean([z.cylinder(x, y, z.R_BOSS, z.Z_IFACE - z.Z_WIN, z.Z_IFACE + z.Z_WIN, seg) for x, y in z.BOSSES], z.mf.OpType.Add)
        yel_p = z.mf.Manifold.batch_boolean([z.cylinder(x, y, z.R_BOSS + z.YELLOW_BAND, z.Z_IFACE - z.Z_WIN, z.Z_IFACE + z.Z_WIN, seg) for x, y in z.BOSSES], z.mf.OpType.Add) - pink_p
        zmin, zmax = part_t.bounds[:, 2]
        if name == 'SUPERIOR':
            paths = [(z.HUB, b) for b in z.BOSSES]
        else:
            feet = z.FEET[name]
            own = [b for b in z.BOSSES if min(abs(b[0] - f[0]) for f in feet) < 120]
            paths = [(b, f) for b in own for f in feet if (f[1] > 283) == (b[1] > 283)] + [(own[0], own[1])]
        blue_p = z.corridors(paths, zmin - 1, zmax + 1)
        zones = {
            'CASCA': part - core,
            'BASE20': core - pink_p - blue_p - yel_p,
            'AMARELO30': (core ^ yel_p) - pink_p - blue_p,
            'AZUL50': (core ^ blue_p) - pink_p,
            'ROSA70': core ^ pink_p,
        }
        rec = {'part_lod_cm3': round(z.vol(part), 2), 'part_original_cm3': round(part_t.volume / 1000, 2), 'zones': {}}
        for k, v in zones.items():
            tm = z.to_trimesh(v)
            tm.export(OUT / f'{name}_{k}.stl')
            rec['zones'][k] = {'cm3': round(z.vol(v), 2), 'faces': len(tm.faces), 'watertight': bool(tm.is_watertight)}
        rec['lod_volume_error_pct'] = round(100 * (rec['part_lod_cm3'] / rec['part_original_cm3'] - 1), 3)
        rep[name] = rec
        print(name, json.dumps(rec))
    (OUT / 'fea_lod.json').write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main(sys.argv[1:] or list(FACES))
