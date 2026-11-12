"""R07 - Modelo FEA de 2 corpos para o Fusion (os 98 corpos facetados travaram os contatos automáticos por falta de RAM).

CASCA  = 5 paredes (peça - núcleo), PA6-CF sólido.
NUCLEO = núcleo inteiro, material homogeneizado por média de Voigt dos volumes de zona do r07_zonas/fea_lod:
         COM  = almas + tubos 100%, colar 55, rosa 35, amarelo 20, base 25
         SEM  = mesmas zonas, almas trocadas por giroide 25% (tubos ficam)
         SEM_ISO = almas e base em giroide 32% (mesma massa do COM)
A comparação com/sem no Fusion é só do efeito global de rigidez do núcleo; o efeito local das almas fica no FE por voxels.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import trimesh
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r07_zonas as z  # noqa: E402
import r06_zonas_internas as z6  # noqa: E402

OUT = z.OUT / 'FEA_LOD3'; OUT.mkdir(exist_ok=True)
R = z.ROOT / '06_Engenharia' / 'R07'
MAT = json.loads((R / 'materiais_R07.json').read_text(encoding='utf-8'))['cards']
VOL = json.loads((z.OUT / 'FEA_LOD' / 'fea_lod.json').read_text(encoding='utf-8'))['zones']
CASES = {'COM': {'TUBOS': 'SOLIDO_100', 'ALMAS': 'SOLIDO_100', 'COLAR': 'GIROIDE_55', 'ROSA': 'GIROIDE_35', 'AMARELO': 'GIROIDE_20', 'BASE': 'GIROIDE_25'},
         'SEM': {'TUBOS': 'SOLIDO_100', 'ALMAS': 'GIROIDE_25', 'COLAR': 'GIROIDE_55', 'ROSA': 'GIROIDE_35', 'AMARELO': 'GIROIDE_20', 'BASE': 'GIROIDE_25'},
         'SEM_ISO': {'TUBOS': 'SOLIDO_100', 'ALMAS': 'GIROIDE_32', 'COLAR': 'GIROIDE_55', 'ROSA': 'GIROIDE_35', 'AMARELO': 'GIROIDE_20', 'BASE': 'GIROIDE_32'}}


def voigt(case):
    w = {k: VOL[k]['cm3'] for k in case}; W = sum(w.values())
    out = {p: round(sum(MAT[case[k]][p] * w[k] for k in case) / W, 2) for p in ('E_MPa', 'density_kg_m3', 'UTS_MPa')}
    out['nu'] = 0.3
    return out


def main(nf_part=8000, nf_core=4000):
    part_t = trimesh.load(z.SRC / z.PARTS['SUPERIOR'], force='mesh')
    core_t = z6.core_of(part_t)
    part = z6.to_manifold(part_t.simplify_quadric_decimation(face_count=nf_part))
    core = z6.to_manifold(core_t.simplify_quadric_decimation(face_count=nf_core)) ^ part
    rec = {'cards': {f'NUCLEO_{k}': voigt(c) for k, c in CASES.items()}, 'bodies': {}}
    for k, v in {'CASCA': part - core, 'NUCLEO': core}.items():
        tm = z6.to_trimesh(v); tm.export(OUT / f'SUPERIOR_{k}.stl')
        rec['bodies'][k] = {'cm3': round(z6.vol(v), 2), 'faces': len(tm.faces), 'watertight': bool(tm.is_watertight),
                            'lumps': len(tm.split(only_watertight=False))}
    (OUT / 'fea_lod3.json').write_text(json.dumps(rec, indent=2), encoding='utf-8')
    print(json.dumps(rec, indent=1))


if __name__ == '__main__':
    main()
