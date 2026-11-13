"""Gera a apresentação inteira num único arquivo HTML, para abrir num computador sem internet.

Uso:   python dados/scripts/apresentacao_offline.py   (na raiz do site, com internet só na primeira vez)
Saída: offline/Projeto_SAI_apresentacao.html  (abre com dois cliques no Chrome ou no Edge)

O que vai dentro do arquivo:
  - os slides visíveis (o arquivo de slides escondidos, <template id="arquivo">, fica de fora), o CSS e o JS;
  - as fontes (Inter Tight, Instrument Serif, JetBrains Mono) e o three.js dos visualizadores 3D;
  - imagens, vídeos e as peças STL usadas nos slides;
  - a página de evidências e os 3 relatórios nativos do Fusion, que abrem por cima da apresentação.
Os links para o GitHub e para as fichas técnicas continuam online: sem internet eles não abrem.

Na primeira vez o script baixa o three.js (jsDelivr) e as fontes (Google Fonts) para offline/.cache.
Depois disso roda sem internet.
"""
import base64, gzip, json, re, sys, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
R = Path(__file__).resolve().parents[2]
OUT = R / 'offline'
CACHE = OUT / '.cache'
GH = 'https://github.com/Cir0Arruda/SENAI-DI-RedTeam/blob/main/'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
FONTES = ('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700'
          '&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap')
THREE = 'https://cdn.jsdelivr.net/npm/three@0.160.0/'
MIME = {'.webp': 'image/webp', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.gif': 'image/gif',
        '.svg': 'image/svg+xml', '.mp4': 'video/mp4', '.webm': 'video/webm', '.stl': 'model/stl', '.html': 'text/html'}
IMG = {'.webp', '.jpg', '.jpeg', '.png', '.gif', '.svg'}
VID = {'.mp4', '.webm'}


def baixa(url, nome):
    """Baixa uma vez para o cache e devolve os bytes."""
    f = CACHE / nome
    if not f.is_file():
        f.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
            f.write_bytes(r.read())
        print('baixado', nome)
    return f.read_bytes()


def b64(b):
    return base64.b64encode(b).decode('ascii')


def limpa(p):
    return p.split('?')[0].split('#')[0].lstrip('./')


def local(v):
    return not re.match(r'^(https?:|mailto:|data:|javascript:|blob:|#)', v) and v.strip() != ''


def data_uri(p):
    return f'data:{MIME[Path(p).suffix.lower()]};base64,' + b64((R / p).read_bytes())


def js_seguro(s):
    return s.replace('</script', '<\\/script')


# ---------- fontes: só os blocos latin e latin-ext, com o woff2 dentro ----------
css_f = baixa(FONTES, 'fontes.css').decode('utf-8')
blocos = re.findall(r'/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})', css_f, flags=re.S)
fontes = []
for sub, bloco in blocos:
    if sub not in ('latin', 'latin-ext'):
        continue
    url = re.search(r'url\((https://[^)]+\.woff2)\)', bloco).group(1)
    nome = 'fontes/' + re.sub(r'[^a-zA-Z0-9._-]', '_', url.split('/s/')[-1])
    fontes.append(bloco.replace(url, 'data:font/woff2;base64,' + b64(baixa(url, nome))))
FONT_CSS = '\n'.join(fontes)
assert FONT_CSS, 'fontes não encontradas'

# ---------- three.js como módulos data: no importmap ----------
mods = {
    'three': baixa(THREE + 'build/three.module.js', 'three/three.module.js'),
    'three/addons/loaders/STLLoader.js': baixa(THREE + 'examples/jsm/loaders/STLLoader.js', 'three/STLLoader.js'),
    'three/addons/controls/OrbitControls.js': baixa(THREE + 'examples/jsm/controls/OrbitControls.js', 'three/OrbitControls.js'),
}
IMPORTMAP = json.dumps({'imports': {k: 'data:text/javascript;base64,' + b64(v) for k, v in mods.items()}})

# ---------- depósito: arquivos grandes em blocos base64, decodificados só quando usados ----------
deposito = {}


def guarda(p, gz=False):
    p = limpa(p)
    if p not in deposito:
        b = (R / p).read_bytes()
        if p.endswith('.html'):
            b = b.decode('utf-8-sig').encode('utf-8')
        deposito[p] = (MIME[Path(p).suffix.lower()], 'gz' if gz else 'b64', b64(gzip.compress(b, 9) if gz else b))
    return p


# ---------- apresentação ----------
html = (R / 'index.html').read_text(encoding='utf-8')
assert html.count('<template') == 1
i = html.index('<template id="arquivo">')
j = html.index('</template>', i) + len('</template>')
html = html[:i] + '<!-- arquivo de slides escondidos: fora da versão offline -->' + html[j:]

# fontes do Google -> @font-face embutido
html = re.sub(r'\s*<link rel="preconnect"[^>]*>', '', html)
html = re.sub(r'<link href="https://fonts\.googleapis\.com[^>]*>', '<style id="off-fonts">' + FONT_CSS + '</style>', html)
# CSS
html = re.sub(r'<link rel="stylesheet" href="([^"]+)">',
              lambda m: '<style>' + (R / limpa(m.group(1))).read_text(encoding='utf-8') + '</style>', html)
# importmap
html = re.sub(r'<script type="importmap">.*?</script>', lambda m: '<script type="importmap">' + IMPORTMAP + '</script>', html, flags=re.S)


def js(p):
    t = (R / limpa(p)).read_bytes().decode('utf-8', errors='replace')
    if 'viewer3d' in p:
        a = 'loader.load(`assets/models/${name}.stl`, g => res(g), undefined, rej)));'
        assert t.count(a) == 1, 'viewer3d mudou: ajustar o carregamento dos STL'
        t = t.replace(a, 'OFF.urlAsync(`assets/models/${name}.stl`).then(u => loader.load(u, g => res(g), undefined, rej), rej)));')
    return js_seguro(t)


# STL usados pelos visualizadores dos slides visíveis
v3d = (R / 'assets/js/viewer3d.js').read_text(encoding='utf-8', errors='replace')
partes = set(re.findall(r'data-part="([^"]+)"', html))
for tab in re.findall(r'data-tabs="([^"]+)"', html):
    bloco = re.search(r'id="' + re.escape(tab) + r'".*?</div>', html, flags=re.S)
    partes |= set(re.findall(r'data-part="([^"]+)"', bloco.group(0))) if bloco else set()
stl = set()
for parte in partes:
    linha = re.search(r'^\s*' + re.escape(parte) + r':\s*\{.*$', v3d, flags=re.M).group(0)
    for nome in re.findall(r"'([a-z0-9_/]+)'", linha):
        if (R / f'assets/models/{nome}.stl').is_file():
            stl.add(nome)
    if 'pads_montados' in linha:
        stl |= {f'pads_montados/{f.stem}' for f in (R / 'assets/models/pads_montados').glob('*.stl')}
for nome in sorted(stl):
    guarda(f'assets/models/{nome}.stl', gz=True)


def atributos(t, pagina):
    """Troca caminhos locais: imagem do slide vira data:, vídeo vai para o depósito, o resto aponta para o GitHub."""
    def troca(m):
        esp, attr, v = m.groups()
        if not local(v):
            return m.group(0)
        p = limpa(v)
        ext = Path(p).suffix.lower()
        if p == 'evidencias.html':
            guarda(p)
            return f'{esp}href="#" data-offpage="{p}"'
        if p.startswith('index.html'):
            return f'{esp}href="#" data-offclose'
        if not (R / p).is_file():
            return m.group(0)
        if pagina:                                   # página de evidências: tudo pelo depósito
            if attr == 'href' and ext in IMG:
                return f'{esp}href="#" data-offimg="{guarda(p)}"'
            if attr == 'href' and ext == '.html':
                return f'{esp}href="#" data-offpage="{guarda(p)}"'
            if ext in IMG | VID:
                return f'{esp}data-offx-{attr}="{guarda(p)}"'
        else:
            if ext in IMG:
                return f'{esp}{attr}="{data_uri(p)}"'
            if ext in VID:
                return f'{esp}data-offx-{attr}="{guarda(p)}"'
        if attr == 'href':
            return f'{esp}href="{GH}{p}"'
        return m.group(0)
    t = re.sub(r'(\s)(src|href|poster|data-zoom|data-src|data-poster)="([^"]*)"', troca, t)
    return re.sub(r'url\((["\']?)(assets/[^)"\']+)\1\)', lambda m: f'url("{data_uri(limpa(m.group(2)))}")', t)


html = atributos(html, False)

# página de evidências: CSS embutido; fontes e mídia entram quando ela abre
ev = (R / 'evidencias.html').read_text(encoding='utf-8')
ev = re.sub(r'\s*<link rel="preconnect"[^>]*>', '', ev)
ev = re.sub(r'<link href="https://fonts\.googleapis\.com[^>]*>', '', ev)
ev = re.sub(r'<link rel="stylesheet" href="([^"]+)">',
            lambda m: '<style>' + (R / limpa(m.group(1))).read_text(encoding='utf-8') + '</style>', ev)
ev = atributos(ev, True)
deposito['evidencias.html'] = ('text/html', 'b64', b64(ev.encode('utf-8')))

# ---------- leitor do depósito e camada das páginas extras ----------
RUNTIME = r'''
<style>
#off-ov{position:fixed;inset:0;z-index:2147483000;display:none;flex-direction:column;background:#f4f2fb}
#off-ov.on{display:flex}
#off-ov>header{flex:none;display:flex;align-items:center;gap:12px;height:46px;padding:0 14px;border-bottom:1px solid rgba(21,21,29,.1);background:rgba(248,246,255,.95);font:600 14px "Inter Tight","Segoe UI",sans-serif;color:#15151d}
#off-ov>header button{height:32px;padding:0 14px;border-radius:999px;border:1px solid rgba(21,21,29,.15);background:#fff;font:inherit;cursor:pointer}
#off-ov>header span{color:#6b6d82;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#off-ov iframe{flex:1;width:100%;border:0;background:#fff}
</style>
<div id="off-ov" role="dialog" aria-modal="true"><header><button type="button" id="off-volta">← Voltar</button><span id="off-tit"></span></header></div>
<script>
// Versão offline: lê os arquivos guardados neste HTML (blocos base64) e abre as páginas extras por cima dos slides.
window.OFF = (() => {
  const S = {}, urls = {}, pend = {};
  document.querySelectorAll('script[type="application/x-off"]').forEach(s => { S[s.dataset.off] = s; });
  const norm = p => p.split('?')[0].split('#')[0].replace(/^\.?\//, '');
  const bytes = s => { const b = atob(s.textContent.trim()), u = new Uint8Array(b.length); for (let i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; };
  const url = p => {
    p = norm(p); if (urls[p]) return urls[p];
    const s = S[p]; if (!s || s.dataset.enc !== 'b64') return null;
    return (urls[p] = URL.createObjectURL(new Blob([bytes(s)], { type: s.dataset.mime })));
  };
  const urlAsync = async p => {
    p = norm(p); if (urls[p]) return urls[p];
    const s = S[p]; if (!s) throw new Error('offline: falta ' + p);
    if (s.dataset.enc !== 'gz') return url(p);
    return (pend[p] ||= new Response(new Blob([bytes(s)]).stream().pipeThrough(new DecompressionStream('gzip'))).blob()
      .then(b => (urls[p] = URL.createObjectURL(new Blob([b], { type: s.dataset.mime })))));
  };
  const dataUri = p => { const s = S[norm(p)]; return s ? `data:${s.dataset.mime};base64,${s.textContent.trim()}` : null; };
  const text = p => new TextDecoder().decode(bytes(S[norm(p)]));
  // atributos data-offx-<nome>: imagem vira data:, vídeo vira blob:
  const fill = root => root.querySelectorAll('*').forEach(el => {
    for (const a of [...el.attributes]) {
      if (!a.name.startsWith('data-offx-')) continue;
      const nome = a.name.slice(10), s = S[norm(a.value)];
      if (!s) continue;
      el.setAttribute(nome, s.dataset.mime.startsWith('image/') ? dataUri(a.value) : url(a.value));
    }
  });
  return { url, urlAsync, dataUri, text, fill };
})();
OFF.fill(document);

(() => {
  const ov = document.getElementById('off-ov'), tit = document.getElementById('off-tit');
  const pilha = [];
  const fontes = document.getElementById('off-fonts').textContent;
  const fecharTudo = () => { pilha.splice(0).forEach(f => f.remove()); ov.classList.remove('on'); };
  const voltar = () => { const f = pilha.pop(); if (f) f.remove(); if (pilha.length) { pilha.at(-1).hidden = false; tit.textContent = pilha.at(-1).dataset.tit; } else ov.classList.remove('on'); };
  const imagem = (d, src) => {
    const o = d.createElement('div');
    o.style.cssText = 'position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;padding:24px;background:rgba(10,10,16,.88);cursor:zoom-out';
    const im = d.createElement('img'); im.src = src; im.style.cssText = 'max-width:100%;max-height:100%;border-radius:10px;box-shadow:0 20px 60px rgba(0,0,0,.5)';
    o.appendChild(im); o.addEventListener('click', () => o.remove()); d.body.appendChild(o);
  };
  const abrir = (p, nome) => {
    let h = OFF.text(p);
    h = h.includes('</head>') ? h.replace('</head>', '<style>' + fontes + '</style></head>') : '<style>' + fontes + '</style>' + h;
    const f = document.createElement('iframe');
    f.dataset.tit = nome || '';
    f.srcdoc = h;
    f.addEventListener('load', () => {
      const d = f.contentDocument;
      OFF.fill(d);
      d.addEventListener('click', ev => {
        const a = ev.target.closest('a'); if (!a) return;
        if (a.hasAttribute('data-offclose')) { ev.preventDefault(); fecharTudo(); }
        else if (a.dataset.offpage) { ev.preventDefault(); abrir(a.dataset.offpage, a.textContent.trim()); }
        else if (a.dataset.offimg) { ev.preventDefault(); imagem(d, OFF.dataUri(a.dataset.offimg)); }
        else if (/^https?:/.test(a.getAttribute('href') || '') && !navigator.onLine) { ev.preventDefault(); alert('Este link precisa de internet.'); }
      });
      d.addEventListener('keydown', ev => { if (ev.key === 'Escape') voltar(); });
    });
    pilha.forEach(o => { o.hidden = true; });
    pilha.push(f); ov.appendChild(f); tit.textContent = f.dataset.tit; ov.classList.add('on');
  };
  document.getElementById('off-volta').addEventListener('click', voltar);
  document.addEventListener('click', ev => {
    const a = ev.target.closest && ev.target.closest('a[data-offpage]');
    if (a) { ev.preventDefault(); ev.stopPropagation(); abrir(a.dataset.offpage, 'Evidências dos dados'); }
  }, true);
  document.addEventListener('keydown', ev => {
    if (!ov.classList.contains('on')) return;
    ev.stopPropagation();
    if (ev.key === 'Escape') { ev.preventDefault(); voltar(); }
  }, true);
})();
</script>
'''

dep = '\n'.join(f'<script type="application/x-off" data-off="{p}" data-mime="{m}" data-enc="{e}">{d}</script>'
                for p, (m, e, d) in deposito.items())

# scripts da apresentação, depois do depósito e do leitor
primeiro = re.search(r'\s*<script src="assets/js/', html).start()
html = html[:primeiro] + '\n' + dep + RUNTIME + html[primeiro:]
html = re.sub(r'<script src="([^"]+)"></script>', lambda m: '<script>' + js(m.group(1)) + '</script>', html)
html = re.sub(r'<script type="module" src="([^"]+)"></script>', lambda m: '<script type="module">' + js(m.group(1)) + '</script>', html)
html = html.replace('<title>RedLab · SENAI</title>', '<title>RedLab · SENAI (offline)</title>')

sobra = re.findall(r'\s(?:src|href|poster)="(assets/[^"]+)"', html)
assert not sobra, f'caminhos locais sobrando: {sobra[:5]}'

OUT.mkdir(exist_ok=True)
(OUT / '.gitignore').write_text('*\n', encoding='utf-8')
saida = OUT / 'Projeto_SAI_apresentacao.html'
saida.write_text(html, encoding='utf-8', newline='\n')
print(f'{saida.relative_to(R)}: {saida.stat().st_size / 1e6:.1f} MB, {len(deposito)} arquivos no depósito '
      f'({len(stl)} STL, {sum(1 for p in deposito if p.endswith((".mp4", ".webm")))} vídeos)')
