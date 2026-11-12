"""Estudo de custos e durabilidade da garra SAI (R07 sem esqueleto) contra a garra de Tritan atual.

Tudo sai de dados já publicados no site (assets/js/r07-dados.js, gerado a partir do Orca e do FE da montagem)
e dos dados informados pela equipe. Hipóteses novas ficam marcadas com HIP e aparecem no relatório.
Nada aqui é ensaio: a durabilidade é estimativa de engenharia.

Uso: python estudo_custos.py <pasta do site>
Saída: dados/estudo_custos/estudo_custos.json
"""
from __future__ import annotations
import json, math, re, sys
from pathlib import Path

SITE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
txt = (SITE / 'assets' / 'js' / 'r07-dados.js').read_text(encoding='utf-8')
R07 = json.loads(re.search(r'window\.R07 = (\{.*\});', txt, re.S).group(1))
SEM = next(v for v in R07['variantes'] if v['k'] == 'R07_SEM')
PADS = R07['pads']

# ---------- entradas ----------
E = {
    # equipe
    'preco_pacf_kg': R07['precos']['pacf_kg'], 'preco_tpu_kg': R07['precos']['tpu_kg'],
    'tritan_garra_rs': 250.0, 'tritan_quebras_ano': 4, 'parada_min': 45, 'caixas_por_parada': 280,
    'custo_oportunidade_parada_rs': 84000.0,          # 280 caixas a preço de mercado (equipe); é receita, não margem
    'prazo_tritan_dias': (15, 20), 'prazo_pacf_dias_uteis': (5, 8),
    'bico_rs': 23.50,
    # Orca (R07 sem esqueleto, K1 Max 1:1)
    'fil_garra_g': SEM['fil_g'], 'garra_g': SEM['garra_g'], 'sup_g': SEM['sup_g'], 'inf_g': SEM['inf_g'],
    'tempo_garra_h': SEM['tempo_h'], 'fil_pads_g': PADS['total_g'], 'tempo_pads_h': PADS['tempo_h'],
    # FE da montagem (R07 sem esqueleto), carga numa asa = massa x (g + 5 m/s2)
    'sz24_MPa': SEM['sz24'], 'sz_tranco24_MPa': SEM['impacto']['sz'],
    'S_pa6cf_MPa': 48.0, 'S_paht_MPa': 18.2,
    'reducao_pad': 0.63,                               # modelo 1D de molas (slide do PAD)
    # HIP: hipóteses deste estudo (a confirmar com a equipe/Ajinomoto)
    'HIP_ciclos_h_real': 180,                          # 6 caixas/min, 2 caixas por ciclo (uma em cada asa)
    'HIP_ciclos_h_relatorio': 480,                     # hipótese conservadora do RELATORIO_R07 (8/min)
    'HIP_horas_ano': 8760,                             # 24/7, igual ao ROI atual (730 h/mês)
    'HIP_potencia_impressora_kW': 0.30,                # média K1 Max imprimindo PA-CF (mesa quente); medir com tomada
    'HIP_tarifa_kWh': 0.90,
    'HIP_refugo': 0.10,                                # 10% de material para impressões perdidas e testes
    'HIP_trocas_pad_ano': 6,                           # conjunto de 8 PADs a cada 2 meses (premissa atual do slide)
}

# ---------- durabilidade (mesma curva S-N do RELATORIO_R07: s/S = 1 - 0,10 log10 N) ----------
def ciclos(sigma, S):
    r = sigma / S
    return math.inf if r <= 0 else (0.0 if r >= 1 else 10 ** ((1 - r) / 0.10))

dur = {}
for mat, S in (('PA6-CF (TDS seco)', E['S_pa6cf_MPa']), ('PAHT CF15 (pior adesão entre camadas)', E['S_paht_MPa'])):
    s12 = E['sz24_MPa'] / 2
    N12 = ciclos(s12, S)
    d = {'N_rotina_12kg': N12,
         'anos_rotina_180h': N12 / (E['HIP_ciclos_h_real'] * E['HIP_horas_ano']),
         'anos_rotina_480h': N12 / (E['HIP_ciclos_h_relatorio'] * E['HIP_horas_ano']),
         'horas_rotina_480h_confere_site': N12 / 480,
         'eventos_24kg_estatico': ciclos(E['sz24_MPa'], S),
         'eventos_30kg_estatico': ciclos(E['sz24_MPa'] * 30 / 24, S),
         'eventos_tranco24_sem_pad': ciclos(E['sz_tranco24_MPa'], S),
         'eventos_tranco24_com_pad': ciclos(E['sz_tranco24_MPa'] * (1 - E['reducao_pad']), S),
         'FS_tranco_sem_pad': S / E['sz_tranco24_MPa'], 'FS_tranco_com_pad': S / (E['sz_tranco24_MPa'] * (1 - E['reducao_pad']))}
    # dano por ano: rotina + 52 erros de seladora (1 por semana) + 52 trancos com PAD
    ano_rot = E['HIP_ciclos_h_real'] * E['HIP_horas_ano']
    d['dano_ano_rotina'] = ano_rot / N12
    d['dano_ano_52_erros_24kg'] = 52 / d['eventos_24kg_estatico']
    d['dano_ano_52_trancos_com_pad'] = 52 / d['eventos_tranco24_com_pad']
    d['vida_anos_cenario_misto'] = 1 / (d['dano_ano_rotina'] + d['dano_ano_52_erros_24kg'] + d['dano_ano_52_trancos_com_pad'])
    dur[mat] = d

# ---------- custos ----------
def r2(x): return round(x, 2)
mat_garra = E['fil_garra_g'] / 1000 * E['preco_pacf_kg']
mat_pads = E['fil_pads_g'] / 1000 * E['preco_tpu_kg']
energia = (E['tempo_garra_h'] + E['tempo_pads_h']) * E['HIP_potencia_impressora_kW'] * E['HIP_tarifa_kWh']
refugo = (mat_garra + mat_pads) * E['HIP_refugo']
frac_sup = E['sup_g'] / E['garra_g']
aq = {'garra_material': r2(mat_garra), 'pads_material': r2(mat_pads), 'bico': E['bico_rs'],
      'slide_atual': r2(mat_garra + mat_pads + E['bico_rs']),
      'energia_impressao': r2(energia), 'refugo_10pct': r2(refugo),
      'completo_sem_mao_de_obra': r2(mat_garra + mat_pads + E['bico_rs'] + energia + refugo),
      'so_peca_superior_material': r2(mat_garra * frac_sup), 'frac_superior': round(frac_sup, 3)}
pad_troca = mat_pads + E['tempo_pads_h'] * E['HIP_potencia_impressora_kW'] * E['HIP_tarifa_kWh']

def tco(meses, vida_meses, quebras_ano_sai=0.0, com_parada=False):
    """Gasto acumulado em `meses`. Tritan: 4 garras/ano. SAI: compra no mês 0, nova garra a cada `vida_meses`,
    PADs 6x/ano e quebras inesperadas (garra inteira + parada)."""
    anos = meses / 12
    trit = E['tritan_garra_rs'] * E['tritan_quebras_ano'] * anos
    trit_par = E['custo_oportunidade_parada_rs'] * E['tritan_quebras_ano'] * anos if com_parada else 0
    garra_nova = mat_garra + energia * (E['tempo_garra_h'] / (E['tempo_garra_h'] + E['tempo_pads_h'])) + refugo
    n_garras = 1 + max(0, math.ceil(meses / vida_meses) - 1)
    sai = aq['completo_sem_mao_de_obra'] + (n_garras - 1) * garra_nova
    sai += pad_troca * E['HIP_trocas_pad_ano'] * anos
    sai += quebras_ano_sai * anos * garra_nova
    sai_par = E['custo_oportunidade_parada_rs'] * quebras_ano_sai * anos if com_parada else 0
    return {'tritan': r2(trit + trit_par), 'sai': r2(sai + sai_par), 'garras_sai': n_garras}

cen = {}
for nome, vida, q in (('otimista: vida 36 meses, sem quebra', 36, 0), ('base: vida 24 meses, sem quebra', 24, 0),
                      ('conservador: vida 12 meses + 1 quebra/ano', 12, 1)):
    cen[nome] = {'pecas_24m': tco(24, vida, q), 'pecas_36m': tco(36, vida, q),
                 'com_parada_24m': tco(24, vida, q, True), 'com_parada_36m': tco(36, vida, q, True)}

out = {'entradas': E, 'durabilidade': dur, 'aquisicao': aq, 'troca_pads_rs': r2(pad_troca),
       'pads_ano_rs': r2(pad_troca * E['HIP_trocas_pad_ano']), 'cenarios': cen,
       'tritan_ano_pecas': E['tritan_garra_rs'] * E['tritan_quebras_ano'],
       'tritan_ano_paradas': E['custo_oportunidade_parada_rs'] * E['tritan_quebras_ano'],
       'tritan_horas_paradas_ano': E['parada_min'] * E['tritan_quebras_ano'] / 60,
       'tritan_caixas_perdidas_ano': E['caixas_por_parada'] * E['tritan_quebras_ano']}
dst = SITE / 'dados' / 'estudo_custos'; dst.mkdir(parents=True, exist_ok=True)
(dst / 'estudo_custos.json').write_text(json.dumps(out, ensure_ascii=False, indent=1, default=lambda x: None if x == math.inf else x), encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
