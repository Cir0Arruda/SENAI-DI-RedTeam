"""R07 - Modelo FEA de 2 corpos LIMPO para o Fusion (LOD4).

O LOD3 (peça - núcleo por booleana) herdava triângulos-agulha da tesselação original do CAD
(razão de aspecto até ~40.000) e o Fusion falhava ao gerar a malha da casca ("falha de corpo").
Aqui as duas superfícies saem do MESMO campo de distância assinada (voxel 0,5 mm):
  exterior = isosuperfície 0 do campo;  núcleo = isosuperfície a WALL para dentro.
CASCA  = exterior + núcleo invertido (sem booleana: a face interna da casca é exatamente a do núcleo).
NUCLEO = núcleo.
Mesmo referencial do LOD3 (coordenadas da montagem), então as seleções de furos/ressaltos continuam valendo.
Saída: 04_Modificadores/R07/FEA_LOD4/SUPERIOR_{CASCA,NUCLEO}.stl + fea_lod4.json
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
import trimesh
from scipy import ndimage
from skimage import measure
import pymeshlab as ml
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r07_zonas as z  # noqa: E402

OUT = z.OUT / 'FEA_LOD4'; OUT.mkdir(exist_ok=True)
PITCH, WALL, PAD = 0.5, 2.25, 4


def aspect(m):
    t = m.triangles; L = np.linalg.norm(t[:, [1, 2, 0]] - t, axis=2)
    h = 2 * m.area_faces / L.max(1)
    return L.max(1) / np.maximum(h, 1e-12)


def surface(field, level, origin, edge):
    """Isossuperfície fechada com triângulos quase equiláteros (remalha isotrópica, aresta ~edge mm)."""
    v, f, _, _ = measure.marching_cubes(field, level)
    m = trimesh.Trimesh(v * PITCH + origin, f[:, ::-1], process=True)
    if m.volume < 0:
        m.invert()
    m = max(m.split(only_watertight=True), key=lambda x: x.volume)
    trimesh.smoothing.filter_taubin(m, lamb=0.5, nu=-0.53, iterations=6)
    ms = ml.MeshSet()
    ms.add_mesh(ml.Mesh(m.vertices, m.faces))
    ms.meshing_decimation_quadric_edge_collapse(targetfacenum=max(60000, len(m.faces) // 10), preservetopology=True, preservenormal=True)
    ms.meshing_isotropic_explicit_remeshing(targetlen=ml.PureValue(edge), iterations=8, featuredeg=40)
    ms.meshing_repair_non_manifold_edges(); ms.meshing_repair_non_manifold_vertices()
    ms.meshing_close_holes(maxholesize=50)
    k = ms.current_mesh()
    m = trimesh.Trimesh(k.vertex_matrix(), k.face_matrix(), process=True)
    m = max(m.split(only_watertight=False), key=lambda x: len(x.faces))
    if m.volume < 0:
        m.invert()
    print('  remalha', len(m.faces), 'faces, aresta', edge, 'mm, fechada', m.is_watertight, flush=True)
    return m


def main(edge_ext=3.0, edge_core=4.5):
    part = trimesh.load(z.SRC / z.PARTS['SUPERIOR'], force='mesh')
    cache = OUT / 'campo_phi.npz'
    if cache.exists():
        c = np.load(cache); phi, origin = c['phi'], c['origin']
    else:
        vox = part.voxelized(PITCH).fill()
        inside = np.pad(vox.matrix, PAD)
        din = ndimage.distance_transform_edt(inside) * PITCH
        dout = ndimage.distance_transform_edt(~inside) * PITCH
        phi = ndimage.gaussian_filter((din - dout).astype(np.float32), 0.8)   # > 0 dentro, em mm
        origin = vox.transform[:3, 3] - PAD * PITCH
        np.savez_compressed(cache, phi=phi, origin=origin)
    # o voxel cheio infla a peça (~meio voxel): extrai no nível 0 (malha fechada) e recua a superfície
    # pela normal do vértice até o volume bater com o da peça real; o núcleo fica WALL para dentro disso.
    ext = surface(phi, 0.0, origin, edge_ext)
    d = (ext.volume - part.volume) / ext.area
    ext = trimesh.Trimesh(ext.vertices - ext.vertex_normals * d, ext.faces, process=True)
    core = surface(phi, WALL + d, origin, edge_core)
    L0 = d
    print('recuo do exterior', round(d, 3), 'mm · vol', round(ext.volume / 1000, 1), 'wt', ext.is_watertight, core.is_watertight, flush=True)
    casca = trimesh.Trimesh(np.vstack([ext.vertices, core.vertices]),
                            np.vstack([ext.faces, core.faces[:, ::-1] + len(ext.vertices)]), process=False)
    # folga mínima entre as superfícies (não podem se tocar)
    gap = np.abs(trimesh.proximity.signed_distance(ext, core.sample(6000)))
    dev = np.abs(trimesh.proximity.signed_distance(part, ext.sample(6000)))
    rec = {'pitch_mm': PITCH, 'aresta_mm': [edge_ext, edge_core], 'nivel_exterior_mm': round(L0, 3), 'parede_mm': WALL, 'desvio_exterior_mm': {'p95': round(float(np.percentile(dev, 95)), 3), 'max': round(float(dev.max()), 3)},
           'folga_min_casca_mm': round(float(gap.min()), 3), 'bodies': {}}
    for k, m in {'CASCA': casca, 'NUCLEO': core}.items():
        m.export(OUT / f'SUPERIOR_{k}.stl')
        a = aspect(m)
        rec['bodies'][k] = {'cm3': round(abs(m.volume) / 1000, 2), 'faces': len(m.faces), 'watertight': bool(m.is_watertight),
                            'aspecto_max': round(float(a.max()), 1), 'aspecto_gt20': int((a > 20).sum())}
    rec['original'] = {'cm3': round(part.volume / 1000, 2), 'aspecto_max': round(float(aspect(part).max()), 1)}
    (OUT / 'fea_lod4.json').write_text(json.dumps(rec, indent=2), encoding='utf-8')
    print(json.dumps(rec, indent=1))


if __name__ == '__main__':
    main()
