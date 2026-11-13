"""Pacote final da garra SAI: os arquivos 3D prontos para imprimir, com nomes claros.

Monta `modelos/SAI_final/` a partir das pastas de trabalho (`../desempenho`), confere cada arquivo e grava
`manifesto.json` com o que foi conferido. Nada é recalculado nem enviado à impressora: os projetos do Orca
são copiados como estão, só com nome novo.

Uso:
  python sai_pacote_final.py            monta o pacote e confere
  python sai_pacote_final.py --conferir só confere o pacote já montado (lê apenas modelos/SAI_final)

O que a conferência exige (falha se algo não bater):
  - superior: 5 paredes, camada 0,2 mm, giroide 25%, PA6-CF, e 4 modificadores internos
    (100% tubos dos furos, 55% colar, 35% ressaltos, 20% assento), iguais aos STL "sem almas";
  - inferiores: 5 paredes, giroide 20%, PA6-CF, e 3 modificadores (100% tubos, 35% ressaltos e pés,
    20% assento), iguais aos STL "sem almas";
  - PADs: 8 meias-peças, TPU, giroide 40%, 3 paredes, iguais aos STL R02;
  - exterior de cada peça igual ao STL original (volume, caixa e número de faces);
  - cada STL de zona no mesmo lugar, em relação ao STL da peça, que o modificador no projeto
    (as zonas de origem estão nas coordenadas da garra montada; o script as desloca para as da peça);
  - todas as malhas fechadas;
  - o FE da garra montada (montagem_R07_SEM.json) é da mesma variante (R07_SEM: giroide 25% e 20%, sem almas);
  - nenhum caminho de pasta pessoal dentro dos arquivos de texto do pacote.
"""
from __future__ import annotations
import hashlib, json, re, shutil, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
import trimesh

REPO = Path(__file__).resolve().parents[2]
DES = REPO.parent / 'desempenho'
OUT = REPO / 'modelos' / 'SAI_final'
DADOS = REPO / 'dados'
NS = '{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}'
ZONA_SUP = DES / '04_Modificadores/R07/SEM_ALMAS_SUPERIOR'
ZONA_INF = DES / '04_Modificadores/R07/SEM_ALMAS'

PROJETOS = {
    'SAI_superior_PA6-CF_giroide25.3mf': DES / '05_Orca/R07/COMPARATIVO/GARRA_SUPERIOR_R07_SEM_ESQUELETO_GIROIDE25_K1MAX.3mf',
    'SAI_inferior_esq_PA6-CF_giroide20.3mf': DES / '05_Orca/R07/GARRA_INFERIOR_ESQ_R07_ESQUELETO_GIROIDE20_K1MAX.3mf',
    'SAI_inferior_dir_PA6-CF_giroide20.3mf': DES / '05_Orca/R07/GARRA_INFERIOR_DIR_R07_ESQUELETO_GIROIDE20_K1MAX.3mf',
    'SAI_PADs_TPU95A_giroide40.3mf': DES / '05_Orca/CONFIRMADO_R05/PADs_TPU95A40_K1MAX_ESCALA_REAL.3mf',
}
CAD = {
    'cad/SAI_garra_montada_3pecas_8PADs.step': DES / '01_Fusion/GARRA_R04_EXTERIOR_ORIGINAL_PREPARACAO.step',
    'cad/SAI_PADs_8_pecas.step': DES / '01_Fusion/PADs_R04_SEPARADOS.step',
}
STL = {
    'stl/pecas/SAI_superior.stl': DES / '03_STL_Garra/GARRA_SUPERIOR_BASE20.stl',
    'stl/pecas/SAI_inferior_esq.stl': DES / '03_STL_Garra/GARRA_INFERIOR_ESQ_BASE20.stl',
    'stl/pecas/SAI_inferior_dir.stl': DES / '03_STL_Garra/GARRA_INFERIOR_DIR_BASE20.stl',
    **{f'stl/pecas/SAI_PAD_{a}_{s}.stl': DES / f'02_STL_PAD/PAD95_R02_{a}_{s}_ENVELOPE_INFILL40.stl'
       for a in ('A1', 'A2', 'A3', 'A4') for s in ('L', 'R')},
    'stl/zonas/superior_tubos_100.stl': ZONA_SUP / 'SUPERIOR_MOD_SOLIDO_100.stl',
    'stl/zonas/superior_colar_55.stl': ZONA_SUP / 'SUPERIOR_MOD_COLAR_55.stl',
    'stl/zonas/superior_ressaltos_35.stl': ZONA_SUP / 'SUPERIOR_MOD_ROSA_35.stl',
    'stl/zonas/superior_assento_20.stl': ZONA_SUP / 'SUPERIOR_MOD_AMARELO_20.stl',
    **{f'stl/zonas/inferior_{l}_{n}.stl': ZONA_INF / f'INFERIOR_{L}_MOD_{z}.stl'
       for l, L in (('esq', 'ESQ'), ('dir', 'DIR'))
       for n, z in (('tubos_100', 'SOLIDO_100'), ('ressaltos_e_pes_35', 'ROSAPES_35'), ('assento_20', 'AMARELO_20'))},
}

# o que cada projeto precisa ter (nome do modificador no Orca -> densidade, STL da zona no pacote)
ESPERADO = {
    'SAI_superior_PA6-CF_giroide25.3mf': dict(
        material='PA6-CF', paredes='5', infill='25%', exterior='stl/pecas/SAI_superior.stl',
        zonas={'MOD_SOLIDO_100_INTERNO_R07': ('100%', 'stl/zonas/superior_tubos_100.stl'),
               'MOD_COLAR_55_INTERNO_R07': ('55%', 'stl/zonas/superior_colar_55.stl'),
               'MOD_ROSA_35_INTERNO_R07': ('35%', 'stl/zonas/superior_ressaltos_35.stl'),
               'MOD_AMARELO_20_INTERNO_R07': ('20%', 'stl/zonas/superior_assento_20.stl')}),
    **{f'SAI_inferior_{l}_PA6-CF_giroide20.3mf': dict(
        material='PA6-CF', paredes='5', infill='20%', exterior=f'stl/pecas/SAI_inferior_{l}.stl',
        zonas={'MOD_SOLIDO_100_INTERNO_R07': ('100%', f'stl/zonas/inferior_{l}_tubos_100.stl'),
               'MOD_ROSAPES_35_INTERNO_R07': ('35%', f'stl/zonas/inferior_{l}_ressaltos_e_pes_35.stl'),
               'MOD_AMARELO_20_INTERNO_R07': ('20%', f'stl/zonas/inferior_{l}_assento_20.stl')})
       for l in ('esq', 'dir')},
    'SAI_PADs_TPU95A_giroide40.3mf': dict(
        material='TPU', paredes='3', infill='40%', zonas={},
        pads={f'PAD95_R02_{a}_{s}_ENVELOPE_INFILL40': f'stl/pecas/SAI_PAD_{a}_{s}.stl'
              for a in ('A1', 'A2', 'A3', 'A4') for s in ('L', 'R')}),
}
PRIVADO = re.compile(rb'(?i)(onedrive|@gmail|\b[a-z]:[\\/]users[\\/]|/users/[a-z]|/home/[a-z])')


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def malha(v, t):
    a, b, c = v[t[:, 0]], v[t[:, 1]], v[t[:, 2]]
    vol = abs(np.einsum('ij,ij->i', a, np.cross(b, c)).sum()) / 6000.0
    e = np.sort(np.concatenate([t[:, [0, 1]], t[:, [1, 2]], t[:, [2, 0]]]), axis=1)
    _, n = np.unique(e, axis=0, return_counts=True)
    return {'faces': int(len(t)), 'volume_cm3': round(float(vol), 2), 'fechada': bool((n == 2).all()),
            'caixa_mm': [round(float(x), 1) for x in v.max(0) - v.min(0)]}


def malha_stl(p: Path):
    m = trimesh.load(p, force='mesh')
    return malha(np.asarray(m.vertices), np.asarray(m.faces))


def ler_3mf(p: Path):
    z = zipfile.ZipFile(p)
    ps = json.loads(z.read('Metadata/project_settings.config'))
    cache = {}

    def objetos(nome):
        if nome not in cache:
            r = ET.fromstring(z.read(nome)); d = {}
            for o in r.iter(NS + 'object'):
                me = o.find(NS + 'mesh')
                if me is None:
                    continue
                v = np.array([[float(x.get(k)) for k in 'xyz'] for x in me.find(NS + 'vertices')])
                t = np.array([[int(x.get(k)) for k in ('v1', 'v2', 'v3')] for x in me.find(NS + 'triangles')])
                d[o.get('id')] = malha(v, t)
            cache[nome] = d
        return cache[nome]

    comp = {}
    for o in ET.fromstring(z.read('3D/3dmodel.model')).iter(NS + 'object'):
        lst = []
        for c in o.iter(NS + 'component'):
            cam = [v for k, v in c.attrib.items() if k.endswith('path')]
            lst.append(objetos(cam[0].lstrip('/') if cam else '3D/3dmodel.model').get(c.get('objectid')))
        comp[o.get('id')] = lst
    partes = []
    for o in ET.fromstring(z.read('Metadata/model_settings.config')).findall('object'):
        cl = comp.get(o.get('id'), [])
        for i, pt in enumerate(o.findall('part')):
            md = {m.get('key'): m.get('value') for m in pt.findall('metadata')}
            partes.append({'nome': md.get('name'), 'tipo': pt.get('subtype'),
                           'preenchimento': md.get('sparse_infill_density'), 'padrao': md.get('sparse_infill_pattern'),
                           'malha': cl[i] if i < len(cl) else None})
    g = lambda k: (ps.get(k)[0] if isinstance(ps.get(k), list) else ps.get(k))
    cfg = {'impressora': ps.get('printer_model') or g('printer_settings_id'), 'bico_mm': g('nozzle_diameter'),
           'camada_mm': g('layer_height'), 'paredes': g('wall_loops'), 'preenchimento': g('sparse_infill_density'),
           'padrao': g('sparse_infill_pattern'), 'topo_fundo': [g('top_shell_layers'), g('bottom_shell_layers')],
           'material': g('filament_type'), 'perfil_filamento': g('filament_settings_id'), 'bico_C': g('nozzle_temperature'),
           'suporte': g('enable_support') == '1'}
    privado = [n for n in z.namelist() if not n.endswith('.png') and PRIVADO.search(z.read(n))]
    return cfg, partes, privado


STL_DT = np.dtype([('n', '<f4', 3), ('v', '<f4', 9), ('a', '<u2')])


def stl_sopa(p: Path):
    """Triângulos do STL binário, na ordem do arquivo (n x 3 x 3, mm)."""
    b = p.read_bytes(); n = int(np.frombuffer(b, '<u4', 1, 80)[0])
    return np.frombuffer(b, STL_DT, n, 84)['v'].reshape(-1, 3, 3).astype(float)


def stl_mover(p: Path, d):
    """Desloca o STL binário pelo vetor d (mm). Só translação: forma e normais não mudam."""
    b = p.read_bytes(); n = int(np.frombuffer(b, '<u4', 1, 80)[0])
    a = np.frombuffer(b, STL_DT, n, 84).copy()
    a['v'] = (a['v'].reshape(-1, 3, 3).astype(float) + d).reshape(-1, 9).astype(np.float32)
    p.write_bytes(b[:84] + a.tobytes() + b[84 + 50 * n:])


def _mat(s):
    m = np.eye(4)
    if s:
        v = [float(x) for x in s.split()]
        m[:3, :3] = np.array(v[:9]).reshape(3, 3).T; m[:3, 3] = v[9:12]
    return m


def sopas_3mf(p: Path):
    """Triângulos de cada parte do projeto, já na posição da mesa (com as transformações do 3MF)."""
    z = zipfile.ZipFile(p); raiz = '3D/3dmodel.model'; cache = {}

    def objs(nome):
        if nome not in cache:
            cache[nome] = {o.get('id'): o for o in ET.fromstring(z.read(nome)).iter(NS + 'object')}
        return cache[nome]
    nomes = {o.get('id'): [{m.get('key'): m.get('value') for m in pt.findall('metadata')}.get('name')
                           for pt in o.findall('part')]
             for o in ET.fromstring(z.read('Metadata/model_settings.config')).findall('object')}
    out = {}
    for it in ET.fromstring(z.read(raiz)).find(NS + 'build'):
        oid = it.get('objectid'); m0 = _mat(it.get('transform'))
        for i, c in enumerate(objs(raiz)[oid].iter(NS + 'component')):
            cam = [v for k, v in c.attrib.items() if k.endswith('path')]
            me = objs(cam[0].lstrip('/') if cam else raiz)[c.get('objectid')].find(NS + 'mesh')
            v = np.array([[float(x.get(k)) for k in 'xyz'] for x in me.find(NS + 'vertices')])
            t = np.array([[int(x.get(k)) for k in ('v1', 'v2', 'v3')] for x in me.find(NS + 'triangles')])
            m = m0 @ _mat(c.get('transform'))
            out[nomes[oid][i]] = (v @ m[:3, :3].T + m[:3, 3])[t]
    return out


def posicao_zonas(base: Path, nome: str, esp: dict):
    """Compara a posição de cada zona em relação à peça: no projeto 3MF e nos STL do pacote.
    Devolve, por zona, o deslocamento que falta no STL da zona (mm) e o erro de forma."""
    sop = sopas_3mf(base / nome)
    ext = [k for k in sop if k not in esp['zonas']]
    peca = stl_sopa(base / esp['exterior'])
    t = (sop[ext[0]] - peca).reshape(-1, 3).mean(0)            # peça do 3MF = STL da peça + t
    r = {'_peca': float(np.abs(sop[ext[0]] - peca - t).max())}
    for mn, (_, arq) in esp['zonas'].items():
        z = stl_sopa(base / arq); d = (sop[mn] - t - z).reshape(-1, 3).mean(0)
        r[mn] = (d, float(np.abs(sop[mn] - t - z - d).max()))
    return r


def igual(a, b, tol=0.05):
    return (a and b and a['faces'] == b['faces'] and abs(a['volume_cm3'] - b['volume_cm3']) <= tol
            and all(abs(x - y) <= 0.2 for x, y in zip(sorted(a['caixa_mm']), sorted(b['caixa_mm']))))


def conferir(base: Path):
    erros, rel = [], {}
    stl = {k: malha_stl(base / k) for k in STL}
    for k, m in stl.items():
        if not m['fechada']:
            erros.append(f'{k}: malha aberta')
    for nome, esp in ESPERADO.items():
        cfg, partes, privado = ler_3mf(base / nome)
        r = {'config': cfg, 'partes': partes, 'checagens': []}
        ok = lambda cond, txt: (r['checagens'].append(('OK ' if cond else 'ERRO ') + txt), None if cond else erros.append(f'{nome}: {txt}'))
        ok(cfg['material'] == esp['material'], f"material {cfg['material']}")
        ok(cfg['paredes'] == esp['paredes'], f"{cfg['paredes']} paredes")
        ok(cfg['preenchimento'] == esp['infill'] and cfg['padrao'] == 'gyroid', f"giroide {cfg['preenchimento']}")
        ok(cfg['camada_mm'] == '0.2' and cfg['bico_mm'] == '0.4', f"camada {cfg['camada_mm']} mm, bico {cfg['bico_mm']} mm")
        ok(not privado, 'sem caminho pessoal' if not privado else f'caminho pessoal em {privado}')
        for p in partes:
            ok(bool(p['malha'] and p['malha']['fechada']), f"malha fechada: {p['nome']}")
        mods = {p['nome']: p for p in partes if p['tipo'] == 'modifier_part'}
        ok(set(mods) == set(esp['zonas']), f"modificadores {sorted(mods)}")
        for mn, (dens, arq) in esp['zonas'].items():
            p = mods.get(mn)
            ok(bool(p) and p['preenchimento'] == dens, f'{mn} a {dens}')
            ok(bool(p) and igual(p['malha'], stl[arq]), f'{mn} igual a {arq}')
        if 'exterior' in esp:
            ext = [p for p in partes if p['tipo'] == 'normal_part']
            ok(len(ext) == 1 and igual(ext[0]['malha'], stl[esp['exterior']]), f"exterior igual a {esp['exterior']}")
            # posição: o STL da zona tem de ficar no mesmo lugar da peça que no projeto (só translação da mesa)
            pos = posicao_zonas(base, nome, esp)
            ok(pos['_peca'] < 0.01, f"STL da peça = projeto só deslocado na mesa (erro {pos['_peca']:.4f} mm)")
            for mn, (_, arq) in esp['zonas'].items():
                d, e = pos[mn]
                ok(float(np.abs(d).max()) < 0.01 and e < 0.01,
                   f'{arq} na mesma posição da peça que no projeto (fora {float(np.abs(d).max()):.3f} mm)')
        if 'pads' in esp:
            pn = {p['nome']: p for p in partes}
            ok(set(pn) == set(esp['pads']), f'{len(pn)} PADs')
            for n, arq in esp['pads'].items():
                ok(n in pn and igual(pn[n]['malha'], stl[arq]), f'{n} igual a {arq}')
        rel[nome] = r
    for k in CAD:
        b = (base / k).read_bytes()
        n = len(re.findall(rb'MANIFOLD_SOLID_BREP', b))
        rel[k] = {'corpos_solidos': n, 'privado': bool(PRIVADO.search(b[:4000]))}
        if PRIVADO.search(b[:4000]):
            erros.append(f'{k}: caminho pessoal no cabeçalho')
    rel['stl'] = stl
    # FE da garra montada: mesma variante que vai para a impressão
    fe = json.loads((DADOS / 'montagem/montagem_R07_SEM.json').read_text(encoding='utf-8'))
    okfe = fe.get('variante') == 'R07_SEM'
    rel['fe_montagem'] = {'variante': fe.get('variante'), 'FS_24kg_PA6-CF': fe.get('FS_24kg_PA6-CF_Z48'),
                          'kg_max_asa': fe.get('kg_max_PA6-CF_Z48'), 'confere': okfe}
    if not okfe:
        erros.append('FE da montagem não é a variante R07_SEM')
    return rel, erros


def montar():
    # refaz tudo o que o script copia; o LEIA-ME.md e o .gitattributes são escritos à mão e ficam
    if OUT.exists():
        for p in OUT.iterdir():
            if p.is_dir():
                shutil.rmtree(p)
            elif p.name not in ('LEIA-ME.md', '.gitattributes'):
                p.unlink()
    for dest, src in {**PROJETOS, **CAD, **STL}.items():
        d = OUT / dest; d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, d)
    # as zonas de origem estão nas coordenadas da garra montada (as do FE); as peças em STL estão
    # centradas na origem. Desloca cada zona para ficar, em relação ao STL da peça, onde está no projeto.
    for nome, esp in ESPERADO.items():
        if 'exterior' not in esp:
            continue
        pos = posicao_zonas(OUT, nome, esp)
        for mn, (_, arq) in esp['zonas'].items():
            d, e = pos[mn]
            if e > 0.01:
                raise SystemExit(f'{nome}: a zona {mn} não é a mesma forma do projeto (erro {e:.4f} mm)')
            stl_mover(OUT / arq, d)


def main():
    if '--conferir' not in sys.argv:
        montar()
    rel, erros = conferir(OUT)
    orca = json.loads((DADOS / 'orca/r07_comparativo_fatiamento.json').read_text(encoding='utf-8'))['R07_SEM_SUPERIOR']
    base20 = json.loads((DADOS / 'orca/r07_fatiamento_base20.json').read_text(encoding='utf-8'))
    pads = json.loads((DADOS / 'orca/pads_tpu95a_fatiamento.json').read_text(encoding='utf-8'))
    fat = {'SAI_superior_PA6-CF_giroide25.3mf': (orca['mass_g']['peca'], orca['time_s']),
           'SAI_inferior_esq_PA6-CF_giroide20.3mf': (base20['INFERIOR_ESQ']['mass_g']['peca'], base20['INFERIOR_ESQ']['time_s']),
           'SAI_inferior_dir_PA6-CF_giroide20.3mf': (base20['INFERIOR_DIR']['mass_g']['peca'], base20['INFERIOR_DIR']['time_s'])}
    for k, (g, s) in fat.items():
        rel[k]['fatiamento_K1Max'] = {'massa_peca_g': round(g, 1), 'horas': round(s / 3600, 1)}
    arquivos = {str(p.relative_to(OUT)).replace('\\', '/'): {'bytes': p.stat().st_size, 'sha256': sha(p)}
                for p in sorted(OUT.rglob('*')) if p.is_file() and p.name != 'manifesto.json'}
    man = {'pacote': 'Garra SAI, arquivos finais (R07 sem almas)', 'gerado_por': 'dados/scripts/sai_pacote_final.py',
           'enviado_a_impressora': False, 'erros': erros, 'conferencia': rel, 'arquivos': arquivos,
           'pads_fatiamento_K1Max': {'massa_8_pecas_g': round(pads['category_mass_g']['peca'], 1),
                                     'suporte_g': round(pads['category_mass_g']['suporte'], 1),
                                     'horas': round(pads['Orca_summary']['prediction_s'] / 3600, 1)}}
    if '--conferir' in sys.argv:
        velho = json.loads((OUT / 'manifesto.json').read_text(encoding='utf-8'))
        dif = [k for k in set(arquivos) | set(velho['arquivos']) if arquivos.get(k) != velho['arquivos'].get(k)]
        if dif:
            erros.append(f'arquivos diferentes do manifesto: {dif}')
    else:
        (OUT / 'manifesto.json').write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding='utf-8')
    for nome, r in rel.items():
        if isinstance(r, dict) and 'checagens' in r:
            print(nome); [print('  ', c) for c in r['checagens']]
    print('CAD:', {k: rel[k] for k in CAD}); print('FE:', rel['fe_montagem'])
    print(f'{len(arquivos)} arquivos, {sum(a["bytes"] for a in arquivos.values()) / 1e6:.1f} MB')
    print('ERROS:', erros if erros else 'nenhum')
    sys.exit(1 if erros else 0)


if __name__ == '__main__':
    main()
