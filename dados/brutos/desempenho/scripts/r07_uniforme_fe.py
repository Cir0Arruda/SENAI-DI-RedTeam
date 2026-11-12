"""R07 - FE por voxels das variantes de preenchimento UNIFORME (sem esqueleto, sem zonas), peças superior e inferior.

Mesmo modelo, mesma malha, mesmas cargas e engastes do r07_projeto / r07_inferior, só muda o núcleo:
toda a peça = 5 paredes (2,25 mm) + preenchimento homogêneo phi (Gibson-Ashby E*phi^2).
LIMITE: a lei homogeneizada não distingue giroide, 3D honeycomb e TPMS-D com a mesma densidade.
Saídas: 06_Engenharia/R07/UNI_<pct>.json (superior) e INF_UNI_<pct>.json (inferior).
Uso: python r07_uniforme_fe.py [30 35 40]
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r07_vfe as v  # noqa: E402
import r07_projeto as p  # noqa: E402
import r07_inferior as q  # noqa: E402

if __name__ == '__main__':
    pcts = [int(a) for a in sys.argv[1:]] or [30, 35, 40]
    m = p.load_model()
    for pct in pcts:
        p.evaluate(m, v.Design(f'UNI_{pct}', base_phi=pct / 100, wall_mm=2.25), plot=True)
    del m
    mi = q.load_model()
    for pct in pcts:
        q.evaluate(mi, v.Design(f'INF_UNI_{pct}', base_phi=pct / 100, wall_mm=2.25))
