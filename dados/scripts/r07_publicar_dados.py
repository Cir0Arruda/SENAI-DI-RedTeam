"""Copia os dados das simulações/fatiamentos R07 para a pasta `dados/` do site (repositório GitHub).

Só copia resultados já calculados. Remove caminhos locais da máquina (C:\\Users\\...) dos JSON.
Uso: python r07_publicar_dados.py <pasta do site>
"""
from __future__ import annotations
import json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / 'SENAI-DI-REDTEAM-APRESENTACAO'
OUT = SITE / 'dados'
R = ROOT / '06_Engenharia' / 'R07'
O = ROOT / '05_Orca'
LOCAL = re.compile(r'[A-Za-z]:[\\/]+Users[\\/]+[^"\\/]+[\\/]+(?:OneDrive[\\/]+)?[^"\\/]*Trabalho[\\/]+', re.I)


def clean_json(src: Path, dst: Path):
    txt = src.read_text(encoding='utf-8')
    txt = LOCAL.sub('', txt)
    json.loads(txt)  # garante que continua JSON válido
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(txt, encoding='utf-8')


def copy(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main():
    files = {
        'decisao/DECISAO_ESQUELETO.json': R / 'DECISAO_ESQUELETO.json',
        'decisao/dados_comparativos.csv': R / 'GALERIA' / 'dados_comparativos.csv',
        'montagem/montagem_resumo.json': R / 'MONTAGEM' / 'montagem_resumo.json',
        'orca/r07_fatiamento_base25.json': O / 'R07' / 'r07_fatiamento_base25.json',
        'orca/r07_fatiamento_base20.json': O / 'R07' / 'r07_fatiamento_base20.json',
        'orca/r07_comparativo_fatiamento.json': O / 'R07' / 'COMPARATIVO' / 'r07_comparativo_fatiamento.json',
        'orca/r06_fatiamento_resumo.json': O / 'R06' / 'r06_fatiamento_resumo.json',
        'orca/pads_tpu95a_fatiamento.json': O / 'Resultado_PAD_K1MAX' / 'dados_fatiamento.json',
        'fadiga/r07_vida.json': R / 'r07_vida.json',
        'materiais/materiais_R07.json': R / 'materiais_R07.json',
        'fusion/fusion_build_2corpos.json': R / 'fusion_build_2corpos.json',
    }
    for f in sorted((R / 'MONTAGEM').glob('montagem_*.json')):
        files[f'montagem/{f.name}'] = f
    for f in sorted((R / 'IMPACTO').glob('impacto_*.json')):
        files[f'impacto/{f.name}'] = f
    for f in sorted((R / 'FUSION').glob('*.json')) if (R / 'FUSION').exists() else []:
        files[f'fusion/{f.name}'] = f
    n = 0
    for rel, src in files.items():
        if not src.exists():
            print('ausente:', src.name); continue
        dst = OUT / rel
        (clean_json if src.suffix == '.json' else copy)(src, dst); n += 1
    rel_md = (R / 'RELATORIO_R07.md').read_text(encoding='utf-8')
    (OUT / 'RELATORIO_R07.md').write_text(LOCAL.sub('', rel_md), encoding='utf-8')
    for s in ['r07_comparativo.py', 'r07_uniforme_fe.py', 'r07_montagem.py', 'r07_impacto.py',
              'r07_decisao.py', 'r07_galeria.py', 'r07_publicar_dados.py']:
        if (ROOT / 'scripts' / s).exists():
            copy(ROOT / 'scripts' / s, OUT / 'scripts' / s); n += 1
    print(n + 1, 'arquivos em', OUT)


if __name__ == '__main__':
    main()
