"""R06 - Zonas de preenchimento INTERNAS da garra SAMI (corrige o erro do R04).

Erro do R04: os modificadores eram primitivas (cilindros R46, barras retas) maiores que a
própria peça (amarelo superior = 1.648 cm³ > peça 1.391 cm³), atravessando o contorno externo.

R06: cada zona é recortada de um NÚCLEO obtido da própria peça, recuado 2 mm da superfície
(5 perímetros x 0,4 mm). Nada sai do contorno externo; o exterior não é alterado.
As zonas são disjuntas e obtidas por booleanas sobre as mesmas primitivas, então as interfaces
coincidem (necessário para contato colado no FEA do Fusion).

Prioridade: rosa 70% > azul 50% > amarelo 30% > base 20% (TPMS-D).
Saídas (por peça), em desempenho/04_Modificadores/R06/:
  <PECA>_MOD_ROSA_70.stl, _MOD_AZUL_50.stl, _MOD_AMARELO_30.stl   -> modificadores do Orca
  <PECA>_FEA_CASCA.stl, _FEA_BASE20.stl, _FEA_AMARELO30.stl, _FEA_AZUL50.stl, _FEA_ROSA70.stl -> partição FEA
  r06_zonas.json  -> volumes, parâmetros e verificações
Uso: python r06_zonas_internas.py
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import trimesh
import manifold3d as mf
from scipy import ndimage
from skimage import measure

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / '04_Modificadores' / 'origem'
OUT = ROOT / '04_Modificadores' / 'R06'
OUT.mkdir(parents=True, exist_ok=True)

PITCH = 1.0          # mm, voxel para o recuo
WALL = 2.0           # mm, 5 perímetros x 0,4 mm
R_BOSS = 31.5        # mm, raio dos ressaltos (mesmo raio medido no R04)
YELLOW_BAND = 16.0   # mm, faixa amarela além do ressalto
BLUE_HALF = 9.0      # mm, meia-largura do corredor azul (18 mm)
Z_IFACE = 267.4      # mm, interface superior/inferior (fundo sup. 264,9 / topo inf. 269,9)
Z_WIN = 30.0         # mm, janela vertical do rosa/amarelo em torno da interface

BOSSES = [(-478.33, 218.0), (-478.33, 348.0), (-677.33, 218.0), (-677.33, 348.0)]
HUB = (-577.8, 383.0)  # centro do flange superior (topo da peça)
FEET = {
    'INFERIOR_ESQ': [(-791.0, 155.0), (-791.0, 410.0), (-619.0, 155.0), (-619.0, 410.0)],
    'INFERIOR_DIR': [(-536.0, 155.0), (-536.0, 410.0), (-364.0, 155.0), (-364.0, 410.0)],
}
PARTS = {
    'SUPERIOR': 'SUPERIOR_BASE_20.stl',
    'INFERIOR_ESQ': 'INFERIOR_ESQ_BASE_20.stl',
    'INFERIOR_DIR': 'INFERIOR_DIR_BASE_20.stl',
}


def to_manifold(m: trimesh.Trimesh) -> mf.Manifold:
    mesh = mf.Mesh(vert_properties=np.asarray(m.vertices, np.float32), tri_verts=np.asarray(m.faces, np.uint32))
    out = mf.Manifold(mesh)
    if out.status() != mf.Error.NoError:
        raise RuntimeError(f'malha não-manifold: {out.status()}')
    return out


def to_trimesh(m: mf.Manifold) -> trimesh.Trimesh:
    mesh = m.to_mesh()
    return trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts), process=True)


def vol(m: mf.Manifold) -> float:
    return m.volume() / 1000.0  # cm³


def core_of(part: trimesh.Trimesh) -> trimesh.Trimesh:
    """Núcleo = pontos a >= WALL da superfície, via voxel + transformada de distância."""
    vox = part.voxelized(PITCH).fill()
    inside = np.pad(vox.matrix, 3)
    dist = ndimage.distance_transform_edt(inside) * PITCH
    core = dist >= WALL + 0.5 * PITCH          # margem de meio voxel => recuo efetivo >= WALL
    field = ndimage.gaussian_filter(core.astype(np.float32), 0.7)
    verts, faces, _, _ = measure.marching_cubes(field, 0.5)
    origin = vox.transform[:3, 3] - 3 * PITCH  # pad de 3 voxels
    verts = verts * PITCH + origin
    m = trimesh.Trimesh(verts, faces[:, ::-1], process=True)
    if m.volume < 0:
        m.invert()
    m = max(m.split(only_watertight=True), key=lambda x: x.volume)  # descarta ilhas mínimas
    return m.simplify_quadric_decimation(face_count=40000)


def cylinder(cx, cy, r, z0, z1, seg=96) -> mf.Manifold:
    return mf.Manifold.cylinder(z1 - z0, r, r, seg).translate((cx, cy, z0))


def corridors(paths, z0, z1) -> mf.Manifold:
    secs = []
    for a, b in paths:
        ca = mf.CrossSection.circle(BLUE_HALF, 48).translate(a)
        cb = mf.CrossSection.circle(BLUE_HALF, 48).translate(b)
        secs.append(mf.CrossSection.batch_hull([ca, cb]))
    cs = mf.CrossSection.batch_boolean(secs, mf.OpType.Add)
    return cs.extrude(z1 - z0).translate((0, 0, z0))


def main():
    report = {'revision': 'R06_ZONAS_INTERNAS', 'wall_mm': WALL, 'pitch_mm': PITCH,
              'priority': [70, 50, 30, 20], 'r_boss_mm': R_BOSS, 'yellow_band_mm': YELLOW_BAND,
              'blue_width_mm': 2 * BLUE_HALF, 'z_interface_mm': Z_IFACE, 'z_window_mm': Z_WIN,
              'exterior_changed': False, 'parts': {}}
    for name, fn in PARTS.items():
        part_t = trimesh.load(SRC / fn, force='mesh')
        part = to_manifold(part_t)
        zmin, zmax = part_t.bounds[:, 2]
        core = to_manifold(core_of(part_t)) ^ part  # interseção garante núcleo dentro da peça

        pink_p = mf.Manifold.batch_boolean(
            [cylinder(x, y, R_BOSS, Z_IFACE - Z_WIN, Z_IFACE + Z_WIN) for x, y in BOSSES], mf.OpType.Add)
        yel_p = mf.Manifold.batch_boolean(
            [cylinder(x, y, R_BOSS + YELLOW_BAND, Z_IFACE - Z_WIN, Z_IFACE + Z_WIN) for x, y in BOSSES],
            mf.OpType.Add) - pink_p
        if name == 'SUPERIOR':
            paths = [(HUB, b) for b in BOSSES]
        else:
            feet = FEET[name]
            own = [b for b in BOSSES if min(abs(b[0] - f[0]) for f in feet) < 120]
            paths = [(b, f) for b in own for f in feet if (f[1] > 283) == (b[1] > 283)]
            paths.append((own[0], own[1]))
        blue_p = corridors(paths, zmin - 1, zmax + 1)

        pink = core ^ pink_p
        blue = (core ^ blue_p) - pink_p
        yellow = (core ^ yel_p) - pink_p - blue_p
        base = core - pink_p - blue_p - yel_p
        shell = part - core

        zones = {'CASCA': shell, 'BASE20': base, 'AMARELO30': yellow, 'AZUL50': blue, 'ROSA70': pink}
        rec = {'source': fn, 'part_cm3': round(vol(part), 2), 'core_cm3': round(vol(core), 2),
               'zones_cm3': {k: round(vol(v), 2) for k, v in zones.items()}, 'paths_xy_mm': paths}
        rec['partition_sum_cm3'] = round(sum(rec['zones_cm3'].values()), 2)
        rec['partition_error_pct'] = round(100 * abs(rec['partition_sum_cm3'] - rec['part_cm3']) / rec['part_cm3'], 4)
        # Verificação: nenhum modificador fora da peça
        outside = {k: round(vol(v - part), 4) for k, v in {'ROSA70': pink, 'AZUL50': blue, 'AMARELO30': yellow}.items()}
        rec['modifier_volume_outside_part_cm3'] = outside
        for k, v in zones.items():
            tm = to_trimesh(v)
            tm.export(OUT / f'{name}_FEA_{k}.stl')
            if k in ('ROSA70', 'AZUL50', 'AMARELO30'):
                tm.export(OUT / f'{name}_MOD_{k[:-2]}_{k[-2:]}.stl')
        report['parts'][name] = rec
        print(name, json.dumps(rec['zones_cm3']), 'outside', outside, 'err%', rec['partition_error_pct'])
    (OUT / 'r06_zonas.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
