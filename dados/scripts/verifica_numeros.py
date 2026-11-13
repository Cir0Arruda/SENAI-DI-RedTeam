"""Confere cada número da apresentação contra o arquivo de origem (dados/) e refaz a conta.

Uso: python dados/scripts/verifica_numeros.py   (na raiz do site)
Saída: tabela no terminal e dados/verificacao_numeros.json. Termina com erro se algum número não bater.
Tolerância: o arredondamento mostrado no slide (ex.: 3,9 aceita 3,85 a 3,95).
"""
import csv, json, math, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
R = Path(__file__).resolve().parents[2]
D = R / 'dados'
HTML = (R / 'index.html').read_text(encoding='utf-8')
VIS = HTML[:HTML.index('<template id="arquivo">')]          # só os slides visíveis
J = lambda p: json.loads((D / p).read_text(encoding='utf-8'))
G, A = 9.80665, 5.0
linhas, falhas = [], []


def txt(s):
    """Texto visível sem tags, com espaços normalizados."""
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))


VTXT = txt(VIS)


def ok(slide, item, mostrado, calculado, casas, fonte, no_slide=None):
    """mostrado: número no slide; calculado: conta a partir da fonte; casas: casas decimais exibidas."""
    bate = abs(round(calculado, casas) - mostrado) <= 10 ** -casas * 0.51
    presente = True if no_slide is None else (no_slide in VTXT)
    st = 'OK' if bate and presente else ('NÃO ESTÁ NO SLIDE' if bate else 'DIVERGE')
    linhas.append(dict(slide=slide, item=item, mostrado=mostrado, calculado=round(calculado, 4), status=st, fonte=fonte))
    if st != 'OK':
        falhas.append(linhas[-1])


# ---------- fontes ----------
mont = J('montagem/montagem_R07_SEM.json')
imp = J('impacto/impacto_F25_SEM.json')
pad = J('impacto/pad_limites.json')
r03 = J('brutos/impacto_pad_hexa15/02_Dados/parametros_resultados_R03.json')['results_reduced_model']
r03e = J('brutos/impacto_pad_hexa15/02_Dados/parametros_resultados_R03.json')
orca = J('orca/r07_comparativo_fatiamento.json')['R07_SEM_SUPERIOR']
b20 = J('orca/r07_fatiamento_base20.json')
pads = J('orca/pads_tpu95a_fatiamento.json')
vida = J('fadiga/r07_vida.json')['variantes']['R07 SEM esqueleto (mesmos %)']['materiais']
camp = J('brutos/fusion/preparacao_garra/campanha_2026-11-11.json')
peso = {r['k']: r for r in csv.DictReader(open(D / 'decisao/peso_conjunto.csv', encoding='utf-8-sig'), delimiter=';')}

# ---------- dados da equipe (slides 3, 4, 10) ----------
CAIXAS, ITENS, KG_CX, PALETE, QUEBRAS, MIN_PARADA, RITMO = 280, 12, 12, 40, 4, 45, 6
ok(3, 'paletes por parada (280 ÷ 40)', 7, CAIXAS / PALETE, 0, 'equipe')
ok(3, 'kg parados (280 × 12 kg)', 3360, CAIXAS * KG_CX, 0, 'equipe', '3.360')
ok(3, 'caixas por ano (4 × 280)', 1120, QUEBRAS * CAIXAS, 0, 'equipe', '1.120')
ok(4, 'itens no lote (280 × 12)', 3360, CAIXAS * ITENS, 0, 'equipe')
ok(4, '280 caixas a cerca de 6/min (min)', 47, CAIXAS / RITMO, 0, 'equipe: 45 min de parada ≈ 280 ÷ 6', 'cerca de 6 caixas por minuto')
ok(3, '7 paletes de 40 no slide', 7, CAIXAS / PALETE, 0, 'equipe', '7 paletes de 40')
ok(4, 'garra + 2 caixas (kg)', 26.8, 2.834 + 24, 1, 'equipe', '26,8 kg')
ok(4, '% do limite do UR30', 89, (2.834 + 24) / 30 * 100, 0, 'equipe')

# ---------- material (slide 6) ----------
ok(6, 'PA6-CF ÷ Tritan, rigidez ("quase 3×")', 2.9, 4430 / 1548, 1, 'fichas [M1] [M3]')
ok(6, 'garra rompe numa asa (kg)', 93, mont['kg_max_PA6-CF_Z48'], 0, 'montagem_R07_SEM.json')

# ---------- garra montada (slides 11, 13, vídeo) ----------
F24 = 24 * (G + A)
ok(0, 'carga 24 kg × (g + 5) (N)', 355.36, F24, 2, 'campanha Fusion / README')
ok(0, 'carga do Fusion = 4 × 88,84 N', 355.36, 4 * camp['boundary_conditions']['force_each_N'][2] * -1, 2, 'campanha_2026-11-11.json')
ok(13, 'FS 24 kg = 48 ÷ σZ', 3.9, 48 / mont['sigma_Z_24kg_MPa_(x PICO)'], 1, 'montagem_R07_SEM.json', '3,9×')
ok(13, 'kg máx = 24 × FS', 93, 24 * 48 / mont['sigma_Z_24kg_MPa_(x PICO)'], 0, 'montagem_R07_SEM.json', '93 kg')
ok(0, 'pior colagem: kg máx (18,2 MPa)', 35.4, 24 * 18.2 / mont['sigma_Z_24kg_MPa_(x PICO)'], 1, 'montagem_R07_SEM.json')
ok(14, 'tranco 24 kg em 10 ms: FS = 48 ÷ σZ pico', 2.65, 48 / imp['sigma_Z_pico_MPa_(x PICO)'], 2, 'impacto_F25_SEM.json', 'FS 2,65')

# ---------- fadiga (slides 11, 13) ----------
anos = vida['PA6-CF valor usado no FE (Z=48 MPa)']['fadiga']['horas_so_12kg'] / 8760
ok(0, 'fadiga, PA6-CF da ficha: passa de 100 anos', 1, float(anos > 100), 0, 'r07_vida.json')
cus = J('estudo_custos/estudo_custos.json')['durabilidade']['PAHT CF15 (pior adesão entre camadas)']
ok(11, 'vida no pior caso de colagem (anos)', 2.4, cus['vida_anos_cenario_misto'], 1, 'estudo_custos.json', '2,4 anos')
ok(11, 'vida estimada = pior caso arredondado para baixo (meses)', 24, (cus['vida_anos_cenario_misto'] * 12) // 12 * 12, 0, 'estudo_custos.json', 'Vida estimada: 24 meses')

# ---------- PAD (slides 8, 11, 13) ----------
ok(8, 'pico sem PAD (N)', 451, r03['peak_force_without_PAD_N'], 0, 'parametros_resultados_R03.json', '451 N')
ok(8, 'pico com PAD (N)', 169, r03['peak_force_with_PAD_N'], 0, 'parametros_resultados_R03.json', '169 N')
ok(8, 'redução (%)', 62.6, r03['peak_force_reduction_percent'], 1, 'parametros_resultados_R03.json', '−62,6%')
ok(8, 'redução arredondada (%)', 63, r03['peak_force_reduction_percent'], 0, 'parametros_resultados_R03.json', '−63%')
ok(8, 'energia no PAD (%)', 86, r03e['results_reduced_model']['peak_PAD_elastic_energy_J'] / r03e['impact']['energy_J'] * 100, 0, 'parametros_resultados_R03.json', '86%')
ok(8, 'força em que o PAD se esmaga (N)', 240, pad['pad_no_limite']['forca_N'], -1, 'pad_limites.json', '≈ 240 N')
ok(8, '240 N em kgf ("24 kg")', 24, pad['pad_no_limite']['forca_N'] / 9.81, 0, 'pad_limites.json')
ok(8, '% da ruptura que chega à garra', 17, pad['pad_no_limite']['forca_N'] / pad['garra_rompe']['forca_N'] * 100, 0, 'pad_limites.json', 'só 17%')
ok(8, 'ruptura da garra (N)', 1380, pad['garra_rompe']['forca_N'], -1, 'pad_limites.json', '≈ 1.380 N')
ok(8, 'ruptura = 93,3 kg × (g + 5)', 1380, 93.3 * (9.81 + 5), -1, 'pad_limites.py')
ok(8, '1.380 N em kgf ("140 kg")', 140, pad['garra_rompe']['forca_N'] / 9.81, -1, 'pad_limites.json', '≈ 140 kg')
ok(8, 'energia com ÷ sem PAD', 2.2, pad['garra_rompe']['energia_com_PAD_J'] / pad['garra_rompe']['energia_sem_PAD_J'], 1, 'pad_limites.json', '2,2×')
ok(8, '1 kg caindo, com PAD (cm)', 27, pad['garra_rompe']['energia_com_PAD_J'] / (1 * 9.81) * 100, 0, 'pad_limites.json', '27 cm')
ok(8, '1 kg caindo, sem PAD (cm)', 12, pad['garra_rompe']['energia_sem_PAD_J'] / (1 * 9.81) * 100, 0, 'pad_limites.json', '12 cm')
ok(8, '"pouco mais de um terço" (169 ÷ 451)', 0.37, r03['peak_force_with_PAD_N'] / r03['peak_force_without_PAD_N'], 2, 'R03')

# ---------- fatiamento e peso (slides 10, 12, 13, 14) ----------
sup, ie, idr = orca['mass_g']['peca'], b20['INFERIOR_ESQ']['mass_g']['peca'], b20['INFERIOR_DIR']['mass_g']['peca']
fil = round(orca['orca_total_g'] + b20['INFERIOR_ESQ']['orca_total_g'] + b20['INFERIOR_DIR']['orca_total_g'], 1)   # 1.744,5 g, como no slide
horas = (orca['time_s'] + b20['INFERIOR_ESQ']['time_s'] + b20['INFERIOR_DIR']['time_s']) / 3600
ok(14, 'garra SAI impressa (g)', 1433, sup + ie + idr, 0, 'Orca', '1.433 g')
ok(14, 'tempo de impressão da garra (h)', 75.2, horas, 1, 'Orca', '75,2 h')
ok(10, 'filamento dos PADs (g)', 139, pads['Orca_summary']['total_filament_mass_g'], 0, 'Orca', '139')
ok(0, 'tempo dos PADs (h)', 11.0, pads['Orca_summary']['prediction_s'] / 3600, 1, 'Orca')
pads_g = pads['category_mass_g']['peca']
conj = 2834 - float(peso['TRITAN']['garra_g']) + sup + ie + idr + pads_g
ok(10, 'conjunto SAI com 8 PADs (kg)', 2.783, conj / 1000, 3, 'peso_conjunto.csv + PADs', '2,783 kg')
ok(10, 'mais leve que a atual (g)', 51, 2834 - conj, 0, 'peso_conjunto.csv + PADs', '51 g')
ok(13, 'mais leve que a atual (%)', 1.8, (2834 - conj) / 2834 * 100, 1, 'peso_conjunto.csv + PADs', '(−1,8%)')
ok(12, 'garra sozinha, menos que a de Tritan (g)', 144, float(peso['TRITAN']['garra_g']) - (sup + ie + idr), 0, 'peso_conjunto.csv', '144 g menos')

# ---------- custo real (slides 10, 11, 13): custo_real.json, refeito em parte aqui ----------
E = {k: v['valor'] for k, v in J('custos/entradas_custo.json')['entradas'].items()}
CR = J('custos/custo_real.json')
P, CO = CR['cenarios']['previsto'], CR['cenarios']['conservador']
S24, T24 = CR['periodo_24m']['sai'], CR['periodo_24m']['tritan']
EV = CR['eventos']
ok(0, 'filamento da garra no modelo = Orca (g)', E['sai_fil_g'], fil, 1, 'Orca')
ok(10, 'material da garra SAI = Orca × R$ 420/kg', 732.69, fil / 1000 * E['preco_pacf_kg'], 2, 'entradas_custo.json')
ok(0, 'material da garra no modelo (R$)', 732.69, CR['impressoes']['sai']['material'], 2, 'custo_real.json')
ok(0, 'material dos PADs = 139 g × R$ 158/kg', CR['impressoes']['pads']['material'], 139.0 / 1000 * E['preco_tpu_kg'], 2, 'entradas_custo.json')
ok(0, 'peça superior de Tritan = 0,81 kg × R$ 220/kg', CR['impressoes']['tritan']['material'], E['tritan_sup_kg'] * E['preco_tritan_kg'], 2, 'entradas_custo.json')
ok(11, 'troca da garra SAI: 30 min × 6 caixas/min', 180, EV['sai_troca']['caixas'], 0, 'custo_real.json', '30 min (180 caixas)')
ok(11, 'troca dos PADs: 10 min × 6 caixas/min', 60, EV['pads']['caixas'], 0, 'custo_real.json', '10 min (60 caixas)')
ok(0, 'caixas do SAI em 2 anos = instalação + 7 trocas de PAD', P['caixas_perdidas_24m']['sai'], 180 + 7 * 60, 0, 'custo_real.json')
ok(0, 'cruzamento em caixas refeito: 180 ÷ (180 + 280 − 240) × 3 meses', P['encontro_caixas']['mes'], 180 / (180 - (240 - 280)) * 3, 2, 'custo_real.json')
ok(0, 'caixas por mês (6/min × 60 × 730)', CR['producao']['caixas_por_mes'], 6 * 60 * 8760 / 12, 0, 'entradas_custo.json')
ok(10, 'garra SAI pronta e instalada (R$)', 1121.29, EV['sai_inicio']['direto'], 2, 'custo_real.json', 'R$ 1.121,29')
ok(10, 'encontro direto (milhões de caixas)', 4.6, P['encontro_direto']['caixas'] / 1e6, 1, 'custo_real.json', '4,6 milhões de caixas')
ok(10, 'encontro direto (meses)', 17.5, P['encontro_direto']['mes'], 1, 'custo_real.json', '(17,5 meses)')
ok(10, 'custo direto 24 meses, Tritan (R$)', 2342.48, T24['direto'], 2, 'custo_real.json', 'R$ 2.342,48')
ok(10, 'custo direto 24 meses, SAI (R$)', 1854.74, S24['direto'], 2, 'custo_real.json', 'R$ 1.854,74')
ok(10, 'tabela = série do gráfico (SAI, 24 meses)', S24['direto'], P['direto_24m']['sai'], 2, 'custo_real.json')
ok(10, 'tabela = série do gráfico (Tritan, 24 meses)', T24['direto'], P['direto_24m']['tritan'], 2, 'custo_real.json')
ok(10, 'SAI custa menos no ciclo (%)', 21, P['direto_24m']['economia'] / P['direto_24m']['tritan'] * 100, 0, 'custo_real.json', '21% menos')
ok(10, 'por mil caixas, Tritan (R$)', 0.37, P['por_mil_caixas_direto']['tritan'], 2, 'custo_real.json', 'R$ 0,37')
ok(10, 'por mil caixas, SAI (R$)', 0.29, P['por_mil_caixas_direto']['sai'], 2, 'custo_real.json', 'R$ 0,29')
ok(10, 'filamento em 24 meses, SAI (R$)', 908.37, S24['material'], 2, 'custo_real.json', 'R$ 908,37')
ok(10, 'mão de obra + inspeção em 24 meses, SAI (R$)', 564.84, S24['mao_de_obra'] + S24['inspecao'], 2, 'custo_real.json', 'R$ 564,84')
ok(10, 'trocas de PAD no ciclo (a cada 3 meses, a 24ª vai com a garra)', 7, S24['eventos']['trocas_pad'], 0, 'custo_real.json', '7 trocas de PAD')
ok(11, 'SAI compensa a instalação, previsto (dias)', 75, P['encontro_caixas']['dias'], 0, 'custo_real.json', 'compensa a instalação em 75 dias')
ok(11, 'SAI compensa a instalação, conservador (dias)', 110, CO['encontro_caixas']['dias'], 0, 'custo_real.json')
ok(11, 'caixas produzidas até compensar (mil)', 645, P['encontro_caixas']['caixas'] / 1000, 0, 'custo_real.json', '645 mil')
ok(11, 'linha parada em 2 anos, Tritan (min)', 360, 8 * 45, 0, 'equipe', 'Tritan 360 min')
ok(11, 'linha parada em 2 anos, SAI (min)', 100, P['linha_parada_min_24m']['sai'], 0, 'custo_real.json', 'SAI 100 min')
ok(11, 'caixas a mais em 2 anos', 1640, P['caixas_perdidas_24m']['tritan'] - P['caixas_perdidas_24m']['sai'], 0, 'custo_real.json', '1.640')
ok(0, 'caixas a mais, conservador', 960, CO['caixas_perdidas_24m']['a_mais'], 0, 'custo_real.json')
ok(11, 'caixas perdidas pelo Tritan (8 × 280)', 2240, 8 * 280, 0, 'equipe', 'Tritan perde 2.240')
ok(11, 'paradas surpresa em 2 anos (Tritan)', 8, P['paradas_surpresa_24m']['tritan'], 0, 'custo_real.json', '8 → 0')
ok(11, 'vida no pior caso no slide (anos)', 2.4, E['vida_pior_caso_anos'], 1, 'estudo_custos.json', '2,4 anos do pior caso')
ok(13, 'caixas a mais por ano', 820, (P['caixas_perdidas_24m']['tritan'] - P['caixas_perdidas_24m']['sai']) / 2, 0, 'custo_real.json', 'sobram 820 caixas')
ok(13, 'compensa a instalação em cerca de 75 dias (conclusão)', 75, P['encontro_caixas']['dias'], 0, 'custo_real.json', 'em cerca de 75 dias o SAI já compensa')

# ---------- Fusion (slides 6, 14) ----------
res = camp['results']
ok(14, 'FS mínimo PA6-CF = 102 ÷ 1ª principal', 19.8, 102 / 5.163, 1, 'COMPARACAO_SAMI', 'FS mínimo 19,8')
ok(14, 'FS mínimo Tritan = 58 ÷ 1ª principal', 11.5, 58 / 5.025, 1, 'COMPARACAO_SAMI', 'FS mínimo 11,5')
ok(14, 'PA6-CF deforma menos (%)', 65, (1 - 0.080 / 0.230) * 100, 0, 'COMPARACAO_SAMI', '65% menos')
ok(14, 'nós da malha', 498261, camp['mesh']['nodes'], 0, 'campanha_2026-11-11.json', '498.261')
cal = J('fusion/calibracao_pico.json')
ok(14, 'fator de pico = Fusion ÷ voxel (von Mises, peça maciça)', 2.2, cal['fusion_F1']['von_mises_max_MPa'] / cal['fe_voxels_H3mm']['von_mises_max_MPa'], 1, 'calibracao_pico.json', 'fator de pico 2,2')
ok(0, 'reação do FE de calibração = carga (N)', 355.36, cal['fe_voxels_H3mm']['reacao_Z_N'], 2, 'calibracao_pico.json')

# ---------- saída ----------
w = max(len(l['item']) for l in linhas)
for l in linhas:
    print(f"{l['slide']:>2} {l['item']:<{w}}  mostrado {l['mostrado']:<10} calculado {l['calculado']:<12} {l['status']}")
print(f'\n{len(linhas)} números conferidos, {len(falhas)} com problema.')
(D / 'verificacao_numeros.json').write_text(json.dumps(dict(conferidos=len(linhas), problemas=falhas, linhas=linhas), ensure_ascii=False, indent=1), encoding='utf-8')
sys.exit(1 if falhas else 0)
