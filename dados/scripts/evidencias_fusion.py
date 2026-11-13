"""Separa as imagens do Autodesk Fusion para a página de evidências (evidencias.html).

O que faz, sem criar nada novo:
1. Abre os 3 relatórios nativos exportados pelo Fusion (HTML com as imagens embutidas
   em base64) e salva cada figura de resultado com os MESMOS bytes do relatório.
   Se a figura já existe em assets/img/bancada (mesmo SHA-256), a página usa aquela.
   Figuras repetidas ou corrompidas no próprio relatório são registradas, não consertadas.
2. Copia as capturas de tela do Fusion (feitas pela API, Viewport.saveAsImageFile)
   da pasta de trabalho ../desempenho/01_Fusion, se ela existir.
3. Grava evidencias/fusion/manifesto.json com o SHA-256 de cada relatório e de cada imagem.

Cuidado: a cópia publicada dos relatórios difere da exportada só no nome do autor ("usuario").
Não passe filtro de texto por dentro do base64: em 11/2026 um filtro de privacidade trocou letras
dentro da figura "Fixo1" do F1 e a corrompeu (já restaurada a partir do arquivo original).

Uso:  python dados/scripts/evidencias_fusion.py            (extrai e grava o manifesto)
      python dados/scripts/evidencias_fusion.py --conferir (só confere contra o manifesto)
"""
import base64, hashlib, io, json, re, shutil, sys
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / 'evidencias' / 'fusion'
BANCADA = REPO / 'assets' / 'img' / 'bancada'
TRABALHO = REPO.parent / 'desempenho' / '01_Fusion'
BRUTOS = 'dados/brutos/fusion'

RELATORIOS = [
    ('F1', 'pa6cf', f'{BRUTOS}/preparacao_garra/SAMI_PA6CF_24kg_Relatorio_Fusion.html'),
    ('F2', 'tritan', f'{BRUTOS}/preparacao_garra/SAMI_TRITAN_24kg_Relatorio_Fusion.html'),
    ('F3', 'esfera', f'{BRUTOS}/Esfera_SUNLU_100N_Relatorio_Fusion.html'),
]
# posição da imagem no HTML exportado -> o que ela mostra (igual nos 3 relatórios)
FIGURAS = {
    8: ('modelo', 'Modelo analisado'),
    9: ('restricoes', 'Restrição: Fixo1'),
    10: ('cargas', 'Carga: Força1'),
    11: ('fator_seguranca', 'Fator de segurança (resultados guiados)'),
    12: ('fator_seguranca_resultados', 'Fator de segurança (resultados)'),
    13: ('von_mises', 'Tensão de von Mises'),
    14: ('principal_1', '1ª tensão principal'),
    15: ('principal_3', '3ª tensão principal'),
    16: ('deslocamento', 'Deslocamento total'),
}
CAPTURAS = [
    ('GARRA_R04_EXTERIOR_ORIGINAL_PREPARACAO.png', 'captura_garra_exterior_original.png'),
    ('GARRA_SUPERIOR_ZONAS_R04_EXTERIOR_INALTERADO.png', 'captura_superior_exterior_inalterado.png'),
    ('GARRA_INFERIOR_ESQ_ZONAS_R04_EXTERIOR_INALTERADO.png', 'captura_inferior_esq_exterior_inalterado.png'),
    ('GARRA_INFERIOR_DIR_ZONAS_R04_EXTERIOR_INALTERADO.png', 'captura_inferior_dir_exterior_inalterado.png'),
    ('PADs_R04_SEPARADOS.png', 'captura_pads_separados.png'),
]
IMG = re.compile(r'<img[^>]*src="data:image/(\w+);base64,([^"]+)"[^>]*>')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rel(p):
    return p.relative_to(REPO).as_posix()


def decodifica(s):
    s = re.sub(r'[^A-Za-z0-9+/=]', '', s).rstrip('=')
    return base64.b64decode(s + '=' * (-len(s) % 4))


def abre_ok(b):
    try:
        im = Image.open(io.BytesIO(b)); im.load()
        return im.size
    except Exception:
        return None


def extrai():
    OUT.mkdir(parents=True, exist_ok=True)
    na_bancada = {sha(p.read_bytes()): p for p in BANCADA.glob('*.png')}
    man = {'gerado_por': 'dados/scripts/evidencias_fusion.py', 'relatorios': [], 'capturas': []}
    for cod, tag, caminho in RELATORIOS:
        html = (REPO / caminho).read_bytes()
        texto = html.decode('utf-8', errors='replace')
        versao = re.search(r'Autodesk Fusion \(([\d.]+)\)', texto)
        r = {'ref': cod, 'relatorio': caminho, 'sha256': sha(html), 'bytes': len(html),
             'versao_fusion': versao.group(1) if versao else None, 'figuras': []}
        vistos = {}
        for i, m in enumerate(IMG.finditer(texto)):
            if i not in FIGURAS:
                continue
            nome, titulo = FIGURAS[i]
            b = decodifica(m.group(2)); h = sha(b)
            f = {'posicao_no_html': i, 'nome': nome, 'titulo': titulo, 'sha256': h, 'bytes': len(b)}
            tam = abre_ok(b)
            if tam is None:
                f['estado'] = 'corrompida no relatório exportado pelo Fusion (não abre em nenhum visualizador)'
            elif h in vistos:
                f['estado'] = f'repetida: o relatório traz aqui a mesma imagem de "{vistos[h]}"'
            else:
                vistos[h] = titulo
                f['tamanho_px'] = list(tam)
                if h in na_bancada:
                    f['arquivo'] = rel(na_bancada[h])
                else:
                    dst = OUT / f'{tag}_{nome}.png'
                    dst.write_bytes(b)
                    f['arquivo'] = rel(dst)
                f['estado'] = 'ok'
            r['figuras'].append(f)
        man['relatorios'].append(r)
    for origem, nome in CAPTURAS:
        src = TRABALHO / origem
        dst = OUT / nome
        if src.exists():
            b = src.read_bytes()
            if sha(b) in na_bancada:
                arq = na_bancada[sha(b)]
            else:
                shutil.copyfile(src, dst); arq = dst
        elif dst.exists():
            b = dst.read_bytes(); arq = dst
        else:
            print('FALTA', origem); continue
        man['capturas'].append({'origem': f'desempenho/01_Fusion/{origem}', 'arquivo': rel(arq),
                                'sha256': sha(b), 'tamanho_px': list(abre_ok(b)),
                                'como': 'Autodesk Fusion API: Viewport.saveAsImageFile(1600, 1100)'})
    (OUT / 'manifesto.json').write_text(json.dumps(man, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return man


def confere():
    man = json.loads((OUT / 'manifesto.json').read_text(encoding='utf-8'))
    erros = 0
    for r in man['relatorios']:
        html = (REPO / r['relatorio']).read_bytes()
        if sha(html) != r['sha256']:
            print('ERRO relatorio mudou:', r['relatorio']); erros += 1
        texto = html.decode('utf-8', errors='replace')
        imgs = {i: decodifica(m.group(2)) for i, m in enumerate(IMG.finditer(texto))}
        for f in r['figuras']:
            b = imgs.get(f['posicao_no_html'])
            if b is None or sha(b) != f['sha256']:
                print('ERRO figura nao bate com o relatorio:', r['ref'], f['nome']); erros += 1
            if 'arquivo' in f and sha((REPO / f['arquivo']).read_bytes()) != f['sha256']:
                print('ERRO arquivo diferente da figura do relatorio:', f['arquivo']); erros += 1
    for c in man['capturas']:
        if sha((REPO / c['arquivo']).read_bytes()) != c['sha256']:
            print('ERRO captura:', c['arquivo']); erros += 1
    n = sum(len(r['figuras']) for r in man['relatorios'])
    print(f'{n} figuras de {len(man["relatorios"])} relatorios e {len(man["capturas"])} capturas conferidas, {erros} erros')
    return erros


if __name__ == '__main__':
    if '--conferir' not in sys.argv:
        m = extrai()
        for r in m['relatorios']:
            for f in r['figuras']:
                print(r['ref'], f['nome'], f.get('arquivo', '-'), f['estado'][:40].encode('ascii', 'replace').decode())
    sys.exit(1 if confere() else 0)
