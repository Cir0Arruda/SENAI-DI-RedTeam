"""Escreve os slides de Custos e Retorno no index.html a partir de dados/custos/custo_real.json (nada digitado à mão).

Substitui o trecho entre <!-- CUSTO:INICIO --> e <!-- CUSTO:FIM -->. Rodar depois de custo_real.py.
Uso: python dados/scripts/custo_slides.py   (na raiz do site)
"""
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
R = Path(__file__).resolve().parents[2]
C = json.loads((R / 'dados' / 'custos' / 'custo_real.json').read_text(encoding='utf-8'))
E = {k: v['valor'] for k, v in json.loads((R / 'dados' / 'custos' / 'entradas_custo.json').read_text(encoding='utf-8'))['entradas'].items()}


def br(v, d=0):
    s = f'{v:,.{d}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def mil(v):
    return f'R$ {br(v / 1000)} mil'


def mi(cx):
    return f'{br(cx / 1e6, 1)} milhões' if cx >= 1e6 else f'{br(cx / 1e3)} mil'


P = C['cenarios']['previsto']
S24, T24 = C['periodo_24m']['sai'], C['periodo_24m']['tritan']
ed, ec = P['encontro_direto'], P['encontro_caixas']
lp = P['linha_parada_min_24m']
h = lambda m: f'{br(m)} min' if m < 60 else f'{m // 60} h' if m % 60 == 0 else f'{br(m / 60, 1)} h'
EV = C['eventos']
cx = P['caixas_perdidas_24m']

linhas = [
    ('Filamento', 'PA6-CF R$ 420/kg · TPU R$ 158/kg · Tritan R$ 220/kg', T24['material'], S24['material']),
    ('Energia', 'impressora e secador de filamento', T24['energia'], S24['energia']),
    ('Impressora', 'depreciação, desgaste e bico endurecido', T24['impressora'] + T24['bico'], S24['impressora'] + S24['bico']),
    ('Impressões perdidas', 'refugo e consumíveis', T24['refugo'] + T24['consumiveis'], S24['refugo'] + S24['consumiveis']),
    ('Mão de obra', 'imprimir, acabar e trocar', T24['mao_de_obra'], S24['mao_de_obra']),
]
assert abs(sum(l[2] for l in linhas) - T24['direto']) < 0.02 and abs(sum(l[3] for l in linhas) - S24['direto']) < 0.02
tbl = '\n'.join(f'                    <tr><td>{a} <small>{b}</small></td><td>R$ {br(t, 2)}</td><td>R$ {br(s, 2)}</td></tr>' for a, b, t, s in linhas)
eco_d = P['direto_24m']['economia']

# tempo de impressão de todo o produto (Orca), peça por peça
ORCA = R / 'dados' / 'orca'
t_sup = json.loads((ORCA / 'r07_comparativo_fatiamento.json').read_text(encoding='utf-8'))['R07_SEM_SUPERIOR']['time_s'] / 3600
_b20 = json.loads((ORCA / 'r07_fatiamento_base20.json').read_text(encoding='utf-8'))
t_ie, t_id = _b20['INFERIOR_ESQ']['time_s'] / 3600, _b20['INFERIOR_DIR']['time_s'] / 3600
t_pad = C['impressoes']['pads']['horas']
t_tot = t_sup + t_ie + t_id + t_pad
assert abs(t_sup + t_ie + t_id - C['impressoes']['sai']['horas']) < 0.05
t_tri = C['impressoes']['tritan']['horas']
pecas = [('peça de cima', t_sup, '#e5232f'), ('peça de baixo, esq.', t_ie, '#f08a8f'), ('peça de baixo, dir.', t_id, '#f6b8bb'), ('8 PADs', t_pad, '#5b5bd6')]
imp_bar = ''.join(f'<i style="--w:{h / t_tot * 100:.2f}%; background:{c}" title="{n}: {br(h, 1)} h"></i>' for n, h, c in pecas)
imp_leg = ''.join(f'<span><i style="background:{c}"></i>{n} <b>{br(h, 1)} h</b></span>' for n, h, c in pecas)
pct_d = eco_d / P['direto_24m']['tritan'] * 100

html = f'''<!-- CUSTO:INICIO (gerado por dados/scripts/custo_slides.py a partir de dados/custos/custo_real.json) -->
        <section class="slide" data-title="Custos" id="s-custo">
          <div class="wrap wide">
            <div class="s-head compact">
              <span class="kicker">Custos · Custo real em 2 anos</span>
              <h2>Quanto custa a garra SAI <em>de verdade</em></h2>
            </div>
            <div class="split" style="--cols:minmax(0,1.08fr) minmax(0,1fr); align-items:start">
              <div style="display:grid; gap:12px">
              <div class="glass card chart" style="padding:14px 18px">
                <h4>Custo direto acumulado no ciclo de 2 anos <span class="tag sim" style="margin-left:6px">estimativa</span></h4>
                <p class="sub">material, energia, impressora, refugo e mão de obra · sem a produção parada · R$</p>
                <div class="legend"><span><i style="background:#5b5bd6"></i>Tritan (atual)</span><span><i style="background:#e5232f"></i>Garra SAI</span></div>
                <div id="chart-custo" class="roi-host"></div>
                <p class="note" style="margin:4px 0 0">A garra SAI começa mais cara: <b>R$ {br(EV['sai_inicio']['direto'], 2)}</b> para imprimir, montar e instalar. As linhas se cruzam com <b>{mi(ed['caixas'])} de caixas</b> ({br(ed['mes'], 1)} meses). No fim dos 2 anos ela custa <b>{round(pct_d)}% menos</b>.</p>
              </div>
                <div class="glass card imp-card">
                  <h3>Mesma impressora do Tritan, só troca o bico</h3>
                  <p>A impressora que já imprime o Tritan imprime o PA6-CF trocando só o bico por um de <b>aço endurecido</b>, que aguenta a fibra de carbono.</p>
                  <div class="imp-tot"><b>{br(t_tot, 1)} h</b><span>para imprimir todo o SAI (3 peças da garra + 8 PADs), cerca de <b>{br(t_tot / 24, 1)} dias</b> de impressora · a peça de Tritan leva {br(t_tri, 1)} h</span></div>
                  <div class="imp-bar" role="img" aria-label="Tempo de impressão por peça: peça de cima {br(t_sup, 1)} h, peças de baixo {br(t_ie, 1)} h e {br(t_id, 1)} h, 8 PADs {br(t_pad, 1)} h">{imp_bar}</div>
                  <div class="imp-leg">{imp_leg}</div>
                </div>
              </div>
              <div style="display:grid; gap:12px">
                <div class="glass card" style="padding:12px 16px">
                  <h3 style="margin:0 0 6px; font-size:15px">Para onde vai o dinheiro em 2 anos</h3>
                  <table class="tbl compact custo-tbl">
                    <thead><tr><th></th><th>Tritan (atual)</th><th>Garra SAI</th></tr></thead>
                    <tbody>
                    <tr><td>O que acontece</td><td>{T24['eventos']['quebras']} quebras <small>troca corretiva</small></td><td>1 garra + {S24['eventos']['trocas_pad']} trocas de PAD <small>troca preventiva</small></td></tr>
{tbl}
                    <tr class="total"><td>Custo direto em 2 anos</td><td>R$ {br(T24['direto'], 2)}</td><td><b>R$ {br(S24['direto'], 2)}</b></td></tr>
                    <tr><td>Por mil caixas produzidas</td><td>R$ {br(P['por_mil_caixas_direto']['tritan'], 2)}</td><td><b>R$ {br(P['por_mil_caixas_direto']['sai'], 2)}</b></td></tr>
                    </tbody>
                  </table>
                </div>
                <p class="note" style="margin:0"><span class="tag sim">preços de mercado</span> Lojas e tarifas de nov/2026: energia R$ 0,70/kWh (indústria, CPFL), técnico R$ {br(E['rs_h_tecnico'], 2)}/h com encargos, impressora K1 Max R$ 5.500 em 5.000 h. Tempos de troca da equipe: garra {E['min_parada_corretiva']} min; PADs em menos de {E['troca_pads_min']} min, sem parar a linha. Refugo e acabamento são hipóteses. Fontes em <a href="https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/dados/custos/entradas_custo.json" target="_blank" rel="noopener">entradas_custo.json</a>.</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Retorno: custo total com a produção parada, por caixas produzidas -->
        <section class="slide" data-title="Retorno (ROI)" id="s-roi">
          <div class="wrap wide">
            <div class="s-head compact" style="display:flex; justify-content:space-between; align-items:end; gap:16px; flex-wrap:wrap">
              <div>
                <span class="kicker">Custos · Retorno em produção</span>
                <h2>Contando as caixas, o SAI <em id="roi2-tit">compensa a instalação em {ec['dias']} dias</em></h2>
              </div>
              <div class="seg" id="roi2-cen" role="tablist" aria-label="Cenário do SAI">
                <button class="on" role="tab" aria-selected="true" data-c="previsto">Previsto</button>
                <button role="tab" aria-selected="false" data-c="conservador">Conservador</button>
              </div>
            </div>
            <div class="split" style="--cols:minmax(0,1.08fr) minmax(0,1fr); align-items:start">
              <div class="glass card chart" style="padding:14px 18px">
                <h4>Caixas perdidas com a linha parada, somadas mês a mês <span class="tag sim" style="margin-left:6px">estimativa</span></h4>
                <p class="sub">quanto mais baixa a linha, melhor · cada troca de garra para a linha {E['min_parada_corretiva']} min e perde {E['caixas_parada_corretiva']} caixas</p>
                <div class="legend"><span><i style="background:#5b5bd6"></i>Tritan (atual)</span><span><i style="background:#e5232f"></i>Garra SAI</span></div>
                <div id="chart-roi2" class="roi-host"></div>
                <p class="note" id="roi2-txt" style="margin:4px 0 0">Previsto: a garra SAI só para a linha na instalação. Os PADs são trocados a cada trimestre em menos de {E['troca_pads_min']} min, sem contar como parada.</p>
              </div>
              <div style="display:grid; gap:12px">
                <div class="g2 roi-kpi">
                  <div class="glass stat sm"><b id="roi2-pb">{ec['dias']} dias</b><span>para compensar a parada da instalação</span><small id="roi2-pb-s">cerca de {br(ec['mes'], 0 if ec['mes'] % 1 == 0 else 1)} meses de linha rodando</small></div>
                  <div class="glass stat sm"><b class="ink" id="roi2-cx">{br(cx['a_mais'])}</b><span>caixas a mais em 2 anos</span><small id="roi2-cx-s">Tritan perde {br(cx['tritan'])}; SAI {br(cx['sai'])}</small></div>
                  <div class="glass stat sm"><b class="ink" id="roi2-min">{h(lp['tritan'])} → {h(lp['sai'])}</b><span>de linha parada em 2 anos</span><small id="roi2-min-s">Tritan {br(lp['tritan'])} min; SAI {br(lp['sai'])} min</small></div>
                  <div class="glass stat sm"><b class="ink" id="roi2-sp">{P['paradas_surpresa_24m']['tritan']} → {P['paradas_surpresa_24m']['sai']}</b><span>paradas surpresa em 2 anos</span><small>viram trocas com data marcada</small></div>
                </div>
                <div class="glass card prev-card" style="padding:12px 16px">
                  <h3 style="margin:0 0 8px; font-size:15px">Da manutenção corretiva para a preventiva</h3>
                  <div class="prev-tl" aria-hidden="true">
                    <div class="pt-row"><span class="pt-l">Tritan</span><div class="pt-bar tri">{''.join(f'<i style="--x:{(q * 3 - 1.5) / 24 * 100:.2f}%"></i>' for q in range(1, 9))}</div></div>
                    <div class="pt-row"><span class="pt-l">SAI</span><div class="pt-bar sai"><i class="g" style="--x:0%"></i>{''.join(f'<i class="p" style="--x:{q * 3 / 24 * 100:.2f}%"></i>' for q in range(1, 8))}<i class="g" style="--x:100%"></i></div></div>
                    <div class="pt-ax"><span>início</span><span>1 ano</span><span>2 anos</span></div>
                    <div class="pt-leg"><span><i class="q"></i>quebra: para {E['min_parada_corretiva']} min</span><span><i class="s"></i>troca de garra: {E['min_parada_corretiva']} min, com data</span><span><i class="p"></i>troca de PAD: menos de {E['troca_pads_min']} min, não para</span></div>
                  </div>
                  <ul class="hip">
                    <li><b>Hoje, corretiva:</b> a garra quebra sem aviso, cerca de 4 vezes por ano, e a linha para na hora: {E['min_parada_corretiva']} min e {E['caixas_parada_corretiva']} caixas por quebra.</li>
                    <li><b>Com o SAI, preventiva:</b> a linha só para na instalação e na garra nova a cada 2 anos ({E['min_parada_corretiva']} min, como hoje), antes dos {br(E['vida_pior_caso_anos'], 1)} anos do pior caso, com data marcada e peça pronta. Os PADs são trocados a cada trimestre em menos de {E['troca_pads_min']} min, sem contar como parada.</li>
                  </ul>
                </div>
              </div>
            </div>
            <p class="note" style="margin:8px 0 0"><span class="tag sim">estimativa</span> A quebra do Tritan é aleatória (em média 1 a cada 3 meses, dado da equipe), por isso a linha é reta e não em degraus. Troca de garra: {E['min_parada_corretiva']} min e {EV['sai_troca']['caixas']} caixas, igual no Tritan e no SAI; troca de PAD: menos de {E['troca_pads_min']} min, não conta como parada (tempos da equipe). A garra nova dos 2 anos já é do ciclo seguinte. Caixas sem converter em reais. Conservador: a garra SAI dura só {C['cenarios']['conservador']['vida_meses']} meses e ainda quebra {round(C['cenarios']['conservador']['quebras_sai_ano'])} vez por ano.</p>
          </div>
        </section>
<!-- CUSTO:FIM -->'''

p = R / 'index.html'
t = p.read_text(encoding='utf-8')
if '<!-- CUSTO:INICIO' in t:
    t2 = re.sub(r'<!-- CUSTO:INICIO.*?<!-- CUSTO:FIM -->', lambda m: html, t, count=1, flags=re.S)
else:
    ini = t.index('        <section class="slide" data-title="Custos" id="s-custo">')
    fim = t.index('        <!-- Sustentabilidade e segurança -->')
    t2 = t[:ini] + html + '\n\n' + t[fim:]
p.write_text(t2, encoding='utf-8', newline='')
print('ok', len(t), '->', len(t2))
