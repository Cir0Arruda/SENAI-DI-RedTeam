"""R07 - Teste da UNIÃO das peças (superior + inferior direita) num único modelo FE por voxels.

As duas grades de voxels (caches do r07_projeto e do r07_inferior, mesmo sistema de coordenadas do CAD)
são coladas numa grade comum (desalinhamento de arredondamento <= 0,375 mm). Cada peça mantém sua
própria casca de 5 paredes, porque a classificação é feita peça a peça antes de unir.
Contorno: engaste nos 6 furos da flange do robô (peça superior); carga -Z nas 4 bases de ventosa
da asa direita (inferior). A inferior esquerda não recebe carga neste caso e fica fora do modelo.
HIPÓTESE da junta: interface parafusada tratada como COLADA (continuidade de voxels): mais rígida que
a real; não mostra abertura/escorregamento da junta.
Saída: 06_Engenharia/R07/MONTAGEM/montagem_<variante>.json, mapa PNG e montagem_resumo.json.
Uso: python r07_montagem.py [R06 R07_COM R07_SEM UNI_30 UNI_35 UNI_40]
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
import r07_projeto as p  # noqa: E402
import r07_inferior as q  # noqa: E402
import r07_validar as val  # noqa: E402

OUT = v.OUT / 'MONTAGEM'; OUT.mkdir(exist_ok=True)
H = 3.0; G = p.G; A = p.A_EXTRA
PICO = 2.2
if '--pico' in sys.argv:
    PICO = float(sys.argv[sys.argv.index('--pico') + 1])


def pairs():
    D = p.designs()
    uni = lambda tag, x: v.Design(tag, base_phi=x, wall_mm=2.25)
    return {'R06': (D['R06'], q.r06()),
            'R07_COM': (D['F25_COM'], q.VAR['INF_F20_COM']()),
            'R07_SEM': (D['F25_SEM'], q.VAR['INF_F20_SEM']()),
            'UNI_30': (uni('U30', 0.30), uni('IU30', 0.30)),
            'UNI_35': (uni('U35', 0.35), uni('IU35', 0.35)),
            'UNI_40': (uni('U40', 0.40), uni('IU40', 0.40))}


class Combo:
    def __init__(self):
        self.mu = p.load_model(); self.ml = q.load_model()
        mu, ml = self.mu, self.ml; F = mu.FINE; n = mu.n
        o = np.round((ml.lo - mu.lo) / F).astype(int)          # origem da inferior em células finas da superior
        lo_cells = np.minimum(0, o); lo_cells = (np.floor(lo_cells / n) * n).astype(int)
        hi_cells = np.maximum(np.array(mu.fine.shape), o + np.array(ml.fine.shape))
        shape_f = (np.ceil((hi_cells - lo_cells) / n) * n).astype(int)
        self.ou = -lo_cells; self.ol = o - lo_cells; self.shape_f = shape_f
        self.err_mm = float(np.abs((ml.lo - mu.lo) / F - o).max() * F)
        m = v.Model.__new__(v.Model)
        m.H = H; m.n = n; m.FINE = F; m.lo = mu.lo + lo_cells * F; m.shape = shape_f // n; m.mesh = mu.mesh
        self.m = m

    def paste(self, big, small, off):
        sl = tuple(slice(off[i], off[i] + small.shape[i]) for i in range(3))
        return sl

    def label(self, du, dl):
        lu = self.mu.classify(du); ll = self.ml.classify(dl)
        mass = {'superior_g': round(self.mu.mass_g(lu)[0], 1), 'inferior_g': round(self.ml.mass_g(ll)[0], 1)}
        lab = np.full(tuple(self.shape_f), -1.0, np.float32)
        own = np.zeros(tuple(self.shape_f), np.int8)
        su = self.paste(lab, lu, self.ou); lab[su] = lu; own[su][lu >= 0] = 1
        sl = self.paste(lab, ll, self.ol)
        sub = lab[sl]; take = (ll >= 0) & (sub < 0)
        sub[take] = ll[take]; lab[sl] = sub
        osub = own[sl]; osub[take] = 2; own[sl] = osub
        return lab, own, mass


def evaluate(c: Combo, name, du, dl, kgs=(24.0, 30.0)):
    t0 = time.time()
    lab, own, mass = c.label(du, dl)
    m = c.m
    loads = {f'ONE_{int(k)}': q.foot_load(k * (G + A), c.ml) for k in kgs}
    res = m.solve(lab, loads, val.fixed_fn_factory(c.mu, H), tag=name)
    L = m.last; n = m.n; S = m.shape
    ow = own.reshape(S[0], n, S[1], n, S[2], n)
    up = (ow == 1).sum(axis=(1, 3, 5)); lo_ = (ow == 2).sum(axis=(1, 3, 5))
    owner = np.where(up >= lo_, 1, 2)[tuple(L['ei'].T)]
    cen = m.lo + (L['ei'] + 0.5) * H
    out = {'variante': name, 'massa_FE_g': mass, 'desalinhamento_grade_mm': round(c.err_mm, 3), 'casos': {}}
    for k, r in res.items():
        U = r['U']; eps, st = m.stresses(U)
        sig, fr = st[1.0]; has = fr > 0.05
        fxy, fz = v.failure_indices(sig)
        inf = 0.0
        for cl, (s, f) in st.items():
            if cl < 0.999 and (f > 0.05).any():
                inf = max(inf, float((v.vm(s[f > 0.05]) / v.infill_strength(cl)).max()))
        disp = np.linalg.norm(U.reshape(-1, 3), axis=1)
        rec = {'desl_max_mm': round(float(disp.max()), 3), 'reacao_N': r['reaction'].round(1).tolist()}
        for tag, w in (('superior', 1), ('inferior', 2)):
            sel = has & (owner == w)
            i = np.argmax(np.where(sel, fz, 0))
            rec[f'FI_z_{tag}'] = round(float(fz[sel].max()), 4)
            rec[f'FI_xy_{tag}'] = round(float(fxy[sel].max()), 4)
            rec[f'hot_{tag}'] = cen[i].round(1).tolist()
        rec['FI_giroide_max'] = round(inf, 4)
        out['casos'][k] = rec
        if k == 'ONE_24':
            fi = np.where(has, np.maximum(fxy, fz), 0)
            fig, axs = plt.subplots(1, 2, figsize=(14, 6), layout='constrained')
            o = np.argsort(fi)
            for ax, (a, b, ttl) in zip(axs, ((0, 1, 'planta (XY)'), (1, 2, 'vista lateral (YZ)'))):
                sc = ax.scatter(cen[o, a], cen[o, b], c=fi[o], s=3, cmap='inferno', vmin=0, vmax=max(0.05, fi.max()))
                ax.set_aspect('equal'); ax.set_title(f'{name} · 24 kg numa asa · {ttl}')
            fig.colorbar(sc, ax=axs, label='índice de falha do sólido (voxel, sem fator de pico)')
            fig.savefig(OUT / f'mapa_montagem_{name}.png', dpi=90); plt.close(fig)
    c24 = out['casos']['ONE_24']; F24 = 24 * (G + A)
    gov = max(c24['FI_z_superior'], c24['FI_z_inferior'])
    out['peca_critica'] = 'superior' if c24['FI_z_superior'] >= c24['FI_z_inferior'] else 'inferior'
    out['rigidez_asa_montada_N_mm'] = round(F24 / c24['desl_max_mm'], 1)
    out['sigma_Z_24kg_MPa_(x PICO)'] = round(gov * 48 * PICO, 2)
    for mat, S in (('PA6-CF_Z48', 48.0), ('PAHT_CF15_Z18.2', 18.2)):
        Fmax = S / (gov * 48 * PICO / F24)
        out[f'kg_max_{mat}'] = round(Fmax / (G + A), 1)
        out[f'FS_24kg_{mat}'] = round(Fmax / F24, 2)
        out[f'FS_30kg_{mat}'] = round(Fmax / (30 * (G + A)), 2)
    out['PICO'] = PICO; out['tempo_s'] = round(time.time() - t0, 1)
    (OUT / f'montagem_{name}.json').write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False), flush=True)
    return out


if __name__ == '__main__':
    P = pairs()
    keys = [a for a in sys.argv[1:] if not a.startswith('--') and a in P] or list(P)
    c = Combo()
    resf = OUT / 'montagem_resumo.json'
    res = json.loads(resf.read_text(encoding='utf-8')) if resf.exists() else {}
    for k in keys:
        res[k] = evaluate(c, k, *P[k])
        resf.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding='utf-8')
