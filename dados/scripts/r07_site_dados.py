"""Gera assets/js/r07-dados.js para o site a partir dos JSON publicados em dados/ (nada é digitado à mão).

Uso: python r07_site_dados.py <pasta do site>
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / 'SENAI-DI-REDTEAM-APRESENTACAO'
DD = SITE / 'dados'
PRECO_PACF = 258.0   # R$/kg (dado da equipe)
PRECO_TPU = 158.0    # R$/kg (dado da equipe)
RHO_TRI, RHO_PA = 1.18, 1.10


def jl(rel):
    return json.loads((DD / rel).read_text(encoding='utf-8'))


dec = jl('decisao/DECISAO_ESQUELETO.json')
V = dec['variantes']
KEYS = [
    ('R07_COM', 'R07 COM esqueleto (giroide 25/20% + zonas)', 'R07 com esqueleto', 'F25_COM'),
    ('R07_SEM', 'R07 SEM esqueleto (mesmas zonas)', 'R07 sem esqueleto', 'F25_SEM'),
    ('UNI_30', 'Uniforme giroide 30%', 'Giroide 30% uniforme', 'UNI_30'),
    ('UNI_35', 'Uniforme giroide 35%', 'Giroide 35% uniforme', None),
    ('UNI_40', 'Uniforme giroide 40%', 'Giroide 40% uniforme', 'UNI_40'),
    ('HEXA30', 'Uniforme 3D honeycomb 30% (citado como atual)', 'Hexa3D 30% (PA6-CF)', None),
    ('TPMSD40', 'Uniforme TPMS-D 40% (proposta do documento)', 'TPMS-D 40% (proposta)', None),
    ('R06', 'R06 (zonal TPMS-D, atual do projeto)', 'R06 zonal TPMS-D', None),
]
out = {'tritan_g': dec['referencia_instalada']['pecas_impressas_g'], 'variantes': []}
for k, name, rot, imp in KEYS:
    v = V[name]; m = v['massa']; mt = v.get('montagem') or {}
    rec = {'k': k, 'rot': rot, 'garra_g': m['garra_g'], 'sup_g': m['superior_g'], 'inf_g': m['inferior_g'],
           'fil_g': m['filamento_g'], 'tempo_h': m['tempo_h'], 'pct_tritan': m['delta_vs_Tritan_Hexa3D30_pct'],
           'custo_rs': round(m['filamento_g'] / 1000 * PRECO_PACF, 2),
           'proprio_fe': k not in ('HEXA30', 'TPMSD40')}
    if mt:
        rec.update(kg_pa6=mt['kg_max_PA6-CF_Z48'], kg_paht=mt['kg_max_PAHT_CF15_Z18.2'], fs24_pa6=mt['FS_24kg_PA6-CF_Z48'],
                   fs30_pa6=mt['FS_30kg_PA6-CF_Z48'], fs24_paht=mt['FS_24kg_PAHT_CF15_Z18.2'], fs30_paht=mt['FS_30kg_PAHT_CF15_Z18.2'],
                   k_asa=mt['rigidez_asa_montada_N_mm'], desl24=mt['desl_24kg_mm'], sz24=mt['sigma_Z_24kg_MPa_(x PICO)'],
                   vida_paht=v['fadiga_PAHT'], vida_pa6=v['fadiga_PA6CF'])
    if imp:
        im = jl(f'impacto/impacto_{imp}.json')
        h = im['hist']; pico = 2.2
        rec['impacto'] = {'f1': im['f1_Hz_com_24kg'], 'fd': im['fator_dinamico_3D'], 'sz': im['sigma_Z_pico_MPa_(x PICO)'],
                          'fi_gir': im['FI_giroide_pico'], 'desl': im['desl_pico_mm'], 'fs_pa6': im['FS_dinamico_PA6CF_Z48'],
                          'fs_paht': im['FS_dinamico_PAHT_Z18.2'], 't_pico': im['t_pico_ms'], 'massa_fe': im['massa_FE_g'],
                          # série a cada 1 ms: [t, sigmaZ (MPa, x pico), FI giroide, deslocamento mm]
                          'serie': [[h['t_ms'][i], round(h['FI_z'][i] * 48 * pico, 2), round(h['FI_giroide'][i], 3), round(h['disp_mm'][i], 3)]
                                    for i in range(1, len(h['t_ms']), 2)]}
    out['variantes'].append(rec)

pad = jl('orca/pads_tpu95a_fatiamento.json')
out['pads'] = {'n': 8, 'peca_g': round(pad['category_mass_g']['peca'], 1), 'total_g': pad['Orca_summary']['total_filament_mass_g'],
               'tempo_h': round(pad['Orca_summary']['prediction_s'] / 3600, 1), 'infill': pad['effective_settings']['sparse_infill_density'],
               'padrao': pad['effective_settings']['sparse_infill_pattern'], 'paredes': pad['effective_settings']['wall_loops']}
out['pads']['custo_un_peca'] = round(out['pads']['peca_g'] / 8 / 1000 * PRECO_TPU, 2)
out['pads']['custo_un_total'] = round(out['pads']['total_g'] / 8 / 1000 * PRECO_TPU, 2)
out['precos'] = {'pacf_kg': PRECO_PACF, 'tpu_kg': PRECO_TPU}

js = ('// Gerado por desempenho/scripts/r07_site_dados.py a partir de dados/*.json (Orca, FE da montagem, impacto). Não editar à mão.\n'
      'window.R07 = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
(SITE / 'assets' / 'js' / 'r07-dados.js').write_text(js, encoding='utf-8')
print('ok', len(js), 'bytes')
for r in out['variantes']:
    print(r['k'], r['garra_g'], r['pct_tritan'], r['custo_rs'], r.get('kg_pa6'), r.get('impacto', {}).get('fs_paht'))
print(out['pads'])
