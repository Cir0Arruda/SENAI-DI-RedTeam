"""R07 - Vídeos de simulação feitos SÓ com campos já calculados (nenhum resultado novo é inventado).

  carga    "Uma asa pega os 24 kg de uma vez": garra MONTADA (superior + inferior direita), carga subindo de 0 a
           24 kg numa asa. Campos de r07_montagem.py --campos (FE estático linear: o campo escala com o peso).
  impacto  "Como o tranco se distribui": peça superior, carga de 24 kg aplicada em 10 ms (FE transiente),
           índice de falha local voxel a voxel ao longo do tempo. Campos de r07_impacto.py --campos3d.
  absorcao "Como a malha interna absorve": parcela da energia de deformação guardada no giroide × no sólido
           (casca + esqueleto) durante o tranco, e o giroide trabalhando. Mesmos campos do impacto.

Vista oblíqua em "raio X": cada voxel de 3 mm é um ponto; os mais solicitados são desenhados por cima.
Saída: 06_Engenharia/R07/VIDEOS/<nome>.mp4 + _poster.jpg ; resumo em videos_r07.json
Uso: python r07_videos.py [carga impacto absorcao]
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.colors import LinearSegmentedColormap

O = Path(__file__).resolve().parents[1]
R7 = O / '06_Engenharia' / 'R07'
OUT = R7 / 'VIDEOS'; OUT.mkdir(exist_ok=True)
FPS = 24
W, H_PX, DPI = 12.8, 7.2, 100
CMAP = LinearSegmentedColormap.from_list('fi', ['#d9dbe4', '#9fb4d8', '#f2c14e', '#e8590c', '#b91c1c', '#5a0a0a'])
G_A = 9.81 + 5.0
INK, MUTED = '#15151d', '#5d5f70'
RES = {}


def proj(P, az=-58, el=24):
    """Projeção oblíqua: devolve (x_tela, y_tela, profundidade)."""
    a, e = np.radians(az), np.radians(el)
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    xr = x * np.cos(a) - y * np.sin(a)
    yr = x * np.sin(a) + y * np.cos(a)
    return xr, z * np.cos(e) + yr * np.sin(e), yr * np.cos(e) - z * np.sin(e)


plt.rcParams.update({'font.family': 'DejaVu Sans'})


def cloud(ax, P, val, vmax, s=4.0):
    """Nuvem de voxels ordenada por valor (quentes por cima)."""
    o = np.argsort(val)
    xs, ys, _ = proj(P[o])
    k = np.clip(val[o] / vmax, 0, 1)
    col = CMAP(k); col[:, 3] = 0.10 + 0.90 * np.clip(k * 1.6, 0, 1)
    return ax.scatter(xs, ys, c=col, s=s, linewidths=0, rasterized=True)


def save(anim, fig, name, poster_t):
    teste = [int(x) for x in os.environ.get('VID_TESTE', '').split(',') if x.strip()]
    if teste:  # só quadros de conferência, sem mp4
        for i in teste:
            anim._func(i); fig.savefig(OUT / f'_teste_{name}_{i}.png', dpi=DPI, facecolor='white')
        plt.close(fig); return
    mp4 = OUT / f'{name}.mp4'
    anim.save(mp4, writer=animation.FFMpegWriter(fps=FPS, codec='libx264', bitrate=3500,
                                                  extra_args=['-pix_fmt', 'yuv420p', '-movflags', '+faststart']), dpi=DPI)
    anim._func(poster_t)
    fig.savefig(OUT / f'{name}_poster.jpg', dpi=DPI, facecolor='white')
    plt.close(fig)
    print(mp4, flush=True)


# ---------------------------------------------------------------- 24 kg numa asa (garra montada)
def video_carga():
    V = [('R07_COM', 'R07 com esqueleto'), ('R07_SEM', 'R07 sem esqueleto'), ('UNI_30', 'Giroide 30% uniforme')]
    D, J = {}, {}
    for k, _ in V:
        z = np.load(R7 / 'MONTAGEM' / f'campos_{k}_ONE_24.npz')
        D[k] = {n: z[n] for n in z.files}
        J[k] = json.loads((R7 / 'MONTAGEM' / f'montagem_{k}.json').read_text(encoding='utf-8'))
    PICO = float(D['R07_COM']['PICO'])
    MAG = 15.0
    # índice entre camadas × pico, relativo ao PA6-CF (48 MPa): 1 = rompe; escala comum
    vmax = 0.40
    allP = np.vstack([D[k]['cen'] for k, _ in V])
    X0, Y0, _ = proj(allP)
    xl = (X0.min() - 25, X0.max() + 25); yl = (Y0.min() - 30, Y0.max() + 35)
    nramp, nhold = FPS * 6, FPS * 3
    N = nramp + nhold
    fig = plt.figure(figsize=(W, H_PX), dpi=DPI)
    fig.patch.set_facecolor('white')
    fig.text(0.03, 0.94, 'Uma asa pega os 24 kg de uma vez', fontsize=21, fontweight='bold', color=INK)
    fig.text(0.03, 0.905, 'Erro da seladora: as duas caixas numa asa só · garra montada (superior + inferior) · carga de 0 a 24 kg',
             fontsize=11.5, color=MUTED)
    axs = [fig.add_axes([0.01 + i * 0.33, 0.27, 0.32, 0.60]) for i in range(3)]
    for ax in axs:
        ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect('equal'); ax.axis('off')
    cax = fig.add_axes([0.30, 0.115, 0.40, 0.022])
    sm = plt.cm.ScalarMappable(cmap=CMAP, norm=plt.Normalize(0, vmax))
    cb = fig.colorbar(sm, cax=cax, orientation='horizontal')
    cb.set_label('tensão entre camadas ÷ resistência do PA6-CF (pico × 2,2) · 1 = rompe', fontsize=9.5, color=MUTED)
    cb.ax.tick_params(labelsize=8.5)
    fig.text(0.03, 0.025, 'FE por voxels de 3 mm, linear-elástico · giroide homogeneizado (Gibson-Ashby) · pico × 2,2 (calibrado no Fusion R06) · '
             f'junta tratada como colada · deformada ampliada {MAG:.0f}×. Estimativa, não é ensaio.', fontsize=8.6, color=MUTED)
    titles, info, badge, scs = [], [], [], [None] * 3
    arrows = [None] * 3
    tip = {k: int(np.argmax(np.linalg.norm(D[k]['U'], axis=1))) for k, _ in V}
    for ax, (k, rot) in zip(axs, V):
        titles.append(ax.text(0.5, 1.02, rot, transform=ax.transAxes, ha='center', fontsize=14, fontweight='bold', color=INK))
        info.append(ax.text(0.5, -0.09, '', transform=ax.transAxes, ha='center', va='top', fontsize=10.5, color=INK, linespacing=1.5))
        badge.append(ax.text(0.5, 0.93, '', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold'))
    kgtxt = fig.text(0.97, 0.94, '', fontsize=24, fontweight='bold', color='#c2410c', ha='right')

    def frame(i):
        f = min(1.0, (i + 1) / nramp)
        f = 1 - (1 - f) ** 2 if i < nramp else 1.0
        kg = 24.0 * f
        kgtxt.set_text(f'{kg:4.1f} kg'.replace('.', ','))
        for j, (ax, (k, rot)) in enumerate(zip(axs, V)):
            d = D[k]
            if scs[j] is not None:
                scs[j].remove()
            fi = d['fi_z'] * PICO * f
            scs[j] = cloud(ax, d['cen'] + d['U'] * MAG * f, fi, vmax, s=3.2)
            if arrows[j] is not None:
                arrows[j].remove()
            px, py, _ = proj((d['cen'][tip[k]] + d['U'][tip[k]] * MAG * f)[None])
            arrows[j] = ax.annotate(f'{kg:.0f} kg'.replace('.', ','), xy=(px[0], py[0]), xytext=(px[0], py[0] - 14 - 18 * f),
                                    ha='left', va='center', fontsize=11, fontweight='bold', color='#c2410c',
                                    arrowprops=dict(arrowstyle='<-', color='#c2410c', lw=2.2, relpos=(0, 0.5), shrinkA=0, shrinkB=2), zorder=10)
            fs_pa6 = J[k]['kg_max_PA6-CF_Z48'] / max(kg, 1e-6)
            fs_paht = J[k]['kg_max_PAHT_CF15_Z18.2'] / max(kg, 1e-6)
            dmax = J[k]['casos']['ONE_24']['desl_max_mm'] * f
            fsx = lambda v: '—' if kg < 0.5 else f'{v:.2f}'.replace('.', ',')
            info[j].set_text(f'FS PA6-CF {fsx(fs_pa6)}   ·   FS PAHT CF15 {fsx(fs_paht)}\n'
                             f'flecha {dmax:.2f} mm   ·   aguenta até {J[k]["kg_max_PA6-CF_Z48"]:.0f} kg'.replace('.', ','))
            if i >= nramp - 1:
                ok = J[k]['FS_24kg_PAHT_CF15_Z18.2'] >= 1
                badge[j].set_text('✓ aguenta 24 kg (PA6-CF e PAHT)' if ok else '✓ PA6-CF aguenta · ⚠ PAHT rompe')
                badge[j].set_color('#17784f' if ok else '#b42318')
            else:
                badge[j].set_text('')
        return []

    anim = animation.FuncAnimation(fig, frame, frames=N, blit=False)
    save(anim, fig, 'carga_24kg_asa', N - 1)
    RES['carga_24kg_asa'] = {k: {'kg_max_PA6CF': J[k]['kg_max_PA6-CF_Z48'], 'kg_max_PAHT': J[k]['kg_max_PAHT_CF15_Z18.2'],
                                 'FS24_PA6CF': J[k]['FS_24kg_PA6-CF_Z48'], 'FS24_PAHT': J[k]['FS_24kg_PAHT_CF15_Z18.2'],
                                 'desl24_mm': J[k]['casos']['ONE_24']['desl_max_mm']} for k, _ in V}


# ---------------------------------------------------------------- impacto (peça superior, campos 3D no tempo)
def load3d(names):
    D = {}
    for k in names:
        z = np.load(R7 / 'IMPACTO' / f'campos3d_{k}.npz')
        D[k] = {n: z[n] for n in z.files}
        D[k]['J'] = json.loads((R7 / 'IMPACTO' / f'impacto_{k}.json').read_text(encoding='utf-8'))
    return D


def interp(arr, t, tk):
    """Interpola linearmente o campo (nf, ne) no instante tk."""
    j = int(np.clip(np.searchsorted(t, tk) - 1, 0, len(t) - 2))
    a = np.clip((tk - t[j]) / (t[j + 1] - t[j]), 0, 1)
    return arr[j].astype(np.float32) * (1 - a) + arr[j + 1].astype(np.float32) * a


def video_impacto():
    V = [('F25_COM', 'R07 com esqueleto'), ('F25_SEM', 'R07 sem esqueleto')]
    D = load3d([k for k, _ in V])
    MAG = 40.0
    vmax = 0.22
    t = D['F25_COM']['t']
    allP = np.vstack([D[k]['cen'] for k, _ in V])
    X0, Y0, _ = proj(allP, az=-40, el=26)
    xl = (X0.min() - 20, X0.max() + 20); yl = (Y0.min() - 25, Y0.max() + 25)
    N = FPS * 11
    tt = np.linspace(t[0], t[-1], N)
    fig = plt.figure(figsize=(W, H_PX), dpi=DPI); fig.patch.set_facecolor('white')
    fig.text(0.03, 0.94, 'Como o tranco de 24 kg se distribui', fontsize=21, fontweight='bold', color=INK)
    fig.text(0.03, 0.905, 'Peça superior · carga entra em 10 ms na asa direita · câmera lenta (80 ms em 11 s)', fontsize=11.5, color=MUTED)
    axs = [fig.add_axes([0.0 + i * 0.40, 0.25, 0.40, 0.60]) for i in range(2)]
    for ax in axs:
        ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect('equal'); ax.axis('off')
    axc = fig.add_axes([0.825, 0.30, 0.15, 0.50])
    for k, rot in V:
        h = D[k]['J']['hist']
        axc.plot(h['t_ms'], np.array(h['FI_z']) * 48 * 2.2, lw=2, color='#e5232f' if 'COM' in k else '#5b5bd6', label=rot.replace('R07 ', ''))
    axc.axhline(18.2, color=INK, lw=.8, ls='--'); axc.text(1, 18.7, 'limite PAHT 18,2', fontsize=8, ha='left', color=MUTED)
    axc.set_xlim(0, 80); axc.set_ylim(0, 22); axc.set_xlabel('ms', fontsize=9); axc.set_title('σZ no ponto crítico (MPa)', fontsize=9.5, color=INK)
    axc.tick_params(labelsize=8); axc.legend(fontsize=8.5, frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.16), ncol=1)
    for s_ in ('top', 'right'):
        axc.spines[s_].set_visible(False)
    cursor = axc.axvline(0, color=INK, lw=1)
    cax = fig.add_axes([0.20, 0.13, 0.40, 0.022])
    cb = fig.colorbar(plt.cm.ScalarMappable(cmap=CMAP, norm=plt.Normalize(0, vmax)), cax=cax, orientation='horizontal')
    cb.set_label('índice de falha local (voxel, sólido ou giroide · sem fator de pico)', fontsize=9.5, color=MUTED); cb.ax.tick_params(labelsize=8.5)
    fig.text(0.03, 0.035, 'FE transiente 3D (Newmark, Rayleigh 3%), voxels de 3 mm, giroide homogeneizado, massa de 24 kg nos ressaltos, '
             f'linear-elástico (sem dano). Deformada ampliada {MAG:.0f}×. Estimativa, não é ensaio.', fontsize=8.6, color=MUTED)
    ttl = [ax.text(0.5, 1.0, rot, transform=ax.transAxes, ha='center', fontsize=14, fontweight='bold', color=INK) for ax, (k, rot) in zip(axs, V)]
    sub = [ax.text(0.5, -0.02, '', transform=ax.transAxes, ha='center', va='top', fontsize=10.5, color=INK, linespacing=1.5) for ax in axs]
    clock = fig.text(0.97, 0.94, '', fontsize=22, fontweight='bold', color='#c2410c', ha='right')
    scs = [None, None]

    def frame(i):
        tk = tt[i]
        F = min(1.0, tk / 10.0) * 24.0
        clock.set_text(f'{tk:4.1f} ms · {F:4.1f} kg'.replace('.', ','))
        cursor.set_xdata([tk, tk])
        for j, (ax, (k, rot)) in enumerate(zip(axs, V)):
            d = D[k]
            fi = np.maximum(interp(d['fi_s'], d['t'], tk), interp(d['fi_g'], d['t'], tk))
            ue = interp(d['ue'].reshape(len(d['t']), -1), d['t'], tk).reshape(-1, 3)
            if scs[j] is not None:
                scs[j].remove()
            P = d['cen'] + ue * MAG
            o = np.argsort(fi); xs, ys, _ = proj(P[o], az=-40, el=26)
            kk = np.clip(fi[o] / vmax, 0, 1); col = CMAP(kk); col[:, 3] = 0.10 + 0.90 * np.clip(kk * 1.6, 0, 1)
            scs[j] = ax.scatter(xs, ys, c=col, s=5.5, linewidths=0, rasterized=True)
            h = d['J']['hist']; ii = int(np.argmin(np.abs(np.array(h['t_ms']) - tk)))
            sub[j].set_text(f'σZ crítico {h["FI_z"][ii] * 48 * 2.2:.1f} MPa · deslocamento {h["disp_mm"][ii]:.2f} mm\n'.replace('.', ',')
                            + f'giroide a {h["FI_giroide"][ii] * 100:.0f}% da própria resistência')
        return []

    anim = animation.FuncAnimation(fig, frame, frames=N, blit=False)
    tpk = int(np.argmin(np.abs(tt - D['F25_COM']['J']['t_pico_ms'])))
    save(anim, fig, 'impacto_distribuicao', tpk)
    RES['impacto_distribuicao'] = {k: {kk: D[k]['J'][kk] for kk in ('t_pico_ms', 'sigma_Z_pico_MPa_(x PICO)', 'FI_giroide_pico', 'desl_pico_mm',
                                                                       'FS_dinamico_PA6CF_Z48', 'FS_dinamico_PAHT_Z18.2', 'fator_dinamico_3D')} for k, _ in V}


def video_absorcao():
    V = [('F25_COM', 'R07 com esqueleto'), ('F25_SEM', 'R07 sem esqueleto')]
    D = load3d([k for k, _ in V])
    vmax = 0.30
    N = FPS * 11
    t = D['F25_COM']['t']; tt = np.linspace(t[0], t[-1], N)
    fig = plt.figure(figsize=(W, H_PX), dpi=DPI); fig.patch.set_facecolor('white')
    fig.text(0.03, 0.94, 'Como a malha interna absorve o tranco', fontsize=21, fontweight='bold', color=INK)
    fig.text(0.03, 0.905, 'Só os voxels de giroide (casca e almas ocultas) · cor = quanto da própria resistência o giroide usa',
             fontsize=11.5, color=MUTED)
    axs = [fig.add_axes([0.0 + i * 0.31, 0.27, 0.31, 0.58]) for i in range(2)]
    gm = {k: D[k]['solid_frac'] < 0.5 for k, _ in V}
    allP = np.vstack([D[k]['cen'][gm[k]] for k, _ in V])
    X0, Y0, _ = proj(allP, az=-40, el=26)
    for ax in axs:
        ax.set_xlim(X0.min() - 20, X0.max() + 20); ax.set_ylim(Y0.min() - 25, Y0.max() + 25); ax.set_aspect('equal'); ax.axis('off')
    axe = fig.add_axes([0.66, 0.30, 0.31, 0.50])
    pct = {}
    for k, rot in V:
        d = D[k]; E = d['E_sol'] + d['E_gir']
        pct[k] = np.where(E > 1e-9, d['E_gir'] / np.maximum(E, 1e-12) * 100, 0)
        axe.plot(d['t'], pct[k], lw=2.2, color='#e5232f' if 'COM' in k else '#5b5bd6', label=rot)
    axe.set_xlim(0, 80); axe.set_ylim(0, max(60, float(max(p.max() for p in pct.values())) * 1.15))
    axe.set_xlabel('tempo (ms)', fontsize=9.5); axe.set_title('energia de deformação guardada no giroide (% do total)', fontsize=10, color=INK)
    axe.tick_params(labelsize=8.5); axe.legend(fontsize=9, frameon=False, loc='lower right')
    for s_ in ('top', 'right'):
        axe.spines[s_].set_visible(False)
    cursor = axe.axvline(0, color=INK, lw=1)
    cax = fig.add_axes([0.12, 0.15, 0.40, 0.022])
    cb = fig.colorbar(plt.cm.ScalarMappable(cmap=CMAP, norm=plt.Normalize(0, vmax)), cax=cax, orientation='horizontal')
    cb.set_label('von Mises do giroide ÷ resistência do giroide (Gibson-Ashby)', fontsize=9.5, color=MUTED); cb.ax.tick_params(labelsize=8.5)
    fig.text(0.03, 0.035, 'FE transiente 3D, voxels de 3 mm, giroide homogeneizado, linear-elástico: mostra a energia ELÁSTICA guardada em cada material, '
             'não dano nem dissipação própria do giroide. Estimativa, não é ensaio.', fontsize=8.6, color=MUTED)
    for ax, (k, rot) in zip(axs, V):
        ax.text(0.5, 1.0, rot, transform=ax.transAxes, ha='center', fontsize=14, fontweight='bold', color=INK)
    sub = [ax.text(0.5, -0.02, '', transform=ax.transAxes, ha='center', va='top', fontsize=10.5, color=INK) for ax in axs]
    clock = fig.text(0.97, 0.94, '', fontsize=22, fontweight='bold', color='#c2410c', ha='right')
    scs = [None, None]

    def frame(i):
        tk = tt[i]
        clock.set_text(f'{tk:4.1f} ms'.replace('.', ','))
        cursor.set_xdata([tk, tk])
        for j, (ax, (k, rot)) in enumerate(zip(axs, V)):
            d = D[k]; m = gm[k]
            fg = interp(d['fi_g'], d['t'], tk)[m]
            if scs[j] is not None:
                scs[j].remove()
            o = np.argsort(fg); xs, ys, _ = proj(d['cen'][m][o], az=-40, el=26)
            kk = np.clip(fg[o] / vmax, 0, 1); col = CMAP(kk); col[:, 3] = 0.12 + 0.88 * np.clip(kk * 1.6, 0, 1)
            scs[j] = ax.scatter(xs, ys, c=col, s=5.5, linewidths=0, rasterized=True)
            p = float(np.interp(tk, d['t'], pct[k]))
            sub[j].set_text(f'giroide guarda {p:.0f}% da energia elástica\npico a {float(fg.max()) * 100:.0f}% da resistência do giroide')
        return []

    anim = animation.FuncAnimation(fig, frame, frames=N, blit=False)
    tpk = int(np.argmin(np.abs(tt - D['F25_COM']['J']['t_pico_ms'])))
    save(anim, fig, 'absorcao_giroide', tpk)
    RES['absorcao_giroide'] = {k: {'pct_energia_giroide_no_pico': round(float(np.interp(D[k]['J']['t_pico_ms'], D[k]['t'], pct[k])), 1),
                                   'pct_energia_giroide_max': round(float(pct[k].max()), 1),
                                   'FI_giroide_pico': D[k]['J']['FI_giroide_pico']} for k, _ in V}


if __name__ == '__main__':
    todos = {'carga': video_carga, 'impacto': video_impacto, 'absorcao': video_absorcao}
    for n in (sys.argv[1:] or list(todos)):
        todos[n]()
    if os.environ.get('VID_TESTE'):
        sys.exit(0)
    jf = OUT / 'videos_r07.json'
    allr = json.loads(jf.read_text(encoding='utf-8')) if jf.exists() else {}
    allr.update(RES)
    jf.write_text(json.dumps(allr, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(RES, ensure_ascii=False))
