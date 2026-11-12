"""Peso do conjunto inteiro (garra impressa + resto da montagem) para cada rodada de testes.

Lê os resultados do Orca (K1 Max 1:1) na pasta de trabalho `desempenho/` e gera:
  - assets/js/conjunto-dados.js  (window.CONJUNTO, usado no slide "Peso do conjunto")
  - dados/decisao/peso_conjunto.csv

Hipótese declarada: o resto da montagem (ferragens, ventosas e PADs) não muda entre as opções.
Resto = 2,834 kg (garra instalada, dado da equipe) - 1.576,88 g (Tritan Hexa3D 30% estimado no Orca).
Uso: python conjunto_dados.py <pasta desempenho> <pasta do site>
"""
import csv, json, sys
from pathlib import Path

DES = Path(sys.argv[1] if len(sys.argv) > 1 else '../desempenho')
SITE = Path(sys.argv[2] if len(sys.argv) > 2 else '.')
ORCA = DES / '05_Orca'

CONJ_TRITAN_KG = 2.834          # garra instalada, dado da equipe (deck do cliente)
TRITAN = dict(sup=688.27, inf_esq=444.3, inf_dir=444.3)   # Hexa3D 30% × 1,18/1,10 (estimado)
UR30_KG, CAIXAS_KG = 30.0, 24.0


def peca(path):
    s = json.load(open(ORCA / path / 'status.json', encoding='utf8'))
    m = s['mass_g']
    return dict(g=round(m['peca'], 2), fil=round(s['orca_total_g'], 2), h=round(s['time_s'] / 3600, 2))


def r04():
    rows = {r['caso']: r for r in csv.DictReader(open(DES / '06_Engenharia/MASSAS_CONSUMO_R04.csv', encoding='utf-8-sig'))}
    f = lambda k: dict(g=round(float(rows[k]['massa_pecas_g']), 2), fil=round(float(rows[k]['consumo_total_Orca_g']), 2), h=round(float(rows[k]['tempo_s']) / 3600, 2))
    return f('SUPERIOR'), f('INFERIOR_ESQ'), f('INFERIOR_DIR')


C = 'R07/COMPARATIVO/Resultado_'
# (chave, rótulo, rodada, superior, inferior esq, inferior dir [None = espelho da esquerda])
CASOS = [
    ('R04', 'R04 · TPMS-D zonal 20/30/50/70%', '1ª rodada', *r04()),
    ('R06', 'R06 · zonas internas TPMS-D', '2ª rodada', peca('R06/Resultado_SUPERIOR'), peca('R06/Resultado_INFERIOR_ESQ'), peca('R06/Resultado_INFERIOR_DIR')),
    ('TPMSD40', 'TPMS-D 40% uniforme', 'comparativo', peca(C + 'UNI_TPMSD40_SUPERIOR'), peca(C + 'UNI_TPMSD40_INFERIOR_ESQ'), None),
    ('UNI_40', 'Giroide 40% uniforme', 'comparativo', peca(C + 'UNI_GIROIDE40_SUPERIOR'), peca(C + 'UNI_GIROIDE40_INFERIOR_ESQ'), None),
    ('UNI_35', 'Giroide 35% uniforme', 'comparativo', peca(C + 'UNI_GIROIDE35_SUPERIOR'), peca(C + 'UNI_GIROIDE35_INFERIOR_ESQ'), None),
    ('UNI_30', 'Giroide 30% uniforme', 'comparativo', peca(C + 'UNI_GIROIDE30_SUPERIOR'), peca(C + 'UNI_GIROIDE30_INFERIOR_ESQ'), None),
    ('HEXA30', 'Hexa3D 30% em PA6-CF', 'comparativo', peca(C + 'UNI_HONEYCOMB3D30_SUPERIOR'), peca(C + 'UNI_HONEYCOMB3D30_INFERIOR_ESQ'), None),
    ('R07_COM', 'R07 com esqueleto', '3ª rodada', peca('R07/Resultado_SUPERIOR_B25'), peca('R07/Resultado_INFERIOR_ESQ_B20'), peca('R07/Resultado_INFERIOR_DIR_B20')),
    ('R07_B20', 'R07 com esqueleto, superior 20%', '3ª rodada (teste)', peca('R07/Resultado_SUPERIOR_B20'), peca('R07/Resultado_INFERIOR_ESQ_B20'), peca('R07/Resultado_INFERIOR_DIR_B20')),
    ('R07_SEM', 'R07 sem esqueleto', '3ª rodada', peca(C + 'R07_SEM_SUPERIOR'), peca('R07/Resultado_INFERIOR_ESQ_B20'), peca('R07/Resultado_INFERIOR_DIR_B20')),
]
SO_SUPERIOR = [
    ('R06 superior uniforme 20%', peca('R06/Resultado_SUPERIOR_UNIFORME_20')),
    ('R06 superior uniforme 30%', peca('R06/Resultado_SUPERIOR_UNIFORME_30')),
    ('R06 superior uniforme 50%', peca('R06/Resultado_SUPERIOR_UNIFORME_50')),
]
pad = json.load(open(ORCA / 'Resultado_PAD_K1MAX/dados_fatiamento.json', encoding='utf8'))

tritan_garra = round(sum(TRITAN.values()), 2)
resto_g = round(CONJ_TRITAN_KG * 1000 - tritan_garra, 2)


def linha(k, rot, rodada, sup, ie, idr):
    idr = idr or ie
    garra = round(sup['g'] + ie['g'] + idr['g'], 2)
    conj = round(garra + resto_g, 1)
    return dict(k=k, rot=rot, rodada=rodada, sup_g=sup['g'], inf_esq_g=ie['g'], inf_dir_g=idr['g'],
                inf_dir_espelho=idr is ie, garra_g=garra, resto_g=resto_g, conjunto_g=conj,
                dif_conjunto_g=round(conj - CONJ_TRITAN_KG * 1000, 1),
                pct_conjunto=round((conj / (CONJ_TRITAN_KG * 1000) - 1) * 100, 2),
                pct_garra=round((garra / tritan_garra - 1) * 100, 2),
                com_caixas_kg=round(conj / 1000 + CAIXAS_KG, 3),
                folga_ur30_kg=round(UR30_KG - conj / 1000 - CAIXAS_KG, 3),
                fil_g=round(sup['fil'] + ie['fil'] + idr['fil'], 1), tempo_h=round(sup['h'] + ie['h'] + idr['h'], 1))


rows = [dict(k='TRITAN', rot='Tritan instalada (atual)', rodada='referência', sup_g=TRITAN['sup'], inf_esq_g=TRITAN['inf_esq'],
             inf_dir_g=TRITAN['inf_dir'], inf_dir_espelho=True, garra_g=tritan_garra, resto_g=resto_g,
             conjunto_g=CONJ_TRITAN_KG * 1000, dif_conjunto_g=0.0, pct_conjunto=0.0, pct_garra=0.0,
             com_caixas_kg=CONJ_TRITAN_KG + CAIXAS_KG, folga_ur30_kg=round(UR30_KG - CONJ_TRITAN_KG - CAIXAS_KG, 3),
             fil_g=None, tempo_h=None)]
rows += [linha(*c) for c in CASOS]

out = dict(
    conj_tritan_kg=CONJ_TRITAN_KG, tritan_garra_g=tritan_garra, resto_g=resto_g, ur30_kg=UR30_KG, caixas_kg=CAIXAS_KG,
    pads_novos_g=round(pad['Orca_summary'].get('model_mass_g', 93.06) if isinstance(pad.get('Orca_summary'), dict) else 93.06, 2),
    linhas=rows,
    so_superior=[dict(rot=r, sup_g=p['g'], fil_g=p['fil'], tempo_h=round(p['h'], 1)) for r, p in SO_SUPERIOR],
)
(SITE / 'assets/js/conjunto-dados.js').write_text(
    '// Gerado por dados/scripts/conjunto_dados.py — não editar à mão.\nwindow.CONJUNTO = ' + json.dumps(out, ensure_ascii=False) + ';\n', encoding='utf8')
campos = ['k', 'rot', 'rodada', 'sup_g', 'inf_esq_g', 'inf_dir_g', 'inf_dir_espelho', 'garra_g', 'resto_g', 'conjunto_g',
          'dif_conjunto_g', 'pct_conjunto', 'pct_garra', 'com_caixas_kg', 'folga_ur30_kg', 'fil_g', 'tempo_h']
with open(SITE / 'dados/decisao/peso_conjunto.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=campos, delimiter=';'); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['rot']:36s} garra {r['garra_g']:8.1f}  conjunto {r['conjunto_g']:7.1f} g  {r['pct_conjunto']:+5.1f}%  folga UR30 {r['folga_ur30_kg']:.3f} kg")
print('PADs novos', out['pads_novos_g'])
