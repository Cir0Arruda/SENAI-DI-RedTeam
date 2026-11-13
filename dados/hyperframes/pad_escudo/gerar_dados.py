"""Gera assets/serie.js a partir da resposta no tempo do modelo de impacto (R03).

Fonte: dados/brutos/impacto_pad_hexa15/02_Dados/resposta_temporal_R03.csv e parametros_resultados_R03.json.
Teste: esfera de aço de 263 g a 1 m/s (0,13 J). É um valor de teste para comparar com e sem PAD, não uma batida medida na linha.
Uso: python gerar_dados.py   (nesta pasta)
"""
import csv, json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SRC = AQUI.parents[1] / 'brutos' / 'impacto_pad_hexa15' / '02_Dados'
P = json.loads((SRC / 'parametros_resultados_R03.json').read_text(encoding='utf-8'))
res, imp = P['results_reduced_model'], P['impact']

linhas = list(csv.DictReader(open(SRC / 'resposta_temporal_R03.csv', encoding='utf-8')))
passo = 5                                   # 0,005 ms × 5 = 0,025 ms
cols = {'t': 'tempo_ms', 'fc': 'forca_com_PAD_N', 'fs': 'forca_sem_PAD_N', 'cp': 'compressao_PAD_mm',
        'dc': 'deflexao_viga_com_PAD_mm', 'ds': 'deflexao_viga_sem_PAD_mm',
        'ep': 'energia_elastica_PAD_J', 'eg': 'energia_elastica_garra_J'}
serie = {k: [round(float(r[c]), 5) for r in linhas[::passo]] for k, c in cols.items()}

out = {
    'fonte': 'resposta_temporal_R03.csv e parametros_resultados_R03.json (modelo de molas 1D; não é ensaio)',
    'massa_g': round(imp['mass_kg'] * 1000), 'vel_m_s': imp['velocity_m_s'], 'energia_J': round(imp['energy_J'], 3),
    'pico_sem_N': round(res['peak_force_without_PAD_N'], 1), 'pico_com_N': round(res['peak_force_with_PAD_N'], 1),
    'reducao_pct': round(res['peak_force_reduction_percent'], 1),
    'duracao_sem_ms': round(res['contact_duration_without_PAD_ms'], 2), 'duracao_com_ms': round(res['contact_duration_with_PAD_ms'], 2),
    'energia_pad_pct': round(res['peak_PAD_elastic_energy_J'] / imp['energy_J'] * 100),
    'compressao_max_mm': round(res['pad_compression_mm'], 2),
    'serie': serie,
}
(AQUI / 'assets').mkdir(exist_ok=True)
(AQUI / 'assets' / 'serie.js').write_text('window.IMPACTO = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
print({k: v for k, v in out.items() if k != 'serie'}, len(serie['t']), 'pontos')
