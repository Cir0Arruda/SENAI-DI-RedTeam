"""R07 - Gráficos do relatório: carga máxima por variante e vida em fadiga (a partir de r07_vida.json)."""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R = Path(__file__).resolve().parents[1] / '06_Engenharia' / 'R07'
d = json.loads((R / 'r07_vida.json').read_text(encoding='utf-8'))
V = d['variantes']
names = list(V)
short = ['R06\n(atual)', 'R07\nCOM esqueleto', 'R07 SEM\n(mesmos %)', 'R07 SEM\n(giroide denso,\nmesma massa)']
mats = list(next(iter(V.values()))['materiais'])
C = ['#2a78d6', '#e07b39']          # 2 séries: azul / laranja
INK, MUTED, GRID = '#1f2328', '#6b7280', '#e5e7eb'
plt.rcParams.update({'font.size': 10, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK, 'xtick.color': INK,
                     'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False})


def bars(ax, key, title, ylabel, ref=None):
    w = 0.38
    for j, m in enumerate(mats):
        vals = [V[n]['materiais'][m][key] for n in names]
        xs = [i + (j - 0.5) * w for i in range(len(names))]
        b = ax.bar(xs, vals, w - 0.04, color=C[j], label=m, zorder=3)
        for x, v in zip(xs, vals):
            ax.text(x, v, f'{v:g}', ha='center', va='bottom', fontsize=8, color=INK)
    if ref:
        for val, lab in ref:
            ax.axhline(val, color=INK, lw=1, ls='--', zorder=2)
            ax.text(len(names) - 0.5, val, lab, ha='right', va='bottom', fontsize=8, color=INK)
    ax.set_xticks(range(len(names)), short)
    ax.set_title(title, loc='left', color=INK, fontsize=11)
    ax.set_ylabel(ylabel); ax.grid(axis='y', color=GRID, zorder=0)


fig, ax = plt.subplots(1, 2, figsize=(13, 4.8))
bars(ax[0], 'kg_max_com_g+5', 'Carga máxima numa asa (com aceleração g+5 m/s²)', 'kg até a ruptura',
     ref=[(24, '24 kg (erro da seladora)'), (30, '30 kg (teste)')])
ax[0].legend(frameon=False, fontsize=8, loc='upper left')
bars(ax[1], 'energia_ate_ruptura_J', 'Energia de tranco absorvida até romper', 'J')
fig.tight_layout(); fig.savefig(R / 'grafico_carga_max.png', dpi=150)

fig, ax = plt.subplots(figsize=(8, 4.4))
m = mats[0]
vals = [V[n]['materiais'][m]['fadiga']['horas_mix_1pct_erro'] for n in names]
b = ax.bar(range(len(names)), vals, 0.55, color=C[0], zorder=3)
for i, v in enumerate(vals):
    ax.text(i, v, f'{v:,} h'.replace(',', '.'), ha='center', va='bottom', fontsize=9, color=INK)
ax.set_xticks(range(len(names)), short); ax.set_yscale('log')
ax.set_title(f'Vida em fadiga estimada - {m}\n480 ciclos/h, 12 kg por asa + 1% dos ciclos com 24 kg numa asa',
             loc='left', fontsize=10, color=INK)
ax.set_ylabel('horas de operação (escala log)'); ax.grid(axis='y', color=GRID, zorder=0)
fig.tight_layout(); fig.savefig(R / 'grafico_fadiga.png', dpi=150)
print('ok')
