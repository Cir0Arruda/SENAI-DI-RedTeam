"""Vídeo simples da garra SAI com 24 kg numa asa (para o slide Materiais).

Mesmos campos e mesma conta do vídeo "carga_24kg_asa" de r07_videos.py, só com a garra escolhida (R07 sem
esqueleto, chamada de "garra SAI" na apresentação) e textos sem termos técnicos. Nenhum resultado novo.

Uso: python r07_video_sai.py <pasta R07> <pasta de saída> [quadro_teste]
  <pasta R07> contém MONTAGEM/campos_R07_SEM_ONE_24.npz e MONTAGEM/montagem_R07_SEM.json
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.colors import LinearSegmentedColormap

R7, OUT = Path(sys.argv[1]), Path(sys.argv[2])
TESTE = int(sys.argv[3]) if len(sys.argv) > 3 else None
FPS, DPI = 24, 100
CMAP = LinearSegmentedColormap.from_list('fi', ['#d9dbe4', '#9fb4d8', '#f2c14e', '#e8590c', '#b91c1c', '#5a0a0a'])
INK, MUTED, OK, KG = '#15151d', '#5d5f70', '#17784f', '#c2410c'
plt.rcParams.update({'font.family': 'DejaVu Sans'})


def proj(P, az=-58, el=24):
    a, e = np.radians(az), np.radians(el)
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    xr = x * np.cos(a) - y * np.sin(a)
    yr = x * np.sin(a) + y * np.cos(a)
    return xr, z * np.cos(e) + yr * np.sin(e), yr * np.cos(e) - z * np.sin(e)


def cloud(ax, P, val, vmax, s):
    o = np.argsort(val)
    xs, ys, _ = proj(P[o])
    k = np.clip(val[o] / vmax, 0, 1)
    col = CMAP(k); col[:, 3] = 0.10 + 0.90 * np.clip(k * 1.6, 0, 1)
    return ax.scatter(xs, ys, c=col, s=s, linewidths=0, rasterized=True)


z = np.load(R7 / 'MONTAGEM' / 'campos_R07_SEM_ONE_24.npz')
D = {n: z[n] for n in z.files}
J = json.loads((R7 / 'MONTAGEM' / 'montagem_R07_SEM.json').read_text(encoding='utf-8'))
PICO, MAG, VMAX = float(D['PICO']), 15.0, 0.40          # mesma escala de cor do vídeo comparativo
KG_MAX = J['kg_max_PA6-CF_Z48']

X0, Y0, _ = proj(D['cen'])
xl = (X0.min() - 20, X0.max() + 20); yl = (Y0.min() - 34, Y0.max() + 20)
nramp, nhold = FPS * 6, FPS * 3
N = nramp + nhold

fig = plt.figure(figsize=(9.6, 7.2), dpi=DPI)
fig.patch.set_facecolor('white')
fig.text(0.04, 0.925, 'Garra SAI com 24 kg numa asa só', fontsize=22, fontweight='bold', color=INK)
fig.text(0.04, 0.88, 'Se a seladora erra, as duas caixas caem numa asa. A cor mostra onde a garra trabalha.',
         fontsize=12, color=MUTED)
kgtxt = fig.text(0.96, 0.925, '', fontsize=26, fontweight='bold', color=KG, ha='right')
ax = fig.add_axes([0.03, 0.21, 0.94, 0.64])
ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect('equal'); ax.axis('off')
badge = fig.text(0.5, 0.125, '', fontsize=16, fontweight='bold', color=OK, ha='center')
cax = fig.add_axes([0.30, 0.055, 0.40, 0.022])
cb = fig.colorbar(plt.cm.ScalarMappable(cmap=CMAP, norm=plt.Normalize(0, VMAX)), cax=cax, orientation='horizontal')
cb.set_ticks([]); cb.outline.set_linewidth(0.6)
fig.text(0.29, 0.06, 'pouco esforço', fontsize=11, color=MUTED, ha='right', va='center')
fig.text(0.71, 0.06, 'mais esforço', fontsize=11, color=MUTED, ha='left', va='center')
fig.text(0.5, 0.012, 'Simulação por computador · estimativa, não é ensaio', fontsize=9, color=MUTED, ha='center')
tip = int(np.argmax(np.linalg.norm(D['U'], axis=1)))
st = {'sc': None, 'arrow': None}


def frame(i):
    f = min(1.0, (i + 1) / nramp)
    f = 1 - (1 - f) ** 2 if i < nramp else 1.0
    kg = 24.0 * f
    kgtxt.set_text(f'{kg:4.1f} kg'.replace('.', ','))
    if st['sc'] is not None:
        st['sc'].remove()
    st['sc'] = cloud(ax, D['cen'] + D['U'] * MAG * f, D['fi_z'] * PICO * f, VMAX, s=11)
    if st['arrow'] is not None:
        st['arrow'].remove()
    px, py, _ = proj((D['cen'][tip] + D['U'][tip] * MAG * f)[None])
    st['arrow'] = ax.annotate(f'{kg:.0f} kg', xy=(px[0], py[0]), xytext=(px[0], py[0] - 14 - 18 * f),
                              ha='left', va='center', fontsize=14, fontweight='bold', color=KG,
                              arrowprops=dict(arrowstyle='<-', color=KG, lw=2.6, relpos=(0, 0.5), shrinkA=0, shrinkB=2), zorder=10)
    badge.set_text(f'✓ Aguenta os 24 kg com folga: só quebraria com cerca de {KG_MAX:.0f} kg' if i >= nramp - 1 else '')
    return []


anim = animation.FuncAnimation(fig, frame, frames=N, blit=False)
OUT.mkdir(parents=True, exist_ok=True)
if TESTE is not None:
    frame(TESTE); fig.savefig(OUT / f'_teste_carga_sai_{TESTE}.png', dpi=DPI, facecolor='white')
else:
    anim.save(OUT / 'carga_sai.mp4', writer=animation.FFMpegWriter(fps=FPS, codec='libx264', bitrate=2500,
              extra_args=['-pix_fmt', 'yuv420p', '-movflags', '+faststart']), dpi=DPI)
    frame(N - 1); fig.savefig(OUT / 'carga_sai_poster.jpg', dpi=DPI, facecolor='white')
    print(OUT / 'carga_sai.mp4')
