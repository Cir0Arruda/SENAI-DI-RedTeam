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
ok(10, 'filamento da garra (g)', 1744.5, fil, 1, 'Orca', '1.744,5')
ok(14, 'tempo de impressão da garra (h)', 75.2, horas, 1, 'Orca', '75,2 h')
ok(10, 'filamento dos PADs (g)', 139, pads['Orca_summary']['total_filament_mass_g'], 0, 'Orca', '139')
ok(0, 'tempo dos PADs (h)', 11.0, pads['Orca_summary']['prediction_s'] / 3600, 1, 'Orca')
pads_g = pads['category_mass_g']['peca']
conj = 2834 - float(peso['TRITAN']['garra_g']) + sup + ie + idr + pads_g
ok(10, 'conjunto SAI com 8 PADs (kg)', 2.783, conj / 1000, 3, 'peso_conjunto.csv + PADs', '2,783 kg')
ok(10, 'mais leve que a atual (g)', 51, 2834 - conj, 0, 'peso_conjunto.csv + PADs', '51 g')
ok(13, 'mais leve que a atual (%)', 1.8, (2834 - conj) / 2834 * 100, 1, 'peso_conjunto.csv + PADs', '(−1,8%)')
ok(12, 'garra sozinha, menos que a de Tritan (g)', 144, float(peso['TRITAN']['garra_g']) - (sup + ie + idr), 0, 'peso_conjunto.csv', '144 g menos')

# ---------- custos (slides 10, 11, 13) ----------
PA, TPU, BICO, TRI = 258, 158, 23.50, 250
garra_rs, pads_rs = round(fil / 1000 * PA, 2), round(139.0 / 1000 * TPU, 2)
aq = garra_rs + pads_rs + BICO
ok(10, 'material da garra (R$)', 450.08, fil / 1000 * PA, 2, 'Orca × R$ 258/kg', '450,08')
ok(10, 'material dos PADs (R$)', 21.96, 139.0 / 1000 * TPU, 2, 'Orca × R$ 158/kg', 'R$ 21,96')
ok(10, 'custo de aquisição (R$)', 495.54, aq, 2, 'soma', 'R$ 495,54')
ok(10, 'gasto no ano: garra + 6 trocas de PAD (R$)', 627.30, aq + 6 * pads_rs, 2, 'soma', 'R$ 627,30')
ok(10, 'diferença na compra (R$)', 245.54, aq - TRI, 2, 'soma', 'R$ 245,54')
ok(10, 'gasto no ano menor (%)', 37, (1 - (aq + 6 * pads_rs) / (4 * TRI)) * 100, 0, 'soma', '37% menor')
ok(10, 'fatia da garra (%)', 91, garra_rs / aq * 100, 0, 'soma', 'garra · 91%')
ok(10, 'fatia dos PADs (%)', 4, pads_rs / aq * 100, 0, 'soma', '8 PADs · 4%')
ok(10, 'fatia do bico (%)', 5, BICO / aq * 100, 0, 'soma', 'bico · 5%')
sai24 = aq + 12 * pads_rs
ok(11, 'Tritan em 24 meses (R$)', 2000, 8 * TRI, 0, 'quebra a cada 3 meses')
ok(11, 'SAI em 24 meses (R$)', 759.06, sai24, 2, 'garra + 12 trocas de PAD', 'R$ 759,06')
ok(11, 'economia em 2 anos (R$)', 1240.94, 8 * TRI - sai24, 2, 'conta', 'R$ 1.240,94')
ok(11, 'retorno (%)', 163, (8 * TRI - sai24) / sai24 * 100, 0, 'conta', '163%')
pb = next(m for m in range(1, 25) if TRI * (m // 3) > aq + pads_rs * (m // 2))
ok(11, 'mês em que o SAI se paga', 9, pb, 0, 'conta', '9 meses')
ok(11, 'SAI R$ por hora (24 h × 730 h/mês)', 0.04, sai24 / (24 * 730), 2, 'conta', 'R$ 0,04')
ok(11, 'Tritan R$ por hora', 0.11, 8 * TRI / (24 * 730), 2, 'conta', 'R$ 0,11')

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
