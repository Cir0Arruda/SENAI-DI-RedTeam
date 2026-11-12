"""R07 - Impacto/tranco TRANSIENTE 3D (FE por voxels + Newmark) da peça superior: com x sem esqueleto x uniforme.

Cenário (HIPÓTESE, rotulado): as duas caixas (24 kg) ficam presas numa asa e a carga entra em TR_MS
(enganchão / parada de emergência seca): F(t) = 24 kg x (g + 5 m/s²) x min(1, t/TR). A massa de 24 kg fica
pendurada nos ressaltos da asa direita (massa concentrada), a peça tem sua própria massa (densidade x fração).
Integração implícita de Newmark (aceleração média), amortecimento de Rayleigh ZETA nas frequências f1 e 10 f1.
Mesmos voxels, engaste (6 furos da flange) e materiais homogeneizados do r07_projeto.

Saídas (06_Engenharia/R07/IMPACTO/):
  impacto_<variante>.json   histórico de deslocamento, índices de falha (sólido Z/XY, giroide) e pico
  impacto_comparativo.mp4   animação: corte vertical cubo->asa, deformada ampliada, cor = índice de falha
  impacto_curvas.png        tensão entre camadas no ponto crítico x tempo
LIMITES: linear-elástico (sem dano progressivo/ruptura), giroide homogeneizado, sem contato.
Uso: python r07_impacto.py [VARIANTES...]
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import pyamg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import animation
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r07_vfe as v  # noqa: E402
import r07_projeto as p  # noqa: E402
import r07_validar as val  # noqa: E402

OUT = v.OUT / 'IMPACTO'; OUT.mkdir(exist_ok=True)
H = p.H
KG = 24.0
F24 = KG * (p.G + p.A_EXTRA)
TR_MS = 10.0          # tempo de subida da carga (enganchão seco)
T_END_MS = 80.0
DT_MS = 0.5
ZETA = 0.03
PICO = 2.2            # pico real / pico voxel (calibrado no Fusion R06)
MAG = 25.0            # ampliação da deformada no vídeo
RHO_T = v.MAT['rho'] * 1e-6   # g/mm³ -> t/mm³ (unidades N, mm, s)

LABEL = {'F25_COM': 'R07 COM esqueleto (giroide 25% + zonas)', 'F25_SEM': 'R07 SEM esqueleto (mesmas zonas)',
         'UNI_30': 'Uniforme giroide 30% (sem esqueleto/zonas)', 'UNI_40': 'Uniforme giroide 40% (sem esqueleto/zonas)',
         'R06': 'R06 (TPMS-D zonal)'}


def design(name):
    if name.startswith('UNI_'):
        return v.Design(name, base_phi=int(name[4:]) / 100, wall_mm=2.25)
    return p.designs()[name]


def run(m, name):
    d = design(name)
    lab = m.classify(d)
    mass_g = m.mass_g(lab)[0]
    zmin = m.mesh.bounds[0, 2]
    load = val.load_fn(['R1', 'R2'], F24, H, zmin)
    st = m.solve(lab, {'static': load}, val.fixed_fn_factory(m, H), tag=name)['static']
    L = m.last; K = L['K']; X = L['X']; nn = L['nn']; ndof = 3 * nn
    # massa concentrada: elemento -> 1/8 por nó (densidade x fração de cada classe)
    dens = np.array([1.0 if c >= 0.999 else c for c in L['classes']])
    me = (L['Fe'] @ dens) * RHO_T * H ** 3
    mn = np.bincount(L['enodes'].ravel(), np.repeat(me / 8, 8), minlength=nn)
    payload = val.boss_nodes(X, ['R1', 'R2'], H, zmin)
    mn[payload] += (KG / 1000) / payload.sum()          # 24 kg = 0,024 t distribuída nos nós de apoio da caixa
    Mdiag = np.repeat(mn, 3)
    fixed = val.fixed_fn_factory(m, H)(X)
    fd = (3 * np.where(fixed)[0][:, None] + np.arange(3)).ravel()
    free = np.setdiff1d(np.arange(ndof), fd)
    Kf = K[free][:, free].tocsr(); Mf = Mdiag[free]
    f_static = load(X, nn)[free]
    # frequência fundamental (Rayleigh com a deformada estática) -> amortecimento
    u0 = st['U'][free]
    w1 = np.sqrt((u0 @ (Kf @ u0)) / (u0 @ (Mf * u0)))
    w2 = 10 * w1
    a0 = 2 * ZETA * w1 * w2 / (w1 + w2); a1 = 2 * ZETA / (w1 + w2)
    dt = DT_MS / 1000
    c_k = 1 + 2 * a1 / dt; c_m = 4 / dt ** 2 + 2 * a0 / dt
    Keff = (c_k * Kf + sp.diags(c_m * Mf)).tocsr()
    Bn = np.zeros((ndof, 6)); cX = X - X.mean(0)
    Bn[0::3, 0] = 1; Bn[1::3, 1] = 1; Bn[2::3, 2] = 1
    Bn[0::3, 3] = -cX[:, 1]; Bn[1::3, 3] = cX[:, 0]; Bn[1::3, 4] = -cX[:, 2]; Bn[2::3, 4] = cX[:, 1]
    Bn[0::3, 5] = cX[:, 2]; Bn[2::3, 5] = -cX[:, 0]
    Mpre = pyamg.smoothed_aggregation_solver(Keff, B=Bn[free], max_coarse=2000).aspreconditioner()
    # elementos e corte vertical cubo -> asa direita
    cen = m.lo + (L['ei'] + 0.5) * H
    W = np.array([-478.33, 283.0]); hub = np.array(p.HUB)
    dvec = (W - hub) / np.linalg.norm(W - hub); nvec = np.array([-dvec[1], dvec[0]])
    rel = cen[:, :2] - hub
    sec = np.where(np.abs(rel @ nvec) <= 0.5 * H + 1e-6)[0]
    s_sec = rel[sec] @ dvec; z_sec = cen[sec, 2]
    solid_frac = L['Fe'][:, L['classes'].index(1.0)]
    u = np.zeros(len(free)); vel = np.zeros_like(u); acc = np.zeros_like(u)
    nsteps = int(round(T_END_MS / DT_MS))
    hist = {'t_ms': [], 'disp_mm': [], 'FI_z': [], 'FI_xy': [], 'FI_giroide': [], 'F_N': []}
    frames = []
    C3 = '--campos3d' in sys.argv
    f3 = {'t': [], 'fi_s': [], 'fi_g': [], 'ue': [], 'E_sol': [], 'E_gir': [], 'e_el': []}
    U = np.zeros(ndof)
    t0 = time.time()
    for k in range(1, nsteps + 1):
        t = k * dt
        F = f_static * min(1.0, t / (TR_MS / 1000))
        # Newmark aceleração média (beta 1/4, gama 1/2) com Rayleigh
        # (K + 4/dt² M + 2/dt C) u' = F + M(4/dt² u + 4/dt v + a) + C(2/dt u + v),  C = a0 M + a1 K
        rhs = F + Mf * (c_m * u + (4 / dt + a0) * vel + acc) + a1 * (Kf @ (2 / dt * u + vel))
        un, info = spla.cg(Keff, rhs, x0=u, rtol=1e-7, M=Mpre, maxiter=500)
        an = 4 / dt ** 2 * (un - u) - 4 / dt * vel - acc
        vn = vel + dt / 2 * (acc + an)
        u, vel, acc = un, vn, an
        U[free] = u
        eps, stc = m.stresses(U)
        fz_all = np.zeros(len(cen)); fxy_all = np.zeros(len(cen)); finf = np.zeros(len(cen))
        for c, (sig, fr) in stc.items():
            if c >= 0.999:
                a, b = v.failure_indices(sig); has = fr > 0.05
                fxy_all = np.where(has, a, 0); fz_all = np.where(has, b, 0)
            else:
                has = fr > 0.05
                finf = np.maximum(finf, np.where(has, v.vm(sig) / v.infill_strength(c), 0))
        disp = np.linalg.norm(U.reshape(-1, 3), axis=1)
        hist['t_ms'].append(round(t * 1000, 2)); hist['disp_mm'].append(float(disp[payload].mean()))
        hist['FI_z'].append(float(fz_all.max())); hist['FI_xy'].append(float(fxy_all.max()))
        hist['FI_giroide'].append(float(finf.max())); hist['F_N'].append(round(F24 * min(1.0, t / (TR_MS / 1000)), 1))
        if C3 and k % 2 == 0:   # campos 3D por voxel (vídeos): índice de falha sólido/giroide e energia de deformação por classe
            es = np.zeros(len(cen)); eg = np.zeros(len(cen))
            for c, (sig, fr) in stc.items():
                w = 0.5 * (sig * eps).sum(1) * fr * H ** 3          # N·mm = mJ
                if c >= 0.999:
                    es += w
                else:
                    eg += w
            f3['t'].append(t * 1000); f3['fi_s'].append(np.maximum(fz_all, fxy_all).astype(np.float16))
            f3['fi_g'].append(finf.astype(np.float16)); f3['ue'].append(U[L['edofs']].reshape(-1, 8, 3).mean(1).astype(np.float16))
            f3['E_sol'].append(float(es.sum())); f3['E_gir'].append(float(eg.sum())); f3['e_el'].append((es + eg).astype(np.float16))
        if k % 2 == 0:
            ue = U[L['edofs']].reshape(-1, 8, 3).mean(1)[sec]
            fi = np.maximum(np.maximum(fz_all, fxy_all), finf)[sec]
            frames.append((t * 1000, (ue[:, :2] @ dvec), ue[:, 2], fi.astype(np.float32)))
        if k % 20 == 0:
            print(f'[{name}] {t*1000:.1f} ms  disp {hist["disp_mm"][-1]:.3f} mm  FI_z {hist["FI_z"][-1]:.3f}  ({time.time()-t0:.0f}s)', flush=True)
    st_fz = float(v.failure_indices(m.stresses(st['U'])[1][1.0][0])[1][solid_frac > 0.05].max())
    i = int(np.argmax(hist['FI_z']))
    rec = {'variante': name, 'rotulo': LABEL.get(name, name), 'massa_FE_g': round(mass_g, 1),
           'f1_Hz_com_24kg': round(w1 / 2 / np.pi, 1), 'TR_ms': TR_MS, 'zeta': ZETA,
           'FI_z_estatico': round(st_fz, 4), 'FI_z_pico_dinamico': round(hist['FI_z'][i], 4), 't_pico_ms': hist['t_ms'][i],
           'fator_dinamico_3D': round(hist['FI_z'][i] / st_fz, 2),
           'sigma_Z_pico_MPa_(x PICO)': round(hist['FI_z'][i] * 48 * PICO, 2),
           'FI_giroide_pico': round(max(hist['FI_giroide']), 4),
           'desl_pico_mm': round(max(hist['disp_mm']), 3),
           'FS_dinamico_PA6CF_Z48': round(48 / (hist['FI_z'][i] * 48 * PICO), 2),
           'FS_dinamico_PAHT_Z18.2': round(18.2 / (hist['FI_z'][i] * 48 * PICO), 2),
           'hist': hist}
    (OUT / f'impacto_{name}.json').write_text(json.dumps(rec, ensure_ascii=False), encoding='utf-8')
    np.savez_compressed(OUT / f'frames_{name}.npz', s=s_sec, z=z_sec,
                        t=np.array([f[0] for f in frames]), us=np.array([f[1] for f in frames]),
                        uz=np.array([f[2] for f in frames]), fi=np.array([f[3] for f in frames]),
                        lab=np.array([1.0 if solid_frac[j] > 0.5 else 0.0 for j in sec]))
    if C3:
        np.savez_compressed(OUT / f'campos3d_{name}.npz', cen=cen.astype(np.float32), solid_frac=solid_frac.astype(np.float32),
                            **{k_: np.array(v_) for k_, v_ in f3.items()}, H=H, PICO=PICO, TR_MS=TR_MS)
    print(json.dumps({k: v_ for k, v_ in rec.items() if k != 'hist'}, ensure_ascii=False), flush=True)
    return rec


def video(names):
    data = {n: np.load(OUT / f'frames_{n}.npz') for n in names}
    recs = {n: json.loads((OUT / f'impacto_{n}.json').read_text(encoding='utf-8')) for n in names}
    nf = min(len(d['t']) for d in data.values())
    SHORT = {'F25_COM': 'R07 COM esqueleto', 'F25_SEM': 'R07 SEM esqueleto',
             'UNI_30': 'Giroide 30% uniforme', 'UNI_40': 'Giroide 40% uniforme'}
    fig = plt.figure(figsize=(16, 9), dpi=100)
    nc = 2 if len(names) == 4 else len(names)
    nr = (len(names) + nc - 1) // nc
    gs = fig.add_gridspec(nr + 1, nc + 1, height_ratios=[1] * nr + [0.85], width_ratios=[1] * nc + [0.03],
                          hspace=0.42, wspace=0.08, left=0.06, right=0.95, top=0.9, bottom=0.07)
    axs = [fig.add_subplot(gs[i // nc, i % nc]) for i in range(len(names))]
    cax = fig.add_subplot(gs[0:nr, nc])
    axc = fig.add_subplot(gs[nr, 0:nc])
    vmax = 0.5
    scs = []
    for ax, n in zip(axs, names):
        d = data[n]; r = recs[n]
        sc = ax.scatter(d['s'], d['z'], c=d['fi'][0], s=60, marker='s', cmap='viridis', vmin=0, vmax=vmax)
        ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
        pad = 0.08 * (d['s'].max() - d['s'].min())
        ax.set_xlim(d['s'].min() - pad, d['s'].max() + pad); ax.set_ylim(d['z'].min() - pad, d['z'].max() + pad)
        ax.set_title(f"{SHORT.get(n, n)}  ·  {r['massa_FE_g']:.0f} g (modelo)\n"
                     f"pico σZ {r['sigma_Z_pico_MPa_(x PICO)']:.1f} MPa · FS PA6-CF {r['FS_dinamico_PA6CF_Z48']:.2f} · "
                     f"FS PAHT {r['FS_dinamico_PAHT_Z18.2']:.2f}", fontsize=10)
        scs.append(sc)
    fig.colorbar(scs[-1], cax=cax, label='índice de falha local (1 = ruptura)')
    lines = {}
    for n in names:
        h = recs[n]['hist']
        lines[n], = axc.plot(h['t_ms'], np.array(h['FI_z']) * 48 * PICO, label=SHORT.get(n, n), lw=2)
    axc.axhline(18.2, ls='--', c='0.4', lw=1); axc.text(1, 18.7, 'Z PAHT CF15 (18,2 MPa)', fontsize=8, color='0.3')
    axc.set_xlabel('tempo (ms)'); axc.set_ylabel('σ entre camadas\nno ponto crítico (MPa)'); axc.legend(fontsize=9, loc='upper right', ncol=2)
    cur = axc.axvline(0, c='k', lw=1)
    ttl = fig.suptitle('', fontsize=12)

    def upd(i):
        for sc, n in zip(scs, names):
            d = data[n]
            sc.set_offsets(np.c_[d['s'] + MAG * d['us'][i], d['z'] + MAG * d['uz'][i]])
            sc.set_array(d['fi'][i])
        t = data[names[0]]['t'][i]; cur.set_xdata([t, t])
        ttl.set_text(f'Tranco de 24 kg numa asa em {TR_MS:.0f} ms (massa da caixa presa) · t = {t:5.1f} ms · '
                     f'deformada ×{MAG:.0f} · corte vertical cubo → asa · FE por voxels (estimativa)')
        return scs
    ani = animation.FuncAnimation(fig, upd, frames=nf, interval=100)
    ani.save(OUT / 'impacto_comparativo.mp4', writer=animation.FFMpegWriter(fps=10, bitrate=4000))
    upd(int(np.argmax(recs[names[0]]['hist']['FI_z']) // 2))
    fig.savefig(OUT / 'impacto_pico.png', dpi=100)
    plt.close(fig)


if __name__ == '__main__':
    names = [a for a in sys.argv[1:] if not a.startswith('--')] or ['F25_COM', 'F25_SEM', 'UNI_30', 'UNI_40']
    if '--so-video' not in sys.argv:
        m = p.load_model()
        for n in names:
            run(m, n)
    if '--campos3d' not in sys.argv:   # só campos: não sobrescreve o vídeo comparativo de 4 variantes
        video(names)
