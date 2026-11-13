"""Gera assets/js/referencias-dados.js a partir de dados/REFERENCIAS.md.

O visualizador de referências do slide final (assets/js/referencias.js) lê esse arquivo. Assim o site e o
REFERENCIAS.md mostram sempre o mesmo texto: quem edita uma referência edita só o .md e roda este script.

Uso: python dados/scripts/referencias_site.py
"""
from __future__ import annotations
import html, json, re, unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / 'dados' / 'REFERENCIAS.md'
OUT = REPO / 'assets' / 'js' / 'referencias-dados.js'
COD = r'[A-Z]\d*(?:[–-][A-Z]?\d+)?'
INICIO = re.compile(r'^(- )?\*\*\[(' + COD + r')\]\s*(.*?)\*\*\s*(.*)$')


def inline(t: str) -> str:
    keep = []

    def tok(s):
        keep.append(s); return f'\x00{len(keep) - 1}\x00'

    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', lambda m: tok(f'<code>{m.group(1)}</code>'), t)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', lambda m: tok(
        f'<a href="{m.group(2)}" target="_blank" rel="noopener">{m.group(1)}</a>'), t)
    t = re.sub(r'&lt;(https?://[^&\s]+)&gt;', lambda m: tok(
        f'<a href="{m.group(1)}" target="_blank" rel="noopener">{re.sub(r"^https?://(www\.)?", "", m.group(1)).rstrip("/")}</a>'), t)
    t = re.sub(r'\[(' + COD + r')\]', lambda m: tok(f'<a class="rv-x" href="#ref-{m.group(1)}" data-ref="{m.group(1)}">[{m.group(1)}]</a>'), t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<i>\1</i>', t)
    while '\x00' in t:
        t = re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], t)
    return t


def blocos(linhas: list[str]) -> str:
    out, i = [], 0
    while i < len(linhas):
        l = linhas[i]
        if not l.strip():
            i += 1; continue
        if l.lstrip().startswith('|'):
            rows = []
            while i < len(linhas) and linhas[i].lstrip().startswith('|'):
                rows.append([c.strip() for c in linhas[i].strip().strip('|').split('|')]); i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(re.fullmatch(r':?-+:?', c) for c in r)]
            out.append('<div class="rv-tab"><table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) +
                       '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
                                                        for r in body) + '</tbody></table></div>')
            continue
        m = re.match(r'^(\s*)(- |\d+\. )', l)
        if m:
            tag = 'ol' if m.group(2)[0].isdigit() else 'ul'
            base = len(m.group(1)); itens = []
            while i < len(linhas):
                mm = re.match(r'^(\s*)(- |\d+\. )(.*)$', linhas[i])
                if mm and len(mm.group(1)) == base:
                    itens.append([mm.group(3)]); i += 1
                elif linhas[i].strip() and (len(linhas[i]) - len(linhas[i].lstrip())) > base and itens:
                    itens[-1].append(linhas[i][base + 2:] if linhas[i].startswith(' ' * (base + 2)) else linhas[i].strip()); i += 1
                else:
                    break
            out.append(f'<{tag}>' + ''.join('<li>' + inline(it[0]) + (blocos(it[1:]) if len(it) > 1 else '') + '</li>'
                                            for it in itens) + f'</{tag}>')
            continue
        par = []
        while i < len(linhas) and linhas[i].strip() and not re.match(r'^\s*(- |\d+\. |\|)', linhas[i]):
            par.append(linhas[i].strip()); i += 1
        out.append(f'<p>{inline(" ".join(par))}</p>')
    return ''.join(out)


def texto(h: str) -> str:
    t = re.sub(r'<[^>]+>', ' ', h)
    t = unicodedata.normalize('NFKD', html.unescape(t)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'\s+', ' ', t).strip()


def main():
    md = SRC.read_text(encoding='utf-8').splitlines()
    corpo = md[1:]
    cab, secoes, atual = [], [], None
    for l in corpo:
        if l.startswith('## '):
            atual = {'titulo': re.sub(r'^\d+[A-Z]?\.\s*', '', l[3:]).strip(), 'linhas': []}; secoes.append(atual)
        elif atual is None:
            cab.append(l)
        elif l.strip() != '---':
            atual['linhas'].append(l)
    res = []
    for s in secoes:
        itens, nota_ini, cur = [], [], None
        for l in s['linhas']:
            m = INICIO.match(l)
            if m:
                cur = {'cod': m.group(2), 'titulo': m.group(3).strip().rstrip('.'), 'lista': bool(m.group(1)),
                       'linhas': [m.group(4)] if m.group(4).strip() else []}
                itens.append(cur); continue
            if cur and cur['lista'] and l.strip() and not l.startswith('  '):
                cur = {'cod': '', 'titulo': '', 'lista': False, 'linhas': []}; itens.append(cur)
            if cur and not cur['lista'] and cur['cod'] and re.match(r'^\*\*[^\[]', l):
                cur = {'cod': '', 'titulo': '', 'lista': False, 'linhas': []}; itens.append(cur)
            if cur is None:
                nota_ini.append(l)
            else:
                cur['linhas'].append(l[2:] if cur['lista'] and l.startswith('  ') else l)
        sec = {'titulo': s['titulo'], 'intro': blocos(nota_ini), 'itens': []}
        if not itens:   # seção sem códigos (dados da equipe): vira um item só
            sec['itens'].append({'cod': 'Equipe', 'titulo': s['titulo'], 'html': sec['intro']}); sec['intro'] = ''
        for it in itens:
            if not it['cod'] and not ''.join(it['linhas']).strip():
                continue
            sec['itens'].append({'cod': it['cod'], 'titulo': inline(it['titulo']), 'html': blocos(it['linhas'])})
        for it in sec['itens']:
            it['busca'] = texto(f"{it['cod']} {it['titulo']} {it['html']} {sec['titulo']}")
        res.append(sec)
    dados = {'fonte': 'dados/REFERENCIAS.md', 'intro': blocos(cab), 'secoes': res}
    n = sum(1 for s in res for it in s['itens'] if it['cod'])
    OUT.write_text('// Gerado por dados/scripts/referencias_site.py a partir de dados/REFERENCIAS.md. Não editar à mão.\n'
                   'window.REFS = ' + json.dumps(dados, ensure_ascii=False, indent=0) + ';\n', encoding='utf-8', newline='\n')
    print(f'{len(res)} seções, {n} referências com código -> {OUT.relative_to(REPO)}')
    for s in res:
        print(' ', s['titulo'], [it['cod'] or '(nota)' for it in s['itens']])


if __name__ == '__main__':
    main()
