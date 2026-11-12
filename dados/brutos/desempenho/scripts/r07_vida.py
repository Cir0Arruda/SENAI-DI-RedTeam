"""R07 - Carga máxima, impacto, fadiga (milhares de horas), fluência e desgaste: R06 x R07 com/sem esqueleto.

Entradas: resultados FE por voxels (06_Engenharia/R07/*.json) + fator de pico calibrado no Fusion (PICO).
Tudo linear-elástico + modelos de engenharia (rotulados como ESTIMATIVA). Ver HIPOTESES no JSON de saída.
Uso: python r07_vida.py [--pico 2.2]
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1] / '06_Engenharia' / 'R07'
G, A_EXTRA = 9.80665, 5.0
F24 = 24 * (G + A_EXTRA)            # 355.36 N: caso de projeto do FE (24 kg numa asa, g+5)
S_Z_FE = 48.0                       # resistência Z usada no FE por voxels (FI_z = sig/48)

# Materiais (Z = entre camadas, governa). Fonte PAHT CF15: TDS BASF/Forward AM v3.5 (ZX 18,2 MPa seco; XY 103,2)
MATS = {'PAHT CF15 (TDS, Z=18,2 MPa)': 18.2,
        'PA6-CF valor usado no FE (Z=48 MPa)': 48.0}

PICO = 2.2   # pico Fusion / pico voxel (default; substituído pela calibração do Fusion via --pico)
if '--pico' in sys.argv:
    PICO = float(sys.argv[sys.argv.index('--pico') + 1])


def load(name):
    return json.loads((R / f'{name}.json').read_text(encoding='utf-8'))


def sup(name):
    c = load(name)['cases']['ONE_24']
    return {'k': F24 / c['disp_max_mm'], 'fi_z': c['solid_FI_z_max'], 'mass': load(name)['mass_model_g']}


def inf(name):
    c = load(name)
    return {'k': F24 / c['disp_max_mm'], 'fi_z': c['FI_z'], 'mass': c['mass_model_g']}


VARS = {'R06 (atual)': (sup('R06'), inf('INF_R06')),
        'R07 COM esqueleto': (sup('F25_COM'), inf('INF_F20_COM')),
        'R07 SEM esqueleto (mesmos %)': (sup('F25_SEM'), inf('INF_F20_SEM')),
        'R07 SEM esqueleto, giroide mais denso (mesma massa)': (sup('F25_SEM_ISO'), inf('INF_F20_SEM_ISO'))}


def coef(s, i):
    """MPa por N de carga na asa no ponto crítico (Z) de cada peça, com fator de pico."""
    return {'sup': s['fi_z'] * S_Z_FE * PICO / F24, 'inf': i['fi_z'] * S_Z_FE * PICO / F24}


def k_chain(s, i):  # rigidez da asa (superior e inferior em série), N/mm
    return 1 / (1 / s['k'] + 1 / i['k'])


def kg_from_N(F, acc=G + A_EXTRA):
    return F / acc


# ---------- Fadiga: curva S-N normalizada conservadora p/ PA reforçado com fibra curta (FFF)
# smax/S = 1 - B*log10(N), B=0,10 -> 0,30*S em 1e7 ciclos. Literatura de PA-CF FFF reporta limites de fadiga
# maiores (PA12-CF ~48-54 MPa; SCF-PA otimizado ~69-70 MPa), então B=0,10 é conservador. ESTIMATIVA.
B_SN = 0.10


def cycles_to_fail(smax, S):
    r = smax / S
    if r >= 1:
        return 1.0
    return 10 ** ((1 - r) / B_SN)


def dynamic_factor(tr_over_T):
    """Fator de amplificação dinâmica de 1 GL para carga em rampa com tempo de subida tr (T = período natural)."""
    x = math.pi * tr_over_T          # envoltória conservadora de 1 + |sen x|/x
    return min(2.0, 1 + 1 / x) if x > 0 else 2.0


def main():
    out = {'PICO_fator_Fusion_voxel': PICO, 'variantes': {}}
    ciclos_h = 480                         # HIPÓTESE: 8 ciclos/min (pegar-depositar), ajustável
    frac_erro = 0.01                       # HIPÓTESE: 1% dos ciclos com erro da seladora (24 kg numa asa)
    for vn, (s, i) in VARS.items():
        c = coef(s, i); K = k_chain(s, i)
        gov = max(c['sup'], c['inf']); peca = 'superior' if c['sup'] >= c['inf'] else 'inferior'
        v = {'massa_FE_g': {'sup': s['mass'], 'inf': i['mass']}, 'rigidez_asa_N_mm': round(K, 1),
             'peca_critica': peca, 'MPa_por_N': round(gov, 5),
             'tensao_Z_MPa': {kg: round(gov * kg * (G + A_EXTRA), 2) for kg in (12, 24, 30)}, 'materiais': {}}
        fn = (2 * math.pi) ** -1 * math.sqrt(K * 1000 / 24)   # Hz com 24 kg pendurados
        v['freq_natural_24kg_Hz'] = round(fn, 1)
        for mn, S in MATS.items():
            Fmax = S / gov
            m = {'F_ruptura_N': round(Fmax),
                 'kg_max_estatico_g': round(kg_from_N(Fmax, G), 1),
                 'kg_max_com_g+5': round(kg_from_N(Fmax), 1),
                 'FS_24kg_g+5': round(Fmax / F24, 2), 'FS_30kg_g+5': round(Fmax / (30 * (G + A_EXTRA)), 2),
                 'energia_ate_ruptura_J': round(Fmax ** 2 / (2 * K) / 1000, 3)}
            # Fadiga + Miner: normal 12 kg/asa (g+5), erro 24 kg numa asa
            n12 = cycles_to_fail(gov * 12 * (G + A_EXTRA), S); n24 = cycles_to_fail(gov * F24, S)
            n30 = cycles_to_fail(gov * 30 * (G + A_EXTRA), S)
            dano_h = ciclos_h * ((1 - frac_erro) / n12 + frac_erro / n24)
            m['fadiga'] = {'ciclos_12kg': f'{n12:.3g}', 'ciclos_24kg': f'{n24:.3g}', 'ciclos_30kg': f'{n30:.3g}',
                           'horas_so_12kg': round(n12 / ciclos_h), 'horas_so_24kg': round(n24 / ciclos_h),
                           'horas_so_30kg': round(n30 / ciclos_h),
                           'horas_mix_1pct_erro': round(1 / dano_h) if dano_h > 0 else None}
            v['materiais'][mn] = m
        out['variantes'][vn] = v
    # ---------- Impacto / tranco (E-stop, arrancada com caixa presa): DAF de 1 GL
    rec = out['variantes']['R07 COM esqueleto']
    fn = rec['freq_natural_24kg_Hz']; T = 1 / fn
    out['tranco_estop'] = []
    for tr_ms in (10, 25, 50, 100, 200):
        daf = dynamic_factor(tr_ms / 1000 / T)
        out['tranco_estop'].append({'tempo_subida_ms': tr_ms, 'DAF': round(daf, 2)})
    # ---------- Fluência (ESTIMATIVA): módulo de fluência de PA6-CF ~0,70 E (1000 h) / ~0,55 E (10 000 h, condicionado)
    out['fluencia'] = {}
    for vn, v in out['variantes'].items():
        d0 = 12 * (G + A_EXTRA) / v['rigidez_asa_N_mm']
        out['fluencia'][vn] = {'flecha_inicial_12kg_mm': round(d0, 3), 'flecha_1000h_mm': round(d0 / 0.70, 3),
                               'flecha_10000h_mm': round(d0 / 0.55, 3)}
    # ---------- Desgaste (Archard) nos furos M6 e esmagamento
    F_bolt = F24 / 6
    k_w = 1e-5            # mm3/(N.m), ordem de grandeza p/ PA-CF contra aço (ESTIMATIVA)
    slip_mm = 0.01        # micro-deslizamento por ciclo (ESTIMATIVA)
    for horas in (1000, 10000):
        n = horas * ciclos_h
        out.setdefault('desgaste', {})[f'{horas}h'] = {'volume_mm3_por_furo': round(k_w * F_bolt * slip_mm * n / 1000, 4)}
    out['desgaste']['esmagamento_M6_MPa_24kg'] = round(F_bolt / (6 * 10), 2)
    # ---------- Justificativa do material: mesma geometria R07 COM, troca só a resistência Z (TDS dos fabricantes)
    mo = json.loads((R.parent / 'R06' / 'otimizacao_multiobjetivo.json').read_text(encoding='utf-8'))
    gov = max(coef(*VARS['R07 COM esqueleto']).values())
    lst = []
    for mm in mo['level1_materials']['materials']:
        vv = mm['values']; rho = 1 / vv['1/rho']; sz = vv['UTS_Z/rho'] * rho
        lst.append({'material': mm['name'], 'UTS_Z_MPa': round(sz, 1), 'E_Z_MPa': round(vv['E_Z/rho'] * rho),
                    'HDT_C': vv['HDT_1.8MPa'], 'kg_max_g+5': round(sz / gov / (G + A_EXTRA), 1),
                    'FS_24kg': round(sz / gov / F24, 2), 'TOPSIS_24_7': mm['topsis']['estrutural_24_7'], 'fonte': mm['source']})
    lst.append({'material': 'PAHT CF15 (BASF)', 'UTS_Z_MPa': 18.2, 'E_Z_MPa': None, 'HDT_C': None,
                'kg_max_g+5': round(18.2 / gov / (G + A_EXTRA), 1), 'FS_24kg': round(18.2 / gov / F24, 2),
                'TOPSIS_24_7': None, 'fonte': 'https://forward-am.com/material-portfolio/ultrafuse-filaments-for-fused-filaments-fabrication-fff/reinforced-filaments/ultrafuse-paht-cf15/'})
    out['justificativa_material_R07'] = sorted(lst, key=lambda r: -r['kg_max_g+5'])
    out['HIPOTESES'] = [f'{ciclos_h} ciclos/h (8/min); 1% dos ciclos com erro de 24 kg numa asa',
                        'carga de projeto = massa x (g + 5 m/s2) (aceleração do robô)',
                        f'pico real = pico voxel x {PICO} (calibrado contra Fusion)',
                        'S-N normalizada smax/S = 1 - 0,10 log10 N (conservadora para PA-CF curto, FFF)',
                        'falha governada por tração/cisalhamento entre camadas (Z)',
                        'fluência e desgaste: ordens de grandeza de literatura, não ensaiados']
    (R / 'r07_vida.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
