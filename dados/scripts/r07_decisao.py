"""R07 - Tabela de DECISÃO (com x sem esqueleto x preenchimento uniforme) para a equipe.

Junta só resultados já calculados (nada inventado):
  massa/consumo/tempo  -> fatiamentos reais do Orca (K1 Max, 1:1, PA6-CF, 5 paredes)
  resistência          -> FE por voxels da MONTAGEM (superior + inferior direita), 24/30 kg numa asa
  impacto              -> FE transiente 3D (tranco de 24 kg em 10 ms) da peça superior
  fadiga               -> curva S-N normalizada (mesma hipótese do r07_vida) com a tensão da montagem
Saídas: 06_Engenharia/R07/DECISAO_ESQUELETO.json
"""
from __future__ import annotations
import json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / '06_Engenharia' / 'R07'
ORCA = ROOT / '05_Orca'
G, A = 9.80665, 5.0
F24 = 24 * (G + A)


def jl(p):
    p = Path(p)
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


r06 = jl(ORCA / 'R06' / 'r06_fatiamento_resumo.json')
b25 = jl(ORCA / 'R07' / 'r07_fatiamento_base25.json')
b20 = jl(ORCA / 'R07' / 'r07_fatiamento_base20.json')
cmp_ = jl(ORCA / 'R07' / 'COMPARATIVO' / 'r07_comparativo_fatiamento.json')


def part(rec):
    if not rec or not rec.get('ok', True) or 'mass_g' not in rec:
        return None
    return {'peca_g': rec['mass_g']['peca'], 'filamento_g': rec['orca_total_g'], 'tempo_h': rec['time_s'] / 3600}


def garra(sup, inf_esq, inf_dir=None):
    """Garra = superior + 2 inferiores (direita = espelho da esquerda quando não fatiada)."""
    if not sup or not inf_esq:
        return None
    inf_dir = inf_dir or inf_esq
    t = lambda k: sup[k] + inf_esq[k] + inf_dir[k]
    return {'superior_g': round(sup['peca_g'], 1), 'inferior_g': round(inf_esq['peca_g'], 1),
            'garra_g': round(t('peca_g'), 1), 'filamento_g': round(t('filamento_g'), 1), 'tempo_h': round(t('tempo_h'), 1)}


C = lambda k: part(cmp_.get(k))
VAR = {
    'R06 (zonal TPMS-D, atual do projeto)': dict(massa=garra(part(r06.get('SUPERIOR')), part(r06.get('INFERIOR_ESQ')), part(r06.get('INFERIOR_DIR'))),
                                                 fe='R06', imp='R06'),
    'R07 COM esqueleto (giroide 25/20% + zonas)': dict(massa=garra(part(b25.get('SUPERIOR')), part(b20.get('INFERIOR_ESQ')), part(b20.get('INFERIOR_DIR'))),
                                                       fe='R07_COM', imp='F25_COM'),
    'R07 SEM esqueleto (mesmas zonas)': dict(massa=garra(C('R07_SEM_SUPERIOR'), part(b20.get('INFERIOR_ESQ')), part(b20.get('INFERIOR_DIR'))),
                                             fe='R07_SEM', imp='F25_SEM'),
    'Uniforme giroide 30%': dict(massa=garra(C('UNI_GIROIDE30_SUPERIOR'), C('UNI_GIROIDE30_INFERIOR_ESQ')), fe='UNI_30', imp='UNI_30'),
    'Uniforme giroide 35%': dict(massa=garra(C('UNI_GIROIDE35_SUPERIOR'), C('UNI_GIROIDE35_INFERIOR_ESQ')), fe='UNI_35', imp=None),
    'Uniforme giroide 40%': dict(massa=garra(C('UNI_GIROIDE40_SUPERIOR'), C('UNI_GIROIDE40_INFERIOR_ESQ')), fe='UNI_40', imp='UNI_40'),
    'Uniforme 3D honeycomb 30% (citado como atual)': dict(massa=garra(C('UNI_HONEYCOMB3D30_SUPERIOR'), C('UNI_HONEYCOMB3D30_INFERIOR_ESQ')),
                                                          fe='UNI_30', imp=None, nota='resistência = giroide 30% (a lei homogeneizada não distingue o padrão)'),
    'Uniforme TPMS-D 40% (proposta do documento)': dict(massa=garra(C('UNI_TPMSD40_SUPERIOR'), C('UNI_TPMSD40_INFERIOR_ESQ')),
                                                        fe='UNI_40', imp=None, nota='resistência = giroide 40% (a lei homogeneizada não distingue o padrão)'),
}


def hours(sig12, sig24, S, ciclos_h=480, erro=0.01):
    n = lambda s: 1.0 if s >= S else 10 ** ((1 - s / S) / 0.10)
    n12, n24 = n(sig12), n(sig24)
    return {'so_12kg_h': round(n12 / ciclos_h), 'mix_1pct_24kg_h': round(1 / (ciclos_h * ((1 - erro) / n12 + erro / n24)))}


def main():
    ref = VAR['R06 (zonal TPMS-D, atual do projeto)']['massa']
    hx = VAR['Uniforme 3D honeycomb 30% (citado como atual)']['massa']
    # garra instalada (deck do cliente): Tritan Hexa3D 30% -> mesmo caminho do Hexa3D 30% PA6-CF x 1,18/1,10
    tri = round(hx['garra_g'] * 1.18 / 1.10, 1) if hx else None
    out = {'fontes': {'massa': 'Orca CLI K1 Max 1:1 (05_Orca)', 'resistencia': 'FE voxels montagem (06_Engenharia/R07/MONTAGEM)',
                      'impacto': 'FE transiente 3D (06_Engenharia/R07/IMPACTO)'},
           'referencia_instalada': {'descricao': 'Garra atual Tritan Hexa3D 30% (deck do cliente); massa = fatiamento Hexa3D 30% x 1,18/1,10',
                                    'pecas_impressas_g': tri}, 'variantes': {}}
    for name, cfg in VAR.items():
        rec = {'massa': cfg['massa']}
        if cfg['massa'] and ref:
            rec['massa']['delta_vs_R06_pct'] = round(100 * (cfg['massa']['garra_g'] / ref['garra_g'] - 1), 1)
        if cfg['massa'] and tri:
            rec['massa']['delta_vs_Tritan_Hexa3D30_pct'] = round(100 * (cfg['massa']['garra_g'] / tri - 1), 1)
            rec['massa']['delta_vs_Tritan_Hexa3D30_g'] = round(cfg['massa']['garra_g'] - tri, 1)
        mt = jl(R / 'MONTAGEM' / f'montagem_{cfg["fe"]}.json')
        if mt:
            sig24 = mt['sigma_Z_24kg_MPa_(x PICO)']; sig12 = sig24 / 2
            rec['montagem'] = {k: mt[k] for k in ('rigidez_asa_montada_N_mm', 'sigma_Z_24kg_MPa_(x PICO)', 'peca_critica',
                                                  'kg_max_PA6-CF_Z48', 'FS_24kg_PA6-CF_Z48', 'FS_30kg_PA6-CF_Z48',
                                                  'kg_max_PAHT_CF15_Z18.2', 'FS_24kg_PAHT_CF15_Z18.2', 'FS_30kg_PAHT_CF15_Z18.2')}
            rec['montagem']['desl_24kg_mm'] = mt['casos']['ONE_24']['desl_max_mm']
            rec['fadiga_PAHT'] = hours(sig12, sig24, 18.2)
            rec['fadiga_PA6CF'] = hours(sig12, sig24, 48.0)
        if cfg.get('imp'):
            im = jl(R / 'IMPACTO' / f'impacto_{cfg["imp"]}.json')
            if im:
                rec['impacto_superior'] = {k: im[k] for k in ('f1_Hz_com_24kg', 'fator_dinamico_3D', 'sigma_Z_pico_MPa_(x PICO)',
                                                               'FI_giroide_pico', 'desl_pico_mm', 'FS_dinamico_PA6CF_Z48', 'FS_dinamico_PAHT_Z18.2')}
        if cfg.get('nota'):
            rec['nota'] = cfg['nota']
        out['variantes'][name] = rec
    (R / 'DECISAO_ESQUELETO.json').write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
    for k, v in out['variantes'].items():
        m = v.get('massa') or {}; mt = v.get('montagem') or {}
        print(f"{k[:46]:46s} garra {m.get('garra_g')} g (Tritan {m.get('delta_vs_Tritan_Hexa3D30_pct')}%) fil {m.get('filamento_g')} "
              f"| kgmax PA6 {mt.get('kg_max_PA6-CF_Z48')} PAHT {mt.get('kg_max_PAHT_CF15_Z18.2')} k {mt.get('rigidez_asa_montada_N_mm')}")


if __name__ == '__main__':
    main()
