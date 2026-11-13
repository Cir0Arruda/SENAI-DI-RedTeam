"""Custo real da garra SAI contra a garra de Tritan, com os custos ocultos, e a produção perdida em caixas.

Entradas: dados/custos/entradas_custo.json (cada valor com tipo e fonte: equipe, medido, pesquisa ou HIP).
Saídas:   dados/custos/custo_real.json e assets/js/custo-dados.js (dados dos gráficos dos slides de Custos e Retorno).
Uso:      python dados/scripts/custo_real.py   (na raiz do site)

Modelo:
  - Custo direto (R$, preços de mercado): cada impressão custa material + energia (impressora, secagem do filamento e
    secador durante a impressão) + uso da impressora (depreciação e desgaste) + desgaste do bico endurecido (só PA6-CF)
    + consumíveis + refugo (a fração perdida em falhas, sobre material, energia e máquina) + mão de obra.
  - Produção (caixas): cada parada da linha deixa de produzir caixas no ritmo da linha (6 por minuto);
    a quebra do Tritan perde 280 caixas (dado da equipe). As caixas NÃO são convertidas em reais:
    o valor real da caixa para a fábrica não é conhecido.
  - Garra SAI: compra no início (3 peças + 8 PADs + montagem + instalação numa parada programada);
    troca preventiva a cada 24 meses; PADs a cada trimestre, também em parada programada; checklist semanal.
  - Tritan: já está instalada. Quebra em média 4 vezes por ano; cada quebra custa a reimpressão da peça
    superior + a troca corretiva, e para a linha 45 min. Como a quebra é aleatória, o gráfico usa o valor
    esperado: uma reta, não uma escada.
"""
import copy, json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
R = Path(__file__).resolve().parents[2]
D = R / 'dados'
E0 = json.loads((D / 'custos' / 'entradas_custo.json').read_text(encoding='utf-8'))
V0 = {k: v['valor'] for k, v in E0['entradas'].items()}
r2 = lambda x: round(x, 2)
CAT = ['material', 'energia', 'impressora', 'bico', 'consumiveis', 'refugo', 'mao_de_obra']


def modelo(V):
    CX_MIN = V['caixas_por_min']
    CX_MES = CX_MIN * 60 * V['horas_ano'] / 12
    TAR, RH = V['tarifa_kwh_rs'], V['rs_h_tecnico']
    MAQ_H = V['impressora_preco_rs'] / V['impressora_vida_h'] + V['desgaste_geral_rs_h']

    def impressao(nome, kg, preco_kg, horas, n_imp, refugo, seca_h_kg, cf, pos_min):
        mat = kg * preco_kg
        ene = horas * V['impressora_kw'] * TAR + kg * seca_h_kg * V['secador_kw'] * TAR
        if cf:
            ene += horas * V['secador_na_impressao_kw'] * TAR
        maq = horas * MAQ_H
        bico = horas * V['bico_cf_rs_h'] if cf else 0.0
        cons = n_imp * V['consumiveis_rs_impressao']
        ref = refugo * (mat + ene + maq + bico)
        mo = (n_imp * V['preparo_min_impressao'] + pos_min) / 60 * RH
        c = dict(material=mat, energia=ene, impressora=maq, bico=bico, consumiveis=cons, refugo=ref, mao_de_obra=mo)
        return {'nome': nome, 'horas': horas, 'kg': kg, **{k: r2(v) for k, v in c.items()}, 'total': r2(sum(c.values()))}

    def parada(minutos, programada, caixas=None):
        perde = (not programada) or V['parada_programada_perde_producao']
        cx = (caixas if caixas is not None else CX_MIN * minutos) if perde else 0
        return {'min': minutos, 'linha_parada_min': minutos if perde else 0, 'mao_de_obra': r2(minutos / 60 * RH), 'caixas': cx}

    kg_sai, kg_pad = V['sai_fil_g'] / 1000, V['pads_fil_g'] / 1000
    imp_sai = impressao('garra SAI (3 peças)', kg_sai, V['preco_pacf_kg'], V['sai_horas'], V['sai_impressoes'],
                        V['refugo_pacf'], V['secagem_pacf_h_kg'], True, 3 * V['pos_min_peca_grande'] + V['montagem_sai_min'])
    imp_pad = impressao('8 PADs', kg_pad, V['preco_tpu_kg'], V['pads_horas'], 1, V['refugo_tpu'], V['secagem_tpu_h_kg'], False,
                        V['pos_min_pads'])
    imp_tri = impressao('peça superior de Tritan', V['tritan_sup_kg'], V['preco_tritan_kg'],
                        V['tritan_garra_horas'] * V['tritan_sup_frac'], 1, V['refugo_tritan'], V['secagem_tritan_h_kg'], False,
                        V['pos_min_peca_grande'])
    par = {'sai_troca': parada(V['troca_garra_min'] + V['troca_pads_min'], True),
           'pads': parada(V['troca_pads_min'], True),
           'corretiva': parada(V['min_parada_corretiva'], False, V['caixas_parada_corretiva'])}

    def evento(nome, imps, p):
        c = {k: sum(i[k] for i in imps) for k in CAT}
        c['mao_de_obra'] += p['mao_de_obra']
        return {'nome': nome, **{k: r2(v) for k, v in c.items()}, 'direto': r2(sum(c.values())), 'parada_min': p['min'],
                'linha_parada_min': p['linha_parada_min'], 'caixas': p['caixas']}

    EV = {'sai_inicio': evento('compra e instalação da garra SAI (com 8 PADs)', [imp_sai, imp_pad], par['sai_troca']),
          'sai_troca': evento('troca preventiva da garra SAI (com 8 PADs novos)', [imp_sai, imp_pad], par['sai_troca']),
          'pads': evento('troca dos 8 PADs', [imp_pad], par['pads']),
          'tritan': evento('quebra da garra de Tritan (troca corretiva)', [imp_tri], par['corretiva']),
          'sai_quebra': evento('quebra inesperada da garra SAI (conservador)', [imp_sai, imp_pad], par['corretiva'])}
    # checklist semanal do PAD, por trimestre (13 semanas)
    insp_min = V['inspecao_min_semana'] * 52 / 4 if V['inspecao_perde_producao'] else 0
    INSP = {'direto': r2(V['inspecao_min_semana'] / 60 * RH * 52 / 4), 'caixas': insp_min * CX_MIN, 'linha_parada_min': insp_min}

    TRI, N = 3, V['horizonte_meses'] // 3
    VIDA, PAD_M = V['sai_troca_preventiva_meses'], V['pads_troca_meses']
    Q_TRI = V['quebras_tritan_ano'] / 4

    def serie(campo, q_sai, vida, meses=N * TRI, troca_no_fim=True):
        """Valor esperado acumulado no fim de cada trimestre (campo: direto em R$, caixas ou linha_parada_min).
        troca_no_fim=False: o ciclo de 2 anos termina antes da garra nova (ela já serve o ciclo seguinte)."""
        sai = tri = 0.0
        out = []
        for q in range(meses // TRI + 1):
            m = q * TRI
            if q == 0:
                sai += EV['sai_inicio'][campo]
            else:
                tri += Q_TRI * EV['tritan'][campo]
                sai += INSP[campo] + q_sai / 4 * EV['sai_quebra'][campo]
                if m % vida == 0:
                    sai += EV['sai_troca'][campo] if (troca_no_fim or m < meses) else 0
                elif m % PAD_M == 0:
                    sai += EV['pads'][campo]
            out.append({'mes': m, 'caixas': round(m * CX_MES), 'tritan': r2(tri), 'sai': r2(sai)})
        return out

    def encontro(s):
        for a, b in zip(s, s[1:]):
            d0, d1 = a['sai'] - a['tritan'], b['sai'] - b['tritan']
            if d0 > 0 >= d1:
                k = d0 / (d0 - d1)
                mes = a['mes'] + k * (b['mes'] - a['mes'])
                return {'mes': round(mes, 2), 'dias': round(mes * 365 / 12), 'caixas': round(mes * CX_MES),
                        'valor': r2(a['sai'] + k * (b['sai'] - a['sai']))}
        return None

    cx24 = 24 * CX_MES
    n_pad_24 = len([m for m in range(PAD_M, 24, PAD_M) if m % VIDA])
    cen = {}
    for nome, q, vida in (('previsto', 0.0, VIDA), ('conservador', V['conservador_quebras_sai_ano'], V['conservador_vida_meses'])):
        sd = serie('direto', q, vida, 24, False)          # Custos: o ciclo de 2 anos
        sc = serie('caixas', q, vida)                     # Retorno: caixas perdidas até 30 meses
        a, c24 = sd[-1], serie('caixas', q, vida, 24, False)[-1]
        mn = serie('linha_parada_min', q, vida, 24, False)[-1]
        n_troca = len(range(vida, 24, vida))
        n_pad = len([m for m in range(PAD_M, 24, PAD_M) if m % vida])
        cen[nome] = {
            'vida_meses': vida, 'quebras_sai_ano': q, 'trocas_garra_24m': n_troca, 'trocas_pad_24m': n_pad,
            'serie_direto': sd, 'serie_caixas': sc, 'encontro_direto': encontro(sd), 'encontro_caixas': encontro(sc),
            'direto_24m': {'tritan': a['tritan'], 'sai': a['sai'], 'economia': r2(a['tritan'] - a['sai'])},
            'por_mil_caixas_direto': {'tritan': r2(a['tritan'] / cx24 * 1000), 'sai': r2(a['sai'] / cx24 * 1000)},
            'caixas_perdidas_24m': {'tritan': round(c24['tritan']), 'sai': round(c24['sai']), 'a_mais': round(c24['tritan'] - c24['sai'])},
            'linha_parada_min_24m': {'tritan': round(mn['tritan']), 'sai': round(mn['sai'])},
            'paradas_surpresa_24m': {'tritan': round(V['quebras_tritan_ano'] * 2), 'sai': round(q * 2)},
            'paradas_programadas_24m': {'tritan': 0, 'sai': 1 + n_troca + n_pad},
        }

    # 24 meses por categoria (slide de Custos)
    def soma(lista, extra=0.0):
        d = {k: r2(sum(EV[e][k] * n for e, n in lista)) for k in CAT + ['direto', 'caixas']}
        d['inspecao'] = r2(extra)
        d['direto'] = r2(d['direto'] + extra)
        return d
    p24 = {'sai': soma([('sai_inicio', 1), ('pads', n_pad_24)], INSP['direto'] * 8),
           'tritan': soma([('tritan', V['quebras_tritan_ano'] * 2)])}
    p24['sai']['eventos'] = {'garras': 1, 'trocas_pad': n_pad_24, 'paradas_programadas': 1 + n_pad_24, 'paradas_surpresa': 0}
    p24['tritan']['eventos'] = {'quebras': V['quebras_tritan_ano'] * 2, 'paradas_programadas': 0, 'paradas_surpresa': V['quebras_tritan_ano'] * 2}

    return {
        'producao': {'caixas_por_min': CX_MIN, 'caixas_por_mes': round(CX_MES), 'caixas_24m': round(cx24)},
        'impressora_rs_h': r2(MAQ_H), 'inspecao_trimestre_rs': INSP['direto'],
        'impressoes': {'sai': imp_sai, 'pads': imp_pad, 'tritan': imp_tri}, 'paradas': par,
        'eventos': EV, 'periodo_24m': p24, 'cenarios': cen,
        'vida': {'pior_caso_anos': V['vida_pior_caso_anos'], 'troca_preventiva_meses': VIDA, 'pads_meses': PAD_M},
    }


BASE = modelo(V0)

# ---------- sensibilidade: cada dúvida muda uma entrada ----------
SENS = [
    ('PA6-CF pelo preço da equipe (R$ 258/kg)', {'preco_pacf_kg': 258}),
    ('PA6-CF Bambu Lab (R$ 786/kg)', {'preco_pacf_kg': 786}),
    ('material da peça de Tritan a R$ 250 (valor da equipe), mais os custos ocultos', {'preco_tritan_kg': 250 / V0['tritan_sup_kg']}),
    ('mão de obra mais cara (R$ 43,91/h)', {'rs_h_tecnico': 43.91}),
    ('impressora a 280 W e tarifa B3 (R$ 0,99/kWh)', {'impressora_kw': 0.28, 'tarifa_kwh_rs': 0.99}),
    ('refugo de 20% no PA6-CF', {'refugo_pacf': 0.20}),
    ('Tritan quebra só 2 vezes por ano', {'quebras_tritan_ano': 2}),
    ('270 caixas por quebra (45 min × 6/min)', {'caixas_parada_corretiva': 270}),
    ('trocas programadas dentro da janela de sanitização (sem perder caixas)', {'parada_programada_perde_producao': False}),
    ('inspeção semanal do PAD com a linha parada (fora da janela de limpeza)', {'inspecao_perde_producao': True}),
]
sens = []
for nome, mud in SENS:
    V = copy.deepcopy(V0); V.update(mud)
    m = modelo(V)['cenarios']['previsto']
    sens.append({'caso': nome, 'mudanca': mud,
                 'encontro_direto_meses': m['encontro_direto']['mes'] if m['encontro_direto'] else None,
                 'encontro_caixas_dias': m['encontro_caixas']['dias'] if m['encontro_caixas'] else None,
                 'economia_direta_24m': m['direto_24m']['economia'], 'caixas_a_mais_24m': m['caixas_perdidas_24m']['a_mais']})

out = {'gerado_por': 'dados/scripts/custo_real.py', 'entradas': 'dados/custos/entradas_custo.json', **BASE, 'sensibilidade': sens}
(D / 'custos' / 'custo_real.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
(R / 'assets' / 'js' / 'custo-dados.js').write_text(
    '// Gerado por dados/scripts/custo_real.py a partir de dados/custos/entradas_custo.json. Não editar à mão.\n'
    'window.CUSTO = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')

if __name__ == '__main__':
    print('impressora R$/h', BASE['impressora_rs_h'])
    for k, i in BASE['impressoes'].items():
        print(f"impressão {k:7}", {c: i[c] for c in CAT}, 'total', i['total'])
    for k, e in BASE['eventos'].items():
        print(f"{k:11} direto {e['direto']:9.2f}  caixas {e['caixas']:5}  linha parada {e['linha_parada_min']} min")
    for c in ('previsto', 'conservador'):
        p = BASE['cenarios'][c]
        print(c, '| encontro direto', p['encontro_direto'], '| caixas', p['encontro_caixas'])
        print('   24m direto', p['direto_24m'], '| por mil cx', p['por_mil_caixas_direto'])
        print('   caixas', p['caixas_perdidas_24m'], 'min', p['linha_parada_min_24m'], 'surpresa', p['paradas_surpresa_24m'],
              'programadas', p['paradas_programadas_24m'])
    print('24m categorias SAI', BASE['periodo_24m']['sai'])
    print('24m categorias TRI', BASE['periodo_24m']['tritan'])
    for s in sens:
        print(f"  {s['caso'][:62]:62} enc.direto {s['encontro_direto_meses']} m | enc.caixas {s['encontro_caixas_dias']} d | eco dir {s['economia_direta_24m']} | caixas a mais {s['caixas_a_mais_24m']}")
