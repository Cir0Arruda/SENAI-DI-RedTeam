"""R06 - Otimização multiobjetivo de material e preenchimento da garra SAMI (dados atuais).

Nível 1 (material): 8 graus do banco FUSION/ensaios_multimateriais/materiais.json + Fiberon PA12-CF10.
  Objetivos (todos de fonte do fabricante; Z = direção de camada, a mais fraca em FFF):
    max E_Z/rho (rigidez específica), max UTS_Z/rho (resistência específica),
    max HDT a 1,8 MPa (operação térmica 24/7), max impacto (Charpy/Izod não-entalhado ou relatado - métodos
    diferentes, usado só como critério ordinal), min densidade (massa).
  Métodos: fronteira de Pareto (não-dominância) + TOPSIS com 3 conjuntos de pesos (cenários).
  Dados ausentes são ausentes (não zero): material sem o dado fica fora do critério e é marcado.

Nível 2 (preenchimento, PA6-CF): massa e tempo REAIS do Orca (K1 Max) para uniforme 20/30/50/70% e zonal R06;
  rigidez/tensão vêm do FEA do Fusion quando disponível (06_Engenharia/R06/fea_resultados.json).

Saída: 06_Engenharia/R06/otimizacao_multiobjetivo.json + figuras PNG.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DESK = Path(__file__).resolve().parents[2]
O = DESK / 'desempenho'
DEST = O / '06_Engenharia' / 'R06'
DEST.mkdir(parents=True, exist_ok=True)
DB = DESK / 'FUSION' / 'ensaios_multimateriais' / 'materiais.json'
PA12CF = DESK / 'FUSION' / 'preparacao_garra' / 'pa12cf10_candidato.json'
ORCA = O / '05_Orca' / 'R06'
FEA = DEST / 'fea_resultados.json'

SHORT = {'petg_polymaker_v2': 'PETG', 'pctg_3dfuel_pro': 'PCTG', 'tritan_tx1001_eastman': 'Tritan*',
         'tpu95ahf_bambu_v3': 'TPU95A', 'pa6_lehvoss9936': 'PA6 (LEHVOSS)', 'pa12_fiberlogy': 'PA12',
         'pc_polymax_v54': 'PC', 'pa6cf_bambu_v3': 'PA6-CF', 'pa12cf10_fiberon': 'PA12-CF10'}


def num(v, key='Z'):
    """Valor escalar: dict XY/Z -> pega Z (camada) se existir, senão XY; números passam direto."""
    if v is None:
        return None
    if isinstance(v, dict):
        for k in (key, 'XY', '1.8_MPa', '1.82_MPa', '23_degC', 'XY_ambient'):
            if k in v and isinstance(v[k], (int, float)):
                return float(v[k])
        vals = [x for x in v.values() if isinstance(x, (int, float))]
        return float(vals[0]) if vals else None
    return float(v) if isinstance(v, (int, float)) else None


def load_materials():
    d = json.loads(DB.read_text(encoding='utf-8'))
    recs = next(v for v in d.values() if isinstance(v, list) and v and isinstance(v[0], dict))
    rows = []
    for m in recs:
        p = {k: x.get('value') for k, x in m['properties'].items()}
        imp = None; imp_src = None
        for k in ('impact_iso179', 'impact_charpy_unnotched', 'impact_reported', 'impact_izod_notched', 'impact_charpy_notched', 'impact_iso179_notched'):
            if k in p:
                imp = num(p[k], 'XY'); imp_src = k; break
        hdt = p.get('HDT')
        hdt18 = None
        if isinstance(hdt, dict):
            hdt18 = next((float(v) for k, v in hdt.items() if k.startswith('1.8')), None)
        rows.append({'id': m['id'], 'name': SHORT.get(m['id'], m['id']), 'rho': num(p.get('density')),
                     'E_Z': num(p.get('young_modulus')), 'E_XY': num(p.get('young_modulus'), 'XY'),
                     'UTS_Z': num(p.get('ultimate_tensile_strength')) or num(p.get('yield_stress')),
                     'UTS_XY': num(p.get('ultimate_tensile_strength'), 'XY') or num(p.get('yield_stress')),
                     'HDT18': hdt18, 'impact': imp, 'impact_method': imp_src, 'Tg': num(p.get('Tg')),
                     'source': m.get('source_url'), 'origin': m.get('data_origin')})
    c = json.loads(PA12CF.read_text(encoding='utf-8'))
    rows.append({'id': 'pa12cf10_fiberon', 'name': 'PA12-CF10', 'rho': c['density_g_cm3'],
                 'E_Z': c['dry']['E_MPa']['Z'], 'E_XY': c['dry']['E_MPa']['XY'],
                 'UTS_Z': c['dry']['tensile_strength_MPa']['Z'], 'UTS_XY': c['dry']['tensile_strength_MPa']['XY'],
                 'HDT18': c['HDT_C']['1.8_MPa'], 'impact': c['dry']['charpy_unnotched_kJ_m2']['XY'],
                 'impact_method': 'charpy_unnotched', 'Tg': c['Tg_C'], 'source': c['source_url'], 'origin': 'FFF XY/Z, seco'})
    return rows


def pareto(F):
    """F: n x k, todos a MAXIMIZAR. Retorna máscara não-dominada."""
    n = len(F); nd = np.ones(n, bool)
    for i in range(n):
        for j in range(n):
            if i != j and np.all(F[j] >= F[i]) and np.any(F[j] > F[i]):
                nd[i] = False; break
    return nd


def topsis(F, w):
    R = F / np.linalg.norm(F, axis=0)
    V = R * w
    best, worst = V.max(0), V.min(0)
    dp = np.linalg.norm(V - best, axis=1); dm = np.linalg.norm(V - worst, axis=1)
    return dm / (dp + dm)


def level1():
    rows = load_materials()
    crit = [('E_Z/rho', lambda r: r['E_Z'] / r['rho']), ('UTS_Z/rho', lambda r: r['UTS_Z'] / r['rho']),
            ('HDT_1.8MPa', lambda r: r['HDT18']), ('1/rho', lambda r: 1 / r['rho'])]
    # Impacto FORA do composto: unidades/métodos incompatíveis (Izod J/m x Charpy kJ/m² x 'relatado').
    ok = [r for r in rows if all(r.get(k) is not None for k in ('E_Z', 'UTS_Z', 'HDT18', 'rho'))]
    out_rows = [r for r in rows if r not in ok]
    F = np.array([[f(r) for _, f in crit] for r in ok])
    nd = pareto(F)
    scen = {'estrutural_24_7': [0.35, 0.35, 0.25, 0.05],
            'equilibrado': [0.25, 0.25, 0.25, 0.25],
            'leveza': [0.25, 0.20, 0.10, 0.45]}
    res = {'criteria': [c for c, _ in crit], 'scenarios_weights': scen, 'materials': [], 'excluded_missing_data': [
        {'name': r['name'], 'missing': [k for k in ('E_Z', 'UTS_Z', 'HDT18') if r.get(k) is None]} for r in out_rows],
        'impact_same_method_kJ_m2_unnotched_XY': {r['name']: r['impact'] for r in rows
            if r['impact_method'] in ('impact_iso179', 'impact_charpy_unnotched', 'charpy_unnotched')}}
    scores = {s: topsis(F, np.array(w)) for s, w in scen.items()}
    for i, r in enumerate(ok):
        res['materials'].append({'name': r['name'], 'id': r['id'], 'values': dict(zip(res['criteria'], F[i].round(3).tolist())),
                                 'pareto': bool(nd[i]), 'topsis': {s: round(float(v[i]), 3) for s, v in scores.items()},
                                 'impact_method': r['impact_method'], 'source': r['source']})
    for s in scen:
        res[f'ranking_{s}'] = [m['name'] for m in sorted(res['materials'], key=lambda m: -m['topsis'][s])]
    # Figura: rigidez específica Z x HDT, tamanho = resistência específica
    fig, ax = plt.subplots(figsize=(8.5, 5.6), layout='constrained')
    for i, r in enumerate(ok):
        x, y, s = F[i, 0], F[i, 2], F[i, 1]
        ax.scatter(x, y, s=30 + 9 * s, color='#d63b3b' if nd[i] else '#8a96a3', alpha=.85,
                   edgecolor='white', linewidth=1.5, zorder=3)
        ax.annotate(r['name'], (x, y), textcoords='offset points', xytext=(8, 6), fontsize=9)
    ax.set_xlabel('Rigidez específica na direção Z  E_Z/ρ  [MPa·cm³/g]')
    ax.set_ylabel('HDT a 1,8 MPa [°C]')
    ax.set_title('Materiais: fronteira de Pareto (vermelho) | tamanho = resistência específica Z\n'
                 'dados de fabricante; *Tritan = resina moldada (sem Z impresso)', fontsize=10)
    ax.grid(alpha=.2)
    fig.savefig(DEST / 'OTIM_materiais_pareto.png', dpi=160); plt.close(fig)
    return res


def level2():
    """Preenchimento (PA6-CF): massa/tempo do Orca; rigidez do FEA quando existir."""
    cases = {}
    for f, key in [(ORCA / 'r06_variantes_resumo.json', None), (ORCA / 'r06_fatiamento_resumo.json', 'SUPERIOR')]:
        if not f.exists():
            continue
        d = json.loads(f.read_text(encoding='utf-8'))
        for k, v in d.items():
            if key and k != key:
                continue
            if v.get('ok'):
                name = 'ZONAL_R06' if k == 'SUPERIOR' else k.replace('SUPERIOR_', '')
                cases[name] = {'mass_part_g': round(v['mass_g']['peca'], 1), 'total_g': v['orca_total_g'],
                               'time_h': round(v['time_s'] / 3600, 2)}
    fea = json.loads(FEA.read_text(encoding='utf-8')) if FEA.exists() else {}
    for k, v in cases.items():
        if k in fea:
            v.update(fea[k])
    return {'cases': cases, 'fea_source': str(FEA) if fea else 'FEA pendente'}


if __name__ == '__main__':
    r = {'level1_materials': level1(), 'level2_infill_PA6CF': level2(),
         'honesty': 'Rankings dependem dos pesos (cenários explícitos). Propriedades de fabricante, não ensaio próprio. '
                    'Impacto com métodos distintos é só ordinal. Nada aqui é vida em fadiga.'}
    (DEST / 'otimizacao_multiobjetivo.json').write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding='utf-8')
    L1 = r['level1_materials']
    for s in L1['scenarios_weights']:
        print(s, L1[f'ranking_{s}'])
    print('pareto', [m['name'] for m in L1['materials'] if m['pareto']])
    print('excluidos', L1['excluded_missing_data'])
    print('nivel2', json.dumps(r['level2_infill_PA6CF'], ensure_ascii=False))
